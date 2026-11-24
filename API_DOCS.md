# 📡 TenderMind API & MCP Specification

This document provides complete documentation for the REST API endpoints and MCP tool schemas.

---

## 1. REST API Endpoints

### Health Check
- **`GET /health`**
  - **Response**: `{"status": "HEALTHY", "system": "TenderMind AI & MCP Platform", "version": "1.0.0"}`

### Tenders
- **`GET /api/tenders`**
  - **Query Params**: `query` (str), `category` (str), `location` (str), `max_value` (float)
  - **Returns**: Array of `Tender` objects.
- **`GET /api/tenders/{tender_id}`**
  - **Returns**: Complete `Tender` object with `requirements` and `corrigenda`.
- **`POST /api/tenders/upload`**
  - **Body (JSON)**: `TenderUploadRequest`
  - **Returns**: Newly created and structured tender record.

### Company Profile & Vault
- **`GET /api/company`**
  - **Query Params**: `company_id` (str, default: `"comp_nexus_01"`)
  - **Returns**: `CompanyProfile` with credentials, turnover history, and documents.
- **`POST /api/company/documents/resolve-gap`**
  - **Query Params**: `company_id`, `document_type`, `title`
  - **Returns**: Updated profile and confirmation of resolved document.

### Eligibility & MSME Intelligence
- **`GET /api/eligibility/{tender_id}`**
  - **Query Params**: `company_id`
  - **Returns**: `EligibilityReport` with 3-state assessments, citations, readiness percentage, and gaps.
- **`GET /api/eligibility/msme-benefits/{tender_id}`**
  - **Query Params**: `company_id`
  - **Returns**: `MSMEBenefitAssessment` with GFR Rule 170 EMD waiver details.

### Bid Preparation
- **`GET /api/bids/{tender_id}`**
  - **Query Params**: `company_id`
  - **Returns**: `BidPackage` with 5/9 checklist, draft proposals, and statutory undertakings.
- **`POST /api/bids/{tender_id}/checklist/{item_id}/toggle`**
  - **Query Params**: `company_id`
  - **Returns**: Updated bid package with recalculated readiness fraction.
- **`POST /api/bids/{tender_id}/proposal/{section_id}/approve`**
  - **Query Params**: `company_id`
  - **Returns**: Approval status of proposal section.

### Corrigenda & Monitoring
- **`GET /api/corrigenda`**
  - **Returns**: All active amendments and impact notifications across active tenders.

### Model Context Protocol (MCP)
- **`GET /api/mcp/tools`**
  - **Returns**: List of all registered MCP tool definitions across 7 servers.
- **`POST /api/mcp/invoke`**
  - **Body (JSON)**: `{"server_name": "TenderMCPServer", "tool_name": "search_tenders", "arguments": {...}}`
  - **Returns**: `MCPCallResponse` with result, execution time, and status.
- **`GET /api/mcp/traces`**
  - **Returns**: Auditable live execution traces (Screen 7).

### Conversational Agent
- **`POST /api/chat`**
  - **Body (JSON)**: `{"query": "...", "active_tender_id": "...", "company_id": "..."}`
  - **Returns**: Formatted answer with verbatim citations, evidence, and list of MCP tools used.

---

## 2. MCP JSON-RPC Server Interfaces

Each server implements the standard MCP protocol schema:

```json
{
  "name": "evaluate_eligibility",
  "description": "Run audit-grade comparison between tender requirements and business documents",
  "server_name": "EligibilityMCPServer",
  "parameters": {
    "type": "object",
    "properties": {
      "tender_id": { "type": "string" },
      "company_id": { "type": "string" }
    },
    "required": ["tender_id", "company_id"]
  }
}
```
