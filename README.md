# 🏛️ TenderMind — AI-Powered Government Tender Discovery, Eligibility Intelligence & Bid Preparation Agent for MSMEs

> **Track 1: MCP + Agentic AI**  
> *"TenderMind doesn't just find tenders. It determines whether a business is ready to apply, what is missing, and what it needs to do next."*

---

## 🌟 Executive Summary

Government tenders across platforms like **GeM (Government e-Marketplace)** and **CPPP (Central Public Procurement Portal)** represent massive revenue opportunities for small businesses, contractors, and startups. However, these opportunities are gated by 50–200 page tender documents with intricate financial thresholds, technical qualification clauses, and mandatory statutory certificates.

**TenderMind bridges this divide through an intelligent multi-agent workflow powered by the Model Context Protocol (MCP)**. Instead of simply generating high-level summaries of PDFs, TenderMind builds a persistent two-way understanding between **what the government department mandates** and **what the business credentials and documents prove**.

### 💡 Core Innovations
1. **Business-to-Tender Two-Way Matching**: Ranks tenders not merely by keyword relevance, but by empirical financial feasibility, sector capabilities, and location proximity.
2. **Evidence-Backed 3-State Eligibility Engine**: Eliminates LLM hallucination through a deterministic rule engine outputting three verified states:
   - **Satisfied** (with verbatim page & section citations, e.g. *Page 12, Section 4.2*)
   - **Not satisfied** (identifying specific deficit or missing document)
   - **Needs verification** (flagging ambiguities requiring human interpretation)
3. **MSME Opportunity Optimizer**: Automatically checks eligibility for the *Public Procurement Policy for MSEs Order, 2012* and *GFR Rule 170*, applying **100% EMD exemptions**, tender fee waivers, and prior experience/turnover relaxations.
4. **Corrigendum & Deadline Intelligence**: Monitors published amendments, detects revisions to deadlines or criteria, and flags their direct impact on prepared bids.
5. **Bid Preparation Workspace**: Assembles multi-envelope compliance checklists (e.g., 5/9 readiness), criterion-aligned technical proposals, and statutory undertakings (Non-blacklisting, Make-in-India local content).
6. **The "Killer Moment" Copilot**: Directly answers: *"Can my company apply for this tender? What exactly is preventing us from being submission-ready?"* with instantaneous evidence citations.

---

## 🏗️ Architecture & Multi-Server MCP Design

TenderMind coordinates specialized AI agents via independent **Model Context Protocol (MCP)** servers:

```
                          ┌────────────────────────────────┐
                          │   TenderMind AI Orchestrator   │
                          │   Planning · Context · Routing │
                          └───────────────┬────────────────┘
                                          │
                                          ▼
                          ┌────────────────────────────────┐
                          │     Central MCP Tool Registry  │
                          │   Cross-Server Tool Execution  │
                          └───────────────┬────────────────┘
                                          │
        ┌───────────────┬─────────────────┼─────────────────┬────────────────┐
        ▼               ▼                 ▼                 ▼                ▼
┌──────────────┐ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ ┌──────────────┐
│  Tender MCP  │ │ Document MCP │  │ Business MCP │  │EligibilityMCP│ │   Bid MCP    │
│  search      │ │ extract_text │  │ get_profile  │  │ evaluate     │ │ checklist    │
│  details     │ │ requirements │  │ search_docs  │  │ msme_benefits│ │ proposal     │
│  corrigenda  │ │ page_citates │  │ credentials  │  │ gap_analysis │ │ undertakings │
└──────────────┘ └──────────────┘  └──────────────┘  └──────────────┘ └──────────────┘
```

### Registered MCP Servers & Tools
| MCP Server | Exposed Tools | Responsibility |
| :--- | :--- | :--- |
| **TenderMCPServer** | `search_tenders`, `get_tender_details`, `get_corrigenda`, `get_tender_document` | Discovery across GeM, CPPP & portals |
| **DocumentMCPServer** | `extract_pdf_text`, `extract_requirements` | Structured extraction with page-level citations |
| **BusinessMCPServer** | `get_company_profile`, `search_company_documents` | Enterprise vault, Udyam, GST, and turnover |
| **EligibilityMCPServer** | `evaluate_eligibility`, `check_msme_benefits` | Deterministic 3-state evaluation & GFR 170 rules |
| **BidMCPServer** | `generate_compliance_checklist`, `generate_draft_proposal` | Multi-envelope checklist & technical proposal |
| **MonitoringMCPServer** | `monitor_tender_updates`, `check_corrigenda_impact` | Corrigendum diff detection & impact alerts |
| **CommunicationMCPServer**| `create_calendar_reminder`, `draft_notification` | Deadline reminders & human approval actions |

