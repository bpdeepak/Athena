# Project Plan & Gantt Chart
**Document ID:** Athena_Project-Plan_Detailed-Schedule_v0.2.0  
**Project:** Athena — Autonomous Multi-Agent Framework for Real-Time Program Management  
**Date:** 2026-02-20 | **Version:** 0.2.0

---

## 1. Project Overview

**Goal:** Develop an autonomous multi-agent system that ingests enterprise project data, synthesizes knowledge via GraphRAG (Neo4j + ChromaDB), and proactively detects risks — powered by a dual-mode `LLMProvider` (Gemini for development, Ollama for air-gapped demos).

**SDLC Model:** Agile-Incremental (15 weeks, 5 phases)  
**Team Size:** 4 members  
**Budget:** $0 (open-source + free-tier APIs)

---

## 2. SDLC Phases

### Phase 1 — Requirements & Research (Weeks 1–3)
This phase focuses on understanding the problem domain and establishing the project's foundation. Stakeholder analysis and problem definition are conducted to produce the Synopsis. A literature survey covering 15 research papers across multi-agent systems, GraphRAG, local LLM deployment, and AI-driven project management is completed. Functional and non-functional requirements are gathered through use case modeling and actor identification, resulting in the SRS document and use case diagrams. A feasibility study assessing technical, economic, and operational viability is also prepared during this phase.

### Phase 2 — System Design (Weeks 3–5)
The system architecture is designed using the C4 model (L1 Context, L2 Container), producing the HLD document. Database schemas for SQLite (relational), Neo4j (knowledge graph), and ChromaDB (vector store) are specified in the DDD document. API contracts are defined using OpenAPI specifications, and the LangGraph agent state machine is designed with defined nodes, edges, and conditional routing. UI/UX wireframes for the Next.js dashboard are created, and the Docker Compose service topology — including the dual-mode `LLMProvider` configuration — is finalized as the deployment specification.

### Phase 3 — Implementation (Weeks 5–9)
Core development begins with the Project Universe enterprise simulator, including the Jira-Sim REST API (FastAPI, 15+ endpoints), Chaos Engine (5 fault injection types), and Webhook Dispatcher. The `LLMProvider` abstraction layer is implemented with `GeminiProvider` and `OllamaProvider` backends, enabling seamless switching via the `LLM_BACKEND` environment variable. The LangGraph agent workflow (4 agents: Ingestion, Synthesis, Risk, Communication) is built along with the GraphRAG pipeline for ingesting data into Neo4j and ChromaDB. The Next.js 14 dashboard with chat interface and God Mode console is developed. Synthetic datasets and the Docker development environment are set up in parallel.

### Phase 4 — Testing & Validation (Weeks 9–11)
Comprehensive testing is conducted across all layers. Unit tests (pytest, Jest) validate individual modules, while integration tests verify inter-service communication across Docker containers. End-to-end scenarios using the Chaos Engine validate the full pipeline from fault injection to agent alert generation. Performance benchmarking measures response times and throughput. The system is validated against acceptance criteria: query response under 5 seconds, risk detection latency under 60 seconds, blocker identification rate of at least 95%, zero hallucination (all responses citation-backed), and 100% offline capability in demo mode.

### Phase 5 — Documentation & Deployment (Weeks 11–15)
Final documentation is prepared, including an IEEE-format technical paper, the complete project report, and a user manual. Demo packages are built for both deployment modes — cloud-connected development mode (Gemini) and air-gapped demonstration mode (Ollama). The hard-bound report is compiled and the system is prepared for the Pradarshana exhibition and final submission.

---

## 3. Risk Summary

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM hallucination | HIGH | Citation-grounded responses + human-in-the-loop |
| RAM pressure (16 GB, demo mode) | MED | `--profile demo` selective startup; dev mode skips Ollama |
| Gemini API rate limits | LOW | 15 RPM free tier sufficient; fallback to Ollama |
| Scope creep | MED | Phase gates + university milestone deadlines |

---

## 4. Gantt Chart

```
PROJECT ATHENA — SDLC GANTT CHART (15 Weeks: 14-Feb to 28-May 2026)
══════════════════════════════════════════════════════════════════════════════════════

                              FEB        MARCH           APRIL            MAY
  PHASE / ACTIVITY           W1  W2  W3  W4  W5  W6  W7  W8  W9  W10 W11 W12 W13 W14 W15
  ──────────────────────────  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──

  PHASE 1: REQUIREMENTS
  Problem Definition          ██  ██
  Literature Survey               ██  ██
  SRS & Use Cases                 ██  ██
  Feasibility Study           ██  ██  ██
                                          ▲R1

  PHASE 2: DESIGN
  HLD (C4 Architecture)                  ██  ██
  DDD (Database Schema)                      ██  ██
  API Contracts & Agent FSM                  ██  ██
  UI/UX Wireframes                           ██  ██
                                                  ▲R2

  PHASE 3: IMPLEMENTATION
  Project Universe Simulator                      ██  ██  ██
  Chaos Engine & Webhooks                         ██  ██
  LLMProvider (Gemini/Ollama)                     ██  ██
  LangGraph Agent Workflow                            ██  ██  ██
  GraphRAG Pipeline                                   ██  ██  ██
  Next.js Dashboard                                   ██  ██  ██
  Synthetic Data & Docker                         ██  ██
                                                              ▲R3

  PHASE 4: TESTING
  Unit & Integration Tests                                    ██  ██
  E2E Chaos Scenarios                                         ██  ██
  Performance Benchmarks                                          ██
  Acceptance Validation                                           ██
                                                                  ▲R4

  PHASE 5: DOCUMENTATION
  Technical Paper (IEEE)                                              ██  ██
  Final Report & User Manual                                          ██  ██  ██
  Demo Preparation                                                        ██  ██
  Hard Bound & Exhibition                                                     ██
                                                                              ▲R5
  ──────────────────────────  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──  ──

  LEGEND:  ██ = Active work    ▲Rn = Phase review/milestone
```

---

**Document Version History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-02-19 | Team Athena | Initial schedule-only document |
| 0.2.0 | 2026-02-20 | Team Athena | Rewritten as standard SDLC project plan with 5 phases, risk summary, and phase-aligned Gantt chart |
