import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Loan Prediction System", layout="wide")

# ---------------------- LOAD MODEL ONCE ----------------------
@st.cache_resource
def load_model():
    model = joblib.load("loan_model.pkl")
    columns = joblib.load("model_columns.pkl")
    return model, columns

model, model_columns = load_model()

# ---------------------- CUSTOM CSS ----------------------
st.markdown("""
<style>
.main {background-color:#f5f7fb;}
h1 {color:#1f4e79;text-align:center;}
.metric-card {
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- SIDEBAR ----------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home Dashboard","Prediction Results"])

# ---------------------- PREPROCESS FUNCTION ----------------------
def preprocess(data):

    data = data.copy()

    # Clean job & term
    if "Years in current job" in data.columns:
        data["Years in current job"] = (
            data["Years in current job"]
            .astype(str).str.extract(r'(\d+)')
        )
        data["Years in current job"] = pd.to_numeric(data["Years in current job"], errors="coerce")

    if "Term" in data.columns:
        data["Term"] = data["Term"].astype(str).str.extract(r'(\d+)')
        data["Term"] = pd.to_numeric(data["Term"], errors="coerce")

    # Drop unnecessary
    data = data.drop(["Loan Status","Customer ID","Loan ID"], axis=1, errors="ignore")
    # handle credit score
    data["Credit Score"] = data["Credit Score"].fillna(650)  # neutral score

    # Numeric columns
    num_cols = [
        "Credit Score","Annual Income","Monthly Debt",
        "Years of Credit History","Months since last delinquent",
        "Number of Open Accounts","Number of Credit Problems",
        "Current Credit Balance","Maximum Open Credit",
        "Bankruptcies","Tax Liens"
    ]

    for col in num_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    # Fill missing
    data = data.fillna(0)

    # Align columns
    data = data.reindex(columns=model_columns, fill_value=0)

    return data
    

# ---------------------- HOME PAGE ----------------------
if page == "Home Dashboard":

    st.title("Smart Loan Eligibility Prediction System")

    uploaded_file = st.file_uploader("Upload Loan Dataset (.csv)")

    if uploaded_file is not None:

        data = pd.read_csv(uploaded_file)
        st.dataframe(data, width="stretch")
        if st.button("Run Prediction"):

            X = preprocess(data)

            #FIX: convert to numpy (NO WARNING)
            y_prob = model.predict_proba(X.values)[:,1]

            threshold = 0.57
            predictions = (y_prob > threshold).astype(int)
            data["Prediction"] = predictions 
            data["Probability"] = (y_prob * 100).round(2) 
            # ---------------------- RISK FUNCTION ----------------------
            def classify_risk(prob):
                    if prob > 0.57:
                        return "Low Risk"
                    else:
                        return "High Risk"

            data["Risk"] = pd.Series(y_prob, index=data.index).apply(classify_risk)
            # Metrics
            col1, col2 = st.columns(2)
            col1.metric("Eligible", (predictions == 1).sum())
            col2.metric("Not Eligible", (predictions == 0).sum())

            col3, col4 = st.columns(2)
            col3.metric("Low Risk", (data["Risk"] == "Low Risk").sum())
            col4.metric("High Risk", (data["Risk"] == "High Risk").sum())
            
            st.session_state["result"] = data
            st.success("Prediction Completed ✅")


# ---------------------- RESULT PAGE ----------------------
if page == "Prediction Results":

    st.title("Prediction Results")

    if "result" in st.session_state:
        result = st.session_state["result"]

        result["Probability"] = result["Probability"].round(2)

        st.dataframe(result, width="content")
        st.download_button(
            label="Download Report",
            data=result.to_csv(index=False),
            file_name="loan_prediction_report.csv"
        )
    else:
        st.warning("Run prediction first.")