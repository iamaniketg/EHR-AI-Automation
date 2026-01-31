# AI-Agent Driven EHR Automation Demo

This project demonstrates a backend automation framework for Epic EHR-based health systems, as described in the research paper "AI-Agent–Driven Automation of Epic EHR-Based Health Systems".

It simulates an event-driven microservices architecture where specialized AI agents handle scheduling, clinical documentation, and billing compliance.

## Project Structure

The project is organized as a Python package `ehr_automation`.

```
ehr_automation/
├── main.py                 # Entry point for the end-to-end simulation
├── verify_demo.py          # Verification script to test individual components
├── config.py               # Configuration settings
├── models/                 # Data Transfer Objects (DTOs)
│   └── dtos.py             # Patient, Appointment, Claim, Document definitions
├── services/               # Core infrastructure services
│   ├── mock_ehr.py         # Simulates Epic SMART on FHIR API
│   ├── event_bus.py        # Simple in-memory event publisher/subscriber
│   └── orchestrator.py     # Coordinates workflow between agents and events
└── agents/                 # AI Agent implementations
    ├── scheduling_agent.py # Optimizes appointments based on urgency & availability
    ├── nlp_agent.py        # Extracts structured SOAP notes from raw text
    └── billing_agent.py    # Detects anomalies in insurance claims
```

## How to Run

### Prerequisites
- Python 3.8+

### Running the Demo Simulation
This script runs a full scenario covering scheduling, clinical notes, and billing.

```bash
# Set PYTHONPATH to current directory (Windows PowerShell)
$env:PYTHONPATH="."
python ehr_automation/main.py
```

**Expected Output:**
You will see logs indicating the orchestrator handling events:
1.  **Appointment Request**: Scheduled based on urgency.
2.  **Clinical Note**: Processed into structured data.
3.  **Claim Submission**: Flagged if anomalous, approved otherwise.

### Running Verification Tests
To verify the logic of individual agents:

```bash
$env:PYTHONPATH="."
python ehr_automation/verify_demo.py
```

## Demo Video
[Watch the Demo](https://www.youtube.com/watch?v=XOWjNx-_K9c)
