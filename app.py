"""Interactive reviewer demo for the Cynbit Lead Intelligence Copilot."""
import json
import streamlit as st

from src.retrieval import retrieve
from src.scorer import Lead, score_lead

st.set_page_config(page_title="Cynbit Lead Intelligence Copilot", page_icon="◈", layout="wide")
st.title("◈ Lead Intelligence Copilot")
st.caption("Human-in-the-loop lead triage • Prototype • Synthetic/demo data only")
st.info("This tool recommends a priority; it never rejects a lead or sends outreach automatically.")

with st.sidebar:
    st.header("Pilot controls")
    source = st.selectbox("Lead source", ["website", "contact form", "campaign", "shared inbox"])
    st.caption("Rules are visible and intentionally deterministic for the pilot. A future model is evaluated against reviewer outcomes.")

left, right = st.columns([1, 1])
with left:
    st.subheader("Inbound enquiry")
    name = st.text_input("Contact name", value="Aarav Mehta")
    email = st.text_input("Business email", value="aarav@northstarretail.example")
    service = st.selectbox("Interested service", ["AI automation", "Software development", "Cloud", "SEO", "Digital marketing", "Not sure"])
    company_size = st.number_input("Company size", min_value=0, value=180, step=1)
    budget = st.number_input("Indicative budget (INR)", min_value=0, value=1500000, step=50000)
    timeline = st.selectbox("Desired timeline", ["this month", "this week", "next quarter", "not provided"])
    message = st.text_area("Problem statement", value="We need to automate invoice extraction and CRM updates across three teams.", height=120)
    submitted = st.button("Generate reviewer brief", type="primary", use_container_width=True)

if submitted:
    lead = Lead(name=name or "Unknown", email=email, service=service, company_size=int(company_size), budget=int(budget),
                timeline="" if timeline == "not provided" else timeline, message=message, source=source)
    result = score_lead(lead)
    snippets = retrieve(result["service_route"], message)
    with right:
        st.subheader("Reviewer decision card")
        priority_colors = {"P0": "🔴", "P1": "🟠", "P2": "🔵"}
        st.metric("Recommended priority", f"{priority_colors[result['priority']]} {result['priority']}", f"{result['score']}/100")
        st.write(f"**Route:** {result['service_route']}  ")
        st.write(f"**Suggested owner:** {result['recommended_owner']}  ")
        st.write(f"**SLA:** {result['next_step_sla']}")
        st.write("**Brief**")
        st.write(result["brief"])
        decision = st.radio("Human reviewer action", ["Pending review", "Approve and create CRM draft", "Edit before routing", "Override priority"], horizontal=True)
        if decision != "Pending review":
            st.success(f"Recorded as: {decision}. In production this emits an authenticated, auditable CRM workflow event.")
    st.divider()
    a, b = st.columns(2)
    with a:
        st.subheader("Why this score?")
        st.dataframe(result["score_explanation"], use_container_width=True, hide_index=True)
        st.subheader("Questions to complete discovery")
        if result["missing_questions"]:
            for question in result["missing_questions"]:
                st.write(f"• {question}")
        else:
            st.success("The initial discovery fields are complete.")
    with b:
        st.subheader("Approved knowledge retrieved")
        for snippet in snippets:
            with st.expander(f"{snippet['id']} · {snippet['title']}"):
                st.write(snippet["content"])
        st.subheader("Auditable payload")
        st.code(json.dumps(result, indent=2, ensure_ascii=False), language="json")
else:
    st.markdown("### How to review this POC")
    st.markdown("Enter an enquiry, generate the brief, inspect the reasons and retrieved content, then simulate a human approval or override. The app demonstrates the reviewer control point before any CRM or email action.")
