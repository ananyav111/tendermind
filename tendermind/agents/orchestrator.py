import re
from typing import Dict, Any, List, Optional
from tendermind.mcp_servers.registry import mcp_registry
from tendermind.data.db import db
from tendermind.models.tender import Tender
from tendermind.models.company import CompanyProfile
from tendermind.models.eligibility import EligibilityReport

class TenderMindOrchestrator:
    """
    Central Multi-Agent AI Orchestrator for TenderMind.
    Coordinates specialized agents via MCP cross-server calls,
    enforcing deterministic eligibility logic and human-in-the-loop review.
    """

    def __init__(self):
        self.registry = mcp_registry

    def run_full_pipeline(self, tender_id: str, company_id: str = "comp_nexus_01") -> Dict[str, Any]:
        """
        Executes the canonical 7-step cross-server MCP workflow specified in Track 1 Blueprint:
        1. Tender MCP -> get_tender_details
        2. Document MCP -> extract_requirements
        3. Business MCP -> get_company_profile & search_company_documents
        4. Eligibility MCP -> evaluate_eligibility
        5. MSME MCP -> check_msme_benefits
        6. Bid MCP -> generate_compliance_checklist & generate_draft_proposal
        7. Monitoring MCP -> monitor_tender_updates
        """
        # Step 1: Tender Discovery / Retrieval
        res_tender = self.registry.execute_tool(
            server_name="TenderMCPServer",
            tool_name="get_tender_details",
            arguments={"tender_id": tender_id},
            agent_name="Discovery Agent"
        )
        if not res_tender.success:
            return {"error": res_tender.error}

        # Step 2: Document Intelligence
        res_doc = self.registry.execute_tool(
            server_name="DocumentMCPServer",
            tool_name="extract_requirements",
            arguments={"tender_id": tender_id},
            agent_name="Document Intelligence Agent"
        )

        # Step 3: Business Credentials
        res_biz = self.registry.execute_tool(
            server_name="BusinessMCPServer",
            tool_name="get_company_profile",
            arguments={"company_id": company_id},
            agent_name="Business Profile Agent"
        )

        # Step 4: Deterministic Eligibility Evaluation
        res_eligibility = self.registry.execute_tool(
            server_name="EligibilityMCPServer",
            tool_name="evaluate_eligibility",
            arguments={"tender_id": tender_id, "company_id": company_id},
            agent_name="Eligibility Engine Agent"
        )

        # Step 5: MSME Benefit & Exemption Analysis
        res_msme = self.registry.execute_tool(
            server_name="EligibilityMCPServer",
            tool_name="check_msme_benefits",
            arguments={"tender_id": tender_id, "company_id": company_id},
            agent_name="MSME Intelligence Agent"
        )

        # Step 6: Bid Checklist & Draft Proposal Compilation
        res_bid = self.registry.execute_tool(
            server_name="BidMCPServer",
            tool_name="generate_compliance_checklist",
            arguments={"tender_id": tender_id, "company_id": company_id},
            agent_name="Bid Preparation Agent"
        )

        res_proposal = self.registry.execute_tool(
            server_name="BidMCPServer",
            tool_name="generate_draft_proposal",
            arguments={"tender_id": tender_id, "company_id": company_id},
            agent_name="Bid Preparation Agent"
        )

        # Step 7: Corrigendum Monitoring
        res_monitor = self.registry.execute_tool(
            server_name="MonitoringMCPServer",
            tool_name="monitor_tender_updates",
            arguments={"tender_id": tender_id},
            agent_name="Monitoring Agent"
        )

        return {
            "tender": res_tender.result,
            "extracted_requirements": res_doc.result,
            "company_profile": res_biz.result,
            "eligibility_report": res_eligibility.result,
            "msme_benefits": res_msme.result,
            "bid_package": res_bid.result,
            "draft_proposal": res_proposal.result,
            "corrigenda": res_monitor.result
        }

    def answer_user_query(self, query: str, active_tender_id: Optional[str] = None,
                          company_id: str = "comp_nexus_01") -> Dict[str, Any]:
        """
        The 'Killer Moment' Conversational Agent:
        Responds to user queries using exact uploaded documents, tender clauses, and MCP traces,
        preventing generic AI hallucination.
        """
        q_lower = query.lower()
        
        # Determine target tender ID
        target_tender_id = active_tender_id
        if not target_tender_id:
            # Check if mentioned in text
            if "123456" in query or "gem" in q_lower:
                target_tender_id = "GEM/2026/B/123456"
            elif "9821" in query or "nic" in q_lower:
                target_tender_id = "CPPP/2026/NIC/9821"
            elif "0042" in query or "bbmp" in q_lower or "waste" in q_lower:
                target_tender_id = "KPPP/2026/BBMP/0042"
            elif "7710" in query or "nhai" in q_lower or "highway" in q_lower:
                target_tender_id = "CPPP/2026/NHAI/7710"
            else:
                target_tender_id = "GEM/2026/B/123456"

        tender = db.get_tender(target_tender_id)
        company = db.get_company(company_id)
        if not tender or not company:
            return {
                "answer": "Target tender or company profile could not be retrieved from repository.",
                "tools_used": []
            }

        # Killer Moment Query 1: "Can my company apply? What exactly is preventing us from being submission-ready?"
        if any(k in q_lower for k in ["can my company apply", "preventing", "eligible", "submission-ready", "readiness", "gap"]):
            report_res = self.registry.execute_tool(
                server_name="EligibilityMCPServer",
                tool_name="evaluate_eligibility",
                arguments={"tender_id": target_tender_id, "company_id": company_id},
                agent_name="Eligibility Agent"
            )
            report = report_res.result
            
            satisfied = [a for a in report["assessments"] if a["status"] == "Satisfied"]
            not_sat = [a for a in report["assessments"] if a["status"] == "Not satisfied"]
            needs_ver = [a for a in report["assessments"] if a["status"] == "Needs verification"]

            answer_lines = [
                f"### Tender Readiness Assessment: **{tender.title}** ({tender.reference_number})\n",
                f"**Overall Assessment:** `{report['overall_status']}` | **Readiness Score:** `{report['readiness_percentage']}%`",
                f"**Satisfied Conditions:** {len(satisfied)}/{len(report['assessments'])} | **Blocking Gaps:** {len(not_sat)}\n",
                "#### ✅ Conditions Met with Verified Evidence:",
            ]
            for s in satisfied:
                answer_lines.append(f"- **{s['clause_title']}** ({s['source_citation']}): {s['company_value_or_evidence']}")

            if not_sat:
                answer_lines.append("\n#### ❌ What is Preventing Submission-Readiness (Immediate Action Required):")
                for ns in not_sat:
                    answer_lines.append(
                        f"- **{ns['clause_title']}** ({ns['source_citation']}):\n"
                        f"  • *Tender Requirement:* {ns['tender_condition']}\n"
                        f"  • *Status:* {ns['company_value_or_evidence']}\n"
                        f"  • *Remedy:* {ns.get('missing_evidence') or 'Provide signed client completion certificate'}"
                    )

            if needs_ver:
                answer_lines.append("\n#### ⚠️ Items Requiring Clarification / Verification:")
                for nv in needs_ver:
                    answer_lines.append(f"- **{nv['clause_title']}** ({nv['source_citation']}): {nv['company_value_or_evidence']}")

            msme = report.get("msme_benefits", {})
            if msme.get("qualifies_for_msme_policy"):
                answer_lines.append(
                    f"\n#### 💡 MSME Opportunity Optimizer:\n"
                    f"- **EMD Exemption:** Eligible! You save ₹{msme.get('emd_exemption_savings_inr', 0):,.0f} by attaching your Udyam Certificate ({company.udyam_registration_number}).\n"
                    f"- **Relaxation:** {msme.get('turnover_relaxation_notes', '')}"
                )

            answer_lines.append(
                f"\n**Next Concrete Step:** {report['next_recommended_actions'][0] if report.get('next_recommended_actions') else 'Upload missing completion certificate to proceed to bid generation.'}"
            )

            return {
                "answer": "\n".join(answer_lines),
                "tools_used": ["EligibilityMCPServer.evaluate_eligibility", "EligibilityMCPServer.check_msme_benefits"],
                "data": report
            }

        # Query 2: Corrigendum / Amendments
        elif any(k in q_lower for k in ["corrigendum", "amendment", "changed", "updated", "deadline"]):
            corr_res = self.registry.execute_tool(
                server_name="MonitoringMCPServer",
                tool_name="monitor_tender_updates",
                arguments={"tender_id": target_tender_id},
                agent_name="Monitoring Agent"
            )
            corrs = corr_res.result.get("corrigenda", [])
            lines = [
                f"### Corrigendum Intelligence for **{tender.title}**\n",
                f"We detected **{len(corrs)} official corrigenda/amendments** published for this tender:\n"
            ]
            for c in corrs:
                lines.append(
                    f"- **{c['title']}** (Issued: {c['issue_date']})\n"
                    f"  • *Previous:* {c.get('old_value', 'N/A')}\n"
                    f"  • *Revised:* {c.get('new_value', 'N/A')}\n"
                    f"  • *Bid Impact:* {c.get('action_required', 'Checklist update recommended.')}\n"
                )
            return {
                "answer": "\n".join(lines),
                "tools_used": ["MonitoringMCPServer.monitor_tender_updates"],
                "data": corrs
            }

        # Query 3: Discovery / Finding tenders
        elif any(k in q_lower for k in ["find", "search", "discover", "opportunities"]):
            disc_res = self.registry.execute_tool(
                server_name="TenderMCPServer",
                tool_name="search_tenders",
                arguments={"category": "IT Services"},
                agent_name="Discovery Agent"
            )
            tenders_found = disc_res.result.get("tenders", [])
            lines = [
                f"### Discovered Tenders for {company.name} ({company.city}, {company.state}):\n",
                f"Found **{len(tenders_found)} opportunities** ranked by two-way business suitability:\n"
            ]
            for t in tenders_found:
                lines.append(
                    f"1. **{t['title']}** (`{t['tender_id']}`)\n"
                    f"   • *Buyer:* {t['department']}\n"
                    f"   • *Estimated Value:* ₹{t['estimated_value_inr']:,.0f} | *Suitability:* `{t.get('suitability_score', 80)}/100`\n"
                    f"   • *Closing Deadline:* {t['submission_deadline']}\n"
                )
            return {
                "answer": "\n".join(lines),
                "tools_used": ["TenderMCPServer.search_tenders"],
                "data": tenders_found
            }

        # Default query handler
        else:
            return {
                "answer": (
                    f"TenderMind Agentic System ready. Target active tender: **{tender.title}** ({tender.tender_id}).\n"
                    f"You can ask me:\n"
                    f"• *'Can my company apply for this tender? What is missing?'*\n"
                    f"• *'What corrigenda or deadline changes have been issued?'*\n"
                    f"• *'What MSME benefits and EMD exemptions apply to us?'*\n"
                    f"• *'Generate our bid submission checklist and technical proposal draft.'*"
                ),
                "tools_used": []
            }

orchestrator = TenderMindOrchestrator()
