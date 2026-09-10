
<p align="center">
  <img src="open-source-ai-architecture.jpg"
       alt="JFXAI4ARCH Open-Source AI Platform Architecture"
       width="100%" />
</p>

<p align="center">
  <em>Open-source, modular and self-hosted AI platform architecture for enterprise agents, RAG, MCP integrations, hybrid cloud/local inference and cloud-native deployment.</em>
</p>

# Open-Source Agent-Powered Cloud Platform Architecture

> Modular, self-hosted and hybrid AI platform architecture combining enterprise AI, local models, agent workflows, MCP integrations, declarative YAML automation, local agent-harness routing, Microsoft 365/.NET agents, RAG, observability and cloud-native deployment.

## Overview

`jfxai4arch` defines an open, modular and self-hosted alternative architecture for enterprise AI platforms.

The platform combines:

- Open WebUI for the user-facing AI portal.
- LangGraph / LangChain for stateful agent orchestration.
- Model Context Protocol (MCP) for standardized tool and enterprise-system integration.
- Azure AI / Azure AI Foundry for managed cloud AI.
- Ollama and vLLM for local inference.
- LiteLLM or equivalent model-gateway abstractions.
- Qdrant for vector search and RAG.
- PostgreSQL for transactional, workflow and operational data.
- Docker and Kubernetes / Azure Kubernetes Service for deployment.
- **model-compose** as an alternative declarative YAML automation and AI-service composition layer.
- **HarnessRouter** as an optional self-hosted local router/runtime abstraction for coding-agent harnesses such as Codex.
- **Microsoft 365 Agents SDK for C#/.NET** as an optional enterprise-agent SDK for .NET, Microsoft 365, Teams, Copilot Studio and multichannel integrations.

The goal is not to require every component simultaneously. The architecture is designed so that orchestration, model routing, agent runtimes, enterprise SDKs and deployment technologies can be selected or replaced according to workload, privacy, cost and operational requirements.

---

# Updated High-Level Architecture

```text
Users / Enterprise Teams
          |
          v
+------------------------------+
|          Open WebUI          |
| Chat | RAG | Docs | Roles    |
+--------------+---------------+
               |
               v
+------------------------------+
|          API Gateway         |
| OAuth2 | OIDC | Audit | RBAC |
+--------------+---------------+
               |
               v
+-------------------------------------------------------------+
|                 AGENT / WORKFLOW LAYER                      |
|                                                             |
|  LangGraph / LangChain                                      |
|       |                                                     |
|       +---- model-compose (alternative YAML composition)    |
|       |                                                     |
|       +---- Microsoft 365 Agents SDK (.NET)                 |
|                                                             |
|  Stateful workflows | Tools | Human approval | Multi-agent  |
+----------------------+--------------------------------------+
                       |
          +------------+-------------+
          |                          |
          v                          v
+-------------------------+   +------------------------------+
| MCP / Enterprise Tools  |   | Agent Harness / Model Access |
| ERP | CRM | DB | Git    |   |                              |
| E-Commerce | Azure APIs |   | HarnessRouter (local option) |
+------------+------------+   | Codex / other harnesses      |
             |                |                              |
             |                | LiteLLM / Model Router       |
             |                | Azure AI / Local LLMs        |
             |                +--------------+---------------+
             |                               |
             +----------------+--------------+
                              |
                              v
+-------------------------------------------------------------+
|               KNOWLEDGE / APPLICATION DATA                  |
| Qdrant | PostgreSQL | Files | State | Checkpoints | Audit   |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                 OBSERVABILITY & SECURITY                    |
| Langfuse | OpenTelemetry | Prometheus | Grafana | Keycloak |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|               CONTAINER / CLOUD PLATFORM                    |
| Docker Compose -> Kubernetes -> Azure Kubernetes Service    |
+-------------------------------------------------------------+
```

---

# Agent and Automation Strategy

The project supports multiple complementary orchestration patterns instead of treating one agent framework as mandatory.

## Option A — LangGraph / LangChain

Recommended for:

- stateful workflows;
- conditional routing;
- persistent agent state;
- retry/recovery;
- tool invocation;
- human-in-the-loop approval;
- multi-agent coordination;
- enterprise MCP integrations.

## Option B — model-compose

Repository:

