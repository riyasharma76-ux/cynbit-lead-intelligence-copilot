"""Explainable, deterministic lead triage for the prototype."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


SERVICE_KEYWORDS = {
    "ai automation": ("AI Automation", "AI/ML Solutions Consultant"),
    "software development": ("Custom Software", "Solutions Architect"),
    "cloud": ("Cloud Infrastructure", "Cloud/DevOps Architect"),
    "seo": ("Growth & SEO", "Growth Strategist"),
    "digital marketing": ("Growth & SEO", "Growth Strategist"),
}
URGENCY_TERMS = ("this week", "this month", "urgent", "asap", "immediately")
HIGH_INTENT_TERMS = ("budget", "proposal", "demo", "implementation", "automation", "integrate", "migration")


@dataclass
class Lead:
    name: str
    email: str
    service: str = ""
    company_size: int = 0
    budget: int = 0
    timeline: str = ""
    message: str = ""
    source: str = "website"


def _contains(text: str, words: tuple[str, ...]) -> bool:
    return any(word in text.lower() for word in words)


def score_lead(lead: Lead) -> dict[str, Any]:
    """Return a transparent triage decision and an audit trail.

    Scoring weights are explicit prototype assumptions, to be calibrated after a
    four-week sales review. The output must not be used to reject a prospect.
    """
    points = 0
    reasons: list[dict[str, Any]] = []
    text = f"{lead.service} {lead.message}".lower()

    def add(label: str, value: int, evidence: str) -> None:
        nonlocal points
        points += value
        reasons.append({"signal": label, "points": value, "evidence": evidence})

    if lead.company_size >= 100:
        add("company size", 25, f"{lead.company_size} employees (100+)")
    elif lead.company_size >= 25:
        add("company size", 15, f"{lead.company_size} employees (25–99)")
    elif lead.company_size > 0:
        add("company size", 5, f"{lead.company_size} employees (1–24)")

    if lead.budget >= 1_000_000:
        add("budget", 25, f"₹{lead.budget:,} (₹10L+)")
    elif lead.budget >= 300_000:
        add("budget", 15, f"₹{lead.budget:,} (₹3L–9.99L)")
    elif lead.budget > 0:
        add("budget", 5, f"₹{lead.budget:,} (under ₹3L)")

    if _contains(lead.timeline, URGENCY_TERMS):
        add("timeline", 20, f"time-sensitive: {lead.timeline}")
    elif lead.timeline:
        add("timeline", 8, f"timeline supplied: {lead.timeline}")

    if _contains(text, HIGH_INTENT_TERMS):
        add("problem intent", 15, "message contains delivery or buying intent")
    if lead.email and "@" in lead.email and not lead.email.lower().endswith(("@gmail.com", "@yahoo.com", "@outlook.com")):
        add("work email", 10, "non-consumer email domain")
    if any(key in text for key in SERVICE_KEYWORDS):
        add("service fit", 5, "matches a Cynbit service area")

    score = min(points, 100)
    if score >= 65:
        priority, sla = "P0", "Contact within 4 business hours"
    elif score >= 35:
        priority, sla = "P1", "Contact within 1 business day"
    else:
        priority, sla = "P2", "Nurture; invite to a discovery call"

    matched = next((v for key, v in SERVICE_KEYWORDS.items() if key in text), ("General Discovery", "Business Development"))
    missing = []
    for field, question in (
        (lead.company_size, "How many users or team members will be affected?"),
        (lead.budget, "What budget range has been approved or is being considered?"),
        (lead.timeline, "What outcome date or decision deadline are you working toward?"),
    ):
        if not field:
            missing.append(question)
    if not lead.message.strip():
        missing.append("What workflow, system, or business outcome should this project improve?")

    brief = (
        f"{lead.name} reached Cynbit via {lead.source} seeking {matched[0]}. "
        f"Route to {matched[1]}; {sla.lower()}. "
        f"Known context: {lead.message or 'No problem statement supplied.'}"
    )
    return {"lead": asdict(lead), "score": score, "priority": priority, "service_route": matched[0],
            "recommended_owner": matched[1], "next_step_sla": sla, "brief": brief,
            "missing_questions": missing, "score_explanation": reasons,
            "safety_note": "Decision support only; a human must review before outreach or rejection."}
