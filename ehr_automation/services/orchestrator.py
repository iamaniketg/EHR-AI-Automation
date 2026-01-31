from ehr_automation.services.event_bus import EventBus
from ehr_automation.services.mock_ehr import MockEHR
from ehr_automation.agents.scheduling_agent import SchedulingAgent
from ehr_automation.agents.nlp_agent import NLPAgent
from ehr_automation.agents.billing_agent import BillingAgent
from ehr_automation.models.dtos import ClaimDTO, AppointmentDTO

class Orchestrator:
    def __init__(self, ehr: MockEHR, event_bus: EventBus):
        self.ehr = ehr
        self.event_bus = event_bus
        
        # Initialize Agents
        self.scheduler = SchedulingAgent(ehr)
        self.nlp = NLPAgent()
        self.biller = BillingAgent()
        
        # Subscribe to events
        self.event_bus.subscribe("APPOINTMENT_REQUESTED", self.handle_appointment_request)
        self.event_bus.subscribe("CLINICAL_NOTE_CREATED", self.handle_clinical_note)
        self.event_bus.subscribe("CLAIM_SUBMITTED", self.handle_claim_submission)

    def handle_appointment_request(self, data):
        print("\n--- [Orchestrator] Handling Appointment Request ---")
        patient_id = data.get("patient_id")
        urgency = data.get("urgency")
        
        appt = self.scheduler.schedule_appointment(patient_id, urgency)
        if appt:
            print(f"[Orchestrator] Appointment confirmed: {appt.id} on {appt.start}")
        else:
            print("[Orchestrator] Failed to schedule appointment.")

    def handle_clinical_note(self, data):
        print("\n--- [Orchestrator] Handling Clinical Note ---")
        patient_id = data.get("patient_id")
        raw_text = data.get("text")
        
        doc = self.nlp.process_encounter_note(patient_id, raw_text)
        print(f"[Orchestrator] Note processed. Structured content preview:\n{doc.content[:100]}...")

    def handle_claim_submission(self, data):
        print("\n--- [Orchestrator] Handling Claim Submission ---")
        claim = data.get("claim")
        
        is_anomalous, reasons = self.biller.check_claim(claim)
        if is_anomalous:
            print(f"[Orchestrator] Claim {claim.id} flagged for manual review.")
        else:
            print(f"[Orchestrator] Claim {claim.id} auto-approved.")