`https://github.com/sdk2035/model-compose`

`model-compose` is included as an **alternative declarative automation and composition layer**.

It allows AI services to be described through a `model-compose.yml` file, with models, autonomous agents, workflows, tools, RAG pipelines and MCP servers treated as composable building blocks.

### Proposed role in jfxai4arch

```text
model-compose.yml
       |
       +-- Models
       +-- Agents
       +-- Workflows
       +-- RAG
       +-- MCP Servers
       +-- Tools
       |
       v
Portable AI Service
       |
Local | Docker | Kubernetes | Cloud
```

This makes it useful for:

- specification-driven AI deployment;
- lightweight YAML automation;
- portable AI-service definitions;
- local/cloud hybrid workflows;
- agent prototypes;
- MCP service composition;
- reproducible deployment definitions.

Example architecture profile:

```yaml
automation:
  primary:
    type: langgraph

  alternative:
    type: model-compose
    config: model-compose.yml
```

`model-compose` should be treated as an **optional orchestration/deployment alternative**, not as a mandatory replacement for LangGraph.

---

# Local Agent Harness Routing

## HarnessRouter

Repository:

`https://github.com/sdk2035/harnessrouter`

HarnessRouter is included as an optional **local agent-harness router/runtime layer**.

Its Community Edition is self-hosted and exposes a unified interface for agent harnesses while keeping the execution environment, workspace and provider credentials under local control.

### Proposed role

```text
Application / Agent API
        |
        v
   HarnessRouter
        |
+-------+----------------+
|       |                |
v       v                v
Codex   Other Harness   Future UHP-compatible runtimes
        |
        v
Local POSIX Workspace
Bash | Git | Files | Tools
```

### Why it complements the existing model router

The existing `jfxai4arch` model-router concept selects **models/providers**:

```text
Model Router
├── Azure AI
├── Local LLM
├── Ollama
└── vLLM
```

HarnessRouter operates at a different abstraction level: it routes or normalizes access to **agent harness runtimes** that execute work in tool-enabled workspaces.

The two layers can coexist:

```text
Agent Request
     |
Workflow / Orchestrator
     |
+----+----------------------+
|                           |
v                           v
Harness Router          Model Router
Agent runtimes          Model endpoints
Codex / harnesses       Azure / local models
```

### Deployment role

HarnessRouter is especially useful for:

- local-first coding agents;
- controlled agent workspaces;
- software-generation jobs;
- repository automation;
- sandboxed engineering tasks;
- session and file-oriented agent execution;
- avoiding a mandatory hosted agent control plane.

It is an **optional integration** and should not be interpreted as the only model-routing mechanism in the architecture.

---

# Microsoft 365 Agents SDK for .NET

Repository:

`https://github.com/sdk2035/Agents-for-net`

The project is a fork/reference of Microsoft's **Microsoft 365 Agents SDK for C#/.NET**.

It is included in `jfxai4arch` as an **optional enterprise-agent SDK** for organizations building agents in the .NET ecosystem.

## Proposed role

```text
Enterprise Channels
M365 | Teams | Copilot Studio | Webchat
              |
              v
 Microsoft 365 Agents SDK
          C# / .NET
              |
     +--------+---------+
     |                  |
     v                  v
Azure AI Foundry    Semantic Kernel
     |                  |
     +--------+---------+
              |
              v
     jfxai4arch Services
     MCP | RAG | APIs
```

### Potential use cases

- Microsoft 365 enterprise assistants;
- Teams-based agents;
- Copilot Studio integrations;
- multichannel enterprise agents;
- .NET agent services;
- Azure AI Foundry integrations;
- Semantic Kernel integration;
- authentication and enterprise identity workflows;
- collaboration between .NET agents and other agent services.

### Architectural positioning

The Microsoft 365 Agents SDK does not replace LangGraph or model-compose globally.

Instead, it adds a specialized C#/.NET agent-development path:

```text
Agent Development
├── Python
│   └── LangGraph / LangChain
├── Declarative
│   └── model-compose YAML
└── C# / .NET
    └── Microsoft 365 Agents SDK
```

This improves language and platform diversity while preserving the modular architecture.

---

# Updated Orchestration Matrix

