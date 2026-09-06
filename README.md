# JFXAI4ARCH — Open-Source AI Platform Architecture

[![License](https://img.shields.io/badge/license-Open%20Source-blue.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/architecture-Cloud--Native-green.svg)](#architecture)
[![AI](https://img.shields.io/badge/AI-Agentic%20AI-purple.svg)](#ai-agent-platform)
[![RAG](https://img.shields.io/badge/RAG-Qdrant-orange.svg)](#retrieval-augmented-generation-rag)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue.svg)](#model-context-protocol-mcp)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5.svg)](#kubernetes-and-cloud-deployment)

> **Open-source, modular and self-hosted architecture for enterprise AI agents, RAG, MCP integrations, hybrid cloud/local inference and cloud-native deployment.**

---

## Table of Contents

- [Description and Context](#description-and-context)
- [Objectives](#objectives)
- [Functional Scope](#functional-scope)
- [Architecture](#architecture)
- [AI Agent Platform](#ai-agent-platform)
- [Model Context Protocol](#model-context-protocol-mcp)
- [Hybrid AI Model Strategy](#hybrid-ai-model-strategy)
- [Retrieval-Augmented Generation](#retrieval-augmented-generation-rag)
- [Data Architecture](#data-architecture)
- [Software Dependency Compendium](#software-dependency-compendium)
- [Dependency Classification](#dependency-classification)
- [Dependency Matrix](#dependency-matrix)
- [Recommended Technology Stack](#recommended-technology-stack)
- [User Guide](#user-guide)
- [Installation Guide](#installation-guide)
- [Docker Architecture](#docker-architecture)
- [Kubernetes and Azure Deployment](#kubernetes-and-azure-deployment)
- [Security and Privacy](#security-and-privacy)
- [Observability](#observability)
- [Testing and Evaluation](#testing-and-evaluation)
- [Repository Structure](#repository-structure)
- [How to Contribute](#how-to-contribute)
- [Code of Conduct](#code-of-conduct)
- [Authors](#authors)
- [Additional Information](#additional-information)
- [License](#license)
- [Roadmap](#roadmap)

---

# Description and Context

**JFXAI4ARCH** is an open-source reference architecture for building modular, self-hosted and cloud-native artificial intelligence platforms.

The architecture combines:

- Open WebUI
- LangGraph
- LangChain
- Model Context Protocol (MCP)
- Azure AI / Azure AI Foundry
- Local and open-weight language models
- Ollama
- vLLM
- Qdrant
- PostgreSQL
- FastAPI
- Docker
- Kubernetes
- Azure Kubernetes Service
- Keycloak / Azure Entra ID
- Langfuse
- OpenTelemetry
- Prometheus
- Grafana
- GitHub Actions
- Argo CD

The objective is to provide an alternative architectural foundation to proprietary AI platforms while maintaining flexibility between cloud AI services and local inference.

The current project explicitly describes this architecture as a modular, open-source and self-hosted alternative based on Open WebUI, LangGraph, MCP, Azure AI, local LLMs, Qdrant, PostgreSQL, Docker and Kubernetes.

---

# Objectives

## Primary Objectives

1. Provide a reusable enterprise AI architecture.
2. Support autonomous and semi-autonomous AI agents.
3. Integrate enterprise systems through MCP.
4. Provide Retrieval-Augmented Generation capabilities.
5. Support hybrid cloud/local inference.
6. Minimize vendor lock-in.
7. Support self-hosted deployments.
8. Provide Kubernetes-native scalability.
9. Separate AI orchestration from enterprise integrations.
10. Provide observability and governance for AI workloads.

## Architectural Principles

- Open source first
- API first
- Cloud native
- Container first
- Kubernetes ready
- Model agnostic
- Vendor neutral
- Security by design
- Human-in-the-loop
- Replaceable components
- Observable AI
- Reproducible deployment

---

# Functional Scope

JFXAI4ARCH is intended to support:

### Enterprise AI Assistants

Conversational interfaces for employees, customers and enterprise users.

### AI Agents

Stateful agents capable of:

- reasoning
- planning
- tool execution
- workflow orchestration
- API interaction
- database interaction
- multi-step tasks
- human approval

### RAG Applications

Knowledge assistants based on:

- enterprise documents
- databases
- internal repositories
- APIs
- semantic search
- vector databases

### Business Automation

Agents can interact with:

- ERP systems
- e-commerce platforms
- CRM systems
- PostgreSQL
- REST APIs
- Git repositories
- file systems
- internal services

### Cloud-Native AI

Production deployment through:

- Docker
- Kubernetes
- Azure Kubernetes Service
- Azure AI
- Azure infrastructure

---

# Architecture

## High-Level Architecture

```text
                         ┌─────────────────────────┐
                         │         USERS           │
                         │ Employees / Customers   │
                         │ Developers / Operators  │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       OPEN WEBUI        │
                         │ Chat / RAG / Documents  │
                         │ Users / Roles / Models  │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       API GATEWAY       │
                         │ FastAPI / OAuth2 / RBAC │
                         │ Rate Limits / Auditing  │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       LANGGRAPH         │
                         │ Agents / State / Tools  │
                         │ Routing / Workflows     │
                         └────────────┬────────────┘
                                      │
                     ┌────────────────┼────────────────┐
                     │                │                │
                     ▼                ▼                ▼
              ┌────────────┐   ┌────────────┐   ┌────────────┐
              │ MCP        │   │ RAG        │   │ Model      │
              │ Servers    │   │ Pipeline   │   │ Router     │
              └─────┬──────┘   └─────┬──────┘   └─────┬──────┘
                    │                │                │
                    ▼                ▼                ▼
              Enterprise       Qdrant / DB       Azure AI
              Systems          Embeddings        Local LLM
                                                   Ollama
                                                   vLLM
                                     
                         ┌─────────────────────────┐
                         │     DATA PLATFORM       │
                         │ PostgreSQL / Qdrant     │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ DOCKER / KUBERNETES    │
                         │       / AKS            │
                         └─────────────────────────┘
```

The architecture follows the structure documented by the current project, including Open WebUI, API Gateway, LangGraph, MCP, model routing, Qdrant, PostgreSQL and Kubernetes/Azure deployment.

---

# AI Agent Platform

## Open WebUI

Open WebUI provides the principal human-facing interface.

Capabilities:

- conversational AI
- model selection
- document upload
- RAG
- knowledge retrieval
- user management
- role management
- API integration
- extensible pipelines

It can operate as the primary enterprise AI portal.

---

## LangGraph

LangGraph provides the stateful agent orchestration layer.

Supported patterns include:

- multi-step workflows
- agent routing
- tool execution
- persistent state
- conditional execution
- retries
- recovery
- human approval
- multi-agent collaboration
- long-running workflows

Example:

```text
User Request
     │
     ▼
Request Classification
     │
     ├── Knowledge Question
     │       │
     │       ▼
     │     RAG
     │
     ├── Business Action
     │       │
     │       ▼
     │     MCP Tool
     │
     └── Complex Reasoning
             │
             ▼
          AI Model
```

---

# Model Context Protocol (MCP)

MCP provides a standardized integration mechanism between AI agents and external systems.

Potential MCP integrations include:

- PostgreSQL
- ERP
- e-commerce
- REST APIs
- Git
- file systems
- Azure services
- business applications
- legacy systems

Architecture:

```text
                    LangGraph Agent
                           │
                           ▼
                       MCP Client
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
     PostgreSQL          ERP            E-Commerce
       Server           Server             Server
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                     Enterprise APIs
```

MCP reduces direct coupling between the agent layer and enterprise integrations.

---

# Hybrid AI Model Strategy

The architecture supports multiple inference strategies.

```text
                         Model Router
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        Azure AI          Local LLM       Small Model
             │                │                │
       Reasoning        Private Data     Classification
       Enterprise       Cost Control     Extraction
       Workloads        Offline          Routing
```

## Workload Matrix

| Workload | Recommended Strategy |
|---|---|
| General chat | Local LLM |
| Internal RAG | Local LLM + Qdrant |
| Complex reasoning | Azure AI |
| High-volume classification | Small local model |
| Structured extraction | Local model / Azure AI |
| Enterprise automation | LangGraph + MCP |
| High-risk action | AI + human approval |

The existing project defines this hybrid routing approach explicitly.

---

# Retrieval-Augmented Generation (RAG)

## RAG Architecture

```text
Enterprise Documents
        │
        ▼
Document Processing
        │
        ▼
Text Extraction
        │
        ▼
Chunking
        │
        ▼
Embedding Model
        │
        ▼
Qdrant
        │
        ▼
Semantic Retrieval
        │
        ▼
Context Assembly
        │
        ▼
Language Model
        │
        ▼
Grounded Response
```

## Qdrant

Qdrant acts as the vector database for:

- semantic search
- vector similarity
- metadata filtering
- hybrid retrieval
- document retrieval
- embeddings
- scalable vector indexing

The project identifies Qdrant as its principal vector retrieval component.

---

# Data Architecture

## PostgreSQL

PostgreSQL is the principal transactional data store.

Recommended domains:

```text
PostgreSQL
│
├── Users
├── Organizations
├── Roles
├── Permissions
├── Agent Configurations
├── Conversations
├── Workflow Executions
├── Business Records
├── Audit Logs
├── Application Settings
└── Agent State / Checkpoints
```

PostgreSQL may also persist LangGraph workflow state.

---

# Software Dependency Compendium

This section converts the project's technology references into a reusable dependency catalog following the documentation requirements of the reference repository template.

The reference template specifically requests documentation of external resources, libraries, frameworks, databases, licenses and tested versions, together with operating-system, package-manager, SDK/compiler, internal dependency and test requirements.

---

## 1. User Interface

| Software | Role | Type | License / Status |
|---|---|---|---|
| Open WebUI | AI web interface | Core | Open source |
| Dify | Visual AI platform | Optional | Open source |
| Flowise | Visual AI workflow builder | Optional | Open source |

---

## 2. Agent Orchestration

| Software | Role | Type |
|---|---|---|
| LangGraph | Stateful agent orchestration | Core |
| LangChain | LLM application framework | Core |
| AutoGen | Multi-agent orchestration | Optional |
| Haystack | RAG/AI framework | Optional |

---

## 3. Model Integration

| Software | Role | Type |
|---|---|---|
| Azure AI | Managed AI inference | Cloud |
| Azure AI Foundry | AI development platform | Cloud |
| Ollama | Local model runtime | Core/Development |
| vLLM | High-performance inference | Production |
| LiteLLM | Model gateway | Optional |

---

## 4. Open-Weight Models

Potential model families include:

- Llama
- Qwen
- Mistral
- Gemma

Model selection should be based on:

- license
- model size
- hardware requirements
- context window
- latency
- inference cost
- multilingual capabilities
- benchmark performance
- security requirements

---

# 5. Retrieval and Vector Databases

| Software | Role | Type |
|---|---|---|
| Qdrant | Vector database | Core |
| PostgreSQL | Transactional database | Core |
| PostgreSQL + vector extension | Relational/vector workloads | Optional |
| Redis | Cache/session layer | Optional |
| Object storage | Documents/artifacts | Optional |

---

# 6. Identity and Access Management

| Software | Role |
|---|---|
| Keycloak | Self-hosted IAM / SSO |
| Azure Entra ID | Enterprise identity |
| OpenID Connect | Authentication protocol |
| OAuth 2.0 | Authorization protocol |

---

# 7. API and Backend

| Software | Role |
|---|---|
| Python | Primary backend language |
| FastAPI | API framework |
| REST | Enterprise integration |
| JSON | API data format |
| WebSocket | Real-time communication |
| MCP | AI-tool integration protocol |

---

# 8. Observability

| Software | Role |
|---|---|
| Langfuse | LLM tracing/evaluation |
| OpenTelemetry | Telemetry standard |
| Prometheus | Metrics |
| Grafana | Visualization |
| Azure Monitor | Azure observability |

---

# 9. Containerization

| Software | Role |
|---|---|
| Docker | Container runtime/build |
| Docker Compose | Local multi-service deployment |
| OCI images | Portable container artifacts |

---

# 10. Kubernetes

| Software | Role |
|---|---|
| Kubernetes | Container orchestration |
| Azure Kubernetes Service | Managed Kubernetes |
| Helm | Package management |
| Ingress | HTTP routing |
| Secrets | Secret management |
| ConfigMaps | Configuration |
| Horizontal Pod Autoscaler | Scaling |

---

# 11. CI/CD and GitOps

| Software | Role |
|---|---|
| GitHub Actions | CI/CD |
| Argo CD | GitOps |
| Git | Source control |
| Container Registry | Image storage |

---

# 12. Security

Recommended components:

- OAuth 2.0
- OpenID Connect
- Keycloak
- Azure Entra ID
- TLS
- Kubernetes Secrets
- Azure Key Vault
- network policies
- RBAC
- audit logging
- container scanning
- dependency scanning
- static analysis

---

# Dependency Classification

Every dependency should be classified as one of the following:

| Classification | Description |
|---|---|
| Core | Required by the architecture |
| Runtime | Required during execution |
| Build | Required to compile/build |
| Development | Required by developers |
| Test | Required for testing |
| Optional | Replaceable capability |
| Cloud | External cloud service |
| Integration | Enterprise integration |
| Research | Experimental technology |
| Reference | Architectural reference |
| Legacy | Maintained for compatibility |
| Deprecated | Not recommended for new deployments |

---

# Dependency Specification Template

Each dependency should eventually be documented using the following structure:

```yaml
name:
category:
dependency_type:
purpose:

repository:
official_website:

license:
license_compatibility:

programming_language:
version_tested:

installation:
runtime_requirements:
build_requirements:

api:
protocols:
data_formats:

integration:
security_considerations:
privacy_considerations:

performance_considerations:
hardware_requirements:
operating_systems:

container_support:
ai_integration:
rag_integration:
mcp_integration:

status:
maintenance_status:
last_review:

documentation:
```

This structure is intended to make the compendium maintainable as the platform evolves.

---

# Dependency Matrix

| Component | Category | Required | Deployment | Main Function |
|---|---|---:|---|---|
| Open WebUI | UI | Yes | Docker/K8s | AI interface |
| FastAPI | Backend | Yes | Docker/K8s | API |
| LangGraph | Agents | Yes | Docker/K8s | Orchestration |
| LangChain | AI Framework | Yes | Docker/K8s | LLM integration |
| MCP | Integration | Yes | Docker/K8s | Tool integration |
| Qdrant | RAG | Yes | Docker/K8s | Vector search |
| PostgreSQL | Data | Yes | Docker/Azure | Transactional data |
| Ollama | Inference | Optional | Local | Local models |
| vLLM | Inference | Optional | GPU/K8s | Production inference |
| Azure AI | AI | Optional | Azure | Managed inference |
| Keycloak | Security | Optional | Docker/K8s | IAM |
| Entra ID | Security | Optional | Azure | Enterprise IAM |
| Langfuse | Observability | Recommended | Docker/K8s | AI tracing |
| OpenTelemetry | Observability | Recommended | K8s | Telemetry |
| Prometheus | Observability | Recommended | K8s | Metrics |
| Grafana | Observability | Recommended | K8s | Dashboards |
| Docker | Infrastructure | Yes | Host/CI | Containers |
| Kubernetes | Infrastructure | Production | K8s | Orchestration |
| Helm | Deployment | Recommended | K8s | Packaging |
| Argo CD | DevOps | Recommended | K8s | GitOps |
| GitHub Actions | CI/CD | Recommended | GitHub | Automation |

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

integration:
  - Model Context Protocol
  - MCP Servers

cloud_ai:
  - Azure AI
  - Azure AI Foundry

local_ai:
  development:
    - Ollama

  production:
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

The technology stack corresponds closely to the architecture currently documented in JFXAI4ARCH.

---

# User Guide

## 1. Start the Platform

Start the local infrastructure:

```bash
docker compose up -d
```

## 2. Access Open WebUI

Open the configured Open WebUI endpoint.

## 3. Configure Models

Configure:

- local models
- Azure AI models
- model routing policies

## 4. Configure Knowledge

Load:

- PDFs
- documents
- enterprise knowledge
- structured data
- repositories

## 5. Configure RAG

Configure:

```text
Documents
   ↓
Embedding
   ↓
Qdrant
   ↓
Retriever
   ↓
LangGraph
   ↓
LLM
```

## 6. Configure MCP

Register MCP servers for required enterprise systems.

## 7. Execute Agent Workflows

Users can submit:

- questions
- document queries
- business actions
- automation tasks
- multi-step workflows

---

# Installation Guide

## System Requirements

Recommended baseline:

```text
OS:
  Linux
  macOS
  Windows + WSL2

Container:
  Docker
  Docker Compose

Development:
  Python 3.x
  Git

Production:
  Kubernetes
  Helm
  Container Registry

AI:
  CPU inference or
  NVIDIA GPU for accelerated inference

Data:
  PostgreSQL
  Qdrant
```

> Exact tested versions should be recorded in the project's dependency matrix before declaring a release as reproducible.

---

# Local Installation

Clone the repository:

```bash
git clone https://github.com/robotics-intelligent-systems/jfxai4arch.git
cd jfxai4arch
```

Create the environment:

```bash
cp .env.example .env
```

Configure:

```text
DATABASE_URL
QDRANT_URL
AZURE_AI_ENDPOINT
AZURE_AI_API_KEY
MODEL_PROVIDER
MCP_SERVER_URL
```

Start the infrastructure:

```bash
docker compose up -d
```

Check services:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

---

# Testing

Recommended validation levels:

## Unit Tests

```bash
pytest
```

## API Tests

```bash
pytest tests/api
```

## Agent Tests

Validate:

- state transitions
- tool execution
- retry behavior
- human approval
- model routing

## RAG Tests

Evaluate:

- retrieval precision
- retrieval recall
- grounding
- hallucination rate
- answer relevance

## MCP Tests

Validate:

- authentication
- authorization
- tool discovery
- tool execution
- failure handling

## Infrastructure Tests

Validate:

- Docker images
- Kubernetes manifests
- Helm charts
- readiness probes
- liveness probes
- autoscaling

---

# Docker Architecture

The recommended container organization is:

```text
ai-platform/
│
├── open-webui/
│
├── agent-api/
│   ├── FastAPI/
│   ├── LangGraph/
│   ├── MCP Clients/
│   └── Model Router/
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

This organization follows the Docker architecture already proposed by the project.

---

# Kubernetes and Cloud Deployment

Production deployment can target Azure Kubernetes Service.

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
├── PostgreSQL
│
├── Azure AI
│
├── Azure Key Vault
│
├── Azure Container Registry
│
└── Azure Monitor
```

The existing repository describes AKS as the production target and includes Azure AI, Key Vault, Container Registry and Azure Monitor in the deployment architecture.

---

# Security and Privacy

## Security Principles

- Zero-trust service communication
- Least privilege
- RBAC
- OAuth2/OIDC
- Secret isolation
- TLS
- Network segmentation
- Audit logging
- Container scanning
- Dependency scanning

## AI Security

Agents should not automatically execute high-risk operations.

Recommended pattern:

```text
User
 │
 ▼
Agent
 │
 ▼
Risk Assessment
 │
 ├── Low Risk ───────► Automatic Execution
 │
 ├── Medium Risk ────► Additional Validation
 │
 └── High Risk ──────► Human Approval
```

---

# Observability

AI workloads require observability beyond conventional application metrics.

Recommended telemetry:

### Application

- request latency
- throughput
- errors
- availability

### AI

- token consumption
- model latency
- inference cost
- model selection
- prompt/response traces
- agent execution paths

### RAG

- retrieval latency
- top-k results
- relevance
- embedding latency
- grounding quality

### Agents

- workflow duration
- tool execution
- retries
- failures
- state transitions

Recommended stack:

```text
OpenTelemetry
      │
      ├── Metrics ──► Prometheus ──► Grafana
      │
      ├── Traces ──► Langfuse
      │
      └── Logs ────► Central Logging
```

---

# Testing and Evaluation

## Functional Testing

Validate:

- API functionality
- authentication
- model invocation
- RAG
- MCP tools
- agent workflows

## AI Evaluation

Measure:

- answer correctness
- groundedness
- hallucination
- relevance
- latency
- token consumption
- cost

## Security Evaluation

Perform:

- dependency scanning
- SAST
- container scanning
- API security testing
- authentication testing
- authorization testing
- prompt injection testing
- tool abuse testing

---

# Repository Structure

Recommended repository structure:

```text
jfxai4arch/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE-OF-CONDUCT.md
│
├── docs/
│   ├── architecture/
│   ├── deployment/
│   ├── security/
│   ├── rag/
│   ├── agents/
│   ├── mcp/
│   ├── observability/
│   └── dependencies/
│       ├── software-compendium.md
│       └── dependency-matrix.csv
│
├── src/
│   ├── api/
│   ├── agents/
│   ├── mcp/
│   ├── rag/
│   ├── models/
│   ├── routing/
│   └── security/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── agents/
│   ├── rag/
│   └── security/
│
├── docker/
│
├── kubernetes/
│   ├── namespaces/
│   ├── deployments/
│   ├── services/
│   ├── ingress/
│   └── secrets/
│
├── helm/
│
└── docker-compose.yml
```

---

# How to Contribute

Contributions are welcome.

Recommended workflow:

```bash
git checkout -b feature/my-feature
```

Implement the change.

Run tests:

```bash
pytest
```

Run static analysis:

```bash
ruff check .
```

Commit:

```bash
git commit -m "feat: add new AI capability"
```

Push:

```bash
git push origin feature/my-feature
```

Then open a Pull Request.

Contributions should include:

- documentation
- tests
- architecture impact
- security considerations
- dependency changes
- backward compatibility information

---

# Code of Conduct

All contributors should:

- communicate respectfully
- provide constructive feedback
- avoid discrimination or harassment
- document architectural decisions
- respect software licenses
- protect confidential information
- follow responsible AI principles

The repository should maintain a `CODE-OF-CONDUCT.md` file defining the complete community rules.

---

# Authors

**Robotics Intelligent Systems**

GitHub organization:

```text
https://github.com/robotics-intelligent-systems
```

Project:

```text
https://github.com/robotics-intelligent-systems/jfxai4arch
```

Reference documentation template:

```text
https://github.com/sdk2035/Plantilla-de-repositorio
```

---

# Additional Information

## Related Architecture Projects

JFXAI4ARCH can be considered part of a broader AI/software engineering ecosystem.

Potential complementary repositories include:

- **JFXAI4NLP** — Natural Language Processing and language intelligence.
- **JFXAI4MAD** — AI-powered social/matchmaking applications.
- **JFXENGINE** — Engineering, MBSE and digital-twin architecture.

The three domains can share:

```text
                JFXAI4ARCH
              AI Platform Core
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
   JFXAI4NLP     JFXAI4MAD     JFXENGINE
   Language      Social AI     Engineering
   Intelligence  Intelligence  Intelligence
```

---

# Architecture Governance

Architectural changes should be documented through Architecture Decision Records (ADRs).

Recommended structure:

```text
docs/
└── architecture/
    └── adr/
        ├── ADR-001-agent-orchestration.md
        ├── ADR-002-model-routing.md
        ├── ADR-003-vector-database.md
        ├── ADR-004-mcp-integration.md
        ├── ADR-005-identity-management.md
        └── ADR-006-kubernetes-deployment.md
```

Each ADR should document:

- Context
- Decision
- Alternatives
- Consequences
- Security implications
- Operational implications

---

# Responsible AI

The platform should implement responsible AI controls for:

- transparency
- traceability
- human oversight
- data minimization
- privacy
- security
- model evaluation
- bias assessment
- explainability where appropriate

Agents should not be granted unrestricted access to enterprise systems.

---

# Roadmap

## Phase 1 — Foundation

- [x] Open WebUI architecture
- [x] LangGraph architecture
- [x] MCP integration concept
- [x] Qdrant RAG architecture
- [x] PostgreSQL architecture
- [x] Docker architecture

## Phase 2 — AI Platform

- [ ] Agent API implementation
- [ ] Model router
- [ ] MCP server catalog
- [ ] RAG service
- [ ] Authentication
- [ ] Observability

## Phase 3 — Cloud Native

- [ ] Kubernetes manifests
- [ ] Helm charts
- [ ] AKS deployment
- [ ] GitHub Actions
- [ ] Argo CD
- [ ] Azure Key Vault integration

## Phase 4 — Enterprise AI

- [ ] Multi-agent workflows
- [ ] Enterprise ERP integration
- [ ] E-commerce integration
- [ ] Advanced RAG
- [ ] AI governance
- [ ] Model evaluation platform

## Phase 5 — Sovereign / Hybrid AI

- [ ] Local GPU inference
- [ ] vLLM production cluster
- [ ] Model quantization
- [ ] Offline deployment
- [ ] Private AI infrastructure
- [ ] Air-gapped deployment

---

# Key Benefits

JFXAI4ARCH provides:

- Open-source architecture
- Self-hosted AI
- Hybrid cloud/local inference
- Replaceable AI components
- Enterprise agent orchestration
- Standardized MCP integrations
- RAG with Qdrant
- Transactional persistence with PostgreSQL
- Docker-based deployment
- Kubernetes scalability
- Azure integration
- AI observability
- Improved infrastructure control
- Flexible model routing

These benefits are consistent with the project's current architecture and stated goals.

---

# License

The license of the implementation must be explicitly defined in the repository's `LICENSE` file.

All third-party dependencies must be reviewed individually for:

- license compatibility
- redistribution requirements
- attribution requirements
- model-specific terms
- commercial-use restrictions
- deployment restrictions

> **Important:** The dependency compendium should not assume that every component listed in the architecture has the same license. Each dependency must be verified against its authoritative project documentation before release.

---

# Dependency Governance

For every production dependency, maintain:

```text
Name
Version
License
Repository
Official Documentation
Purpose
Runtime Requirements
Build Requirements
Security Status
Known CVEs
Container Support
Kubernetes Support
Last Review
Replacement Candidate
```

A recommended file is:

```text
docs/dependencies/software-compendium.md
```

and a machine-readable matrix:

```text
docs/dependencies/dependency-matrix.csv
```

---

# Conclusion

JFXAI4ARCH defines a modular architecture for building enterprise AI systems without coupling the entire platform to a single model provider or proprietary application stack.

The combination of:

```text
Open WebUI
      +
FastAPI
      +
LangGraph
      +
MCP
      +
Azure AI / Local LLMs
      +
Qdrant
      +
PostgreSQL
      +
Docker
      +
Kubernetes
```

provides a reusable foundation for:

- enterprise AI assistants
- RAG systems
- multi-agent platforms
- business automation
- ERP integrations
- e-commerce integrations
- AI-powered developer tools
- knowledge management
- hybrid Azure/on-premises AI
- private and sovereign AI deployments

The architecture therefore functions not only as an individual repository but also as a **reference platform for integrating language intelligence, enterprise automation, agentic AI and domain-specific AI applications**.

---

## Reference Sources

- JFXAI4ARCH repository: https://github.com/robotics-intelligent-systems/jfxai4arch
- Repository documentation template: https://github.com/sdk2035/Plantilla-de-repositorio
- Robotics Intelligent Systems organization: https://github.com/robotics-intelligent-systems