import streamlit as st
import db
import review_engine

st.title("1. Draft and Review")

if st.session_state.get("role") != "Creator":
    st.warning("Switch to the Creator role on the Home page to create a draft.")

content_type = st.selectbox("Content type", ["Social post", "Email", "Press release", "Ad copy"])
channel = st.selectbox("Channel", ["Instagram", "LinkedIn", "Email", "Website", "Twitter/X"])
draft_text = st.text_area("Paste or write your draft here", height=200)

if st.button("Run Review", type="primary"):
    if not draft_text.strip():
        st.error("Please enter some draft text first.")
    else:
        with st.spinner("Checking against approved guidelines..."):
            draft = db.create_draft(content_type, channel, draft_text)
            version = db.create_version(draft["id"], draft_text)
            findings, error = review_engine.run_review(draft_text)

            if error:
                st.error(error)
            else:
                for f in findings:
                    db.insert_finding(version["id"], f)
                db.insert_audit(draft["id"], "Creator", "Draft created and reviewed")
                st.session_state["current_draft_id"] = draft["id"]
                st.success(f"Review complete. {len(findings)} finding(s). Go to the Findings page to resolve them.")

st.divider()
st.subheader("Your recent drafts")
drafts = db.list_drafts()
for d in drafts[:10]:
    st.write(f"**Draft #{d['id']}** — {d['content_type']} / {d['channel']} — status: `{d['status']}`")