| Layer | Primary / Existing Option | New Alternative / Integration | Role |
|---|---|---|---|
| User Interface | Open WebUI | Custom web / M365 channels | Agent interaction |
| Stateful orchestration | LangGraph | model-compose | Workflow and agent composition |
| Declarative automation | YAML / deployment manifests | model-compose | AI service definitions |
| Tool integration | MCP | Native SDK/API adapters | Enterprise tools |
| Coding-agent runtime | Direct agent integration | HarnessRouter | Local/self-hosted harness abstraction |
| Model gateway | LiteLLM / custom router | Provider-native routing | Cloud/local model access |
| .NET enterprise agents | Custom .NET services | Microsoft 365 Agents SDK | M365/Teams/.NET agents |
| RAG | Qdrant | Replaceable vector stores | Semantic retrieval |
| Operational data | PostgreSQL | Compatible relational stores | State and transactions |
| Identity | Keycloak / Entra ID | Channel-specific identity | AuthN/AuthZ |
| Observability | Langfuse / OpenTelemetry | Prometheus / Grafana | Tracing and metrics |
| Deployment | Docker / Kubernetes | AKS / on-prem | Runtime infrastructure |

---

# Updated Recommended Technology Stack

```yaml
frontend:
  primary:
    - Open WebUI

api:
  - FastAPI
  - REST
  - OpenAPI

agent_orchestration:
  primary:
    - LangGraph
    - LangChain
  alternatives:
    - model-compose

declarative_ai_automation:
  - model-compose
  - model-compose.yml

agent_harness_runtime:
  optional:
    - HarnessRouter
    - Codex

dotnet_agent_sdk:
  optional:
    - Microsoft 365 Agents SDK
    - C# / .NET

integrations:
  - Model Context Protocol
  - MCP Servers
  - Enterprise REST APIs

ai_models:
  cloud:
    - Azure AI
    - Azure AI Foundry
  local_development:
    - Ollama
  local_production:
    - vLLM
  gateway:
    - LiteLLM

knowledge_retrieval:
  - Qdrant
  - Embedding Models

application_data:
  - PostgreSQL

authentication:
  - Keycloak
  - Microsoft Entra ID
  - OpenID Connect

observability:
  - Langfuse
  - OpenTelemetry
  - Prometheus
  - Grafana

containerization:
  - Docker
  - Docker Compose

orchestration:
  - Kubernetes
  - Azure Kubernetes Service

ci_cd:
  - GitHub Actions
  - Argo CD
```

---

# Updated Hybrid Agent Strategy

A request may be routed according to the workload rather than to a single universal framework.

| Workload | Suggested Architecture |
|---|---|
| General enterprise chat | Open WebUI + local/cloud model |
| Internal RAG | Qdrant + local LLM |
| Complex stateful workflow | LangGraph + MCP |
| Declarative YAML workflow | model-compose |
| Portable AI service | model-compose + Docker/Kubernetes |
| Coding/repository automation | HarnessRouter + Codex |
| Local tool-enabled agent execution | HarnessRouter |
| Microsoft 365 assistant | Microsoft 365 Agents SDK |
| Teams enterprise agent | Microsoft 365 Agents SDK + Entra ID |
| .NET enterprise agent | Agents SDK + Azure AI/Semantic Kernel |
| High-risk business action | Agent workflow + human approval |
| Large-scale managed reasoning | Azure AI |
| Private/offline inference | Ollama or vLLM |

---

# Deployment Profiles

## Minimal Local Profile

```text
Open WebUI
   |
Agent API
   |
LangGraph
   |
Ollama
   |
Qdrant + PostgreSQL
```

## Declarative Local Profile

```text
model-compose.yml
       |
 model-compose
       |
Agents + RAG + MCP
       |
Local Models / Cloud APIs
```

## Coding-Agent Profile

```text
Developer Portal / API
        |
   HarnessRouter
        |
      Codex
        |
Local Workspace
Git + Bash + Files
```

## Microsoft Enterprise Profile

```text
Teams / M365 / Webchat
         |
Microsoft 365 Agents SDK
         |
      .NET Agent
         |
Azure AI / Semantic Kernel
         |
MCP + Enterprise APIs + RAG
```

## Full Hybrid Enterprise Profile

