-- =========================================================================
-- BANK LOAN PORTFOLIO ANALYSIS QUERY SUITE
-- Dialects Covered: Standard ANSI SQL (SQLite, PostgreSQL, MS SQL Server)
-- Purpose: Audit loan performance, calculate key performance indicators (KPIs),
--          assess credit risk, and segment good vs bad loans.
-- Target Dataset Size: 5,000+ records (7,500 active records in bank_loans_5k.csv)
-- =========================================================================

-- -------------------------------------------------------------------------
-- 1. DATABASE SCHEMA & DDL SETUP
-- -------------------------------------------------------------------------

-- Drop table if exists to ensure clean run
DROP TABLE IF EXISTS loans;

CREATE TABLE loans (
    id INTEGER PRIMARY KEY,
    address_state VARCHAR(2) NOT NULL,
    application_type VARCHAR(20),
    emp_length VARCHAR(20),
    emp_title VARCHAR(150),
    grade CHAR(1) NOT NULL,
    home_ownership VARCHAR(20),
    issue_date DATE NOT NULL, -- Stored as YYYY-MM-DD
    last_credit_pull_date DATE,
    last_payment_date DATE,
    loan_status VARCHAR(25) NOT NULL, -- e.g., 'Fully Paid', 'Current', 'Charged Off'
    next_payment_date DATE,
    member_id INTEGER,
    purpose VARCHAR(50),
    sub_grade VARCHAR(3),
    term INTEGER, -- Stored as integer months (36 or 60)
    verification_status VARCHAR(25),
    annual_income DECIMAL(15, 2),
    dti DECIMAL(5, 4), -- Debt-to-Income ratio (e.g. 0.1527)
    installment DECIMAL(10, 2),
    int_rate DECIMAL(5, 4), -- Interest rate (e.g. 0.1250)
    loan_amount DECIMAL(15, 2),
    total_acc INTEGER,
    total_payment DECIMAL(15, 2) -- Total repayment received by the bank
);


-- -------------------------------------------------------------------------
-- 2. HIGH-LEVEL EXECUTIVE CORE KPIs
-- -------------------------------------------------------------------------

-- KPI A: Total Loan Applications
SELECT COUNT(id) AS total_loan_applications
FROM loans;

-- KPI B: Total Funded Amount (Disbursed capital)
SELECT SUM(loan_amount) AS total_funded_amount
FROM loans;

-- KPI C: Total Amount Received (Repayments + Interest collected)
SELECT SUM(total_payment) AS total_amount_received
FROM loans;

-- KPI D: Average Interest Rate
SELECT ROUND(AVG(int_rate) * 100, 2) AS average_interest_rate_pct
FROM loans;

-- KPI E: Average Debt-to-Income (DTI) Ratio
SELECT ROUND(AVG(dti) * 100, 2) AS average_dti_pct
FROM loans;


-- -------------------------------------------------------------------------
-- 3. MONTH-OVER-MONTH (MoM) & MONTH-TO-DATE (MTD) ANALYTICS
-- NOTE: For SQLite, month extraction uses strftime('%m', issue_date). 
-- For SQL Server, use MONTH(issue_date). For PostgreSQL, use EXTRACT(MONTH FROM issue_date).
-- We assume the "current month" is December (Month 12) for historical data auditing.
-- -------------------------------------------------------------------------

-- MTD KPI: Total Loan Applications (December 2021)
-- SQLite:
SELECT COUNT(id) AS mtd_loan_applications
FROM loans
WHERE strftime('%m', issue_date) = '12';

-- [PostgreSQL / MS SQL Server Alternative]:
-- SELECT COUNT(id) AS mtd_loan_applications FROM loans WHERE EXTRACT(MONTH FROM issue_date) = 12;
-- SELECT COUNT(id) AS mtd_loan_applications FROM loans WHERE MONTH(issue_date) = 12;

