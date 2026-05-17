import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA = Path('data/raw/sales_analysis_data.csv')
IMG = Path('images')
REPORT = Path('reports/sales_analysis_summary.md')


def main():
    IMG.mkdir(exist_ok=True)
    df = pd.read_csv(DATA, parse_dates=['order_date'])
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    df['profit_estimate'] = np.round(df['revenue'] * 0.22 - df['marketing_spend'] * 0.08, 2)

    monthly = df.groupby('month', as_index=False)['revenue'].sum()
    category = df.groupby('category', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
    region = df.groupby('region', as_index=False)['profit_estimate'].sum().sort_values('profit_estimate', ascending=False)

    plt.figure(figsize=(10,5))
    plt.plot(monthly['month'], monthly['revenue'], marker='o')
    plt.xticks(rotation=45)
    plt.title('Monthly Revenue Trend')
    plt.tight_layout()
    plt.savefig(IMG/'monthly_revenue.png', dpi=160)
    plt.close()

    plt.figure(figsize=(8,5))
    plt.bar(category['category'], category['revenue'])
    plt.title('Revenue by Category')
    plt.tight_layout()
    plt.savefig(IMG/'category_revenue.png', dpi=160)
    plt.close()

    plt.figure(figsize=(8,5))
    plt.bar(region['region'], region['profit_estimate'])
    plt.title('Estimated Profit by Region')
    plt.tight_layout()
    plt.savefig(IMG/'region_profit.png', dpi=160)
    plt.close()

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(f'''# Sales Analysis Summary\n\n## Key Metrics\n\n- Total revenue: ₹{df['revenue'].sum():,.0f}\n- Average order revenue: ₹{df['revenue'].mean():,.0f}\n- Estimated profit: ₹{df['profit_estimate'].sum():,.0f}\n- Best category: {category.iloc[0]['category']}\n- Best region by estimated profit: {region.iloc[0]['region']}\n\n## Charts Created\n\n- `images/monthly_revenue.png`\n- `images/category_revenue.png`\n- `images/region_profit.png`\n''')
    print('Analysis complete. See reports/sales_analysis_summary.md and images/.')


if __name__ == '__main__':
    main()
