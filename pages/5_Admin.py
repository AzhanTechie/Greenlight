import streamlit as st
import db

st.title("Brand Admin — Knowledge Base")

role = st.session_state.get("role", "Creator")

if role != "Brand Admin":
    st.warning("You are currently viewing as '" + role + "'. Switch to 'Brand Admin' on the Home page for the intended view.")

tab1, tab2, tab3 = st.tabs(["Guideline Rules", "Approved Facts", "Terms"])

with tab1:
    st.subheader("Existing rules")
    rules = db.get_rules()
    if rules:
        for r in rules:
            st.markdown(f"**{r['id']}** ({r['category']}, default severity: {r['severity_default']}) — {r['description']}")
    else:
        st.write("No rules yet.")

    st.divider()
    st.subheader("Add a new rule")
    new_rule_id = st.text_input("Rule ID", key="new_rule_id")
    new_rule_category = st.selectbox("Category", ["Tone", "Terminology", "Claims", "Messaging"], key="new_rule_category")
    new_rule_description = st.text_area("Description", key="new_rule_description")
    new_rule_severity = st.selectbox("Default severity", ["Low", "Medium", "High"], key="new_rule_severity")

    if st.button("Add rule"):
        if new_rule_id.strip() and new_rule_description.strip():
            db.add_rule(new_rule_id.strip(), new_rule_category, new_rule_description.strip(), new_rule_severity)
            st.success(f"Rule {new_rule_id} added.")
            st.rerun()
        else:
            st.error("Rule ID and description are required.")

with tab2:
    st.subheader("Existing facts")
    facts = db.get_facts()
    if facts:
        for f in facts:
            note = f" (source: {f['source_note']})" if f["source_note"] else ""
            st.markdown(f"**{f['id']}** — {f['statement']}{note}")
    else:
        st.write("No facts yet.")

    st.divider()
    st.subheader("Add a new fact")
    new_fact_id = st.text_input("Fact ID", key="new_fact_id")
    new_fact_statement = st.text_area("Statement", key="new_fact_statement")
    new_fact_source = st.text_input("Source note (optional)", key="new_fact_source")

    if st.button("Add fact"):
        if new_fact_id.strip() and new_fact_statement.strip():
            db.add_fact(new_fact_id.strip(), new_fact_statement.strip(), new_fact_source.strip() or None)
            st.success(f"Fact {new_fact_id} added.")
            st.rerun()
        else:
            st.error("Fact ID and statement are required.")

with tab3:
    st.subheader("Existing terms")
    terms = db.get_terms()
    if terms:
        for t in terms:
            alt = f" → prefer '{t['preferred_alternative']}'" if t["preferred_alternative"] else ""
            st.markdown(f"**{t['term']}** — {t['status']}{alt}")
    else:
        st.write("No terms yet.")

    st.divider()
    st.subheader("Add a new term")
    new_term = st.text_input("Term", key="new_term")
    new_term_status = st.selectbox("Status", ["approved", "banned", "caution"], key="new_term_status")
    new_term_alt = st.text_input("Preferred alternative (optional)", key="new_term_alt")

    if st.button("Add term"):
        if new_term.strip():
            db.add_term(new_term.strip(), new_term_status, new_term_alt.strip() or None)
            st.success(f"Term '{new_term}' added.")
            st.rerun()
        else:
            st.error("Term is required.")