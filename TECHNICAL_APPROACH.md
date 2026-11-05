# Technical Approach: Lead Intelligence Copilot

## 1. Product contract

**Input:** consented inbound lead fields, source metadata, and an approved knowledge base.  
**Output:** schema-validated intent, service route, priority recommendation, evidence, missing questions, and draft CRM action.  
**Non-goal:** autonomous rejection, outreach, price quotation, or contractual commitment.

## 2. Reference architecture

```text
Contact form / inbox / campaigns
             |
     API gateway + consent check
             |
PII minimization + validation + prompt-injection screening
             |
  Rules engine ------> feature / decision log ----> analytics warehouse
             |                         ^
  Approved knowledge retrieval          | reviewer override + CRM outcomes
             |
 Structured LLM extraction (JSON schema, low temperature)
             |
 Policy + confidence checks
             |
 Reviewer queue -> approved CRM write / assisted reply draft
```

### Suggested stack

| Layer | Choice | Reason |
|---|---|---|
| API | FastAPI + Pydantic | Typed contracts, validation, OpenAPI. |
| Workflow | Celery/Temporal or managed queue | Retryable asynchronous inbox/CRM jobs. |
| System of record | Existing CRM + PostgreSQL audit store | Avoid parallel lead truth; support analysis. |
| Retrieval | Postgres `pgvector` or Pinecone | Approved service/case-study chunks with metadata filters. |
| LLM | Provider abstraction with a small structured-output model | Swap providers; control cost and reliability. |
| Observability | OpenTelemetry + dashboard | Trace latency, errors, cost, model/version, overrides. |
| Deployment | Docker on AWS/Azure, secrets manager, least-privilege IAM | Aligns with Cynbit's public cloud capabilities. |

## 3. Data pipeline

1. Receive event with `lead_id`, source, consent status, form fields, and timestamp.
2. Reject malformed events; quarantine duplicate or absent-consent records according to policy.
3. Store raw content separately; redact unnecessary PII from model prompts.
4. Normalize company size, budget range, timeline, language, and service hints.
5. Retrieve up to five approved, versioned knowledge chunks filtered by service and region. Never retrieve arbitrary web content at runtime.
6. Call the LLM with system rules, data delimiters, retrieved context, and a strict JSON schema.
7. Validate JSON; run deterministic policies (prohibited claims, confidence threshold, no auto-send); persist all versions and evidence.
8. Present a reviewer card. Only explicit approval emits a CRM update or email-draft action.
9. Join later outcomes back to `lead_id` for evaluation and training.

## 4. Prompt and schema design

The system prompt must say that lead text is untrusted data, cannot change instructions, and cannot authorize tools. Require an object like:

```json
{
  "intent": "automation_project",
  "service_route": "AI Automation",
  "summary": "string <= 80 words",
  "missing_questions": ["string"],
  "evidence_ids": ["kb_..."],
  "confidence": 0.0
}
```

The API rejects extra keys, invalid enumerations, unsupported evidence IDs, and low-confidence outputs. The prompt should not ask the model to score personal worth or infer protected traits. Numeric priority comes from calibrated business rules initially, not opaque model reasoning.

## 5. Model strategy

**Phase 1: rules + LLM extraction.** The included POC embodies this choice. It is inspectable and establishes reliable labels.

**Phase 2: supervised ranker.** After enough consented, quality-controlled outcomes (for example, several hundred leads with stable definitions), train a logistic regression or gradient-boosted ranker for `qualified meeting within 14 days`. Use service/source/time-aware splits and keep the rules/LLM output as features. A calibrated, simpler model is preferred to an unexplainable high-score model.

**Phase 3: contextual optimization.** Only after offline and controlled online evidence, test follow-up timing and message variants. Preserve human approval and causal measurement; do not optimize merely for clicks.

## 6. Evaluation plan

| Component | Offline test | Release gate |
|---|---|---|
| Extraction | 100 hand-labelled, de-identified leads; field-level F1 | ≥0.90 service-route F1; no critical fabricated claim |
| Retrieval | source attribution and relevance review | ≥90% relevant top-3 on judged sample |
| Priority | precision/recall for qualified meeting; calibration curve | improves rules baseline without harming any monitored slice |
| Safety | adversarial prompt-injection and PII tests | no prohibited automated action; all malformed JSON safely fails |
| Operations | load, retry, and failure drills | p95 review-card availability target agreed with business |

Production metrics: time to first review, time to first response, reviewer acceptance/override rate, missing-field completion, booking and win rate, cost/lead, p95 latency, schema-failure rate, retrieval-attribution rate, and outcomes by allowed monitoring slices.

## 7. Security, privacy, and governance

- Use data processing agreements, consent-aware ingestion, role-based access, tenant separation, encryption in transit/at rest, and a secrets manager.
- Set documented retention/deletion windows. Do not train on raw lead data without documented lawful basis and opt-out handling.
- Keep prompt, model, retrieval-index, rules, and policy versions with each decision. Redact PII from application logs.
- Apply rate limits, signed webhooks, idempotency keys, input-size limits, malware scanning for attachments, and egress allowlists.
- Conduct a privacy/security review before CRM or email integration. Escalate uncertain or sensitive requests to a human.

## 8. API outline

`POST /v1/leads/triage` returns a proposed decision only.  
`POST /v1/triages/{id}/review` records an approve/edit/override action with reviewer identity.  
`POST /v1/outcomes` ingests CRM outcome events idempotently.  
`GET /v1/metrics` provides aggregate, access-controlled pilot telemetry.

All state-changing endpoints require service authentication, an audit principal, and idempotency keys.

## 9. Delivery milestones

| Week | Deliverable |
|---:|---|
| 1 | Data map, consent/security review, baseline definitions |
| 2 | Rules POC in shadow mode; offline labelled set |
| 3 | FastAPI service and reviewer UI; telemetry |
| 4 | Retrieval + schema-constrained LLM extraction |
| 5 | CRM sandbox integration and human approval gate |
| 6 | Pilot dashboard, override analysis, red-team review |
| 7–8 | Controlled rollout and scale/stop decision |

## 10. Why this is implementation-ready

The repository includes a runnable, dependency-free scoring slice and tests. Its simple score is a product decision aid—not a substitute for a trained model—and its explicit assumptions make sales calibration straightforward. The production design adds the components the prototype purposely omits: consent management, retrieval, structured LLM output, CRM integration, human controls, security, and measured rollout.
