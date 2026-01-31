from datetime import datetime, timedelta
import random
from ehr_automation.models.dtos import PatientDTO, AppointmentDTO

class MockEHR:
    def __init__(self):
        # Seed with some dummy data
        self.patients = {
            "p1": PatientDTO(id="p1", name="Alice Smith", birthDate="1980-01-01", telecom="555-0101"),
            "p2": PatientDTO(id="p2", name="Bob Jones", birthDate="1975-05-12", telecom="555-0102"),
        }
        self.appointments = []

    def get_patient(self, patient_id: str):
        return self.patients.get(patient_id)

    def get_available_slots(self, date: datetime):
        # Return a list of available slots for a given date
        # Simplified: 9 AM to 5 PM, 1-hour slots
        slots = []
        start_hour = 9
        end_hour = 17
        for hour in range(start_hour, end_hour):
            slot_start = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            slot_end = slot_start + timedelta(hours=1)
            # Check if occupied
            is_occupied = any(
                a.start == slot_start for a in self.appointments if a.status != "cancelled"
            )
            if not is_occupied:
                slots.append((slot_start, slot_end))
        return slots

    def book_appointment(self, appointment: AppointmentDTO):
        print(f"[MockEHR] Booking appointment for {appointment.patient_id} at {appointment.start}")
        self.appointments.append(appointment)
        return True
