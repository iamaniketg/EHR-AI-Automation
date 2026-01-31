import time
from ehr_automation.services.mock_ehr import MockEHR
from ehr_automation.services.event_bus import EventBus
from ehr_automation.services.orchestrator import Orchestrator
from ehr_automation.models.dtos import ClaimDTO

def main():
    print("=== Starting AI-Agent Driven EHR Automation Demo ===\n")
    
    # 1. Initialize Infrastructure
    ehr = MockEHR()
    bus = EventBus()
    orchestrator = Orchestrator(ehr, bus)
    
    # 2. Simulate Scenario: High Urgency Appointment
    print(">>> SCENARIO 1: Booking Urgent Appointment")
    bus.publish("APPOINTMENT_REQUESTED", {"patient_id": "p1", "urgency": 9})
    time.sleep(1)
    
    # 3. Simulate Scenario: Routine Appointment
    print("\n>>> SCENARIO 2: Booking Routine Appointment")
    bus.publish("APPOINTMENT_REQUESTED", {"patient_id": "p2", "urgency": 2})
    time.sleep(1)
    
    # 4. Simulate Scenario: Processing Clinical Note
    print("\n>>> SCENARIO 3: Processing Unstructured Clinical Note")
    raw_note = """
    Subjective: Patient complains of severe headache and nausea for 2 days.
    Objective: BP 140/90, Temp 37.5C. Neuro exam normal.
    Assessment: Potential migraine or tension headache.
    Plan: Prescribed Sumatriptan. Monitor for 24 hours.
    """
    bus.publish("CLINICAL_NOTE_CREATED", {"patient_id": "p1", "text": raw_note})
    time.sleep(1)
    
    # 5. Simulate Scenario: Billing Anomaly Detection
    print("\n>>> SCENARIO 4: Billing Compliance Check")
    
    # Normal Claim
    normal_claim = ClaimDTO(id="c1", patient_id="p1", items=[{'procedure': '99213', 'amount': 150.0}], total=150.0, status="new")
    bus.publish("CLAIM_SUBMITTED", {"claim": normal_claim})
    time.sleep(1)

    # Anomalous Claim (High Amount)
    bad_claim = ClaimDTO(id="c2", patient_id="p2", items=[{'procedure': '99214', 'amount': 6000.0}], total=6000.0, status="new")
    bus.publish("CLAIM_SUBMITTED", {"claim": bad_claim})
    
    print("\n=== Demo Simulation Completed ===")

if __name__ == "__main__":
    main()
