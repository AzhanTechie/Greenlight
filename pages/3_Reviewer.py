import streamlit as st
import db

st.title("Reviewer Approval Queue")

role = st.session_state.get("role", "Creator")

if role != "Reviewer":
    st.warning("You are currently viewing as '" + role + "'. Switch to 'Reviewer' on the Home page to approve drafts.")

submitted_drafts = db.list_drafts(status="submitted")

if not submitted_drafts:
    st.info("No drafts are currently waiting for review.")
    st.stop()

draft_options = {f"Draft #{d['id']} — {d['content_type']} / {d['channel']}": d['id'] for d in submitted_drafts}
selected_label = st.selectbox("Select a draft to review", list(draft_options.keys()))
selected_draft_id = draft_options[selected_label]

versions = db.get_versions_for_draft(selected_draft_id)
latest_version = versions[-1]

st.subheader("Draft text")
st.write(latest_version["text"])

st.subheader("Findings and decisions")
findings = db.get_findings_for_version(latest_version["id"])

if not findings:
    st.write("No findings were recorded for this draft.")
else:
    for f in findings:
        with st.container(border=True):
            st.markdown(f"**[{f['severity']}] {f['category']}** — status: {f['status']}")
            st.markdown(f"> \"{f['quote']}\"")
            st.write(f["explanation"])
            if f["suggestion"]:
                st.caption(f"Suggested fix: {f['suggestion']}")

st.divider()
st.subheader("Comments")

comments = db.get_comments(selected_draft_id)
for c in comments:
    st.markdown(f"**{c['actor_role']}:** {c['text']}")

new_comment = st.text_area("Add a comment")
if st.button("Post comment"):
    if new_comment.strip():
        db.insert_comment(selected_draft_id, role, new_comment.strip())
        st.rerun()

st.divider()
st.subheader("Decision")

reason = st.text_area("Reason (required if requesting changes)")

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Approve"):
        db.update_draft_status(selected_draft_id, "approved")
        db.add_audit_log(selected_draft_id, role, "approved", reason)
        st.success("Draft approved.")
        st.rerun()

with col2:
    if st.button("🔁 Request changes"):
        if not reason.strip():
            st.error("Please provide a reason for requesting changes.")
        else:
            db.update_draft_status(selected_draft_id, "changes_requested")
            db.add_audit_log(selected_draft_id, role, "changes_requested", reason)
            st.warning("Changes requested. Sent back to Creator.")
            st.rerun()