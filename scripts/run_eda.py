import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda_analysis():
    print("Running exploratory data analysis...")
    
    # Setup aesthetic themes
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 12
    
    # Resolve directories dynamically
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    plots_dir = os.path.join(project_root, "reports", "plots")
    os.makedirs(plots_dir, exist_ok=True)
    
    # Load dataset
    csv_path = os.path.join(project_root, "data", "bank_loans_5k.csv")
    df = pd.read_csv(csv_path)
    print(f"Loaded {df.shape[0]} rows for EDA plotting.")
    
    # 1. Good vs. Bad Loan Indicator
    df['loan_category'] = df['loan_status'].apply(lambda x: 'Bad Loan' if x == 'Charged Off' else 'Good Loan')
    category_counts = df['loan_category'].value_counts()
    category_pct = df['loan_category'].value_counts(normalize=True) * 100
    
    # Plot Good vs. Bad Loan Distribution
    plt.figure(figsize=(8, 6))
    colors = ['#1f77b4', '#d62728'] # Classic Slate Blue & Crimson Red
    sns.barplot(x=category_counts.index, y=category_counts.values, palette=colors, hue=category_counts.index, legend=False)
    plt.title('Distribution of Good vs. Bad Loans (7.5K Sample)', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Loans')
    plt.xlabel('Loan Portfolio Class')
    for i, val in enumerate(category_counts.values):
        plt.text(i, val + 100, f"{val} ({category_pct.values[i]:.1f}%)", ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'good_vs_bad_distribution.png'), dpi=300)
    plt.close()
    print("Saved good_vs_bad_distribution.png")
    
    # Helper for default rates
    def get_default_rate(df, group_col):
        grouped = df.groupby(group_col)['loan_category'].value_counts(normalize=True).unstack().fillna(0) * 100
        if 'Bad Loan' not in grouped.columns:
            grouped['Bad Loan'] = 0.0
        return grouped.sort_values(by='Bad Loan', ascending=False)
        
    # 2. Credit Grade
    grade_defaults = get_default_rate(df, 'grade')
    plt.figure(figsize=(10, 6))
    grade_sorted = grade_defaults.sort_index()
    sns.barplot(x=grade_sorted.index, y=grade_sorted['Bad Loan'], palette='Reds', hue=grade_sorted.index, legend=False)
    plt.title('Default Rate (%) by Borrower Credit Grade', fontsize=14, fontweight='bold')
    plt.ylabel('Default Rate (%)')
    plt.xlabel('Credit Grade')
    for i, val in enumerate(grade_sorted['Bad Loan'].values):
        plt.text(i, val + 0.5, f"{val:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'default_rate_by_grade.png'), dpi=300)
    plt.close()
    print("Saved default_rate_by_grade.png")
    
    # 3. Income Groups
    def categorize_income(income):
        if income < 40000:
            return 'Low (<$40k)'
        elif income < 80000:
            return 'Medium ($40k-$80k)'
        elif income < 120000:
            return 'High ($80k-$120k)'
        else:
            return 'Very High (>$120k)'
            
    df['income_group'] = df['annual_income'].apply(categorize_income)
    income_defaults = get_default_rate(df, 'income_group')
    plt.figure(figsize=(10, 6))
    income_order = ['Low (<$40k)', 'Medium ($40k-$80k)', 'High ($80k-$120k)', 'Very High (>$120k)']
    income_plot_data = income_defaults.loc[income_order]
    sns.barplot(x=income_plot_data.index, y=income_plot_data['Bad Loan'], palette='YlOrRd', hue=income_plot_data.index, legend=False)
    plt.title('Default Rate (%) by Borrower Income Group', fontsize=14, fontweight='bold')
    plt.ylabel('Default Rate (%)')
    plt.xlabel('Annual Income Group')
    for i, val in enumerate(income_plot_data['Bad Loan'].values):
        plt.text(i, val + 0.2, f"{val:.1f}%", ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'default_rate_by_income.png'), dpi=300)
    plt.close()
    print("Saved default_rate_by_income.png")
    
    # 4. Correlation Heatmap
    numeric_cols = ['loan_amount', 'int_rate', 'dti', 'annual_income', 'total_payment']
    corr_matrix = df[numeric_cols].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Credit Risk Indicators', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'correlation_matrix.png'), dpi=300)
    plt.close()
    print("Saved correlation_matrix.png")
    
    # Clean up generation helper script from folder to keep workspace clean
    print("EDA execution completed successfully. Charts exported!")

if __name__ == "__main__":
    run_eda_analysis()
