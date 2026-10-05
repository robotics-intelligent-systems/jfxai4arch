# Technical RAG pilot

This is the first executable slice of the architecture in the root README: LlamaIndex nodes and retriever interfaces, an explicit BM25 lexical baseline, FastAPI, optional local Ollama generation, optional local Langfuse metadata and Bruno requests. No default embedding or language model provider is instantiated.

## Start locally

From the repository root, with Python 3.11+ (tested on Linux / Python 3.12):

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r services/rag-service/requirements-tested.txt
python -m pip install --no-deps -e services/rag-service
export RAG_CORPUS_DIR="$PWD/docs/rag/sample-corpus"
export RAG_API_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
sh deploy/local/run-rag.sh
```

Installation is a connected preparation step. `requirements-tested.txt` records the exact versions tested, including optional telemetry and testing dependencies. It is not a hash-verified offline supply bundle. Build and approve a wheelhouse for the target platform before disconnected deployment. These commands do not download models.

In another terminal with the same token set securely:

```sh
curl http://127.0.0.1:8000/v1/answers \
  -H "Authorization: Bearer $RAG_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"question":"¿Cómo se relacionan Qdrant y PostgreSQL?","top_k":3}'
```

The default returns `evidence_only`: text, relative source file, one-based line range, SHA-256 and evidence ID. No lexical match returns `abstained`. A matching term establishes lexical relevance, not that a passage answers the entire question.

Use a dedicated directory of UTF-8 Markdown/TXT files; extensions are case-insensitive. The [sample corpus](sample-corpus/) is a bilingual paraphrase of the [architecture at commit 99c7fe6](https://github.com/robotics-intelligent-systems/jfxai4arch/blob/99c7fe6ca3d593fcde02f5cd3a0bd40620bb51ea/README.md). It describes proposed components, not deployed systems. It is demonstration data, not an approved engineering knowledge base. PDF, OCR and bibliography ingestion remain future work.

## Optional generated answers

Provision Ollama separately and select an **already installed** local model that supports structured JSON output:

```sh
export RAG_MODEL='your-approved-local-model'
export RAG_OLLAMA_URL='http://127.0.0.1:11434'
sh deploy/local/run-rag.sh
```

The service requests structured claims and checks that every claim cites only retrieved evidence IDs. Unknown citations, invalid JSON and unavailable inference fall back to `evidence_only`. Empty model claims return `abstained`. Requests time out after 60 seconds and do not follow redirects or use environment proxies.

**Valid citation IDs do not establish factual correctness or entailment.** Human support assessment is still required. No real model was available during development: the adapter was tested with simulated Ollama responses, including success, timeout, invalid citations and abstention. Model quality, hardware needs, inference latency and resource cost remain unmeasured. The service has no tool execution capability.

## API and document lifecycle

| Route | Behavior |
|---|---|
| `GET /health` | Public process liveness, not corpus/model readiness |
| `POST /v1/search` | Authenticated retrieval; `question` and optional `top_k` (1–10) |
| `POST /v1/answers` | Same input; `generated`, `evidence_only`, or `abstained` |
| `GET /v1/evidence/{id}` | Authenticated lookup of current evidence |

Each request reads a fresh in-memory corpus. No persistent index, cache or upload API exists. The generation hash covers document paths and hashes; evidence IDs also cover line ranges. Replacing/removing a file invalidates its previous IDs at the next request. A corpus change detected after inference produces HTTP 409 for retry; unreadable or invalid corpora produce HTTP 503.

The corpus must be operator-controlled and stable during requests. This reader is not a transactional filesystem snapshot and does not protect against a malicious concurrent filesystem writer. Publish updates between requests. Managed ingestion and transactional revocation are required before production. Already delivered evidence cannot be recalled from clients.

Limits: 1,000 candidate documents, 2 MB/file, 20 MB total, 6,000 characters/line, 30 lines/chunk with 5-line overlap, 2,000 characters/question. Symlinks are excluded. Documents are treated as text; embedded links and commands are not executed. Rebuilding BM25 each request is suitable only for a small pilot. There is no semantic translation or cross-language retrieval: sample documents contain both English and Spanish.

## Local scope

The launcher binds to `127.0.0.1`. All content routes require a random bearer token of at least 24 characters. Swagger/OpenAPI routes are disabled. This is a **single-user shared-corpus pilot**, without per-document ACLs. Do not expose the service publicly or combine documents with different access permissions.

Model/telemetry endpoints must use loopback hosts. This configuration check is not an OS-level egress boundary. Validate a deny-egress deployment separately before claiming complete offline compliance.

The target architecture's Qdrant/PostgreSQL hybrid retrieval, GLiNER2 extraction, reranking, ACLs, OCR, bibliography workflows, managed ingestion and enterprise deployment remain unimplemented.

## Optional Langfuse

Provision a local Langfuse server separately; the tested requirements include its SDK. Set:

```sh
export RAG_LANGFUSE_URL='http://127.0.0.1:3000'
export LANGFUSE_PUBLIC_KEY='your-local-public-key'
export LANGFUSE_SECRET_KEY='your-local-secret-key'
```

Leave `RAG_LANGFUSE_URL` unset to disable telemetry (default). The application sends only status, evidence count and duration in a `rag-answer` observation, without questions, file names, document text or generated claims. Keep SDK debugging and unrelated auto-instrumentation disabled. Local tests verify adapter metadata; a live Langfuse backend was not provisioned. This is not a Langfuse deployment package.

## Verification

```sh
python -m pytest -q tests/rag
python tests/rag/evaluate.py
```

Development verification: 22 automated tests passed on Python 3.12, including provenance, authentication, file withdrawal, invalid citations, inference failure and metadata minimization. The launcher also passed a live loopback HTTP check; Bruno CLI 4.2.0 passed all 3 requests and 3 tests. One upstream Starlette TestClient deprecation warning remains.

The [starter report](smoke-results.json) measures document recall@3, MRR@3 and no-match abstention over 12 positive bilingual questions and 2 negatives. These easy synthetic cases detect basic regressions; they do not establish domain quality or a calibrated abstention threshold.

Before expansion, curate at least 50 independently written questions with relevant passages and unanswerable cases from approved technical documents. Separate development and held-out sets. Measure recall/nDCG, claim support, citation validity, false answers on unsupported questions, p50/p95 latency and resource use. Compare embeddings, reranking and GLiNER2 against this same baseline.

Open `tools/bruno/rag` in Bruno and define local variables `baseUrl=http://127.0.0.1:8000` and `token` (the running service token). Keep secrets outside Git. Run Health, Search and Answers with the sample corpus. Search and Answers assert evidence and response structure.

## Integration sequence

1. Review the baseline and replace samples with an approved technical corpus.
2. Validate an installed local generation model and a local Langfuse backend.
3. Compare dense retrieval against BM25 on held-out questions.
4. Add identity, document permissions and transactional ingestion/withdrawal before team use.
5. Evaluate whether GLiNER2 improves extraction and answer support.

## References

- [LlamaIndex core source](https://github.com/run-llama/llama_index/tree/main/llama-index-core/llama_index/core)
- [Ollama structured outputs](https://github.com/ollama/ollama/blob/main/docs/capabilities/structured-outputs.mdx)
- [Langfuse Python SDK](https://github.com/langfuse/langfuse-python)
- [Bruno scripting reference](https://github.com/usebruno/bruno-docs/blob/main/testing/script/javascript-reference.mdx)
