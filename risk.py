import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

# Minimal configuration
st.set_page_config(
    page_title="⚡ Quick Credit Check",
    layout="centered"
)

# Title with loading simulation
st.title("⚡ Credit Risk Assessment")

# Simplified data generation
def generate_data(n_samples=500):
    np.random.seed(42)
    data = {
        "income": np.abs(np.random.normal(60000, 20000, n_samples)),
        "debt": np.abs(np.random.exponential(20000, n_samples)),
        "score": np.random.randint(300, 850, n_samples)
    }
    df = pd.DataFrame(data)
    df["high_risk"] = ((df["debt"]/df["income"] > 0.4) | (df["score"] < 600)).astype(int)
    return df

# Minimal model training
@st.cache_resource
def train_model():
    df = generate_data()
    X = df[["income", "debt", "score"]]
    y = df["high_risk"]
    
    model = LogisticRegression()
    model.fit(X, y)
    joblib.dump(model, "quick_model.joblib")
    return model

# Load model
try:
    model = joblib.load("quick_model.joblib")
except:
    model = train_model()

# Input form
with st.form("quick_check"):
    income = st.number_input("Annual Income ($)", 20000, 500000, 60000)
    debt = st.number_input("Existing Debt ($)", 0, 300000, 20000)
    score = st.slider("Credit Score", 300, 850, 700)
    
    if st.form_submit_button("Check Risk"):
        # Predict
        proba = model.predict_proba([[income, debt, score]])[0][1]
        risk = "High Risk 🚨" if proba > 0.5 else "Low Risk ✅"
        
        # Results
        st.subheader("Result")
        st.metric("Risk Level", risk)
        st.metric("Risk Probability", f"{proba:.1%}")
        
        # Minimal visualization
        st.progress(proba)
        st.caption("Risk probability (0% = safe, 100% = high risk)")
        
        # Key factors
        factors = {
            "Debt/Income Ratio": f"{(debt/income):.1%}",
            "Credit Score": score,
            "Model Confidence": f"{max(proba, 1-proba):.1%}"
        }
        st.json(factors)

