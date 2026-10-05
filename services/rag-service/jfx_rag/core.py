"""Small, offline lexical baseline. No implicit model or embedding downloads."""
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from math import log
from pathlib import Path
import re
import unicodedata

from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import NodeWithScore, QueryBundle, TextNode

STOP = set('a an and are as at be by for from in is it of on or that the this to was with y de del el en es la las los o para por que un una con como qué cuál'.split())


def tokens(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if not unicodedata.combining(c))
    return [t for t in re.findall(r'[\w]+(?:[-./][\w]+)*', text) if t not in STOP and len(t) > 1]


@dataclass(frozen=True)
class Corpus:
    nodes: list[TextNode]
    generation: str


def read_corpus(root: Path) -> Corpus:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Corpus root must be a directory')
    nodes, manifest = [], []
    paths = sorted(p for p in root.rglob('*') if p.suffix.lower() in {'.txt', '.md'})
    if len(paths) > 1000:
        raise ValueError('Pilot corpus limit: 1000 documents')
    total = 0
    for path in paths:
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != root):
            continue
        if not path.is_file() or not path.resolve().is_relative_to(root):
            continue
        size = path.stat().st_size
        total += size
        if size > 2_000_000 or total > 20_000_000:
            raise ValueError('Pilot corpus limit: 2 MB/document, 20 MB total')
        raw = path.read_bytes()
        source = path.relative_to(root).as_posix()
        digest = sha256(raw).hexdigest()
        manifest.append(f'{source}:{digest}')
        lines = raw.decode('utf-8-sig').splitlines()
        if any(len(line) > 6000 for line in lines):
            raise ValueError(f'Line exceeds 6000 characters: {source}')
        for start in range(0, len(lines), 25):
            end = min(start + 30, len(lines))
            body = '\n'.join(lines[start:end])
            if not body.strip():
                continue
            identity = sha256(f'{source}:{digest}:{start + 1}:{end}'.encode()).hexdigest()
            nodes.append(TextNode(id_=identity, text=body, metadata={
                'source': source, 'sha256': digest, 'line_start': start + 1, 'line_end': end,
            }, excluded_llm_metadata_keys=['sha256'], excluded_embed_metadata_keys=['sha256']))
            if end == len(lines):
                break
    return Corpus(nodes, sha256('\n'.join(manifest).encode()).hexdigest())


class TechnicalRetriever(BaseRetriever):
    """BM25 over LlamaIndex nodes; a lexical baseline, not hybrid retrieval."""
    def __init__(self, nodes, top_k=5):
        super().__init__()
        self.nodes, self.top_k = nodes, top_k
        self.counts = [Counter(tokens(n.text)) for n in nodes]
        self.lengths = [sum(c.values()) for c in self.counts]
        self.avg = sum(self.lengths) / max(len(nodes), 1) or 1
        self.df = Counter(t for c in self.counts for t in c)

    def _retrieve(self, query_bundle: QueryBundle):
        terms = set(tokens(query_bundle.query_str))
        ranked = []
        for node, counts, length in zip(self.nodes, self.counts, self.lengths):
            score = 0.0
            for term in terms:
                freq = counts[term]
                if freq:
                    idf = log(1 + (len(self.nodes) - self.df[term] + .5) / (self.df[term] + .5))
                    score += idf * freq * 2.5 / (freq + 1.5 * (.25 + .75 * length / self.avg))
            if score > 0:
                ranked.append(NodeWithScore(node=node, score=score))
        return sorted(ranked, key=lambda n: (-n.score, n.node.node_id))[:self.top_k]


def evidence(hit):
    return {'id': hit.node.node_id, 'text': hit.node.text, 'score': hit.score, **hit.node.metadata}
