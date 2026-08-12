# Agent-Powered Cloud Platform

## Overview

sim is an open-source CLI and local runtime that lets Codex, Claude Code, GitHub Copilot, Gemini, and other agents work with simulation software through solver-specific plugins and bundled skills. Kata Containers is an open source container runtime, building lightweight virtual machines. Cloud-Native GenAI Reference Architecture. The SmythOS Runtime Environment (SRE) is an open-source, cloud-native runtime for agentic AI. This project proposes a modular, open-source, and self-hosted alternative to proprietary AI platforms. This project proposes a modular, open-source, and self-hosted alternative to proprietary AI platforms. The architecture is designed to support enterprise-grade AI agents, Retrieval-Augmented Generation (RAG), workflow automation, Model Context Protocol (MCP) integrations, and hybrid AI deployments using both Azure AI services and locally hosted language models.

The platform combines **Open WebUI**, **LangGraph**, **MCP**, **Azure AI**, **local LLMs**, **Qdrant**, **PostgreSQL**, **Docker**, and **Kubernetes** into a scalable and portable AI ecosystem.

---

## High-Level Architecture

```text
Users / Enterprise Teams
          │
          ▼
┌──────────────────────────┐
│        Open WebUI        │
│ Chat · RAG · Documents   │
│ Users · Roles · Models   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       API Gateway        │
│ FastAPI · OAuth2         │
│ Rate Limits · Auditing   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────────────┐
│            LangGraph             │
│ Agents · Workflows · State       │
│ Routing · Human Approval · Retry │
└────────────┬─────────────────────┘
             │
       ┌─────┴──────┐
       ▼            ▼
┌─────────────┐ ┌────────────────┐
│ MCP Servers │ │  Model Router  │
│ Tools · APIs│ │ Azure · Local  │
└──────┬──────┘ └────────┬───────┘
       │                 │
       ▼                 ▼
 Enterprise APIs      Azure AI
 ERP · E-Commerce    Local LLMs
 Databases · Git     Ollama · vLLM
 Files · Services
       │
       ▼
┌──────────────────────────────────┐
│ Knowledge and Application Data   │
│ Qdrant · PostgreSQL              │
└──────────────────────────────────┘
             │
             ▼
 Docker → Kubernetes → Azure AKS
```

---

# Core Components

## Open WebUI

**Open WebUI** provides the main user interface for interacting with AI models and enterprise knowledge systems.

### Main capabilities

* ChatGPT-like self-hosted interface
* Support for local and cloud-based language models
* Document upload and knowledge retrieval
* Retrieval-Augmented Generation (RAG)
* User and role management
* Model selection
* API integrations
* Extensible pipelines and tools

Open WebUI can act as the primary AI portal for employees, customers, development teams, and enterprise users.

---

## LangGraph

**LangGraph** is the core agent orchestration layer.

It manages stateful AI workflows and supports complex agent behaviors, including:

* Multi-step workflows
* Agent routing
* Tool execution
* Persistent state
* Conditional workflows
* Retry and recovery mechanisms
* Human-in-the-loop approval
* Multi-agent collaboration
* Long-running processes

LangGraph is especially suitable for enterprise workflows where AI agents must interact with databases, APIs, business systems, and external services.

Example workflow:

```text
User Request
      │
      ▼
Request Classification
      │
      ├── Knowledge Question
      │         │
      │         ▼
      │       Qdrant RAG
      │
      ├── Business Action
      │         │
      │         ▼
      │       MCP Tool
      │
      └── Complex Reasoning
                │
                ▼
           Azure AI Model
```

---

## Model Context Protocol (MCP)

**Model Context Protocol (MCP)** provides a standardized integration layer between AI agents and external systems.

MCP servers can expose enterprise tools such as:

* PostgreSQL databases
* ERP systems
* E-commerce platforms
* Internal REST APIs
* Git repositories
* File systems
* Azure services
* Business applications
* Legacy enterprise systems

Example:

```text
LangGraph Agent
       │
       ▼
    MCP Client
       │
       ├── PostgreSQL MCP Server
       ├── ERP MCP Server
       ├── E-Commerce MCP Server
       ├── Azure MCP Server
       └── Internal API MCP Server
```

This approach reduces direct coupling between agents and enterprise integrations.

---

## Azure AI and Local Models

The platform supports a hybrid AI strategy.

```text
User Request
      │
      ▼
Model Router
      │
      ├── Azure AI
      │      └── Advanced reasoning and enterprise workloads
      │
      ├── Local LLM
      │      └── Private data and cost-sensitive workloads
      │
      └── Small Local Model
             └── Classification, extraction, and routing
```

### Azure AI use cases

Azure AI can be used for:

* Advanced reasoning
* High-quality responses
* Large-scale enterprise workloads
* Managed AI services
* Cloud-based model deployment
* Enterprise security and governance

### Local model use cases

Local models can be used for:

* Private or sensitive data
* Lower inference costs
* Offline or isolated environments
* Internal knowledge systems
* High-volume classification
* Document extraction
* Lightweight AI tasks

### Local inference options

* **Ollama** — Local development, testing, and small deployments
* **vLLM** — High-performance GPU inference in production
* **Llama** — General-purpose open-weight language models
* **Qwen** — Strong multilingual and coding capabilities
* **Mistral** — Efficient general-purpose models
* **Gemma** — Lightweight and scalable AI workloads

---

# Retrieval-Augmented Generation (RAG)

## Qdrant

**Qdrant** is used as the vector database for semantic search and knowledge retrieval.

### Capabilities

* Vector similarity search
* Semantic search
* Metadata filtering
* Hybrid search
* Document retrieval
* Embedding storage
* Scalable vector indexing

