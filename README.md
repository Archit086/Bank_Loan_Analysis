# Bank Loan Report Dashboard in Tableau

This project presents a comprehensive **Bank Loan Report** built entirely using **Tableau**. It provides a multi-dashboard analytical view of a bank’s lending activities, designed to monitor KPIs, identify trends, and assess the quality of the loan portfolio through interactive visualizations.

---

## Dashboards Overview
![image](https://github.com/user-attachments/assets/55822c9e-8cc7-493b-abdd-51a759aa272d)
<img width="1060" height="534" alt="Screenshot 2025-07-16 173943" src="https://github.com/user-attachments/assets/1e582a6d-e800-43d8-94a8-caa750d1e6a0" />
<img width="1060" height="537" alt="Screenshot 2025-07-16 174038" src="https://github.com/user-attachments/assets/201eaecc-dbe8-451a-80b9-8a8d39750155" />
<img width="1032" height="532" alt="Screenshot 2025-07-16 174112" src="https://github.com/user-attachments/assets/fe53a947-b837-4a3b-90b6-b5787c069094" />





###  **Dashboard 1: Summary**
**Platform:** Tableau  
**Focus:** High-level KPIs to evaluate lending performance and portfolio health.

####  Key Performance Indicators (KPIs):
- **Total Loan Applications**
  - Tracks overall, Month-to-Date (MTD), and Month-over-Month (MoM) application counts.
- **Total Funded Amount**
  - Measures total disbursed loans with MTD and MoM changes.
- **Total Amount Received**
  - Represents repayments received from borrowers (MTD + MoM).
- **Average Interest Rate**
  - Calculates average across all loans with monthly comparison.
- **Average Debt-to-Income (DTI) Ratio**
  - Evaluates borrower financial condition (overall + monthly).

---

#### ✅ Good Loan vs Bad Loan Analysis:
**Criteria:**
- **Good Loans** → `Fully Paid` or `Current`
- **Bad Loans** → `Charged Off`

**Metrics Include:**
- Application counts and percentages
- Total Funded Amount
- Total Received Amount

---

#### Loan Status Grid View:
A tabular visualization in Tableau displaying per-loan-status:
- Applications
- Funded Amount
- Received Amount
- MTD metrics
- Avg. Interest Rate & DTI

---

### **Dashboard 2: Overview**
**Platform:** Tableau  
**Focus:** Exploratory insights via visual analytics.

#### Visualizations:

1. **Monthly Trends**
   - Metrics: Applications, Funded Amount, Received Amount
   - Based on `Issue Date`

2. **Regional Analysis by State**
   - State-wise distribution of loan activities

3. **Loan Term Analysis**
   - Distribution across 36-month and 60-month terms

4. **Employee Length Analysis**
   - Segmentation by borrower job duration

5. **Loan Purpose Breakdown**
   - Shows top reasons for loan applications (e.g., debt consolidation)

6. **Home Ownership Analysis**
   - Lending metrics segmented by ownership status (own, rent, mortgage)

---

###  **Dashboard 3: Details**
**Platform:** Tableau  
**Focus:** Drill-down view of all loan records and borrower details.

Includes:
- Full loan dataset with filtering
- Per-borrower insights
- Metrics: Loan Amount, Interest Rate, DTI, Purpose, Repayment, and Status
---


#### Filters Used in the Dashboard

These filters allow users to refine the loan data dynamically:

- **Good vs Bad Loan**  
  Filters loans based on their repayment performance.  
  **Options:** Good, Bad, All

- **Purpose**  
  Filters data based on loan purpose.  
  **Examples:** Debt consolidation, small business, credit card, home improvement

- **Grade**  
  Filters data based on loan credit grades (A to G)

- **Verification Status**  
  Filters based on whether the borrower’s income was verified or not

---

#### Parameters Used in the Dashboard

- **Select Month (Parameter)**  
  This parameter allows the user to choose a specific month (e.g., December).  
  It dynamically updates all Month-to-Date (MTD) and Month-over-Month (MoM) KPIs.

- **Select Measure (Parameter)**
  - Total Amount Received  
  - Total Funded Amount  
  - Total Loan Applications
  Allows users to select the metric shown in the visualizations (e.g., map, bar charts).


## Objective

- Provide decision-makers with a complete view of bank lending performance.
- Help identify borrower behavior trends and regional patterns.
- Track key financial metrics like repayments, interest, and DTI in real time.
