import unittest
from tendermind.data.sample_data import SAMPLE_COMPANY, SAMPLE_TENDERS
from tendermind.engine.rule_evaluator import EligibilityRuleEngine
from tendermind.engine.msme_rules import MSMERuleEngine
from tendermind.models.eligibility import ConditionStatus

class TestEligibilityEngine(unittest.TestCase):
    def setUp(self):
        self.company = SAMPLE_COMPANY
        self.tender = next(t for t in SAMPLE_TENDERS if t.tender_id == "GEM/2026/B/123456")

    def test_msme_benefits(self):
        benefits = MSMERuleEngine.evaluate_benefits(self.company, self.tender)
        self.assertTrue(benefits.qualifies_for_msme_policy)
        self.assertTrue(benefits.emd_exemption_eligible)
        self.assertEqual(benefits.emd_exemption_savings_inr, 50000.0)

    def test_eligibility_three_state_evaluation(self):
        report = EligibilityRuleEngine.evaluate(self.company, self.tender)
        
        # Check overall status
        self.assertEqual(report.overall_status, "POTENTIAL_GAP")
        
        # Turnover requirement should be Satisfied
        turnover_assessment = next(a for a in report.assessments if "turnover" in a.clause_title.lower())
        self.assertEqual(turnover_assessment.status, ConditionStatus.SATISFIED)
        self.assertIn("Page 12", turnover_assessment.source_citation)

        # Completion certificate should be Not satisfied (missing!)
        comp_cert_assessment = next(a for a in report.assessments if "completion certificate" in a.clause_title.lower())
        self.assertEqual(comp_cert_assessment.status, ConditionStatus.NOT_SATISFIED)
        self.assertIn("Page 14", comp_cert_assessment.source_citation)

        # There should be at least one blocking gap
        self.assertTrue(any(g.severity == "BLOCKING" for g in report.gaps))

if __name__ == "__main__":
    unittest.main()
