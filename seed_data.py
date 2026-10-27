import db

def seed():
    rules = [
        ("TONE-01", "Tone", "Avoid aggressive, pushy, or hyperbolic language in customer-facing copy.", "Medium"),
        ("CLAIM-03", "Claims", "Superlatives (best, #1, fastest) and guarantees require an approved source.", "High"),
        ("TERM-04", "Terminology", "Use only approved product and company names, never nicknames or unofficial terms.", "Low"),
        ("MSG-02", "Messaging", "Do not imply a partnership, endorsement, or certification that has not been approved.", "High"),
    ]
    facts = [
        ("FACT-07", "Average delivery time is 30 minutes.", "Q2 operations report"),
        ("FACT-12", "The product is available in 12 cities as of this quarter.", "Expansion update, Q3"),
    ]
    terms = [
        ("super app", "banned", "our platform"),
        ("fastest", "banned", "quick"),
        ("world's best", "banned", "highly rated"),
    ]

    for r in rules:
        try:
            db.add_rule(*r)
        except Exception as e:
            print(f"Skipped rule {r[0]}: {e}")

    for f in facts:
        try:
            db.add_fact(*f)
        except Exception as e:
            print(f"Skipped fact {f[0]}: {e}")

    for t in terms:
        try:
            db.add_term(*t)
        except Exception as e:
            print(f"Skipped term {t[0]}: {e}")

    print("Seeding complete.")

if __name__ == "__main__":
    seed()