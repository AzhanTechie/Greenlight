import streamlit as st
import db

st.title("Findings")

role = st.session_state.get("role", "Creator")

drafts = db.get_recent_drafts()

if not drafts:
    st.info("No drafts yet. Go to the Draft page to create one.")
    st.stop()

draft_options = {f"Draft #{d['id']} — {d['content_type']} / {d['channel']} — status: {d['status']}": d['id'] for d in drafts}
selected_label = st.selectbox("Select a draft to review findings", list(draft_options.keys()))
selected_draft_id = draft_options[selected_label]

versions = db.get_versions_for_draft(selected_draft_id)

if not versions:
    st.warning("This draft has no versions yet.")
    st.stop()

latest_version = versions[-1]
st.subheader("Current draft text")
st.write(latest_version["text"])

findings = db.get_findings_for_version(latest_version["id"])

open_findings = [f for f in findings if f["status"] == "open"]

if not open_findings:
    st.success("No open findings for this draft version.")
else:
    severity_order = {"High": 0, "Medium": 1, "Low": 2}
    open_findings.sort(key=lambda f: severity_order.get(f["severity"], 3))

    for f in open_findings:
        with st.container(border=True):
            if f["rule_id"] == "UNVERIFIED":
                badge = "⚠️ Unverified Claim"
            elif f["verified"]:
                badge = "✅ Verified"
            else:
                badge = "⚠️ Could Not Verify"

            st.markdown(f"**[{f['severity']}] {f['category']}** — {badge}")
            st.markdown(f"> \"{f['quote']}\"")
            st.write(f["explanation"])

            if f["suggestion"]:
                st.markdown(f"**Suggested fix:** {f['suggestion']}")

            source_bits = []
            if f["rule_id"]:
                source_bits.append(f"Rule: {f['rule_id']}")
            if f["fact_id"]:
                source_bits.append(f"Fact: {f['fact_id']}")
            if source_bits:
                st.caption(" | ".join(source_bits))

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("Accept suggestion", key=f"accept_{f['id']}"):
                    db.update_finding_status(f["id"], "accepted")
                    db.add_decision(f["id"], "accepted", "", role)
                    st.rerun()

            with col2:
                if st.button("Dismiss", key=f"dismiss_{f['id']}"):
                    db.update_finding_status(f["id"], "dismissed")
                    db.add_decision(f["id"], "dismissed", "", role)
                    st.rerun()

            with col3:
                edit_key = f"edit_mode_{f['id']}"
                if st.button("Edit", key=f"edit_btn_{f['id']}"):
                    st.session_state[edit_key] = True

                if st.session_state.get(edit_key, False):
                    new_text = st.text_area("Edit suggestion", value=f["suggestion"], key=f"edit_area_{f['id']}")
                    if st.button("Save edit", key=f"save_edit_{f['id']}"):
                        db.update_finding_status(f["id"], "edited")
                        db.add_decision(f["id"], "edited", new_text, role)
                        st.session_state[edit_key] = False
                        st.rerun()

st.divider()
if st.button("Submit draft for review"):
    db.update_draft_status(selected_draft_id, "submitted")
    db.add_audit_log(selected_draft_id, role, "submitted_for_review", "")
    st.success("Draft submitted for reviewer approval.")
    st.rerun()