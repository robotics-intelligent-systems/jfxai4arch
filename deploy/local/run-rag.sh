#!/usr/bin/env sh
set -eu
: "${RAG_CORPUS_DIR:?Set RAG_CORPUS_DIR to an absolute directory of UTF-8 Markdown/TXT files}"
: "${RAG_API_TOKEN:?Set RAG_API_TOKEN to a random secret of at least 24 characters}"
exec python -m uvicorn jfx_rag.app:create_app --factory --host 127.0.0.1 --port 8000 --no-access-log
