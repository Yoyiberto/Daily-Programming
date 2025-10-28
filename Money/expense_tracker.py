import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Exchange rates (you can update these manually)
EXCHANGE_RATES = {
    'EUR': 1.09,  # EUR to USD
    'USD': 1.00,  # USD to USD (base)
    'PEN': 0.27   # PEN to USD
}

class ExpenseTracker:
    def __init__(self):
        self.transactions_eur = None
        self.transactions_usd = None
        self.transactions_pen = None
        self.vendor_categories = None
        self.load_data()
    
    def load_data(self):
        """Load all CSV files"""
        try:
            self.transactions_eur = pd.read_csv('transactions_eur.csv')
            self.transactions_eur['currency'] = 'EUR'
            self.transactions_eur['account'] = 'EUR Account'
            
            self.transactions_usd = pd.read_csv('transactions_usd.csv')
            self.transactions_usd['currency'] = 'USD'
            self.transactions_usd['account'] = 'USD Account'
            
            self.transactions_pen = pd.read_csv('transactions_pen.csv')
            self.transactions_pen['currency'] = 'PEN'
            self.transactions_pen['account'] = 'PEN Account'
            
            self.vendor_categories = pd.read_csv('vendor_categories.csv')
            
            print("✓ Data loaded successfully!")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def categorize_transactions(self, df):
        """Add category column based on vendor"""
        df = df.copy()
        df['category'] = df['vendor'].map(
            self.vendor_categories.set_index('vendor')['category']
        )
        df['category'].fillna('Other', inplace=True)
        return df
    
    def convert_to_usd(self, df):
        """Convert all amounts to USD for comparison"""
        df = df.copy()
        df['amount_usd'] = df.apply(
            lambda row: row['amount'] * EXCHANGE_RATES[row['currency']], 
            axis=1
        )
        return df
    
    def get_combined_data(self, accounts=['EUR', 'USD', 'PEN']):
        """
        Combine selected accounts
        accounts: list of account currencies to include
        """
        dfs = []
        
        if 'EUR' in accounts:
            dfs.append(self.transactions_eur)
        if 'USD' in accounts:
            dfs.append(self.transactions_usd)
        if 'PEN' in accounts:
            dfs.append(self.transactions_pen)
        
        if not dfs:
            return pd.DataFrame()
        
        combined = pd.concat(dfs, ignore_index=True)
        combined['date'] = pd.to_datetime(combined['date'])
        combined = self.categorize_transactions(combined)
        combined = self.convert_to_usd(combined)
        
        return combined.sort_values('date')
    
    def plot_expenses_by_category(self, accounts=['EUR', 'USD', 'PEN']):
        """Plot expenses by category for selected accounts"""
        df = self.get_combined_data(accounts)
        
        if df.empty:
            print("No data to plot")
            return
        
        # Group by category and sum (in USD)
        category_totals = df.groupby('category')['amount_usd'].sum().sort_values()
        
        plt.figure(figsize=(12, 6))
        category_totals.plot(kind='barh', color='steelblue')
        plt.title(f'Expenses by Category ({", ".join(accounts)} accounts)')
        plt.xlabel('Total Amount (USD)')
        plt.ylabel('Category')
        plt.tight_layout()
        plt.grid(axis='x', alpha=0.3)
        plt.show()
    
    def plot_expenses_over_time(self, accounts=['EUR', 'USD', 'PEN']):
        """Plot expenses over time for selected accounts"""
        df = self.get_combined_data(accounts)
        
        if df.empty:
            print("No data to plot")
            return
        
        # Group by month
        df['month'] = df['date'].dt.to_period('M')
        monthly = df.groupby('month')['amount_usd'].sum()
        
        plt.figure(figsize=(12, 6))
        monthly.plot(kind='line', marker='o', color='coral', linewidth=2)
        plt.title(f'Monthly Expenses ({", ".join(accounts)} accounts)')
        plt.xlabel('Month')
        plt.ylabel('Total Amount (USD)')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()
    
    def plot_expenses_by_account(self, accounts=['EUR', 'USD', 'PEN']):
        """Compare expenses across accounts"""
        df = self.get_combined_data(accounts)
        
        if df.empty:
            print("No data to plot")
            return
        
        account_totals = df.groupby('account')['amount_usd'].sum()
        
        plt.figure(figsize=(10, 6))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        account_totals.plot(kind='bar', color=colors[:len(account_totals)])
        plt.title('Total Expenses by Account (in USD)')
        plt.xlabel('Account')
        plt.ylabel('Total Amount (USD)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(axis='y', alpha=0.3)
        plt.show()
    
    def plot_net_worth(self, initial_balances, current_balances):
        """
        Plot net worth evolution
        initial_balances: dict {'EUR': amount, 'USD': amount, 'PEN': amount}
        current_balances: dict {'EUR': amount, 'USD': amount, 'PEN': amount}
        """
        # Convert to USD
        initial_usd = sum(
            initial_balances.get(curr, 0) * EXCHANGE_RATES[curr] 
            for curr in ['EUR', 'USD', 'PEN']
        )
        current_usd = sum(
            current_balances.get(curr, 0) * EXCHANGE_RATES[curr] 
            for curr in ['EUR', 'USD', 'PEN']
        )
        
        plt.figure(figsize=(10, 6))
        periods = ['Initial', 'Current']
        values = [initial_usd, current_usd]
        colors = ['#2ECC71' if current_usd >= initial_usd else '#E74C3C', '#3498DB']
        
        bars = plt.bar(periods, values, color=colors, width=0.5)
        plt.title('Net Worth Evolution (in USD)', fontsize=16, fontweight='bold')
        plt.ylabel('Amount (USD)', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.2f}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Add difference
        diff = current_usd - initial_usd
        diff_text = f'Change: ${diff:,.2f} ({(diff/initial_usd*100):.1f}%)'
        plt.text(0.5, max(values) * 0.5, diff_text, 
                ha='center', fontsize=14, 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.show()
    
    def summary(self, accounts=['EUR', 'USD', 'PEN']):
        """Print summary statistics"""
        df = self.get_combined_data(accounts)
        
        if df.empty:
            print("No data available")
            return
        
        print("\n" + "="*60)
        print(f"EXPENSE SUMMARY ({', '.join(accounts)} accounts)")
        print("="*60)
        
        print(f"\nTotal transactions: {len(df)}")
        print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
        
        print("\n--- By Currency ---")
        for currency in df['currency'].unique():
            curr_df = df[df['currency'] == currency]
            total = curr_df['amount'].sum()
            print(f"{currency}: {total:,.2f} ({len(curr_df)} transactions)")
        
        print(f"\nTotal in USD: ${df['amount_usd'].sum():,.2f}")
        
        print("\n--- By Category (USD) ---")
        category_summary = df.groupby('category')['amount_usd'].agg(['sum', 'count'])
        category_summary = category_summary.sort_values('sum')
        for cat, row in category_summary.iterrows():
            print(f"{cat:20s}: ${row['sum']:10,.2f} ({int(row['count'])} txns)")
        
        print("\n" + "="*60 + "\n")


# Example usage
if __name__ == "__main__":
    tracker = ExpenseTracker()
    
    # Show summary for all accounts
    tracker.summary(['EUR', 'USD', 'PEN'])
    
    # Plot expenses by category (all accounts)
    tracker.plot_expenses_by_category(['EUR', 'USD', 'PEN'])
    
    # Plot expenses over time (only EUR and USD)
    # tracker.plot_expenses_over_time(['EUR', 'USD'])
    
    # Compare accounts
    tracker.plot_expenses_by_account(['EUR', 'USD', 'PEN'])
    
    # Plot net worth (you need to update these values manually)
    initial_balances = {
        'EUR': 5000,
        'USD': 8000,
        'PEN': 15000
    }
    
    current_balances = {
        'EUR': 4200,
        'USD': 7300,
        'PEN': 12500
    }
    
    tracker.plot_net_worth(initial_balances, current_balances)