```text
Open WebUI / M365 / Enterprise Apps
               |
          API Gateway
               |
+--------------+----------------+
|              |                |
LangGraph   model-compose   .NET Agents SDK
|              |                |
+--------------+----------------+
               |
       MCP / Tool Services
               |
+--------------+----------------+
|                               |
HarnessRouter                Model Router
Codex / harnesses            LiteLLM
|                               |
Local workspaces        Azure AI / Ollama / vLLM
               |
       Qdrant + PostgreSQL
               |
 Docker -> Kubernetes -> AKS
```

---

# Dependency Classification

## Core / Recommended

- Open WebUI
- LangGraph / LangChain
- MCP
- Qdrant
- PostgreSQL
- Docker
- Kubernetes

## Optional Integrations

- Azure AI / Azure AI Foundry
- LiteLLM
- Ollama
- vLLM
- Keycloak
- Langfuse
- Prometheus
- Grafana
- Argo CD

## New Optional Architecture Components

### model-compose

**Category:** Alternative orchestration / declarative automation.

Use when YAML-based portable service composition is preferable to application-code-centric orchestration.

### HarnessRouter

**Category:** Local agent-harness runtime/router.

Use when coding or tool-enabled agent runtimes should execute through a unified local/self-hosted abstraction.

### Microsoft 365 Agents SDK for .NET

**Category:** Enterprise agent SDK.

Use for C#/.NET, Microsoft 365, Teams, Copilot Studio and compatible multichannel agent applications.

---

# Design Principles

1. **No mandatory orchestration framework**  
   LangGraph is a strong default, while model-compose provides a declarative alternative.

2. **Separate model routing from harness routing**  
   Model gateways select inference endpoints; HarnessRouter manages tool-enabled agent harness execution.

3. **Polyglot agent development**  
   Python, declarative YAML and C#/.NET agent stacks can coexist.

4. **Local-first where appropriate**  
   Local models, local agent harnesses and self-hosted services can reduce external infrastructure dependencies.

5. **Cloud when beneficial**  
   Azure AI and AKS remain available for managed enterprise workloads.

6. **Open integrations**  
   MCP and documented APIs reduce direct coupling between agents and business systems.

7. **Replaceable components**  
   The architecture should remain modular enough to substitute models, runtimes, stores, gateways and orchestration systems.

---

# Updated Benefits

- Open-source-oriented and self-hosted architecture.
- Hybrid Azure and local AI.
- Declarative YAML automation through model-compose.
- Local/self-hosted coding-agent execution through HarnessRouter.
- Codex-compatible agent-harness architecture.
- C#/.NET and Microsoft 365 enterprise agents through the Microsoft 365 Agents SDK.
- Stateful orchestration through LangGraph.
- Standardized integrations through MCP.
- Scalable RAG through Qdrant.
- Transactional and workflow state through PostgreSQL.
- Containerized deployment through Docker and Kubernetes.
- Production deployment path through AKS.
- Improved portability and infrastructure control.
- Multiple implementation paths instead of a single framework dependency.

---

# Conclusion

The updated `jfxai4arch` architecture extends the existing open-source AI platform with three complementary capabilities:

1. **model-compose** adds a declarative `model-compose.yml` path for agents, workflows, RAG pipelines, tools and MCP services.
2. **HarnessRouter** adds a local/self-hosted abstraction for tool-enabled coding-agent harnesses such as Codex.
3. **Microsoft 365 Agents SDK for .NET** adds a C#/.NET enterprise-agent path for Microsoft 365, Teams, Copilot Studio, Webchat and related integrations.

Together with Open WebUI, LangGraph, MCP, Azure AI, local LLMs, Qdrant, PostgreSQL, Docker and Kubernetes, these components provide a broader architecture in which workflow orchestration, coding-agent runtimes, model providers and enterprise agent SDKs remain independently replaceable.

> **Open, modular architecture designed to minimize proprietary lock-in and enable independent implementations.**

## Intellectual Property and Integration Note

The repositories referenced above remain independent projects and retain their respective licenses, trademarks and upstream ownership. Inclusion in this architecture is a proposed integration/dependency classification and does not imply endorsement, sponsorship, ownership or automatic license compatibility.

Open-source software does not by itself guarantee freedom from third-party patent or other intellectual-property rights; deployments should perform their own technical and legal review.
