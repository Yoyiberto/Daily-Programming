# Multi-Currency Expense Tracker

A web-based expense tracking system with an interactive GUI that supports multiple currencies (EUR, USD, PEN) and provides real-time categorization and visualization of expenses.

## Features

- ✅ **Interactive Web GUI** - Beautiful, responsive web interface
- ✅ **Multi-Currency Support** - Track EUR, USD, and PEN accounts
- ✅ **Dynamic Exchange Rates** - Input and update exchange rates in real-time
- ✅ **Flexible Account Selection** - View 1, 2, or all 3 accounts simultaneously
- ✅ **CSV File Upload** - Easy to upload and switch between different CSV files
- ✅ **Automatic Categorization** - Based on vendor mapping
- ✅ **Persistent Visualizations** - Interactive charts that stay on screen
- ✅ **Net Worth Tracking** - Manual balance input with visual tracking
- ✅ **Multiple Views**:
  - Expenses by category (bar chart & pie chart)
  - Expenses over time (line charts with trends)
  - Account comparison
  - Net worth evolution
  - Detailed transaction table with filters

## Files

- `transactions_eur.csv` - EUR account transactions (20 entries)
- `transactions_usd.csv` - USD account transactions (20 entries)
- `transactions_pen.csv` - PEN account transactions (20 entries)
- `vendor_categories.csv` - Vendor to category mapping
- `expense_tracker.py` - Main Python script

## Setup

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Run the tracker:
```bash
python expense_tracker.py
```

## Usage

### Basic Usage

```python
from expense_tracker import ExpenseTracker

tracker = ExpenseTracker()

# Show summary for all accounts
tracker.summary(['EUR', 'USD', 'PEN'])

# Show summary for specific accounts only
tracker.summary(['EUR', 'USD'])  # Only EUR and USD
tracker.summary(['PEN'])  # Only PEN account
```

### Visualizations

```python
# Plot expenses by category (all accounts)
tracker.plot_expenses_by_category(['EUR', 'USD', 'PEN'])

# Plot expenses by category (only EUR)
tracker.plot_expenses_by_category(['EUR'])

# Plot expenses over time
tracker.plot_expenses_over_time(['EUR', 'USD', 'PEN'])

# Compare total expenses across accounts
tracker.plot_expenses_by_account(['EUR', 'USD', 'PEN'])

# Plot net worth evolution
initial = {'EUR': 5000, 'USD': 8000, 'PEN': 15000}
current = {'EUR': 4200, 'USD': 7300, 'PEN': 12500}
tracker.plot_net_worth(initial, current)
```

## Categories

The system automatically categorizes expenses into:
- **Groceries** - Supermarkets and food stores
- **Subscriptions** - Netflix, Spotify, etc.
- **Transportation** - Gas stations, fuel
- **Shopping** - General retail
- **Clothing** - Fashion stores
- **Food & Dining** - Restaurants, coffee shops
- **Utilities** - Phone, electricity, internet
- **Travel** - Hotels, flights, bookings
- **Electronics** - Tech purchases
- **Sports & Recreation** - Fitness and sports
- **Home Improvement** - Hardware and tools
- **Other** - Uncategorized

## Exchange Rates

Current exchange rates (to USD) are defined in the script:
- EUR: 1.09
- USD: 1.00 (base)
- PEN: 0.27

Update these in `expense_tracker.py` as needed:
```python
EXCHANGE_RATES = {
    'EUR': 1.09,
    'USD': 1.00,
    'PEN': 0.27
}
```

## CSV File Format

### Transaction Files
Format for `transactions_eur.csv`, `transactions_usd.csv`, `transactions_pen.csv`:
```csv
amount,vendor,date,description
-50.00,Store Name,2025-06-15,What you bought
-25.50,Another Store,2025-06-20,Another purchase
```

**Important:**
- Amounts should be negative for expenses
- Date format: YYYY-MM-DD
- No currency symbol in amount field

### Vendor Categories File
Format for `vendor_categories.csv`:
```csv
vendor,category
Store Name,Shopping
Gas Station,Transportation
Netflix,Subscriptions
```

## 🎨 How to Use

### Quick Start Workflow:

1. **Launch the app** - Double-click `start_app.bat` or run `streamlit run app.py`

2. **Set Exchange Rates** - Update rates in sidebar (top section)

3. **Select Accounts** - Choose which accounts to analyze

4. **Upload CSV Files** (optional) - Replace data with your own files

5. **Input Balances** - Enter initial and current balances for net worth tracking

6. **Explore Tabs** - Click through different visualization tabs

7. **Filter Data** - Use the "Transaction Details" tab to filter and export

### Tips:
- 💡 All changes update instantly - no need to refresh
- 💡 Hover over charts for detailed information
- 💡 Download filtered data from the Transaction Details tab
- 💡 Upload new CSVs anytime to refresh your data

## Next Steps / Future Enhancements

- 🔄 Automatic currency rate fetching from API
- 📱 Web interface (Flask/Streamlit)
- 📊 More detailed analytics (budget tracking, predictions)
- 📧 Automatic email reports
- 💾 Database integration (SQLite/PostgreSQL)
- 📤 Export to PDF/Excel
- 🔔 Budget alerts
