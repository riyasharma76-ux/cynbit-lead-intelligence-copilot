# 2-Minute Demo Guide

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit (normally `http://localhost:8501`). No external service, database, or API key is required.

## Suggested walkthrough

1. Start with the prefilled enterprise AI-automation enquiry and select **Generate reviewer brief**.
2. Point out the P0 recommendation, 100/100 score, four-hour response SLA, service route, and suggested owner.
3. Open **Why this score?** to show that every point is traceable—not an opaque model claim.
4. Show the approved knowledge result. Explain that production replaces local token matching with evaluated, metadata-filtered vector retrieval.
5. Select **Approve and create CRM draft**. Emphasize that it only records a simulated, auditable human approval; no email is sent and no lead is rejected automatically.
6. Change budget to zero and timeline to “not provided,” then regenerate. Show that the system asks discovery questions rather than inventing data.

## What this demonstrates

- explainable deterministic triage baseline;
- local retrieval over approved service knowledge;
- reviewer gate before a consequential action;
- structured audit payload; and
- a concrete path to a production LLM/RAG workflow described in `TECHNICAL_APPROACH.md`.
