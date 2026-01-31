from datetime import datetime, timedelta
from ehr_automation.models.dtos import AppointmentDTO
from ehr_automation.services.mock_ehr import MockEHR

class SchedulingAgent:
    def __init__(self, ehr_service: MockEHR):
        self.ehr = ehr_service

    def schedule_appointment(self, patient_id: str, urgency_level: int, preferred_date: datetime = None):
        """
        Simulate an RL agent deciding the best slot.
        Reward function (implied): Minimize wait time for high urgency, maximize utilization.
        """
        print(f"[SchedulingAgent] Processing request for Patient {patient_id} with Urgency {urgency_level}")
        
        target_date = preferred_date if preferred_date else datetime.now()
        if target_date < datetime.now():
            target_date = datetime.now()

        # Search for slots for up to 7 days
        for day_offset in range(7):
            current_day = target_date + timedelta(days=day_offset)
            available_slots = self.ehr.get_available_slots(current_day)
            
            if not available_slots:
                continue

            # Policy logic:
            # If urgency is high (>7), take the absolute first slot.
            # If urgency is low, maybe avoid "prime time" (e.g., 9-10 AM) to save for urgent cases?
            # For this demo, we just pick the first available for simplicity, 
            # but we could add logic to skip morning slots if urgency is low.
            
            selected_slot = None
            if urgency_level > 7:
                 # High urgency: Grab first available
                 selected_slot = available_slots[0]
            else:
                 # Low urgency: Try to save morning slots (9-11) for urgent care
                 # Look for afternoon slots (> 12:00)
                 afternoon_slots = [s for s in available_slots if s[0].hour >= 12]
                 if afternoon_slots:
                     selected_slot = afternoon_slots[0]
                 else:
                     # If no afternoon slots, take anything
                     selected_slot = available_slots[0]
            
            if selected_slot:
                start, end = selected_slot
                appt = AppointmentDTO(
                    id=f"appt_{datetime.now().timestamp()}",
                    patient_id=patient_id,
                    start=start,
                    end=end,
                    status="booked",
                    urgency_level=urgency_level
                )
                self.ehr.book_appointment(appt)
                return appt

        print("[SchedulingAgent] No suitable slots found.")
        return None
