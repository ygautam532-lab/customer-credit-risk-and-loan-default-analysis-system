import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

a=pd.read_csv("C:\\Users\\gautam yadav\\OneDrive\\Desktop\\loan sytem\\before cleaning and after cleaning report\\cleaned loan_prediction_report.csv")
data=pd.DataFrame(a)
st.header("INSIGHTS OF CUSTOMER CREDIT RISK AND LOAN DEFAULT SYSTEM")

st.set_page_config(page_title="Loan Dashboard", layout="wide")

# count plot
st.subheader("Loan Status Distribution")
fig, ax = plt.subplots()
sns.countplot(x="Loan Status", data=data, ax=ax)
st.pyplot(fig)

# Histogram 
st.subheader("Credit Score Distribution")
fig, ax = plt.subplots()
sns.histplot(data["Credit Score"], bins=30, kde=True, ax=ax)
st.pyplot(fig)

# boxplot
st.subheader("Income vs Loan Status")
fig, ax = plt.subplots()
sns.boxplot(x="Loan Status", y="Annual Income", data=data, ax=ax)
st.pyplot(fig)

# count plot
st.subheader("Prediction Result Distribution")
fig, ax = plt.subplots()
sns.countplot(x="Prediction", data=data, ax=ax)
st.pyplot(fig)

# plot
st.subheader("Loan Approval Rate by Home Ownership")

approval_rate = data.groupby("Home Ownership")["Loan Status"].value_counts(normalize=True).unstack()

fig, ax = plt.subplots()
approval_rate.plot(kind="bar", stacked=True, ax=ax)
st.pyplot(fig)

# scatter plot
st.subheader("Credit Score vs Loan Status")

fig, ax = plt.subplots()
sns.scatterplot(x="Credit Score", y="Annual Income", hue="Loan Status", data=data, ax=ax)
st.pyplot(fig)

# SCATTER PLOT
st.subheader("Debt vs Income Analysis")

fig, ax = plt.subplots()
sns.scatterplot(x="Annual Income", y="Monthly Debt", hue="Loan Status", data=data, ax=ax)
st.pyplot(fig)



# COUNT PLOT
st.subheader("Risk Category Distribution")

fig, ax = plt.subplots()
sns.countplot(x="Risk", data=data, ax=ax)
st.pyplot(fig)


# metrics
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Applications", len(data))
col2.metric("Approval Rate", f"{(data['Loan Status']=='Fully Paid').mean()*100:.2f}%")
col3.metric("Avg Credit Score",int(data["Credit Score"].mean()))

