/*Customer Credit Risk & Loan Default Analytics System for Banking Sector*/

-- LOAN ANALYSIS

-- 1 Loan status distribution
SELECT loan_status, COUNT(*) AS total
FROM loan_data
GROUP BY loan_status;


-- RISK SEGMENTATION

-- 1 Credit risk category
SELECT 
    customer_id,
    credit_score,
    CASE 
        WHEN credit_score >= 750 THEN 'Low Risk'
        WHEN credit_score BETWEEN 650 AND 749 THEN 'Medium Risk'
        ELSE 'High Risk'
    END AS risk_category
FROM loan_data;

-- 2 Count per risk category
SELECT 
    CASE 
        WHEN credit_score >= 750 THEN 'Low Risk'
        WHEN credit_score BETWEEN 650 AND 749 THEN 'Medium Risk'
        ELSE 'High Risk'
    END AS risk_category,
    COUNT(*) AS total_customers
FROM loan_data
GROUP BY risk_category;


-- DEFAULT VS RISKY CUSTOMERS
SELECT 
    CASE 
        WHEN credit_score >= 750 THEN 'Low Risk'
        WHEN credit_score BETWEEN 650 AND 749 THEN 'Medium Risk'
        ELSE 'High Risk'
    END AS risk_category,
    loan_status,
    COUNT(*) AS total
FROM loan_data
GROUP BY risk_category, loan_status
ORDER BY risk_category;


-- 	INCOME ANALYSIS

-- 1 Average Income by loan status
SELECT 
    loan_status,
    AVG(annual_income) AS avg_income
FROM loan_data
GROUP BY loan_status;


-- DEBT ANALYSIS

-- 1 Debt vs default
SELECT 
    loan_status,
    AVG(monthly_debt) AS avg_debt
FROM loan_data
GROUP BY loan_status;


-- CREDIT SCORE IMPACT
SELECT 
    loan_status,
    AVG(credit_score) AS avg_credit_score
FROM loan_data
GROUP BY loan_status;


-- LOAN APPROVAL PROBABILITY
SELECT 
    customer_id,
    credit_score,
    annual_income,
    monthly_debt,
    CASE 
        WHEN credit_score > 700 AND annual_income > 50000 THEN 'High Chance'
        WHEN credit_score BETWEEN 600 AND 700 THEN 'Medium Chance'
        ELSE 'Low Chance'
    END AS approval_probability
FROM loan_data;


-- TOP FECTORS CAUSING DEFAULT
use loan_analysis;
SELECT 
    purpose,
    COUNT(*) AS total_defaults
FROM loan_data
WHERE loan_status = 'Charged Off'
GROUP BY purpose
ORDER BY total_defaults DESC;


-- CREDIT UTILIZATION
SELECT 
    customer_id,
    current_credit_balance,
    maximum_open_credit,
    (current_credit_balance * 100.0 / maximum_open_credit) AS credit_utilization
FROM loan_data;


-- FINAL RISK FLAG
SELECT 
    customer_id,
    credit_score,
    annual_income,
    monthly_debt,
    CASE 
        WHEN credit_score < 600 OR monthly_debt > 3000 THEN 'High Risk'
        WHEN credit_score BETWEEN 600 AND 700 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS final_risk
FROM loan_data;

-- THANK YOU

