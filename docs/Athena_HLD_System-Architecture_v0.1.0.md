# High-Level Design Document (HLD)
**Document ID:** Athena_HLD_System-Architecture_v0.1.0  
**Date:** 2026-02-05  
**Version:** 0.1.0 (Minor - Architecture Defined)

---

## 1. Introduction

### 1.1 Purpose
This document describes the high-level architecture of Project Athena, an Autonomous Multi-Agent Framework for Program Management.

### 1.2 Design Philosophy
The system follows a **Dual-Architecture** approach:
1. **Project Universe** - A high-fidelity enterprise simulator
2. **Athena Core** - The multi-agent reasoning engine

---

## 2. System Architecture

### 2.1 Component Diagram (C4 Level 2 - Container)

```
+===========================================================================+
||                         DOCKER COMPOSE NETWORK                          ||
+===========================================================================+
|                                                                           |
|  +-----------------------------+    +-----------------------------+       |
|  |     PROJECT UNIVERSE        |    |        ATHENA CORE          |       |
|  |        (Simulator)          |    |         (Agent)             |       |
|  +-----------------------------+    +-----------------------------+       |
|  |                             |    |                             |       |
|  |  +-------+    +----------+  |    |  +----------+  +---------+  |       |
|  |  | Jira  |    | Chaos    |  |    |  | Ingest   |  | Agent   |  |       |
|  |  | Sim   |    | Engine   |  |    |  | Pipeline |  | Brain   |  |       |
|  |  | API   |    | (Cron)   |  |    |  | (FastAPI)|  |(LangGrph|  |       |
|  |  +---+---+    +----+-----+  |    |  +----+-----+  +----+----+  |       |
|  |      |             |        |    |       |             |       |       |
|  |      +------+------+        |    |       +------+------+       |       |
|  |             |               |    |              |              |       |
|  +-------------|---------------+    +--------------|-------------+        |
|                |                                   |                      |
|                | Webhook (HTTP POST)               |                      |
|                +---------------------------------->|                      |
|                                                    |                      |
|  +-----------------------------+    +-----------------------------+       |
|  |        DATA LAYER           |    |       INFERENCE LAYER       |       |
|  +-----------------------------+    +-----------------------------+       |
|  |                             |    |                             |       |
|  |  +----------+  +----------+ |    |  +----------+               |       |
|  |  | SQLite   |  | Neo4j    | |    |  | Ollama   |               |       |
|  |  | (Mock    |  | (Graph   | |    |  | (Llama3) |               |       |
|  |  | Jira DB) |  | Store)   | |    |  +----------+               |       |
|  |  +----------+  +----------+ |    |                             |       |
|  |                             |    |                             |       |
|  |  +----------+               |    |                             |       |
|  |  | ChromaDB |               |    |                             |       |
|  |  | (Vector) |               |    |                             |       |
|  |  +----------+               |    |                             |       |
|  |                             |    |                             |       |
|  +-----------------------------+    +-----------------------------+       |
|                                                                           |
|  +--------------------------------------------------------------------+   |
|  |                         PRESENTATION LAYER                          |   |
|  +--------------------------------------------------------------------+   |
|  |                                                                    |   |
|  |  +---------------------------+    +--------------------------+     |   |
|  |  |     Next.js Dashboard     |    |     God Mode Console     |     |   |
|  |  |  (Chat + Visualization)   |    |   (Chaos Injection UI)   |     |   |
|  |  +---------------------------+    +--------------------------+     |   |
|  |                                                                    |   |
|  +--------------------------------------------------------------------+   |
|                                                                           |
+===========================================================================+
```

---

## 3. Component Specifications

### 3.1 Project Universe (Simulator Layer)

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| Jira-Sim API | FastAPI | REST endpoints for CRUD on Tasks, Bugs, Users |
| Chaos Engine | Python (APScheduler) | Periodic injection of failures and blockers |
| Webhook Dispatcher | httpx | Fires HTTP POST to Athena on state changes |
| Mock Database | SQLite | Persistent storage for simulated project data |

### 3.2 Athena Core (Agent Layer)

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| Ingestion Pipeline | FastAPI | Receives webhooks, normalizes data |
| Graph Syncer | py2neo | Upserts nodes and edges to Neo4j |
| Vector Indexer | ChromaDB Client | Embeds text using local embeddings |
| Agent Brain | LangGraph | Orchestrates multi-agent workflow |
| Semantic Router | Custom | Routes queries to Graph vs Vector vs LLM |

### 3.3 Data Layer

| Component | Technology | Purpose |
|-----------|------------|---------|
| SQLite | Standard Library | Relational storage for Mock Jira |
| Neo4j Community | Docker Image | Knowledge Graph (nodes, relationships) |
| ChromaDB | Docker Image | Vector embeddings for semantic search |

### 3.4 Inference Layer

| Component | Technology | Purpose |
|-----------|------------|---------|
| Ollama | Docker Image | Local LLM server |
| Llama 3 (8B) | Meta Model | Reasoning and response generation |

