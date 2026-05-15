import streamlit as st
import smtplib
from email.mime.text import MIMEText

# ---------- CSS Styling ----------
st.markdown("""
<style>
/* Main Background */
[data-testid="stAppViewContainer"] {
    background-color: #F2F2F2;
}

/* Header Simulation */
.header-container {
    background-color: white;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #ddd;
    margin-bottom: 20px;
}

/* Secure Checkout Title */
.main-title {
    font-family: 'Arial', sans-serif;
    font-size: 24px;
    color: #122E66; /* Boots Navy */
    margin-left: 15px;
    font-weight: 400;
}

/* Stepper/Progress Bar Mockup */
.stepper {
    display: flex;
    justify-content: space-around;
    padding: 20px 0;
    margin-bottom: 20px;
    border-bottom: 1px solid #ddd;
}
.step {
    text-align: center;
    font-size: 12px;
    color: #666;
}
.step-icon {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #122E66;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 5px;
}

/* Form Card */
.card {
    background-color: white;
    padding: 30px;
    border-radius: 4px;
    border: 1px solid #ddd;
    max-width: 700px;
    margin: auto;
}

.section-label {
    font-weight: bold;
    font-size: 18px;
    color: #333;
    margin-bottom: 20px;
}

/* Button Styling (Boots White/Navy Style) */
div.stButton > button {
    background-color: white !important;
    color: #122E66 !important;
    border: 2px solid #122E66 !important;
    border-radius: 0px !important;
    font-weight: bold !important;
    padding: 10px 30px !important;
    text-transform: uppercase;
}

div.stButton > button:hover {
    background-color: #122E66 !important;
    color: white !important;
}

/* Labels and Inputs */
label {
    font-weight: 500 !important;
    color: #333 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header & Stepper ----------
st.markdown('''
<div class="header-container">
    <span style="color:#122E66; font-weight:bold; font-size:28px; font-style:italic;">START</span>
    <span class="main-title">Eligibility check Form</span>
</div>
<div class="stepper">
    <div class="step"><div class="step-icon">👤</div>
        Personal Details</div>
    <div class="step"><div class="step-icon" style="background-color:#122E66;">💼</div>
        Income & Job</div>
    <div class="step"><div class="step-icon" style="background-color:#ccc;">📊</div>
        Credit Details</div>
    <div class="step"><div class="step-icon" style="background-color:#ccc;">✅</div>
        Result</div>
</div>
''', unsafe_allow_html=True)

# ---------- Form Card ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Your details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Customer Name", placeholder="Enter full name")
    email = st.text_input("Email address", placeholder="e.g. name@example.com")
    income = st.number_input("Annual Income", min_value=0)
    debt = st.number_input("Monthly Debt", min_value=0)

with col2:
    credit_score = st.number_input("Credit Score", min_value=300, max_value=850)
    job_years = st.number_input("Years in Current Job", min_value=0)
    bankruptcies = st.number_input("Bankruptcies", min_value=0)
    credit_history = st.number_input("Years of Credit History", min_value=0)

credit_problems = st.number_input("Credit Problems", min_value=0)
tax_liens = st.number_input("Tax Liens", min_value=0)

# Submit Button
if st.button("CONFIRM DETAILS"):
    # ... (Keep your existing eligibility and email logic here) ...
    st.write("Processing...")

st.markdown('</div>', unsafe_allow_html=True)


# ---------- Eligibility Logic ----------
def check_eligibility():
    reasons = []
    dti = debt / income if income > 0 else 1

    # Conditions check
    if credit_score >= 650:
        reasons.append("✔ Good Credit Score")
    else:
        reasons.append("❌ Low Credit Score")

    if income >= 30000:
        reasons.append("✔ Sufficient Income")
    else:
        reasons.append("❌ Low Income")

    if dti <= 0.4:
        reasons.append("✔ Low Debt Ratio")
    else:
        reasons.append("❌ High Debt Ratio")

    if job_years >= 1:
        reasons.append("✔ Stable Job")
    else:
        reasons.append("❌ Job Not Stable")

    if credit_problems == 0:
        reasons.append("✔ No Credit Problems")
    else:
        reasons.append("❌ Has Credit Problems")

    if bankruptcies == 0:
        reasons.append("✔ No Bankruptcy")
    else:
        reasons.append("❌ Bankruptcy History")

    if tax_liens == 0:
        reasons.append("✔ No Tax Issues")
    else:
        reasons.append("❌ Tax Liens Found")

    if credit_history >= 5:
        reasons.append("✔ Good Credit History")
    else:
        reasons.append("❌ Short Credit History")

    # Final decision
    if all([
        credit_score >= 650,
        income >= 30000,
        dti <= 0.4,
        job_years >= 1,
        credit_problems == 0,
        bankruptcies == 0,
        tax_liens == 0,
        credit_history >= 5
    ]):
        return "Approved", reasons

    elif credit_score < 600 or dti > 0.5 or bankruptcies > 0:
        return "Rejected", reasons

    else:
        return "Conditionally Approved", reasons

# ---------- Email ----------

def send_email(to_email, subject, body):
    from_email = st.secrets["email"]["sender"]
    password = st.secrets["email"]["password"]

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        return "✅ Email Sent Successfully"

    except Exception as e:
        return f"❌ Error: {e}"
# ---------- Button ----------
if st.button("Check Eligibility"):
    result, reasons = check_eligibility()

    subject = "Loan Application Result"

    body = f"""
    <h2>Loan Result</h2>
    <p><b>Name:</b> {name}</p>
    <p><b>Status:</b> {result}</p>
    <br>
    <h3>Reasons:</h3>
    <ul>
    {''.join([f'<li>{r}</li>' for r in reasons])}
    </ul>
    """

    if result == "Approved":
        st.markdown(f'<p class="success">✅ Loan Approved</p>', unsafe_allow_html=True)
        st.success(send_email(email, subject, body))

    elif result == "Rejected":
        st.markdown(f'<p class="reject">❌ Loan Rejected</p>', unsafe_allow_html=True)
        st.success(send_email(email, subject, body))
    else:
        st.markdown(f'<p class="warning">⚠️ Conditional Approval</p>', unsafe_allow_html=True)
        st.success(send_email(email, subject, body))
    st.subheader("📊 Decision Explanation")
    for r in reasons:
        st.write(r)