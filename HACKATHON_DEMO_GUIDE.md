# 🏆 TenderMind — 5-Minute Hackathon Demo Script (Track 1)

This script provides an end-to-end demonstration flow for judges and evaluators.

---

## ⏱️ Demo Timeline Overview (5 Minutes)

| Time | Phase | Target Screen | Core Message |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:45** | The Problem | Screen 1: Command Center | 50-page tender PDFs vs Small Business qualification |
| **0:45 - 1:30** | Two-Way Discovery | Screen 2: Tender Discovery | Not keyword search: two-way capability & financial matching |
| **1:30 - 2:30** | Document Intelligence & Gaps | Screen 3 & Screen 5 | Verbatim page citations & 3-state deterministic evaluation |
| **2:30 - 3:30** | The "Killer Moment" | Screen 9: Copilot | Asking: *"Can my company apply? What is missing?"* |
| **3:30 - 4:15** | Gap Resolution & MSME Shield | Top bar & Screen 6 | 1-click gap resolution & GFR 170 ₹50,000 EMD waiver |
| **4:15 - 5:00** | Track 1 MCP Architecture | Screen 8: Activity Trace | 7 independent MCP servers operating in a live pipeline |

---

## 🎭 Step-by-Step Walkthrough

### Step 1: Open RFP Command Center (`/`)
- **Action**: Direct judges to `http://localhost:8000`.
- **Narrative**:
  > *"Judges, government procurement represents a ₹10 Lakh Crore market in India, yet small MSMEs lose out because tenders are published as dense 50-page legal PDFs. Here is our enterprise: **Nexus Technology Solutions (a Bengaluru MSE)**. Look at the Command Center: we have targeted a GeM tender for Cloud and IT Maintenance (GEM/2026/B/123456)."*
- **Key Visual**: Point out the **86% Readiness Index** and the alert box: **"1 Blocking Gap: Client Completion Certificate Missing"**.

### Step 2: Show Document Intelligence & Citations
- **Action**: Switch to **"Tender Intelligence"** tab.
- **Narrative**:
  > *"Unlike generic LLM summarizers that hallucinate, TenderMind extracts requirements with exact page-level citations:
  > • Minimum Turnover: Page 12, Section 4.2
  > • Experience: Page 13, Section 4.3
  > • EMD: Page 5, Section 2.5
  > This makes every recommendation completely auditable against the original tender."*

### Step 3: Trigger "The Killer Moment"
- **Action**: Switch to **"The Killer Moment"** tab and click the prompt shortcut:
  > *"Can my company apply for this tender? What exactly is preventing us from being submission-ready?"*
- **Narrative**:
  > *"Watch the agent respond in real-time. It doesn't give a generic response:
  > It verifies our turnover (₹35 Lakh > ₹20 Lakh required, citing Page 12).
  > It identifies the exact blocking gap: Client Completion Certificate for >₹10 Lakh from Page 14, Section 5.1.
  > And it detects that we qualify for a 100% EMD waiver, saving us ₹50,000 under GFR Rule 170!"*

### Step 4: Show Corrigenda & Amendments
- **Action**: Switch to **"Corrigenda & Dates"** tab.
- **Narrative**:
  > *"Government tenders frequently change after publication. TenderMind detected Corrigendum #1 extending the deadline from 10 Dec to 15 Dec, and Corrigendum #2 clarifying MSME EMD exemptions. TenderMind updates our bid timeline automatically."*

### Step 5: Live Gap Resolution Demo
- **Action**: Click the purple button in the top bar: **"Resolve Completion Cert Gap"**.
- **Narrative**:
  > *"Suppose the company secures their completion letter from Bangalore University. Let's upload and verify it in the Document Vault. Watch the Command Center update:
  > The readiness index jumps immediately to **100% SUBMISSION READY**!
  > All 7 requirements are satisfied, and our Bid Preparation dossier (Envelope A, B, and C) is ready for human review."*

### Step 6: Reveal the Track 1 MCP Multi-Server Engine
- **Action**: Switch to **"AI Agent Activity (MCP)"** tab.
- **Narrative**:
  > *"How does this work under the hood? Through **Model Context Protocol (MCP)**. We built 7 independent MCP servers: Tender MCP, Document MCP, Business MCP, Eligibility MCP, Bid MCP, Monitoring MCP, and Communication MCP. Every tool invocation is logged in this live audit trace, demonstrating true agentic multi-server orchestration without hallucination."*

---

## 🎯 Winning Pitch Summary
> *"TenderMind is not an AI search engine; it is an AI procurement-readiness platform for small businesses. It tells an MSME: Which tenders to pursue, does the company qualify, what is missing, and how to resolve it before the deadline."*
