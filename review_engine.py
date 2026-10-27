import json
import streamlit as st
import google.generativeai as genai
from schema import ReviewResult
import db

def get_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel("gemini-3.8-flash")

def build_prompt(draft_text, rules, facts, terms):
    rules_text = "\n".join([f"- {r['id']} ({r['category']}): {r['description']}" for r in rules])
    facts_text = "\n".join([f"- {f['id']}: {f['statement']}" for f in facts])
    terms_text = "\n".join([f"- '{t['term']}' is {t['status']}" +
                             (f", prefer '{t['preferred_alternative']}'" if t['preferred_alternative'] else "")
                             for t in terms])

    prompt = f"""You are a brand-compliance reviewer for marketing content.

You are given approved guideline rules, approved facts, and approved/banned terms.
Review the DRAFT below and return a JSON object with a "findings" array.

For EVERY finding:
- "quote": copy the EXACT text from the draft that triggered this finding, character-for-character.
- "category": one of Tone, Terminology, Claims, Messaging.
- "severity": Low, Medium, or High.
- "rule_id": the exact ID of the rule that applies, if any (or null).
- "fact_id": the exact ID of the fact that applies, if any (or null).
- "explanation": a short, plain-language reason this was flagged.
- "suggestion": the smallest possible edit that fixes the issue while preserving the original meaning.

IMPORTANT: If a claim has no matching approved fact, do NOT invent a fact ID. Leave "fact_id" as null
and explain in the "explanation" field that no approved source exists for this claim.
Do not invent rule IDs that are not in the list below.

APPROVED RULES:
{rules_text}

APPROVED FACTS:
{facts_text}

APPROVED/BANNED TERMS:
{terms_text}

DRAFT:
\"\"\"{draft_text}\"\"\"

Return ONLY a JSON object of the form: {{"findings": [ ... ]}}
If there are no issues, return {{"findings": []}}.
Do not include markdown formatting, backticks, or any text outside the JSON object.
"""
    return prompt

def call_model(prompt):
    model = get_model()
    response = model.generate_content(prompt)
    return response.text

def clean_json_text(raw_text):
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    return text.strip()

def parse_and_validate(raw_json_text):
    try:
        cleaned = clean_json_text(raw_json_text)
        data = json.loads(cleaned)
        result = ReviewResult(**data)
        return result, None
    except Exception as e:
        return None, str(e)

def verify_finding(finding_dict, draft_text, rule_ids, fact_ids):
    quote_ok = finding_dict["quote"] in draft_text
    rule_ok = (finding_dict["rule_id"] is None) or (finding_dict["rule_id"] in rule_ids)
    fact_ok = (finding_dict["fact_id"] is None) or (finding_dict["fact_id"] in fact_ids)

    if not quote_ok or not rule_ok or not fact_ok:
        finding_dict["verified"] = False
        finding_dict["explanation"] += " [Could not verify this finding against source material — please review manually.]"
        return finding_dict

    if finding_dict["category"] == "Claims" and not finding_dict["fact_id"]:
        finding_dict["explanation"] += " [No approved source found for this claim — marked Unverified.]"
        finding_dict["rule_id"] = finding_dict["rule_id"] or "UNVERIFIED"

    finding_dict["verified"] = True
    return finding_dict

def run_review(draft_text):
    rules = db.get_rules()
    facts = db.get_facts()
    terms = db.get_terms()

    rule_ids = {r["id"] for r in rules}
    fact_ids = {f["id"] for f in facts}

    prompt = build_prompt(draft_text, rules, facts, terms)

    try:
        raw = call_model(prompt)
    except Exception as e:
        return [], f"Error calling the AI model: {e}"

    result, error = parse_and_validate(raw)

    if error:
        try:
            raw2 = call_model(prompt + "\n\nReturn STRICT valid JSON only, no markdown, no extra text.")
            result, error2 = parse_and_validate(raw2)
        except Exception as e:
            return [], f"Error calling the AI model on retry: {e}"
        if error2:
            return [], f"Review engine could not produce valid output: {error2}"

    finding_dicts = []
    for f in result.findings:
        fd = f.model_dump()
        fd = verify_finding(fd, draft_text, rule_ids, fact_ids)
        finding_dicts.append(fd)

    return finding_dicts, None