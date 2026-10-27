import streamlit as st
import pandas as pd
import db

st.title("Insights")

role = st.session_state.get("role", "Creator")

if role != "Manager":
    st.warning("You are currently viewing as '" + role + "'. Switch to 'Manager' on the Home page for the intended view.")

drafts = db.list_drafts()

if not drafts:
    st.info("No data yet. Create and review some drafts first.")
    st.stop()

all_findings = []
for d in drafts:
    versions = db.get_versions_for_draft(d["id"])
    for v in versions:
        findings = db.get_findings_for_version(v["id"])
        for f in findings:
            f["draft_id"] = d["id"]
            all_findings.append(f)

if not all_findings:
    st.info("No findings have been generated yet.")
    st.stop()

df = pd.DataFrame(all_findings)

st.subheader("Total drafts and findings")
col1, col2, col3 = st.columns(3)
col1.metric("Total drafts", len(drafts))
col2.metric("Total findings", len(df))
col3.metric("Open findings", len(df[df["status"] == "open"]))

st.divider()

st.subheader("Findings by category")
category_counts = df["category"].value_counts()
st.bar_chart(category_counts)

st.subheader("Findings by severity")
severity_counts = df["severity"].value_counts()
st.bar_chart(severity_counts)

st.subheader("Findings by status (accepted / dismissed / edited / open)")
status_counts = df["status"].value_counts()
st.bar_chart(status_counts)

st.divider()

st.subheader("Most frequently triggered rules")
rule_counts = df[df["rule_id"].notna()]["rule_id"].value_counts()
if len(rule_counts) > 0:
    st.bar_chart(rule_counts)
else:
    st.write("No rule-based findings yet.")

st.subheader("Most frequently dismissed rules")
dismissed_df = df[df["status"] == "dismissed"]
dismissed_rule_counts = dismissed_df[dismissed_df["rule_id"].notna()]["rule_id"].value_counts()
if len(dismissed_rule_counts) > 0:
    st.bar_chart(dismissed_rule_counts)
else:
    st.write("No dismissed rule-based findings yet.")

st.divider()
st.subheader("Unverified claims")
unverified_count = len(df[df["rule_id"] == "UNVERIFIED"])
st.metric("Claims with no approved source", unverified_count)