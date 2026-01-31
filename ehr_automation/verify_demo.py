import pytest
from datetime import datetime
from ehr_automation.services.mock_ehr import MockEHR
from ehr_automation.agents.scheduling_agent import SchedulingAgent
from ehr_automation.agents.nlp_agent import NLPAgent
from ehr_automation.agents.billing_agent import BillingAgent
from ehr_automation.models.dtos import ClaimDTO

def test_scheduling_high_urgency():
    ehr = MockEHR()
    agent = SchedulingAgent(ehr)
    # Urgency 10 should book first available
    appt = agent.schedule_appointment("p1", 10)
    assert appt is not None
    assert appt.urgency_level == 10

def test_nlp_extraction():
    agent = NLPAgent()
    text = "Subjective: Pain. Objective: Fever."
    doc = agent.process_encounter_note("p1", text)
    assert "Pain" in doc.content
    assert "Fever" in doc.content

def test_billing_anomaly():
    agent = BillingAgent()
    # High amount claim
    claim = ClaimDTO(id="test_c", patient_id="p1", items=[], total=10000.0, status="new")
    is_anom, _ = agent.check_claim(claim)
    assert is_anom is True
    assert claim.status == "flagged_for_review"

def test_billing_normal():
    agent = BillingAgent()
    claim = ClaimDTO(id="test_c2", patient_id="p1", items=[], total=100.0, status="new")
    is_anom, _ = agent.check_claim(claim)
    assert is_anom is False
    assert claim.status == "approved"

if __name__ == "__main__":
    # Simple manual runner if pytest not installed
    try:
        test_scheduling_high_urgency()
        print("test_scheduling_high_urgency PASSED")
        test_nlp_extraction()
        print("test_nlp_extraction PASSED")
        test_billing_anomaly()
        print("test_billing_anomaly PASSED")
        test_billing_normal()
        print("test_billing_normal PASSED")
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
    except Exception as e:
        print(f"ERROR: {e}")
