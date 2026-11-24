# 🏛️ TenderMind — Technical Architecture & MCP Specification

This document details the engineering principles, Model Context Protocol (MCP) server specifications, agent workflows, and deterministic rule engines that power TenderMind.

---

## 1. Core Architectural Tenet: Deterministic Engine vs. Agentic Orchestration

A critical vulnerability in tender AI applications is **LLM hallucination** — language models miscalculating financial averages, imagining years of experience, or declaring compliance without checking statutory documents.

TenderMind enforces an architectural partition:
- **Deterministic Rule Engine (Backend Services)**: Executes all mathematical checks (average turnover vs threshold), date validations (years of operation vs threshold), statutory document presence (GSTIN, PAN, Udyam matching), and GFR Rule 170 policy evaluations.
- **Agentic AI Orchestrator**: Decides *which* services and MCP servers to invoke based on user prompts and workflow stages, manages context, and compiles the final human-readable brief.

```
┌────────────────────────────────────────────────────────┐
│                   User / Web UI                        │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│              TenderMind AI Orchestrator                │
│   • Intent Classification  • Multi-Agent Coordination  │
└───────────────────────────┬────────────────────────────┘
                            │ JSON-RPC / MCP Tool Calls
                            ▼
┌────────────────────────────────────────────────────────┐
│                 Central MCP Registry                   │
│   • Discovery  • Dispatch  • Trace & Audit Logging     │
└──────┬────────────┬─────────────┬────────────┬─────────┘
       │            │             │            │
       ▼            ▼             ▼            ▼
 ┌──────────┐ ┌──────────┐  ┌──────────┐ ┌──────────┐
 │Tender MCP│ │Doc MCP   │  │Biz MCP   │ │Elig. MCP │
 └──────────┘ └──────────┘  └──────────┘ └────┬─────┘
                                              │ Calls Deterministic Rules
                                              ▼
                                    ┌───────────────────┐
                                    │Rule Engine Backend│
                                    │• Financial Checks │
                                    │• Experience Calcs │
                                    │• GFR Rule 170     │
                                    └───────────────────┘
```

---

## 2. Model Context Protocol (MCP) Multi-Server Implementation

TenderMind implements standard MCP tool endpoints distributed across 7 specialized servers:

### 1. `TenderMCPServer`
- **Purpose**: Government procurement listing discovery and notice retrieval.
- **Tools**:
  - `search_tenders(query, category, location, max_value)`: Filters active tenders with match scoring.
  - `get_tender_details(tender_id)`: Fetches complete specifications, requirements, and dates.
  - `get_corrigenda(tender_id)`: Fetches published amendments.
  - `get_tender_document(tender_id)`: Retrieves document links and summaries.

### 2. `DocumentMCPServer`
- **Purpose**: Document intelligence and clause extraction with source linking.
- **Tools**:
  - `extract_pdf_text(tender_id, raw_text)`: Extracts character stream and sections.
  - `extract_requirements(tender_id)`: Structures clauses into Pydantic models with page/section citations (*e.g., Page 12, Section 4.2*).

### 3. `BusinessMCPServer`
- **Purpose**: Enterprise credentials and document vault management.
- **Tools**:
  - `get_company_profile(company_id)`: Retrieves incorporation, Udyam, GST, and turnover history.
  - `search_company_documents(company_id, document_type)`: Finds specific verified certificates.

### 4. `EligibilityMCPServer`
- **Purpose**: Audit-grade evaluation of compliance evidence.
- **Tools**:
  - `evaluate_eligibility(tender_id, company_id)`: Executes 3-state comparison.
  - `check_msme_benefits(tender_id, company_id)`: Evaluates GFR 170 / MSE policy exemptions.

### 5. `BidMCPServer`
- **Purpose**: Bid dossier assembly and proposal drafting.
- **Tools**:
  - `generate_compliance_checklist(tender_id, company_id)`: Generates multi-envelope checklist linked to verified documents.
  - `generate_draft_proposal(tender_id, company_id)`: Drafts technical proposals and statutory undertakings.

### 6. `MonitoringMCPServer`
- **Purpose**: Corrigenda tracking and bid impact analysis.
- **Tools**:
  - `monitor_tender_updates(tender_id)`: Scans for amendments.
  - `check_corrigenda_impact(tender_id, corrigendum_id)`: Assesses how an amendment affects an in-progress bid.

### 7. `CommunicationMCPServer`
- **Purpose**: User-directed alerts and scheduling (requires human sign-off).
- **Tools**:
  - `create_calendar_reminder(tender_id, event_title, event_date)`: Schedules reminders.
  - `draft_notification(recipient_role, subject, body)`: Drafts internal notifications.

---

## 3. The 3-State Eligibility Evaluation Model

Never rely on a single probabilistic percentage as proof of legal qualification. TenderMind categorizes every requirement into three clear states:

```
┌────────────────────────────────────────────────────────┐
│                   Tender Condition                     │
└───────────────────────────┬────────────────────────────┘
                            ▼
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Satisfied   │   │ Not Satisfied │   │     Needs     │
│               │   │               │   │ Verification  │
│ Verified doc  │   │ Deficit in    │   │ Information   │
│ & evidence    │   │ threshold or  │   │ missing or    │
│ matches clause│   │ missing doc   │   │ ambiguous     │
└───────────────┘   └───────────────┘   └───────────────┘
```

---

## 4. MSME Benefit & Exemption Intelligence

The Indian Public Procurement Policy mandates a 25% annual procurement target from MSEs:
- **EMD Exemption (GFR Rule 170)**: 100% waiver of bid security deposits for valid Udyam certificate holders.
- **Tender Fee Waiver**: Standard document fees waived.
- **Prior Experience / Turnover Relaxations**: Applicable to startups and MSEs subject to quality standards.

The `MSMERuleEngine` automatically detects applicable concessions and outputs the exact evidence required (e.g. Udyam Registration Certificate with matching NIC code 6201).