Example RAG pipeline:

```text
Enterprise Documents
          │
          ▼
Document Processing
          │
          ▼
Text Chunking
          │
          ▼
Embedding Model
          │
          ▼
Qdrant Vector Database
          │
          ▼
Relevant Context Retrieval
          │
          ▼
Language Model
          │
          ▼
Grounded AI Response
```

---

## PostgreSQL

**PostgreSQL** stores transactional and operational application data.

Recommended data domains include:

* Users
* Organizations
* Roles and permissions
* AI agent configurations
* Conversations
* Workflow executions
* Business records
* Audit logs
* Application settings
* Agent state and checkpoints

PostgreSQL can also be used to persist LangGraph workflow state.

---

# Complementary Open-Source Tools

| Tool       | Primary Role                   | Recommended Use                            |
| ---------- | ------------------------------ | ------------------------------------------ |
| Open WebUI | AI chat interface              | Main enterprise AI portal                  |
| LangGraph  | Agent orchestration            | Stateful and complex AI workflows          |
| MCP        | Standardized integrations      | Enterprise tools and external services     |
| Dify       | Visual AI application platform | Rapid prototyping and low-code development |
| Flowise    | Visual AI workflow builder     | LangChain-based low-code workflows         |
| Haystack   | RAG framework                  | Search and document-centric applications   |
| AutoGen    | Multi-agent framework          | Agent collaboration scenarios              |
| LiteLLM    | LLM gateway                    | Unified access to Azure and local models   |
| Langfuse   | AI observability               | Tracing, evaluation, and cost monitoring   |
| Keycloak   | Identity and access management | Self-hosted authentication and SSO         |
| Argo CD    | GitOps deployment              | Kubernetes continuous delivery             |

---

# Hybrid Model Strategy

A hybrid architecture allows the platform to select the most appropriate model based on workload requirements.

| Workload                   | Recommended Model             |
| -------------------------- | ----------------------------- |
| General chat               | Local LLM                     |
| Internal document RAG      | Local LLM + Qdrant            |
| Complex reasoning          | Azure AI                      |
| High-volume classification | Small local model             |
| Structured data extraction | Small local model or Azure AI |
| Enterprise automation      | LangGraph + MCP               |
| High-risk business actions | Azure AI + human approval     |

---

# Docker Architecture

The platform can initially be deployed using Docker Compose.

```text
ai-platform/
│
├── open-webui/
│
├── agent-api/
│   ├── FastAPI
│   ├── LangGraph
│   ├── MCP Clients
│   └── Model Router
│
├── mcp-servers/
│   ├── postgresql/
│   ├── ecommerce/
│   ├── erp/
│   └── azure/
│
├── rag-service/
│
├── qdrant/
│
├── postgresql/
│
├── observability/
│   ├── langfuse/
│   ├── prometheus/
│   └── grafana/
│
├── docker-compose.yml
│
└── kubernetes/
    ├── namespaces/
    ├── deployments/
    ├── services/
    ├── ingress/
    ├── secrets/
    └── helm/
```

---

# Kubernetes and Azure Deployment

For production environments, the platform can be deployed on **Azure Kubernetes Service (AKS)**.

```text
Azure Kubernetes Service
│
├── Open WebUI
│
├── Agent API
│   ├── FastAPI
│   └── LangGraph
│
├── MCP Servers
│
├── Model Router
│
├── Qdrant
│
├── PostgreSQL Flexible Server
│
├── Azure AI Services
│
├── Azure Key Vault
│
├── Azure Container Registry
│
└── Azure Monitor
```

---

# Recommended Technology Stack

```yaml
frontend:
  - Open WebUI

backend:
  - Python
  - FastAPI

agent_orchestration:
  - LangGraph
  - LangChain

integrations:
  - Model Context Protocol
  - MCP Servers

ai_models:
  cloud:
    - Azure AI
    - Azure AI Foundry
  local_development:
    - Ollama
  local_production:
    - vLLM
  open_models:
    - Llama
    - Qwen
    - Mistral
    - Gemma

knowledge_retrieval:
  - Qdrant
  - Embedding Models

application_data:
  - PostgreSQL

authentication:
  - Keycloak
  - Azure Entra ID
  - OpenID Connect

observability:
  - Langfuse
  - OpenTelemetry
  - Prometheus
  - Grafana

containerization:
  - Docker

orchestration:
  - Kubernetes
  - Azure Kubernetes Service

ci_cd:
  - GitHub Actions
  - Argo CD
```

---

# Key Benefits

* Open-source and self-hosted architecture
* Reduced dependency on proprietary AI platforms
* Support for Azure AI and local language models
* Modular and replaceable components
* Enterprise-ready AI agents
* Standardized integrations through MCP
* Scalable RAG with Qdrant
* Reliable transactional storage with PostgreSQL
* Containerized deployment with Docker
* Production scalability through Kubernetes and AKS
* Improved data privacy and infrastructure control
* Flexible model routing based on cost, performance, and privacy

---

# Conclusion

This architecture provides a modular, scalable, portable, and enterprise-ready open-source AI platform.

By combining **Open WebUI**, **LangGraph**, **MCP**, **Azure AI**, **local language models**, **Qdrant**, **PostgreSQL**, **Docker**, and **Kubernetes**, organizations can build AI systems with greater flexibility and infrastructure control than many closed or proprietary AI platforms.

The architecture is suitable for:

* Enterprise AI assistants
* Internal knowledge platforms
* AI-powered business automation
* Multi-agent systems
* RAG applications
* ERP and e-commerce integrations
* Cloud-native AI services
* Hybrid Azure and on-premises deployments
* Secure enterprise AI workloads
