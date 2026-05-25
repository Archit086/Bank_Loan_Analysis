import os
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split

def run_pipeline():
    print("Starting data pipeline execution...")
    
    # 1. Load the original dataset
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    csv_path = os.path.join(project_root, "data", "financial_loan.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Error: {csv_path} not found!")
        
    print(f"Loading raw dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Successfully loaded raw data with {df.shape[0]} rows and {df.shape[1]} columns.")
    
    # 2. Data Cleaning & Standardization
    print("Standardizing and cleaning data...")
    # Strip any whitespace from string columns
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()
        
    # Standardize empty values in string columns
    df = df.replace(to_replace=["nan", "NAN", "None", "NONE", ""], value=None)
    
    # Standardize columns: Term (e.g., "36 months", "60 months")
    df['term'] = df['term'].str.replace(' months', '', case=False).str.strip()
    df['term'] = pd.to_numeric(df['term'], errors='coerce')
    
    # Parse dates: issue_date is DD-MM-YYYY
    # We will convert it to ISO format (YYYY-MM-DD) for standard SQLite compatibility
    print("Parsing date columns...")
    date_cols = ['issue_date', 'last_credit_pull_date', 'last_payment_date', 'next_payment_date']
    for col in date_cols:
        if col in df.columns:
            # Parse DD-MM-YYYY and handle exceptions
            df[col] = pd.to_datetime(df[col], format='%d-%m-%Y', errors='coerce')
            # Format as YYYY-MM-DD string for SQLite
            df[col] = df[col].dt.strftime('%Y-%m-%d')

    # Convert interest rate and DTI values to standard float percentage representations if needed,
    # but the columns already contain decimals like 0.1527 for 15.27% or 0.2088 for 20.88% DTI.
    # We will keep them as decimal floats for standard statistical calculations, but make sure they are numeric
    df['int_rate'] = pd.to_numeric(df['int_rate'], errors='coerce')
    df['dti'] = pd.to_numeric(df['dti'], errors='coerce')
    df['annual_income'] = pd.to_numeric(df['annual_income'], errors='coerce')
    df['loan_amount'] = pd.to_numeric(df['loan_amount'], errors='coerce')
    df['total_payment'] = pd.to_numeric(df['total_payment'], errors='coerce')
    df['installment'] = pd.to_numeric(df['installment'], errors='coerce')

    # 3. Stratified Sampling (7,500 records)
    print("Performing stratified sampling on 'loan_status' to extract exactly 7,500 records...")
    # Fill any null values in loan_status to prevent sampling errors
    df['loan_status'] = df['loan_status'].fillna('Fully Paid')
    
    # We want exactly 7,500 samples. Let's calculate fraction
    fraction = 7500 / len(df)
    
    # Use train_test_split to perform stratified sampling
    df_sample, _ = train_test_split(
        df,
        train_size=fraction,
        stratify=df['loan_status'],
        random_state=42
    )
    
    # Reset index of the sample
    df_sample = df_sample.reset_index(drop=True)
    print(f"Sampled {df_sample.shape[0]} records successfully.")
    
    # Verify the loan status distribution is preserved
    orig_dist = df['loan_status'].value_counts(normalize=True)
    samp_dist = df_sample['loan_status'].value_counts(normalize=True)
    print("Original loan status distribution:\n", orig_dist)
    print("Sampled loan status distribution:\n", samp_dist)
    
    # 4. Save to bank_loans_5k.csv
    out_csv = os.path.join(project_root, "data", "bank_loans_5k.csv")
    print(f"Saving sample dataset to {out_csv}...")
    df_sample.to_csv(out_csv, index=False)
    print(f"Saved {out_csv} successfully.")
    
    # 5. Set up SQLite database
    db_path = os.path.join(project_root, "data", "bank_loans.db")
    if os.path.exists(db_path):
        print(f"Removing existing database at {db_path} to recreate it...")
        os.remove(db_path)
        
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the table schema explicitly to match standard SQL types
    print("Creating 'loans' table in SQLite...")
    create_table_sql = """
    CREATE TABLE loans (
        id INTEGER PRIMARY KEY,
        address_state TEXT,
        application_type TEXT,
        emp_length TEXT,
        emp_title TEXT,
        grade TEXT,
        home_ownership TEXT,
        issue_date TEXT, -- YYYY-MM-DD format
        last_credit_pull_date TEXT,
        last_payment_date TEXT,
        loan_status TEXT,
        next_payment_date TEXT,
        member_id INTEGER,
        purpose TEXT,
        sub_grade TEXT,
        term INTEGER, -- Number of months (36 or 60)
        verification_status TEXT,
        annual_income REAL,
        dti REAL,
        installment REAL,
        int_rate REAL,
        loan_amount REAL,
        total_acc INTEGER,
        total_payment REAL
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()
    
    # Load pandas DataFrame directly into SQLite database
    print("Loading sampled dataset into database table 'loans'...")
    df_sample.to_sql('loans', conn, if_exists='append', index=False)
    conn.commit()
    
    # Verify database loading
    cursor.execute("SELECT COUNT(*) FROM loans;")
    row_count = cursor.fetchone()[0]
    print(f"Verification successful: The 'loans' table has {row_count} rows loaded.")
    
    conn.close()
    print("Data pipeline executed successfully!")

if __name__ == "__main__":
    run_pipeline()
