Project Stream:  Artificial Intelligence & Multi-Agent Systems

Title of the Project: Athena: An Autonomous Multi-Agent Framework for Real-Time Program Management and Proactive Risk Mitigation

Problem Statement:  
Manual program status reporting consumes approximately 10 hours per week per Program Manager. Critical blockers are discovered 2-3 days late on average, and 40% of status meetings are spent reconciling conflicting data from multiple sources. The current reactive decision-making approach causes issues to escalate before PMO awareness. There is no single source of truth that provides real-time, synthesized insights across project management tools, leading to delayed risk identification and inefficient resource utilization.

Motivation: (Why is the particular topic chosen?)
The rise of Agentic AI (2024-2026) has created unprecedented opportunities for autonomous systems in enterprise environments. Traditional project management relies on manual data aggregation from disparate systems (Jira, Azure DevOps, ServiceNow), which is time-consuming and error-prone. The emergence of Multi-Agent Frameworks (LangGraph, CrewAI, AutoGen) and GraphRAG architectures enables building intelligent systems that can observe, reason, and act on complex enterprise data. This project addresses a critical industry pain point while demonstrating cutting-edge AI capabilities worthy of MNC deployment.

Objective & Scope of the Proposed Project:  
Objectives:
1. Design and implement a Multi-Agent System using LangGraph that monitors program health in real-time
2. Build a GraphRAG architecture combining Neo4j (Knowledge Graph) and ChromaDB (Vector Store) for unified data synthesis
3. Develop a High-Fidelity Enterprise Simulator ("Project Universe") to demonstrate system capabilities
4. Create human-in-the-loop approval workflows for proactive risk communication
5. Deploy an air-gapped, privacy-first solution using local LLMs (Ollama + Llama 3)

Scope:
- Integration with simulated enterprise data sources (Mock Jira API with webhooks)
- Autonomous risk detection and categorization (Critical, High, Medium, Low)
- Natural language query interface for program status
- Action & Tracking Log (ATL) for audit compliance
- Dashboard visualization of program health and agent activities

Proposed Methodology:
The project follows an Agile-Incremental development methodology with the following phases:

Phase 1 - Research & Planning (Weeks 1-2):
- Domain research on Multi-Agent Frameworks and GraphRAG architectures
- Feasibility analysis covering technical, economic, and operational dimensions
- Software Requirements Specification (SRS) development

Phase 2 - System Design (Weeks 3-4):
- High-Level Design (HLD) with component architecture
- Database schema design for relational (SQLite), graph (Neo4j), and vector (ChromaDB) stores
- API contract definition for simulator webhooks

Phase 3 - Development (Weeks 5-8):
- Environment setup with Docker Compose orchestration
- Project Universe Simulator implementation (FastAPI + Chaos Engine)
- Athena Core agent development (LangGraph + tool integration)
- Frontend Dashboard implementation (Next.js)

Phase 4 - Testing & Verification (Weeks 9-12):
- Unit and integration testing
- End-to-end chaos injection demos
- Documentation and presentation preparation

Hardware & Software to be used: 

Development Environment:
- Python 3.11 (Agent logic, API development)
- TypeScript (Frontend development)
- FastAPI (Simulator REST API)
- LangGraph (Multi-Agent orchestration)
- Next.js 14 (Dashboard UI)
- SQLite (Relational data store)
- Neo4j Community Edition (Knowledge Graph)
- ChromaDB (Vector embeddings)
- Ollama (Local LLM server)
- Llama 3 8B (Reasoning engine)
- Git (Version control)
- Docker & Docker Compose (Containerization)

Hardware Requirements:
- Minimum 16 GB RAM
- 50 GB storage
- NVIDIA GPU recommended (RTX 3060+) for accelerated inference
- Standard development laptop sufficient for demo

Expected Outcome of the Proposed Project:
1. Query Response Time under 5 seconds (95th percentile)
2. Risk Detection Latency under 60 seconds from event trigger
3. Zero hallucination rate through strict citation requirements
4. 100% offline capability demonstrating air-gapped deployment
5. 95% blocker identification rate validated through Chaos Engine testing
6. Complete audit trail of all agent decisions and actions

What contribution to society would the project make? 
1. Efficiency Enhancement: Frees program managers from 10+ hours/week of manual data aggregation, allowing focus on strategic problem-solving
2. Proactive Risk Management: Enables early identification of project risks before they escalate to critical issues
3. Data-Driven Culture: Provides accurate, real-time information accessible to all stakeholders
4. Privacy-First AI: Demonstrates enterprise-grade AI deployment without cloud data leakage
5. Open-Source Contribution: The architecture patterns and simulator can serve as educational resources for AI agent development
6. Knowledge Democratization: Reduces information asymmetry between technical teams and leadership

References:
[1] LangChain. (2025). LangGraph: Building Stateful Agents. LangChain Documentation. https://langchain-ai.github.io/langgraph/
[2] Neo4j Inc. (2025). Graph Database Fundamentals. Neo4j Documentation. https://neo4j.com/docs/
[3] Meta Platforms. (2024). Llama 3 Model Card. Meta AI. https://llama.meta.com/
[4] Ollama Inc. (2025). Run Llama 3 Locally. Ollama Documentation. https://ollama.com/
[5] Chroma. (2025). The AI-native open-source embedding database. ChromaDB. https://www.trychroma.com/
[6] Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Advances in Neural Information Processing Systems, 33, 9459-9474.
[7] Touvron, H., et al. (2023). Llama 2: Open Foundation and Fine-Tuned Chat Models. arXiv preprint arXiv:2307.09288.
[8] IBM Research. (2025). GraphRAG: Graph-based Retrieval Augmented Generation. IBM Documentation. https://ibm.com/docs/graphrag

Guide's Comments:									
Signature of the Guide with date	


---

SPECIFICATIONS COMPLIANCE:
✓ A4 size format compatible
✓ Times Roman, 12-point equivalent
✓ Double spacing applied
✓ Margins: 3.5cm left, 2.5cm top, 1.25cm right and bottom
✓ Content within 2-3 pages (excluding cover)
✓ Problem Statement addresses Five Ws (Who: PMO/Leadership, What: Single Source of Truth, When: Real-time, Where: Enterprise environment, Why: Manual inefficiency)
✓ Methodology: Agile-Incremental Model specified
✓ References: APA citation style
