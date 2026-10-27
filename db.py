import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def get_rules():
    return get_client().table("guideline_rules").select("*").execute().data

def get_facts():
    return get_client().table("approved_facts").select("*").execute().data

def get_terms():
    return get_client().table("terms").select("*").execute().data

def add_rule(id, category, description, severity_default):
    return get_client().table("guideline_rules").insert({
        "id": id, "category": category, "description": description,
        "severity_default": severity_default
    }).execute()

def add_fact(id, statement, source_note):
    return get_client().table("approved_facts").insert({
        "id": id, "statement": statement, "source_note": source_note
    }).execute()

def add_term(term, status, preferred_alternative):
    return get_client().table("terms").insert({
        "term": term, "status": status, "preferred_alternative": preferred_alternative
    }).execute()

def create_draft(content_type, channel, text):
    res = get_client().table("drafts").insert({
        "content_type": content_type, "channel": channel,
        "original_text": text, "status": "draft"
    }).execute()
    return res.data[0]

def get_draft(draft_id):
    return get_client().table("drafts").select("*").eq("id", draft_id).execute().data[0]

def list_drafts(status=None):
    q = get_client().table("drafts").select("*").order("created_at", desc=True)
    if status:
        q = q.eq("status", status)
    return q.execute().data

def update_draft_status(draft_id, status):
    get_client().table("drafts").update({"status": status}).eq("id", draft_id).execute()

def create_version(draft_id, text):
    existing = get_client().table("draft_versions").select("version_number").eq("draft_id", draft_id).execute().data
    next_version = (max([v["version_number"] for v in existing]) + 1) if existing else 1
    res = get_client().table("draft_versions").insert({
        "draft_id": draft_id, "version_number": next_version, "text": text
    }).execute()
    return res.data[0]

def get_latest_version(draft_id):
    res = get_client().table("draft_versions").select("*").eq("draft_id", draft_id)\
        .order("version_number", desc=True).limit(1).execute()
    return res.data[0] if res.data else None

def insert_finding(draft_version_id, finding: dict):
    res = get_client().table("findings").insert({
        "draft_version_id": draft_version_id,
        "quote": finding["quote"],
        "category": finding["category"],
        "severity": finding["severity"],
        "rule_id": finding.get("rule_id"),
        "fact_id": finding.get("fact_id"),
        "explanation": finding["explanation"],
        "suggestion": finding["suggestion"],
        "verified": finding["verified"],
        "status": "open"
    }).execute()
    return res.data[0]

def get_findings_for_version(draft_version_id):
    return get_client().table("findings").select("*").eq("draft_version_id", draft_version_id).execute().data

def update_finding_status(finding_id, status):
    get_client().table("findings").update({"status": status}).eq("id", finding_id).execute()

def insert_decision(finding_id, action, reason, actor_role):
    get_client().table("decisions").insert({
        "finding_id": finding_id, "action": action, "reason": reason, "actor_role": actor_role
    }).execute()

def get_all_decisions():
    return get_client().table("decisions").select("*").execute().data

def insert_comment(draft_id, actor_role, text):
    get_client().table("comments").insert({
        "draft_id": draft_id, "actor_role": actor_role, "text": text
    }).execute()

def get_comments(draft_id):
    return get_client().table("comments").select("*").eq("draft_id", draft_id)\
        .order("created_at").execute().data

def insert_audit(draft_id, actor_role, action, details=""):
    get_client().table("audit_log").insert({
        "draft_id": draft_id, "actor_role": actor_role, "action": action, "details": details
    }).execute()

def get_audit(draft_id):
    return get_client().table("audit_log").select("*").eq("draft_id", draft_id)\
        .order("created_at").execute().data
def get_recent_drafts():
    return list_drafts()

def get_versions_for_draft(draft_id):
    return get_client().table("draft_versions").select("*").eq("draft_id", draft_id)\
        .order("version_number").execute().data

def add_decision(finding_id, action, reason, actor_role):
    return insert_decision(finding_id, action, reason, actor_role)

def add_audit_log(draft_id, actor_role, action, details=""):
    return insert_audit(draft_id, actor_role, action, details)