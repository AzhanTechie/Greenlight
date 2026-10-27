import streamlit as st

st.set_page_config(page_title="Greenlight", page_icon="✅", layout="wide")

if "role" not in st.session_state:
    st.session_state.role = "Creator"

st.title("✅ Greenlight")
st.caption("Pre-publication brand governance that explains every finding, cites its source, and leaves the final decision to people.")

st.session_state.role = st.selectbox(
    "Viewing as:",
    ["Creator", "Reviewer", "Manager", "Brand Admin"],
    index=["Creator", "Reviewer", "Manager", "Brand Admin"].index(st.session_state.role)
)

st.info(
    "AI notice: when you run a review, your draft text is sent to Google's Gemini API "
    "for analysis. No other data from this product is shared externally."
)

st.markdown("""
### How to use this demo
1. Go to **Draft** (left sidebar) to write or paste content and run a review.
2. Go to **Findings** to accept, edit, or dismiss each flagged issue.
3. Submit for approval, then switch role to **Reviewer** to approve or request changes.
4. Check **Insights** as a **Manager** to see recurring issues.
5. Manage the brand knowledge base as **Brand Admin**.
""")