"""
ARCH-COUNCIL Knowledge Base Seed Content
TOGAF ADM framework, AI architecture patterns, and best practices.
This is the built-in knowledge that bootstraps the vector store.
Additional content is pulled from public sources during ingest.
"""

# Each document: {id, category, source, content}
SEED_DOCUMENTS = [

    # ── TOGAF ADM Phases ────────────────────────────────────────────────────

    {
        "id": "togaf_preliminary",
        "category": "TOGAF ADM",
        "source": "TOGAF 10 — Preliminary Phase",
        "content": """TOGAF Preliminary Phase: Framework and Principles

Purpose: Prepare the organization to undertake TOGAF-based Enterprise Architecture.

Key Activities:
- Determine the Architecture Capability desired by the organization
- Establish the Architecture Capability (team, processes, tools, governance)
- Define and establish the Architecture Principles (guiding rules for architecture decisions)
- Select and tailor TOGAF and other frameworks for the enterprise context
- Implement Architecture Tools (repositories, modeling tools)
- Define the Architecture Framework: views, viewpoints, governance model

Architecture Principles Examples:
- Primacy of Principles: architecture principles take precedence over ad-hoc decisions
- Maximize Benefit to the Enterprise: decisions maximize overall enterprise benefit
- Information Management is Everybody's Business: all stakeholders responsible for data
- Data is an Asset: enterprise data has intrinsic value and must be managed accordingly
- Technology Independence: applications should be independent of technology choices
- Ease of Use: applications are easy to use and the underlying technology transparent

Key Deliverables:
- Tailored Architecture Framework
- Architecture Principles document
- Architecture Repository baseline
- Architecture Governance framework
- Request for Architecture Work"""
    },

    {
        "id": "togaf_phase_a",
        "category": "TOGAF ADM",
        "source": "TOGAF 10 — Phase A: Architecture Vision",
        "content": """TOGAF Phase A: Architecture Vision

Purpose: Develop a high-level aspirational view of capabilities and business value. Get formal sign-off to proceed.

Key Activities:
- Establish the Architecture Project (scope, governance, team)
- Identify Stakeholders, concerns, and business requirements
- Confirm business goals, drivers, and constraints
- Assess readiness for transformation
- Define scope of the Architecture Effort
- Confirm Architecture Principles
- Develop Architecture Vision (target capability)
- Develop Statement of Architecture Work and gain approval

Key Outputs/Artifacts:
- Approved Statement of Architecture Work
- Architecture Vision document
- Communication Plan
- Stakeholder Map and Management Plan
- Refined Architecture Principles
- Business Scenario (structured description of problem and desired outcome)

Stakeholder Analysis: Identify all stakeholders (exec sponsors, end users, IT ops, compliance, security),
document their concerns, and define how architecture will address each concern.

Architecture Vision Template:
- Problem description and business context
- Objectives and success metrics
- Scope and boundary decisions
- Assumptions and dependencies
- Proposed solution high-level approach
- Risk summary"""
    },

    {
        "id": "togaf_phase_b",
        "category": "TOGAF ADM",
        "source": "TOGAF 10 — Phase B: Business Architecture",
        "content": """TOGAF Phase B: Business Architecture

Purpose: Develop Target Business Architecture that describes how the enterprise needs to operate.

Key Activities:
- Select reference models, viewpoints, and tools
- Develop Baseline Business Architecture Description (current state)
- Develop Target Business Architecture Description (future state)
- Perform Gap Analysis (baseline vs target)
- Define candidate roadmap components
- Resolve impacts across Architecture Landscape
- Conduct formal stakeholder review
- Finalize Business Architecture and create Architecture Definition Document

Key Artifacts:
- Business Capability Map: hierarchical map of capabilities the business performs
- Value Stream Map: end-to-end flow from trigger to stakeholder value
- Business Process Diagram: detailed process flows with actors and decisions
- Organization Map: structure, roles, responsibilities
- Actor/Role Catalogue: who performs what
- Business Service/Function Catalogue: services the business provides
- Business Interaction Matrix: how actors interact
- Business Footprint Diagram: business units, locations, functions, services

Gap Analysis Template:
For each capability: Baseline State | Target State | Gap | Initiative to Close Gap

Business Capability Assessment Dimensions:
- Capability Maturity (1=Initial, 5=Optimizing)
- Strategic Importance (High/Medium/Low)
- AI Enhancement Potential (High/Medium/Low)
- Current Pain Level (High/Medium/Low)"""
    },

    {
        "id": "togaf_phase_c_data",
        "category": "TOGAF ADM",
        "source": "TOGAF 10 — Phase C: Data Architecture",
        "content": """TOGAF Phase C: Data Architecture

Purpose: Define the structure and management of the organization's major data assets.

Key Activities:
- Select data reference models and catalogues
- Develop Baseline Data Architecture
- Develop Target Data Architecture
- Perform Data Gap Analysis
- Define data migration requirements

Key Artifacts:
- Data Entity Catalogue: all significant data entities, definitions, owners
- Data Entity/Business Function Matrix: which functions create/read/update/delete which data
- Conceptual Data Diagram: high-level entity relationships
- Logical Data Diagram: normalized data model
- Data Dissemination Diagram: how data flows between systems/actors
- Data Security Classification: sensitivity levels, access controls
- Data Migration Plan: how to move from current to target state
- Data Lifecycle Diagram: creation, usage, archival, deletion

Data Governance Considerations:
- Data Stewardship: who owns each data domain
- Data Quality: completeness, accuracy, consistency, timeliness KPIs
- Master Data Management: single source of truth for key entities
- Metadata Management: business and technical metadata catalogues
- Data Lineage: audit trail of data transformations

AI/ML Data Architecture:
- Feature Store design: offline (batch training) and online (real-time inference) feature serving
- Training Data Pipeline: ingestion, labelling, versioning, validation
- Embedding Pipeline: text/image/document → vector representations
- Vector Store: semantic search and RAG retrieval
- Model Registry: versioned model artefacts with metadata"""
    },

    {
        "id": "togaf_phase_c_app",
        "category": "TOGAF ADM",
        "source": "TOGAF 10 — Phase C: Application Architecture",
        "content": """TOGAF Phase C: Application Architecture

Purpose: Define the major kinds of application systems needed to process data and support business functions.

Key Activities:
- Select application reference models and patterns
- Develop Baseline Application Architecture
- Develop Target Application Architecture
- Perform Application Gap Analysis

Key Artifacts:
- Application Portfolio Catalogue: all applications, ownership, lifecycle status
- Interface Catalogue: all system interfaces (API contracts, data formats, protocols)
- Application/Function Matrix: which apps support which business functions
- Application Interaction Diagram: data flows between applications
- Application Communication Diagram: technical communication patterns
- Software Engineering Diagram: component structure within applications
- Application Migration Diagram: migration path from baseline to target

AI Application Integration Patterns:
1. Prompt Engineering Pattern: LLM called directly with crafted prompts; suitable for classification, extraction, generation tasks with known structure
2. RAG Pattern: Retrieval + LLM; suitable for knowledge-grounded Q&A, document analysis, search enhancement
3. Fine-tuning Pattern: Domain-adapted model; suitable when prompt engineering insufficient, large labelled dataset available
4. Agentic Loop Pattern: LLM + tool use in autonomous loop; suitable for multi-step reasoning, complex workflows
5. Multi-Agent Pattern: Multiple LLMs with specialized roles; suitable for complex research, review, and synthesis tasks

API Design Principles:
- REST for synchronous request/response
- Async messaging (Kafka, SQS) for AI inference queues (latency unpredictable)
- Streaming responses (SSE, WebSocket) for real-time LLM output
- Webhook callbacks for long-running AI jobs"""
    },

    {
        "id": "togaf_phase_d",
        "category": "TOGAF ADM",
        "source": "TOGAF 10 — Phase D: Technology Architecture",
        "content": """TOGAF Phase D: Technology Architecture

Purpose: Map application components onto technology components (infrastructure, middleware, networks).

Key Activities:
- Select technology reference models and standards
- Develop Baseline Technology Architecture
- Develop Target Technology Architecture
- Perform Technology Gap Analysis

Key Artifacts:
- Technology Standards Catalogue: approved technology standards and versions
- Technology Portfolio Catalogue: installed technology base
- System/Technology Matrix: which tech components support which applications
- Environments and Locations Diagram: deployment environments (dev, staging, prod) and geographic locations
- Platform Decomposition Diagram: technology platform layers
- Processing Diagram: runtime processing flows
- Network Computing/Hardware Diagram: network topology and hardware

Cloud Architecture Considerations:
- Infrastructure as Code: Terraform, Pulumi, CloudFormation
- Container Orchestration: Kubernetes (EKS, GKE, AKS) for AI workloads
- Serverless: AWS Lambda, Cloud Run for inference API endpoints
- GPU Infrastructure:
  * Training: A100/H100 clusters (AWS p4d, Azure NDv5, GCP A3)
  * Inference: T4/A10G instances for cost-effective production serving
  * Spot instances for training (80% cost saving, handle interruptions)
- Storage:
  * Object storage (S3, GCS) for model weights and training data
  * Vector databases (Pinecone, Weaviate, ChromaDB, pgvector) for embeddings
  * Feature stores (Feast, Tecton) for ML features
- MLOps Platforms:
  * MLflow: experiment tracking, model registry (open source)
  * Kubeflow: Kubernetes-native ML pipelines
  * AWS SageMaker: managed end-to-end ML platform
  * Azure Machine Learning: Microsoft's managed ML platform
  * Vertex AI: Google's managed ML platform"""
    },

    {
        "id": "togaf_phase_e_f",
        "category": "TOGAF ADM",
        "source": "TOGAF 10 — Phases E & F: Opportunities, Solutions & Migration",
        "content": """TOGAF Phase E: Opportunities and Solutions

Purpose: Generate initial Architecture Roadmap based on gap analysis from Phases B, C, D.

Key Activities:
- Confirm key corporate change attributes
- Determine business constraints for implementation
- Review and consolidate Gap Analysis results from B, C, D
- Review consolidated requirements across related business functions
- Identify major work packages
- Identify Transition Architectures
- Create Architecture Roadmap

Transition Architecture: Intermediate states between current and target that deliver business value.
Work Package Definition: discrete group of change activities delivering a defined outcome.

Phase F: Migration Planning

Purpose: Finalize detailed Implementation and Migration Plan.

Key Activities:
- Confirm management framework interactions for Implementation Plan
- Assign business value to each work package
- Estimate resource requirements, timelines, and availability
- Prioritize migration projects by business value and dependencies
- Generate Implementation and Migration Plan

Project Prioritization Criteria:
- Business value delivered
- Strategic alignment
- Technical dependencies
- Risk level
- Resource requirements
- Time to value

Implementation Roadmap Template:
Phase 1 (0-3 months): Foundation — infrastructure, data pipeline, team capability
Phase 2 (3-6 months): Core AI solution — MVP deployment, initial user group
Phase 3 (6-12 months): Scale — full rollout, optimization, governance operationalization"""
    },

    {
        "id": "togaf_governance",
        "category": "TOGAF ADM",
        "source": "TOGAF 10 — Phases G & H: Governance & Change Management",
        "content": """TOGAF Phase G: Implementation Governance

Purpose: Ensure conformance with defined architecture during implementation.

Key Activities:
- Confirm scope and priorities for deployment
- Identify deployment resources and skills
- Guide development of Solutions Deployment
- Perform Enterprise Architecture Compliance Reviews
- Implement Business and IT Operations
- Perform Post-Implementation Review and close implementation

Architecture Compliance Review Process:
- Architecture Contract: agreement between development teams and architecture team
- Compliance Assessment: review of implementation against architecture
- Dispensation: formal exception with documented justification

Phase H: Architecture Change Management

Purpose: Keep architecture responsive to enterprise needs.

Change Classification:
- Simplification: reduces complexity, low risk — update Architecture Repository
- Incremental: stays within current Architecture Vision — minor amendment
- Significant: triggers new ADM cycle
- Re-architecting: major business change, triggers full ADM cycle from Phase A

Architecture Governance Framework:
- Architecture Board: cross-functional governance body
- Architecture Compliance: regular compliance reviews of projects
- Architecture Waiver: process for approved deviations
- Architecture Contract: formal agreement for solution delivery

AI-Specific Governance:
- Model Performance Monitoring: track accuracy/latency/cost over time
- Model Drift Detection: alert when model performance degrades
- AI Audit Trail: log all AI decisions for regulatory review
- Human-in-the-Loop: define which AI decisions require human approval
- AI Ethics Review: bias assessment, fairness testing before deployment"""
    },

    # ── AI Architecture Patterns ─────────────────────────────────────────────

    {
        "id": "ai_rag_pattern",
        "category": "AI Patterns",
        "source": "AI Architecture Best Practices",
        "content": """Retrieval-Augmented Generation (RAG) Architecture Pattern

Definition: Augment LLM generation with dynamically retrieved relevant documents from a knowledge base.

When to use RAG:
- Knowledge base is large, frequently updated, or proprietary
- Need to cite sources and ensure factual grounding
- Cannot or should not fine-tune (cost, data privacy, update frequency)
- Questions require combining multiple document sources

RAG Architecture Components:
1. Document Ingestion Pipeline:
   - Document loaders (PDF, Word, web, database)
   - Text chunking (fixed-size, semantic, recursive)
   - Embedding model (text-embedding-3-small, all-MiniLM-L6-v2, BGE)
   - Vector store (Pinecone, Weaviate, ChromaDB, pgvector, Qdrant)

2. Retrieval Layer:
   - Dense retrieval: semantic similarity via embeddings
   - Sparse retrieval: BM25 keyword matching
   - Hybrid retrieval: combine dense + sparse (recommended for production)
   - Re-ranking: cross-encoder reranker to re-sort top-k results (Cohere Rerank, BGE Reranker)

3. Generation Layer:
   - Context assembly: retrieved chunks + query + system prompt
   - LLM generation: GPT-4o, Claude, Gemini, Llama
   - Output parsing: structured extraction if needed

Advanced RAG Patterns:
- HyDE (Hypothetical Document Embeddings): generate hypothetical answer first, retrieve on that
- Self-RAG: model decides when to retrieve and how to use retrieved docs
- RAPTOR: hierarchical summarization for multi-level retrieval
- Agentic RAG: LLM controls retrieval strategy adaptively

Chunking Strategies:
- Fixed-size: 512-1024 tokens with 10-20% overlap — simple, works for most cases
- Semantic: split on meaning boundaries — better quality, more complex
- Recursive: split on paragraph → sentence → word until small enough
- Document-specific: respect document structure (headers, sections)

Evaluation Metrics:
- Context Recall: are relevant documents retrieved?
- Context Precision: are retrieved documents relevant?
- Answer Faithfulness: is the answer grounded in retrieved context?
- Answer Relevance: does the answer address the question?
Tools: RAGAS, TruLens, DeepEval"""
    },

    {
        "id": "ai_agentic_pattern",
        "category": "AI Patterns",
        "source": "AI Architecture Best Practices",
        "content": """Agentic AI System Architecture Pattern

Definition: LLM operates in an autonomous loop, using tools and reasoning to complete multi-step tasks.

ReAct Loop (Reason + Act):
1. Think: LLM reasons about current state and next step
2. Act: LLM selects and calls a tool
3. Observe: tool result returned to LLM context
4. Repeat until task complete or max steps reached

Core Components:
- Agent Brain: LLM with tool-use capability (GPT-4o, Claude 3.5 Sonnet, Gemini 2.0)
- Tool Registry: function definitions the agent can call
- Memory: short-term (context window), long-term (vector store), episodic (conversation history)
- Orchestration: LangChain Agents, LlamaIndex Agents, CrewAI, AutoGen, LangGraph

Common Agent Tools:
- Web search (Tavily, Serper, Bing)
- Code execution (Python REPL, E2B sandbox)
- File read/write
- Database query
- API calls (REST, GraphQL)
- Calculator, calendar, email

Multi-Agent Patterns:
1. Sequential: Agent A output → Agent B input (pipeline)
2. Hierarchical: Manager agent delegates to worker agents
3. Collaborative: Agents debate and converge (council pattern)
4. Competitive: Multiple agents propose, best selected

Safety in Agentic Systems:
- Tool permission scoping: principle of least privilege
- Human-in-the-loop checkpoints: require approval for high-impact actions
- Action sandboxing: run code in isolated environments
- Output validation: check outputs before passing to next step
- Max iteration limits: prevent infinite loops
- Cost monitoring: alert on unexpected API spend

Prompt Injection Defense:
- Separate system instructions from user/tool content
- Validate tool outputs before injecting into context
- Use structured output formats to constrain responses
- Monitor for instruction-overriding patterns in tool results"""
    },

    {
        "id": "ai_finetuning_pattern",
        "category": "AI Patterns",
        "source": "AI Architecture Best Practices",
        "content": """Fine-tuning Architecture Pattern

Definition: Adapt a pre-trained LLM's weights on domain-specific data to improve task performance.

When to use Fine-tuning (vs RAG vs prompt engineering):
- Task requires specific output format consistently (JSON, structured data)
- Domain vocabulary or style not well represented in base model
- Latency requirements prevent long context RAG (shorter prompts after fine-tuning)
- Privacy: can't send sensitive data to external API
- Cost: high-volume inference with shorter prompts cheaper after fine-tuning
- Have 500+ labelled examples available

Fine-tuning Methods:
1. Full Fine-tuning: update all weights — most powerful, most expensive, requires large GPU
2. LoRA (Low-Rank Adaptation): inject small trainable matrices — 90% parameter reduction, popular
3. QLoRA: LoRA + quantization (4-bit) — fine-tune 7B model on single GPU
4. PEFT (Parameter-Efficient Fine-Tuning): umbrella term for LoRA, prefix tuning, adapters

Data Requirements:
- Minimum: 100 examples (prompt + ideal completion pairs)
- Recommended: 500-10,000 examples
- Format: JSONL with messages array (system, user, assistant)
- Quality > Quantity: 100 perfect examples beats 10,000 noisy ones

Infrastructure:
- QLoRA 7B: single GPU (RTX 4090, A10G, T4 — 16GB VRAM)
- LoRA 13B: 2x A100 40GB
- Full fine-tune 7B: 4x A100 80GB
- Tools: Hugging Face Transformers + PEFT, Axolotl, LLaMA-Factory, Unsloth (faster)

Evaluation:
- Hold out 10-20% of data as validation set
- Task-specific metrics (BLEU, ROUGE for generation; accuracy for classification)
- Human evaluation for open-ended generation quality
- Regression testing: ensure fine-tuning doesn't degrade other capabilities"""
    },

    {
        "id": "ai_model_selection",
        "category": "AI Patterns",
        "source": "AI Architecture Best Practices — Model Selection",
        "content": """AI Model Selection Framework for Enterprise Solutions

Proprietary API Models (hosted, no infrastructure):
- GPT-4o (OpenAI): Best overall reasoning, 128k context, strong tool use. ~$2.50/1M input tokens
- Claude Sonnet 4.5 (Anthropic): Excellent coding, analysis, long docs. Strong safety. ~$3/1M input
- Claude Opus 4 (Anthropic): Highest reasoning quality. Use for complex synthesis. ~$15/1M input
- Gemini 2.0 Flash (Google): Fastest + cheapest capable model. Good for high-volume tasks. ~$0.10/1M
- Gemini 2.5 Pro (Google): Best multimodal, 1M context. Strong for document analysis
- Grok 3 (xAI): Strong reasoning, web access. Good alternative to GPT-4o

Open Source Models (self-hosted, data privacy, no per-token cost):
- Llama 3.3 70B: Best open-source overall. Matches GPT-4-class. Needs 2x A100
- Qwen 2.5 72B: Strong coding and multilingual. Good alternative to Llama 70B
- Mistral Large 2: Strong reasoning, 128k context, Apache 2.0 license
- Phi-4 (14B): Microsoft's surprisingly capable small model. Fits on single A100
- Gemma 3 27B: Google's open model, strong instruction following

Embedding Models:
- text-embedding-3-large (OpenAI): Best quality, 3072 dims, ~$0.13/1M tokens
- text-embedding-3-small (OpenAI): Good quality, 1536 dims, ~$0.02/1M tokens
- BGE-M3: Best open-source, multilingual, 8192 token input, free to host
- all-MiniLM-L6-v2: Fast, lightweight (384 dims), good for development/low-resource

Selection Decision Framework:
1. Data privacy/sovereignty required → open source self-hosted
2. Low latency critical (<500ms) → Gemini Flash, GPT-4o mini
3. Highest accuracy required → Claude Opus, GPT-4o, Gemini 2.5 Pro
4. High volume, cost-sensitive → Gemini Flash, GPT-4o mini
5. Complex reasoning/analysis → Claude Sonnet/Opus, GPT-4o
6. Code generation → Claude Sonnet, GPT-4o, DeepSeek Coder"""
    },

    {
        "id": "ai_governance",
        "category": "AI Governance",
        "source": "Enterprise AI Governance Framework",
        "content": """Enterprise AI Governance Framework

AI Risk Categories:
1. Model Risk: hallucination, bias, accuracy degradation over time
2. Data Risk: training data poisoning, privacy violation, data drift
3. Operational Risk: latency spikes, API unavailability, cost overruns
4. Compliance Risk: GDPR violations, EU AI Act non-compliance, sector regulations
5. Reputational Risk: harmful outputs, discriminatory decisions, public incidents

EU AI Act (2024) Risk Classification:
- Unacceptable Risk: social scoring, biometric surveillance — PROHIBITED
- High Risk: hiring, credit, education, law enforcement — strict obligations
- Limited Risk: chatbots, deepfakes — transparency requirements
- Minimal Risk: spam filters, games — no specific obligations

For High-Risk AI Systems (obligations):
- Risk management system in place
- High-quality training data documentation
- Technical documentation and record-keeping
- Logging and audit capability
- Human oversight mechanism
- Accuracy, robustness, cybersecurity measures

GDPR + AI Considerations:
- Personal data used in training requires legal basis
- Right to explanation for automated decisions
- Data minimization in model training
- Right to erasure: can the model "forget" individual data?

AI Governance Operating Model:
- AI Ethics Committee: cross-functional review of high-risk AI decisions
- Model Risk Management: pre-deployment validation, post-deployment monitoring
- AI Audit Trail: log inputs, outputs, decisions, model version for 24+ months
- Human-in-the-Loop: define thresholds requiring human review
- Incident Response: process for AI errors/failures in production

Bias & Fairness:
- Pre-training: audit training data for demographic skews
- In-training: fairness constraints in objective function
- Post-training: evaluate across demographic groups (Fairlearn, AIF360)
- Production: continuous bias monitoring dashboard"""
    },

    {
        "id": "mlops_architecture",
        "category": "MLOps",
        "source": "MLOps Best Practices",
        "content": """MLOps Architecture: Production AI Systems

MLOps Maturity Levels:
Level 0: Manual ML — scripts, manual deployment, no monitoring
Level 1: ML Pipeline Automation — automated training, manual release
Level 2: CI/CD Pipeline — automated training + testing + deployment
Level 3: Full MLOps — self-healing, continuous training, full observability

Core MLOps Components:

1. Experiment Tracking (MLflow, Weights & Biases, Neptune):
   - Track hyperparameters, metrics, artifacts per run
   - Compare experiments visually
   - Reproduce any historical run

2. Model Registry:
   - Version control for trained model artifacts
   - Staging → Production promotion workflow
   - Model lineage (data + code + config → model)

3. Feature Store (Feast, Tecton, Hopsworks):
   - Offline store: batch features for training
   - Online store: low-latency features for inference
   - Feature reuse across teams

4. Model Serving:
   - Real-time: FastAPI, TorchServe, Triton Inference Server, BentoML
   - Batch: Spark, AWS Batch, Vertex AI Batch Prediction
   - Serverless: AWS Lambda, Cloud Run (cold start trade-off)
   - LLM Serving: vLLM (production), Ollama (development), TGI (HuggingFace)

5. Monitoring & Observability:
   - Latency, throughput, error rate (standard SRE metrics)
   - Data drift: distribution shift in input features
   - Concept drift: relationship between features and labels changed
   - Model accuracy decay: ground truth labels collected and compared
   - Embedding drift: semantic shift in RAG retrieval quality
   - Tools: Evidently, Whylogs, Arize, Fiddler

6. CI/CD for ML:
   - Code changes: unit tests, integration tests, lint (same as software)
   - Data changes: data validation (Great Expectations, Deequ)
   - Model changes: evaluation against baseline, A/B test before full rollout
   - Infrastructure changes: Terraform plan/apply with review

LLM-Specific Operations:
- Prompt versioning: treat prompts as code, version-controlled
- Prompt A/B testing: compare prompt variants with real traffic
- Token usage monitoring: alert on unexpected cost spikes
- Latency SLA monitoring: p50, p95, p99 latency per endpoint
- Cache layer: semantic caching (GPTCache) to reduce repeated API calls"""
    },

    {
        "id": "cloud_ai_architecture",
        "category": "Cloud Architecture",
        "source": "Cloud AI Architecture Reference",
        "content": """Cloud AI Architecture Reference Patterns

AWS AI Architecture:
- Bedrock: managed access to Claude, Llama, Titan, Mistral — no infrastructure
- SageMaker: end-to-end ML platform (training, hosting, monitoring)
- OpenSearch: vector search with k-NN plugin
- Aurora pgvector: SQL + vector search in RDS
- Lambda + API Gateway: serverless LLM inference wrapper
- Step Functions: orchestrate multi-step AI workflows
- Kendra: managed enterprise search with ML ranking

Azure AI Architecture:
- Azure OpenAI Service: GPT-4o, Embeddings with private endpoints
- Azure AI Search: cognitive search with vector + semantic ranking
- Azure Machine Learning: MLOps platform
- Azure Container Apps: serverless container hosting for AI APIs
- Cosmos DB: vector search in NoSQL
- Document Intelligence: document extraction with AI

GCP AI Architecture:
- Vertex AI: end-to-end ML platform (similar to SageMaker)
- Gemini API: Google's LLM family via API
- Vertex AI Search: enterprise search with grounding
- AlloyDB: pgvector-compatible PostgreSQL
- Cloud Run: serverless containers for inference

Multi-Cloud Considerations:
- Primary cloud: host data, training, primary inference
- Secondary cloud: disaster recovery, regulatory data residency
- Vendor lock-in mitigation: abstract LLM calls behind interface
- Cost optimization: spot/preemptible for training, reserved for inference

Reference Architecture — Enterprise RAG on Azure:
1. Azure Blob Storage → document store
2. Azure Document Intelligence → extract text from PDFs
3. Azure OpenAI Embeddings → embed chunks
4. Azure AI Search → hybrid retrieval (vector + BM25)
5. Azure OpenAI GPT-4o → generation
6. Azure Container Apps → RAG API hosting
7. Azure Monitor + App Insights → observability
8. Azure AD → authentication, RBAC"""
    },

    {
        "id": "architecture_patterns_enterprise",
        "category": "Enterprise Architecture",
        "source": "Enterprise AI Solution Patterns",
        "content": """Enterprise AI Solution Common Patterns

Pattern 1: AI-Augmented Knowledge Worker
Use case: Help employees find, synthesize, and create information faster
Components: Enterprise document RAG + LLM chat interface + SSO
Key considerations: Data access control (user sees only what they're authorized for), audit logging, PII handling
Stack: Azure OpenAI + Azure AI Search + SharePoint connector + Teams bot

Pattern 2: Intelligent Customer Service
Use case: Automate Tier-1 support, augment human agents
Components: RAG on product docs + CRM integration + escalation to human
Key considerations: Tone consistency, hallucination guardrails, CSAT measurement
Stack: GPT-4o mini + Zendesk/Salesforce API + custom knowledge base + guardrails

Pattern 3: AI-Powered Process Automation
Use case: Extract, classify, route structured data from unstructured documents
Components: Document AI + classification model + workflow trigger
Key considerations: Accuracy thresholds, exception handling, human review queue
Stack: Azure Document Intelligence + fine-tuned classifier + Power Automate/Temporal

Pattern 4: Analytical AI Assistant
Use case: Natural language queries over business data
Components: Text-to-SQL + data warehouse + visualization
Key considerations: SQL injection prevention, row-level security, query guardrails
Stack: GPT-4o + Snowflake/BigQuery + Metabase/Tableau embed

Pattern 5: AI Code Assistant (Enterprise)
Use case: Accelerate software development productivity
Components: Code LLM + IDE plugin + code review integration
Key considerations: IP/copyright, sensitive code exposure, security vulnerability introduction
Stack: GitHub Copilot Enterprise or Codeium on-prem

Pilot-to-Production Framework:
Week 1-4 (Pilot): 10-20 users, manual evaluation, weekly feedback loops
Month 2-3 (Controlled Rollout): 100-500 users, automated eval metrics, A/B test
Month 4-6 (Production): full rollout, SLA agreements, support runbook, governance active
Month 6+ (Optimize): fine-tuning on production data, cost optimization, new capabilities"""
    },

    {
        "id": "architecture_decision_record",
        "category": "TOGAF ADM",
        "source": "Architecture Decision Records — Template & Examples",
        "content": """Architecture Decision Records (ADRs) for AI Solutions

ADR Template:
Title: [Short noun phrase]
Status: [Proposed | Accepted | Deprecated | Superseded]
Context: What is the situation requiring this decision?
Decision: What is the decision made?
Rationale: Why was this decision made over alternatives?
Consequences: What are the positive and negative outcomes?
Alternatives Considered: What else was evaluated?

Example ADR 1 — LLM Provider Selection
Title: Use OpenRouter for multi-model LLM access
Status: Accepted
Context: Need to access multiple LLM providers without managing multiple API keys and billing relationships
Decision: Use OpenRouter as abstraction layer over LLM providers
Rationale: Single API key, unified billing, easy model switching, access to 200+ models
Consequences: (+) Flexibility to switch models; (+) cost comparison easy. (-) Extra latency hop; (-) OpenRouter dependency
Alternatives: Direct API per provider (rejected: operational overhead), AWS Bedrock (rejected: cloud lock-in)

Example ADR 2 — Vector Database Selection
Title: Use ChromaDB for development, migrate to Pinecone for production
Status: Accepted
Context: Need vector database for RAG knowledge base. Development needs local execution, production needs scale.
Decision: ChromaDB (dev/test) → Pinecone (production at scale)
Rationale: ChromaDB is embeddable (no infra for dev). Pinecone is managed, auto-scaling, SOC2 compliant.
Consequences: (+) Fast development iteration; (+) production grade at scale. (-) Migration step required at go-live.

Example ADR 3 — AI Safety Guardrails
Title: Implement Guardrails AI for output validation
Status: Accepted
Context: LLM outputs must be validated before user presentation to prevent harmful/irrelevant content
Decision: Use Guardrails AI with custom validators for each use case
Rationale: Declarative validator definitions, automatic retry on validation failure, structured output enforcement
Alternatives: LLM-based self-critique (rejected: adds latency and cost), manual regex (rejected: too brittle)"""
    },

]

# Public URLs to fetch additional content during ingest
PUBLIC_SOURCES = [
    {
        "url": "https://raw.githubusercontent.com/microsoft/generative-ai-for-beginners/main/README.md",
        "category": "AI Patterns",
        "source": "Microsoft Generative AI for Beginners"
    },
    {
        "url": "https://huggingface.co/docs/transformers/index",
        "category": "AI Patterns",
        "source": "HuggingFace Transformers"
    },
]
