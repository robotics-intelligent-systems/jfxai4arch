"""Starter smoke benchmark; expand with independently curated domain questions."""
import json
from pathlib import Path
from time import perf_counter
from jfx_rag.core import TechnicalRetriever, read_corpus

ROOT = Path(__file__).resolve().parents[2]
CASES = [
    ('gpt-oss-20b hardware', 'deployment.md'),
    ('preparación conectada dependencias', 'deployment.md'),
    ('private runtime embeddings', 'deployment.md'),
    ('GLiNER2 extracción estructurada', 'extraction.md'),
    ('ExtractionRun checkpoint hash', 'extraction.md'),
    ('AutoExtractor completo', 'extraction.md'),
    ('Qdrant PostgreSQL', 'retrieval.md'),
    ('permisos documentales', 'retrieval.md'),
    ('generation unavailable', 'retrieval.md'),
    ('retirada documental', 'governance.md'),
    ('bibliography resolution', 'governance.md'),
    ('validez citas abstención', 'governance.md'),
    ('xylophone', None),
    ('pterodáctilo', None),
]


def evaluate():
    corpus = read_corpus(ROOT / 'docs/rag/sample-corpus')
    retriever = TechnicalRetriever(corpus.nodes, top_k=3)
    rows = []
    for question, expected in CASES:
        start = perf_counter()
        sources = [h.node.metadata['source'] for h in retriever.retrieve(question)]
        rank = sources.index(expected) + 1 if expected in sources else None
        rows.append({'question': question, 'expected': expected, 'rank': rank,
                     'abstained': not sources, 'latency_ms': round((perf_counter()-start)*1000, 3)})
    positive = [r for r in rows if r['expected']]
    negative = [r for r in rows if not r['expected']]
    return {'kind': 'synthetic_smoke_not_domain_quality', 'generation': corpus.generation,
            'positive_questions': len(positive), 'negative_questions': len(negative),
            'document_recall_at_3': sum(bool(r['rank']) for r in positive)/len(positive),
            'mrr_at_3': sum(1/r['rank'] if r['rank'] else 0 for r in positive)/len(positive),
            'no_match_abstention_rate': sum(r['abstained'] for r in negative)/len(negative),
            'results': rows}


if __name__ == '__main__':
    print(json.dumps(evaluate(), ensure_ascii=False, indent=2))
