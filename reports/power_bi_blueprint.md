# Power BI Dashboard Blueprint: Bank Loan Analysis

This blueprint provides a comprehensive guide to building a high-fidelity, interactive **Bank Loan Analysis Dashboard** in **Power BI Desktop**, designed to match your resume's specifications. 

Our data source is the clean, stratify-sampled dataset of **7,500 records** ([bank_loans_5k.csv](file:///E:/Projects/Bank%20loan%20analysis/Bank_Loan_Analysis/bank_loans_5k.csv)) created by our data engineering pipeline, ensuring complete consistency with your Python and SQL files.

---

## 1. Data Connection & Power Query Transformation

### Step A: Load the Dataset
1. Open **Power BI Desktop**.
2. Go to **Home** > **Get Data** > **Text/CSV**.
3. Choose the [bank_loans_5k.csv](file:///E:/Projects/Bank%20loan%20analysis/Bank_Loan_Analysis/bank_loans_5k.csv) file.
4. Click **Transform Data** to open the **Power Query Editor**.

### Step B: Standardize Data Types
Ensure that Power Query assigns the correct data types to your fields:
* **id**, **member_id**: `Whole Number`
* **address_state**, **grade**, **sub_grade**, **home_ownership**, **purpose**, **verification_status**, **loan_status**: `Text`
* **term**: `Whole Number` (represents length in months, 36 or 60)
* **annual_income**, **installment**, **loan_amount**, **total_payment**: `Fixed Decimal Number` (Currency)
* **int_rate**, **dti**: `Decimal Number` (Percentage representation)
* **issue_date**, **last_credit_pull_date**, **last_payment_date**, **next_payment_date**: `Date` (Format: `YYYY-MM-DD`)

*Tip: If DTI or Interest Rate are in decimals (e.g. `0.1527`), highlight the columns, go to the **Transform** ribbon, and change the data type to **Percentage** so they display natively as `15.27%` in your reports.*

Click **Close & Apply** to load the data model.

---

## 2. Dynamic DAX Measures

Create a dedicated table for your measures: Go to **Home** > **Enter Data**, name the table `_Measures Table`, and click **Load**. Create the following measures within this table:

### A. Executive Core KPIs
```dax
-- Total Loan Applications
Total Applications = COUNT(loans[id])

-- Total Funded Amount (Total capital disbursed)
Total Funded Amount = SUM(loans[loan_amount])

-- Total Amount Received (Total repayments + interest collected)
Total Received Amount = SUM(loans[total_payment])

-- Average Interest Rate
Average Interest Rate = AVERAGE(loans[int_rate])

-- Average Debt-to-Income (DTI) Ratio
Average DTI = AVERAGE(loans[dti])
```

### B. Month-to-Date (MTD) & Month-over-Month (MoM) Analytics
*Note: These measures dynamically compute MTD metrics. For historical consistency with the dataset's final audited month (December 2021), they utilize filter contexts.*
```dax
-- MTD Applications (Current Month - December)
MTD Applications = CALCULATE([Total Applications], MONTH(loans[issue_date]) = 12)

-- MTD Funded Amount
MTD Funded Amount = CALCULATE([Total Funded Amount], MONTH(loans[issue_date]) = 12)

-- MTD Amount Received
MTD Received Amount = CALCULATE([Total Received Amount], MONTH(loans[issue_date]) = 12)

-- Previous Month Applications (November)
PM Applications = CALCULATE([Total Applications], MONTH(loans[issue_date]) = 11)

-- Month-over-Month Application Growth Rate
MoM Application Growth = DIVIDE([MTD Applications] - [PM Applications], [PM Applications], 0)
```

### C. Good vs. Bad Loan Segmentation (Portfolio Quality)
```dax
-- GOOD LOANS (Status is Fully Paid or Current)
Good Loan Applications = CALCULATE([Total Applications], FILTER(loans, loans[loan_status] = "Fully Paid" || loans[loan_status] = "Current"))
Good Loan % = DIVIDE([Good Loan Applications], [Total Applications], 0)
Good Loan Funded Amount = CALCULATE([Total Funded Amount], FILTER(loans, loans[loan_status] = "Fully Paid" || loans[loan_status] = "Current"))
Good Loan Received Amount = CALCULATE([Total Received Amount], FILTER(loans, loans[loan_status] = "Fully Paid" || loans[loan_status] = "Current"))

-- BAD LOANS (Status is Charged Off / Defaulted)
Bad Loan Applications = CALCULATE([Total Applications], FILTER(loans, loans[loan_status] = "Charged Off"))
Bad Loan % = DIVIDE([Bad Loan Applications], [Total Applications], 0)
Bad Loan Funded Amount = CALCULATE([Total Funded Amount], FILTER(loans, loans[loan_status] = "Charged Off"))
Bad Loan Received Amount = CALCULATE([Total Received Amount], FILTER(loans, loans[loan_status] = "Charged Off"))

-- Portfolio Default Rate (Matches Bad Loan %)
Default Rate = [Bad Loan %]
```

---

## 3. UI Visual Canvas Layout Blueprint

To make your dashboard feel extremely premium and professional, follow this 3-Page Canvas layout:

### Color Palette Theme:
* **Background:** Light Gray (`#F3F4F6`) or Slate Dark (`#0E1117`)
* **Primary Deep Navy:** `#0F172A` (For headers, card labels)
* **Accent Slate Gray:** `#475569` (For descriptive texts, grid lines)
* **Good Loan Green:** `#10B981` (For Fully Paid numbers, positive indicators)
* **Default Danger Red:** `#EF4444` (For Charged Off numbers, risk indicators)

---

### PAGE 1: Summary Dashboard (Portfolio Overview & Quality)
*Focus: Executive summary metrics and credit portfolio health.*

1. **Executive KPI Banner (5 Cards across the top):**
   * **Card 1 (Applications):** Title: `Total Loan Applications`, Field: `[Total Applications]`. Add a small secondary card underneath displaying: `MTD: [MTD Applications]`.
   * **Card 2 (Funding):** Title: `Total Funded Amount`, Field: `[Total Funded Amount]` (Format as Currency `$M`). Underneath: `MTD: [MTD Funded Amount]`.
   * **Card 3 (Received):** Title: `Total Amount Received`, Field: `[Total Received Amount]`. Underneath: `MTD: [MTD Received Amount]`.
   * **Card 4 (Interest Rate):** Title: `Avg Interest Rate`, Field: `[Average Interest Rate]` (Format as % `12.05%`).
   * **Card 5 (DTI):** Title: `Avg DTI`, Field: `[Average DTI]` (Format as % `13.24%`).

2. **Good vs. Bad Loan Summary Table (Mid-Page Left):**
   * **Visual type:** Matrix or Table.
   * **Fields:** 
     * Row: `loan_category` (Good Loan / Bad Loan)
     * Values: `Applications`, `Application %`, `Funded Amount`, `Received Amount`.
   * *Style:* Add conditional formatting (Data bars) to visually emphasize the ratio.

3. **Loan Status Grid View (Mid-Page Right):**
   * **Visual type:** Table.
   * **Fields:** `loan_status`, `Total Applications`, `Total Funded Amount`, `Total Received Amount`, `Average Interest Rate`, `Average DTI`.

---

### PAGE 2: Overview Dashboard (Exploratory Analytics)
*Focus: Trends, geography, demographic, and cohort risk analysis.*

1. **Monthly Trends (Top Left):**
   * **Visual type:** Area / Line Chart.
   * **Fields:** X-Axis: `issue_date` (Grouped by Month), Y-Axis: `[Total Applications]` and `[Total Funded Amount]`.
   * *Insight:* Shows seasonality in loan dispersals.

2. **Regional Map (Top Right):**
   * **Visual type:** Filled Map (or Bubble Map).
   * **Fields:** Location: `address_state`, Bubble Size: `[Total Funded Amount]`, Tooltips: `[Total Applications]`, `[Default Rate]`.

3. **Loan Term Analysis (Bottom Left):**
   * **Visual type:** Donut Chart.
   * **Fields:** Legend: `term` (36 / 60 Months), Values: `[Total Applications]`.
   * *Style:* Add data labels showing percentages (`78%` for 36 months, `22%` for 60 months).

4. **Home Ownership Breakdown (Bottom Middle):**
   * **Visual type:** Stacked Bar Chart (Horizontal).
   * **Fields:** Y-Axis: `home_ownership`, X-Axis: `[Total Applications]`.
   * *Insight:* Details how MORTGAGE, RENT, and OWN affect borrowing frequency.

5. **Loan Purpose Breakdown (Bottom Right):**
   * **Visual type:** Treemap.
   * **Fields:** Category: `purpose`, Values: `[Total Applications]`.
   * *Insight:* Highlights Debt Consolidation and Credit Cards as top loan drivers.

---

### PAGE 3: Details Dashboard (Drill-Down Audit Logs)
*Focus: Granular borrower level auditing and advanced filtering.*

1. **Top Slicers Bar (Filters):**
   * Place 5 vertical/dropdown slicers along the top panel for rapid filtering:
     * `grade` (A to G)
     * `home_ownership`
     * `purpose`
     * `verification_status`
     * `loan_status`

2. **Master Auditing Grid (Center Canvas):**
   * **Visual type:** Table.
   * **Fields:** `id`, `address_state`, `emp_length`, `grade`, `home_ownership`, `purpose`, `verification_status`, `annual_income`, `dti`, `int_rate`, `loan_amount`, `total_payment`, `loan_status`.
   * *Style:* Enable zebra striping (alternate row colors) and set auto-fit column widths. Enable a "Total" row at the bottom of the table.
