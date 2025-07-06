import streamlit as st
import numpy as np

# Ultra-lightweight credit check (no sklearn needed)
def calculate_risk(income, debt, score):
    risk_score = (debt/(income+1)) * 0.7 + (1 - score/850) * 0.3
    return risk_score

# Streamlit UI
st.title("💳 Instant Credit Check")

income = st.number_input("Annual Income ($)", 20000, 500000, 60000)
debt = st.number_input("Existing Debt ($)", 0, 300000, 20000)
score = st.slider("Credit Score", 300, 850, 700)

if st.button("Check Risk"):
    risk = calculate_risk(income, debt, score)
    
    st.subheader("Result")
    if risk > 0.5:
        st.error(f"High Risk ({risk:.1%}) 🚨")
    else:
        st.success(f"Low Risk ({risk:.1%}) ✅")
    
    # Simple visualization
    st.progress(risk)
    st.caption("Risk meter: 0% (safe) → 100% (high risk)")