-- MTD KPI: Total Funded Amount (December 2021)
SELECT SUM(loan_amount) AS mtd_funded_amount
FROM loans
WHERE strftime('%m', issue_date) = '12';

-- MTD KPI: Total Received Amount (December 2021)
SELECT SUM(total_payment) AS mtd_amount_received
FROM loans
WHERE strftime('%m', issue_date) = '12';

-- Month-over-Month (MoM) Growth Calculation Example (November vs. December)
-- This query computes November (Month 11) vs December (Month 12) growth in funding
SELECT 
    nov.funded_amount AS november_funding,
    dec.funded_amount AS december_funding,
    ROUND(((dec.funded_amount - nov.funded_amount) / nov.funded_amount) * 100, 2) AS mom_funding_growth_pct
FROM 
    (SELECT SUM(loan_amount) AS funded_amount FROM loans WHERE strftime('%m', issue_date) = '11') nov,
    (SELECT SUM(loan_amount) AS funded_amount FROM loans WHERE strftime('%m', issue_date) = '12') dec;


-- -------------------------------------------------------------------------
-- 4. GOOD LOAN VS. BAD LOAN ANALYSIS (CREDIT QUALITY AUDITING)
-- Good Loans: Fully Paid or Current
-- Bad Loans: Charged Off (Defaulted)
-- -------------------------------------------------------------------------

-- Good Loan Performance Metrics
SELECT
    COUNT(id) AS good_loan_applications,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(id) FROM loans), 2) AS good_loan_percentage,
    SUM(loan_amount) AS good_loan_funded_amount,
    SUM(total_payment) AS good_loan_received_amount
FROM loans
WHERE loan_status IN ('Fully Paid', 'Current');

-- Bad Loan Performance Metrics (Default Portfolio)
SELECT
    COUNT(id) AS bad_loan_applications,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(id) FROM loans), 2) AS bad_loan_percentage,
    SUM(loan_amount) AS bad_loan_funded_amount,
    SUM(total_payment) AS bad_loan_received_amount
FROM loans
WHERE loan_status = 'Charged Off';


-- -------------------------------------------------------------------------
-- 5. LOAN STATUS GRID SUMMARY
-- -------------------------------------------------------------------------
SELECT
    loan_status,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_amount_received,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct
FROM loans
GROUP BY loan_status
ORDER BY total_applications DESC;


-- -------------------------------------------------------------------------
-- 6. RISK COHORT SEGMENTATION & REGIONAL ANALYSIS
-- -------------------------------------------------------------------------

-- Cohort A: Risk Segmentation by Credit Grade
SELECT
    grade,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loans
GROUP BY grade
ORDER BY grade;

-- Cohort B: Risk Segmentation by Income Bracket
SELECT
    CASE 
        WHEN annual_income < 40000 THEN 'Low (<$40k)'
        WHEN annual_income >= 40000 AND annual_income < 80000 THEN 'Medium ($40k-$80k)'
        WHEN annual_income >= 80000 AND annual_income < 120000 THEN 'High ($80k-$120k)'
        ELSE 'Very High (>$120k)'
    END AS income_bracket,
    COUNT(id) AS total_applications,
    ROUND(SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loans
GROUP BY income_bracket
ORDER BY default_rate_pct DESC;

-- Cohort C: Risk Segmentation by Home Ownership
SELECT
    home_ownership,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loans
GROUP BY home_ownership
ORDER BY default_rate_pct DESC;

-- Cohort D: Risk Segmentation by Loan Term
SELECT
    term AS term_months,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loans
GROUP BY term
ORDER BY term;

-- Cohort E: Risk Segmentation by Loan Purpose
SELECT
    purpose,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loans
GROUP BY purpose
ORDER BY total_applications DESC
LIMIT 10;

-- Region: State-by-State Lending Volume and Default Rates
SELECT
    address_state AS state,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_payment_received,
    ROUND(SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loans
GROUP BY address_state
ORDER BY total_applications DESC
LIMIT 10;