---

## 🖥️ Interactive Dashboard Screens

- **Screen 1: RFP Command Center** — Executive readiness gauge, extracted requirements %, document audit count (6/7), active risk flags, and timeline.
- **Screen 2: Tender Discovery** — Search by sector, department, value, closing date; 2-way business suitability scores (e.g., 92/100, 85/100, 18/100).
- **Screen 3: Tender Intelligence** — Extracted parameters with verbatim page citations (*Page 12, Section 4.2*).
- **Screen 4: Business Vault & MSME** — Udyam registration, GSTIN, PAN, audited financial turnover FY 2022-25, and document repository.
- **Screen 5: Eligibility & Gap Engine** — Side-by-side comparison, 3-state badges (Satisfied, Not satisfied, Needs verification), and gap resolution remedies.
- **Screen 6: Bid Preparation Workspace** — Interactive 5/9 document checklist, criterion-aligned technical proposal editor, and statutory declarations.
- **Screen 7: Deadline & Corrigendum Intelligence** — Amendment alerts, before/after values, and bid checklist impact.
- **Screen 8: AI Agent Activity (MCP Inspector)** — Live auditable trace of agents, MCP servers called, tools invoked, and human approval status.
- **Screen 9: The Killer Moment Chat** — Conversational agent providing evidence-backed answers to readiness queries.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Modern Web Browser

### Installation & Run

1. **Clone the repository:**
   ```bash
   git clone <repo_url>
   cd tendermind
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch TenderMind:**
   ```bash
   python run.py
   ```

4. **Access the Application:**
   - **Web Dashboard:** [http://localhost:8000](http://localhost:8000)
   - **Interactive OpenAPI Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Running the Automated Test Suite

TenderMind includes a comprehensive 16-test unit and integration suite covering deterministic rule evaluations, MSME benefits, MCP tool invocations, and agent orchestration:

```bash
python -m unittest discover -s tests -v
```

All 16 tests pass:
```
test_bids_package ... ok
test_chat_killer_moment ... ok
test_eligibility ... ok
test_gap_resolution_flow ... ok
test_get_company ... ok
test_get_tender ... ok
test_list_tenders ... ok
test_mcp_tools_and_traces ... ok
test_msme_benefits ... ok
test_eligibility_three_state_evaluation ... ok
test_corrigenda_tool ... ok
test_registered_tools_count ... ok
test_tender_search_tool ... ok
test_full_pipeline ... ok
test_killer_moment_query ... ok

Ran 16 tests in 0.017s
OK
```

---

## 🏆 Hackathon Demonstration Flow (5 Minutes)

1. **Step 1: Open RFP Command Center** (`/`) to review the active target tender: `GEM/2026/B/123456` (₹25 Lakh Cloud & IT Support Services).
2. **Step 2: Note the Gap**: Notice the **86% Readiness Index** and the alert: *"1 Missing Doc: Client Completion Certificate"*.
3. **Step 3: Trigger the Killer Question**: Click **"The Killer Question"** in the sidebar or ask the Copilot:
   > *"Can my company apply for this tender? What exactly is preventing us from being submission-ready?"*
   > 
   > Observe how the agent responds using exact uploaded documents and tender clauses (*Page 14, Section 5.1*), rather than hallucinated text.
4. **Step 4: Check MSME Optimizer**: View the **₹50,000 EMD 100% waiver** under GFR Rule 170.
5. **Step 5: Inspect Corrigenda**: View Corrigendum #1 (Deadline extended from 10 Dec to 15 Dec) and Corrigendum #2 (EMD relaxation clarified).
6. **Step 6: Resolve the Gap**: Click **"Resolve Completion Cert Gap"** in the top bar. The document is uploaded, hash-verified, and the readiness index jumps to **100% SUBMISSION READY**!
7. **Step 7: Inspect MCP Activity**: Navigate to **AI Agent Activity** to review the live cross-server trace demonstrating Track 1 compliance.

---

## ⚖️ Legal & Procurement Disclaimer
TenderMind is an AI-powered bid-preparation and decision-support platform designed to assist MSMEs. It is not a substitute for professional legal advice or official procurement authority rulings. Final interpretation and bid submission remain the responsibility of the bidder.