---

## 4. Data Flow Architecture

### 4.1 Event Processing Flow

```
    [1]                 [2]                 [3]                 [4]
 Chaos Engine       Jira-Sim API        Athena Ingest       Agent Brain
      |                  |                   |                   |
      | Update ticket    |                   |                   |
      | status           |                   |                   |
      |----------------->|                   |                   |
      |                  |                   |                   |
      |                  | Fire webhook      |                   |
      |                  |------------------>|                   |
      |                  |                   |                   |
      |                  |                   | Parse JSON        |
      |                  |                   | Upsert to Neo4j   |
      |                  |                   | Embed to Chroma   |
      |                  |                   |------------------>|
      |                  |                   |                   |
      |                  |                   |                   | Detect anomaly
      |                  |                   |                   | Query sources
      |                  |                   |                   | Generate alert
      |                  |                   |                   |
```

### 4.2 Query Processing Flow

```
    [1]              [2]              [3]              [4]              [5]
   User           Dashboard        Agent Brain       Data Layer        LLM
     |                |                |                |                |
     | Natural        |                |                |                |
     | language       |                |                |                |
     | query          |                |                |                |
     |--------------->|                |                |                |
     |                |                |                |                |
     |                | Forward        |                |                |
     |                | to agent       |                |                |
     |                |--------------->|                |                |
     |                |                |                |                |
     |                |                | Route query    |                |
     |                |                |--------------->|                |
     |                |                |                |                |
     |                |                | Retrieve       |                |
     |                |                | context        |                |
     |                |                |<---------------|                |
     |                |                |                                 |
     |                |                | Generate response               |
     |                |                |-------------------------------->|
     |                |                |                                 |
     |                |                | Formatted answer                |
     |                |                |<--------------------------------|
     |                |                |                |                |
     |                | Display        |                |                |
     |                | with citations |                |                |
     |<---------------|                |                |                |
     |                |                |                |                |
```

---

## 5. LangGraph Agent Design

### 5.1 Agent State Machine

```
                            +------------------+
                            |      START       |
                            +--------+---------+
                                     |
                                     v
                            +------------------+
                            |     PLANNER      |
                            | (Analyze intent) |
                            +--------+---------+
                                     |
                    +----------------+----------------+
                    |                                 |
                    v                                 v
           +----------------+               +----------------+
           |   RESEARCHER   |               |    ALERTER     |
           | (Query tools)  |               | (Draft comms)  |
           +-------+--------+               +--------+-------+
                   |                                 |
                   |     +------------------+        |
                   +---->|    RESPONDER     |<-------+
                         | (Format output)  |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |    HUMAN GATE    |
                         | (Approval check) |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
           +----------------+           +----------------+
           |    EXECUTOR    |           |      END       |
           | (Take action)  |           | (Return result)|
           +----------------+           +----------------+
```

### 5.2 Agent Tools

| Tool Name | Input | Output | Purpose |
|-----------|-------|--------|---------|
| `search_graph` | Cypher query | List of nodes | Query Neo4j for structured data |
| `search_docs` | Natural language | Retrieved chunks | Vector search on ChromaDB |
| `get_user_info` | User ID | User details | Lookup assignee/owner data |
| `draft_message` | Context, template | Formatted message | Generate communications |
| `log_action` | Action details | Confirmation | Write to ATL |

---

## 6. Deployment Architecture

### 6.1 Docker Compose Services

```
+-----------------------------------------------------------------------+
|                          docker-compose.yml                           |
+-----------------------------------------------------------------------+
|                                                                       |
|  services:                                                            |
|                                                                       |
|  +-------------------+  +-------------------+  +-------------------+  |
|  | sim-api           |  | sim-chaos         |  | athena-core       |  |
|  | Port: 8001        |  | (No port)         |  | Port: 8000        |  |
|  | Depends: sim-db   |  | Depends: sim-api  |  | Depends: graph-db |  |
|  +-------------------+  +-------------------+  +-------------------+  |
|                                                                       |
|  +-------------------+  +-------------------+  +-------------------+  |
|  | graph-db (Neo4j)  |  | vector-db(Chroma) |  | ollama            |  |
|  | Port: 7474, 7687  |  | Port: 8002        |  | Port: 11434       |  |
|  +-------------------+  +-------------------+  +-------------------+  |
|                                                                       |
|  +-------------------+                                                |
|  | dashboard         |                                                |
|  | Port: 3000        |                                                |
|  | Depends: athena   |                                                |
|  +-------------------+                                                |
|                                                                       |
+-----------------------------------------------------------------------+
```

---

## 7. Security Considerations

| Concern | Mitigation |
|---------|-----------|
| Data Leakage | All processing is local (Ollama, no external APIs) |
| Unauthorized Actions | Human-in-the-loop gate for external communications |
| Audit Trail | All agent decisions logged to ATL |
| Access Control | Role-based filtering in query layer |

---

**Document Version History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-02-05 | Team Athena | Initial architecture definition |
