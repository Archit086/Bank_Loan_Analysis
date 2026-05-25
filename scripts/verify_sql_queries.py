import sqlite3
import pandas as pd
import os

def verify_queries():
    print("Testing SQL queries against 'bank_loans.db' SQLite database...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, "data", "bank_loans.db")
    
    conn = sqlite3.connect(db_path)
    
    # 1. Total Metrics Verification
    print("\n--- EXECUTIVE SUMMARY KPIs ---")
    kpi_query = """
    SELECT 
        COUNT(id) AS total_applications,
        SUM(loan_amount) AS total_funded_amount,
        SUM(total_payment) AS total_received_amount,
        ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
        ROUND(AVG(dti) * 100, 2) AS avg_dti_pct
    FROM loans;
    """
    df_kpi = pd.read_sql_query(kpi_query, conn)
    print(df_kpi.to_string(index=False))
    
    # 2. Good vs Bad Loan Split Verification
    print("\n--- GOOD LOAN VS BAD LOAN PERFORMANCE ---")
    quality_query = """
    SELECT
        CASE WHEN loan_status IN ('Fully Paid', 'Current') THEN 'Good Loan' ELSE 'Bad Loan' END AS loan_category,
        COUNT(id) AS applications,
        ROUND(COUNT(id) * 100.0 / (SELECT COUNT(id) FROM loans), 2) AS percentage,
        SUM(loan_amount) AS funded_amount,
        SUM(total_payment) AS received_amount
    FROM loans
    GROUP BY loan_category;
    """
    df_quality = pd.read_sql_query(quality_query, conn)
    print(df_quality.to_string(index=False))
    
    # 3. Status Grid Summary
    print("\n--- LOAN STATUS GRID SUMMARY ---")
    status_query = """
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
    """
    df_status = pd.read_sql_query(status_query, conn)
    print(df_status.to_string(index=False))

    # 4. Risk Cohort A: Default Rate by Grade
    print("\n--- RISK SEGMENTATION BY CREDIT GRADE ---")
    grade_query = """
    SELECT
        grade,
        COUNT(id) AS total_applications,
        SUM(loan_amount) AS total_funded_amount,
        ROUND(SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
    FROM loans
    GROUP BY grade
    ORDER BY grade;
    """
    df_grade = pd.read_sql_query(grade_query, conn)
    print(df_grade.to_string(index=False))

    # 5. Risk Cohort B: Default Rate by Income Bracket
    print("\n--- RISK SEGMENTATION BY INCOME BRACKET ---")
    income_query = """
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
    """
    df_income = pd.read_sql_query(income_query, conn)
    print(df_income.to_string(index=False))
    
    conn.close()
    print("\nVerification completed successfully! All SQL queries parsed and executed flawlessly.")

if __name__ == "__main__":
    verify_queries()
