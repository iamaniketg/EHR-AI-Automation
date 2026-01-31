import re
from ehr_automation.models.dtos import DocumentDTO

class NLPAgent:
    def process_encounter_note(self, patient_id: str, raw_text: str) -> DocumentDTO:
        print(f"[NLPAgent] Processing clinical note for Patient {patient_id}...")
        
        # Simulate extraction logic (mocking a Transformer model)
        # We look for simple headers like "Subjective:", "Objective:", etc.
        
        sections = {}
        patterns = {
            "Subjective": r"Subjective:\s*(.*?)(?=(Objective:|Assessment:|Plan:|$))",
            "Objective": r"Objective:\s*(.*?)(?=(Assessment:|Plan:|$))",
            "Assessment": r"Assessment:\s*(.*?)(?=(Plan:|$))",
            "Plan": r"Plan:\s*(.*)"
        }
        
        structured_content = ""
        for section, pattern in patterns.items():
            match = re.search(pattern, raw_text, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                sections[section] = content
                structured_content += f"## {section}\n{content}\n\n"
        
        if not structured_content:
            structured_content = raw_text # Fallback
            
        return DocumentDTO(
            id=f"doc_{patient_id}_1",
            patient_id=patient_id,
            content=structured_content,
            type="SOAP_Structured"
        )
