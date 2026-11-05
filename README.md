# Cynbit Lead Intelligence Copilot

> **AI/ML Engineer Intern assessment submission** — a human-in-the-loop system to turn unstructured inbound enquiries into explainable, CRM-ready discovery briefs.

## Submission at a glance

| Deliverable | Location |
|---|---|
| AI Opportunity Report | [`AI_OPPORTUNITY_REPORT.md`](AI_OPPORTUNITY_REPORT.md) |
| Functional POC | [`app.py`](app.py) Streamlit reviewer demo + CLI |
| Technical Approach Report | [`TECHNICAL_APPROACH.md`](TECHNICAL_APPROACH.md) |
| 2-minute demo script | [`DEMO_GUIDE.md`](DEMO_GUIDE.md) |

This repository contains:

- `AI_OPPORTUNITY_REPORT.md` — opportunity selection and business case
- `TECHNICAL_APPROACH.md` — production architecture and delivery plan
- an interactive Streamlit reviewer demo and a runnable Python CLI

## What the prototype does

It accepts a new inbound enquiry and returns a deterministic priority (`P0`, `P1`, or `P2`), a 0–100 score, missing discovery questions, recommended owner, a concise brief, and an audit trail explaining every score contribution. It deliberately avoids pretending that a probabilistic model is already trained on Cynbit data.

## Run it

Requirements: Python 3.10+.

### Interactive demo (recommended)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

The browser UI includes a lead form, decision card, score explanation, approved knowledge retrieval, human approval/override simulation, and auditable JSON payload. See [`DEMO_GUIDE.md`](DEMO_GUIDE.md) for the suggested walkthrough.

### Dependency-free CLI

```powershell
cd C:\path\to\cynbit-lead-intelligence-copilot
python -m src.cli --input data/sample_leads.json
```

Run the test suite:

```powershell
python -m unittest discover -s tests -v
```

Use a single custom lead:

```powershell
python -m src.cli --name "Northstar Retail" --email "cto@northstar.example" --service "AI automation" --company-size 120 --budget 1200000 --timeline "this month" --message "We need to automate manual invoice extraction and CRM updates across three teams."
```

`budget` is INR. This prototype keeps all logic local and contains only synthetic demo data.

## Design choices

The first release is rules-based and explainable: it is deployable before Cynbit has enough labelled lead-to-revenue history, supports calibration with sales, and produces clean labels for a future ranking model. The demo adds local retrieval over approved service content. The accompanying technical report specifies the production LLM, vector retrieval, human-review, security, monitoring, and model-governance layers.

## Repository structure

```text
app.py                    # Streamlit reviewer experience
src/scorer.py             # Explainable priority rules
src/retrieval.py          # Local, approved-knowledge retrieval
data/                     # Synthetic leads and approved demo knowledge
tests/                    # Unit tests
AI_OPPORTUNITY_REPORT.md  # Business case
TECHNICAL_APPROACH.md     # Production architecture
DEMO_GUIDE.md             # Reviewer walkthrough
```

## Submission notes

1. Create a GitHub repository and upload this folder (including hidden `.gitignore`).
2. Set the repository visibility as requested by the hiring team.
3. Paste the repository URL as the primary deliverable link.
4. Optionally deploy `app.py` on Streamlit Community Cloud and add its URL to the repository description.
5. Use the two report files as additional deliverable links if the portal accepts them separately.

