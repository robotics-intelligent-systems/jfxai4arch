import json
import socket

from fastapi.testclient import TestClient
import httpx
import pytest

from jfx_rag.app import Config, create_app
from jfx_rag.core import TechnicalRetriever, read_corpus

TOKEN = 'test-token-with-at-least-24-characters'
HEADERS = {'Authorization': f'Bearer {TOKEN}'}


@pytest.fixture
def corpus(tmp_path):
    (tmp_path / 'thermal.TXT').write_text('Thermal control\nEl sensor T-401 mide temperatura.\nThe T-401 sensor measures temperature.\n', encoding='utf-8')
    (tmp_path / 'network.md').write_text('The controller uses MQTT port 1883.\n', encoding='utf-8')
    return tmp_path


def client(corpus, model='', handler=None):
    return TestClient(create_app(Config(corpus, TOKEN, model=model),
                                httpx.MockTransport(handler) if handler else None))


def test_offline_retrieval_and_provenance(corpus, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError('Network attempted')
    monkeypatch.setattr(socket.socket, 'connect', forbidden)
    with client(corpus) as api:
        result = api.post('/v1/answers', headers=HEADERS, json={'question': 'T-401 temperatura'}).json()
        assert result['status'] == 'evidence_only'
        item = result['evidence'][0]
        assert item['source'] == 'thermal.TXT'
        assert item['line_start'] == 1 and item['line_end'] == 3
        assert len(item['sha256']) == 64
        assert api.get('/v1/evidence/' + item['id'], headers=HEADERS).json()['text'] == item['text']


@pytest.mark.parametrize('path,method', [('/v1/search', 'post'), ('/v1/answers', 'post'), ('/v1/evidence/unknown', 'get')])
def test_auth(corpus, path, method):
    with client(corpus) as api:
        assert getattr(api, method)(path).status_code == 401


def test_no_match_abstains(corpus):
    with client(corpus) as api:
        result = api.post('/v1/answers', headers=HEADERS, json={'question': 'xylophone'}).json()
        assert result['status'] == 'abstained'
        assert not result['claims'] and not result['evidence']


def test_withdrawal_and_replacement(corpus):
    with client(corpus) as api:
        old = api.post('/v1/search', headers=HEADERS, json={'question': 'T-401'}).json()
        (corpus / 'thermal.TXT').write_text('New sensor T-402.\n')
        assert api.get('/v1/evidence/' + old['evidence'][0]['id'], headers=HEADERS).status_code == 404
        new = api.post('/v1/search', headers=HEADERS, json={'question': 'T-401'}).json()
        assert old['generation'] != new['generation'] and not new['evidence']
        (corpus / 'thermal.TXT').unlink()
        assert not api.post('/v1/search', headers=HEADERS, json={'question': 'T-402'}).json()['evidence']


def test_symlink_not_ingested(corpus, tmp_path_factory):
    outside = tmp_path_factory.mktemp('outside') / 'secret.txt'
    outside.write_text('classified')
    (corpus / 'leak.txt').symlink_to(outside)
    assert all(n.metadata['source'] != 'leak.txt' for n in read_corpus(corpus).nodes)


def test_chunk_coverage(corpus):
    (corpus / 'long.txt').write_text('\n'.join(f'line {i}' for i in range(103)))
    nodes = [n for n in read_corpus(corpus).nodes if n.metadata['source'] == 'long.txt']
    covered = {i for n in nodes for i in range(n.metadata['line_start'], n.metadata['line_end'] + 1)}
    assert covered == set(range(1, 104))


@pytest.mark.parametrize('mode,expected', [('valid', 'generated'), ('unknown', 'evidence_only'), ('malformed', 'evidence_only'), ('abstain', 'abstained'), ('timeout', 'evidence_only')])
def test_model_contract(corpus, mode, expected):
    def handler(request):
        assert request.url.host == '127.0.0.1'
        payload = json.loads(request.content)
        assert payload['stream'] is False
        if mode == 'timeout':
            raise httpx.ReadTimeout('test')
        items = json.loads(payload['messages'][1]['content'])['evidence']
        content = {'claims': [{'text': 'T-401 measures temperature.', 'citations': [items[0]['id'] if mode == 'valid' else 'invented']} ]}
        if mode == 'abstain':
            content = {'claims': []}
        return httpx.Response(200, json={'message': {'content': 'bad json' if mode == 'malformed' else json.dumps(content)}})
    with client(corpus, 'local-model', handler) as api:
        result = api.post('/v1/answers', headers=HEADERS, json={'question': 'T-401'}).json()
        assert result['status'] == expected
        assert bool(result['claims']) == (mode == 'valid')


def test_generation_rejects_changed_corpus(corpus):
    def handler(request):
        (corpus / 'thermal.TXT').unlink()
        return httpx.Response(200, json={'message': {'content': '{"claims": []}'}})
    with client(corpus, 'local-model', handler) as api:
        assert api.post('/v1/answers', headers=HEADERS, json={'question': 'T-401'}).status_code == 409


@pytest.mark.parametrize('url', ['https://cloud.example', 'http://localhost.evil.test', 'http://user:password@localhost'])
def test_remote_endpoints_rejected(corpus, url):
    with pytest.raises(ValueError):
        create_app(Config(corpus, TOKEN, ollama_url=url))


def test_bad_input(corpus):
    with client(corpus) as api:
        assert api.post('/v1/search', headers=HEADERS, json={'question': 'x', 'top_k': 100}).status_code == 422


def test_retrieval_ranking(corpus):
    retriever = TechnicalRetriever(read_corpus(corpus).nodes, 1)
    assert retriever.retrieve('MQTT')[0].node.metadata['source'] == 'network.md'


def test_invalid_root(corpus):
    with pytest.raises(ValueError, match='directory'):
        create_app(Config(corpus / 'thermal.TXT', TOKEN))


def test_invalid_corpus_fails_closed(corpus):
    with client(corpus) as api:
        (corpus / 'invalid.txt').write_bytes(b'\xff\xfe')
        response = api.post('/v1/search', headers=HEADERS, json={'question': 'T-401'})
        assert response.status_code == 503
        assert str(corpus) not in response.text


def test_langfuse_metadata_only(corpus, monkeypatch):
    import sys
    from contextlib import nullcontext
    from types import SimpleNamespace
    observations, shutdown = [], []

    class FakeLangfuse:
        def __init__(self, **kwargs):
            assert kwargs['base_url'] == 'http://127.0.0.1:3000'

        def start_as_current_observation(self, **kwargs):
            observations.append(kwargs)
            return nullcontext()

        def shutdown(self):
            shutdown.append(True)

    monkeypatch.setitem(sys.modules, 'langfuse', SimpleNamespace(Langfuse=FakeLangfuse))
    monkeypatch.setenv('LANGFUSE_PUBLIC_KEY', 'test-public')
    monkeypatch.setenv('LANGFUSE_SECRET_KEY', 'test-secret')
    app = create_app(Config(corpus, TOKEN, langfuse_url='http://127.0.0.1:3000'))
    with TestClient(app) as api:
        assert api.post('/v1/answers', headers=HEADERS, json={'question': 'T-401'}).status_code == 200
    assert shutdown == [True]
    assert len(observations) == 1
    assert set(observations[0]) == {'name', 'as_type', 'metadata'}
    assert set(observations[0]['metadata']) == {'status', 'evidence_count', 'duration_ms'}
    assert 'T-401' not in json.dumps(observations)
