from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime

@dataclass
class PatientDTO:
    id: str
    name: str
    birthDate: str
    telecom: str

@dataclass
class EncounterDTO:
    id: str
    patient_id: str
    status: str
    period_start: datetime
    reason: str

@dataclass
class AppointmentDTO:
    id: str
    patient_id: str
    start: datetime
    end: datetime
    status: str
    urgency_level: int = 1  # 1-10, for scheduling logic

@dataclass
class ClaimDTO:
    id: str
    patient_id: str
    items: List[dict] # {'procedure': 'code', 'amount': 100.00}
    total: float
    status: str

@dataclass
class DocumentDTO:
    id: str
    patient_id: str
    content: str # content of the note
    type: str = "SOAP"
