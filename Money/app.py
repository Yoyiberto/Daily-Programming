import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="Multi-Currency Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    h1 {
        color: #1f77b4;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for exchange rates
if 'exchange_rates' not in st.session_state:
    st.session_state.exchange_rates = {
        'EUR': 1.09,
        'USD': 1.00,
        'PEN': 0.27
    }

# Initialize session state for dataframes
if 'df_eur' not in st.session_state:
    try:
        st.session_state.df_eur = pd.read_csv('transactions_eur.csv')
    except:
        st.session_state.df_eur = pd.DataFrame(columns=['amount', 'vendor', 'date', 'description'])

if 'df_usd' not in st.session_state:
    try:
        st.session_state.df_usd = pd.read_csv('transactions_usd.csv')
    except:
        st.session_state.df_usd = pd.DataFrame(columns=['amount', 'vendor', 'date', 'description'])

if 'df_pen' not in st.session_state:
    try:
        st.session_state.df_pen = pd.read_csv('transactions_pen.csv')
    except:
        st.session_state.df_pen = pd.DataFrame(columns=['amount', 'vendor', 'date', 'description'])

if 'vendor_categories' not in st.session_state:
    try:
        st.session_state.vendor_categories = pd.read_csv('vendor_categories.csv')
    except:
        st.session_state.vendor_categories = pd.DataFrame(columns=['vendor', 'category'])

# Functions
def categorize_transactions(df, vendor_categories):
    """Add category column based on vendor"""
    df = df.copy()
    df['category'] = df['vendor'].map(
        vendor_categories.set_index('vendor')['category']
    )
    df['category'].fillna('Other', inplace=True)
    return df

def convert_to_usd(df, currency, exchange_rates):
    """Convert amounts to USD"""
    df = df.copy()
    df['amount_usd'] = df['amount'] * exchange_rates[currency]
    return df

def get_combined_data(accounts, exchange_rates):
    """Combine selected accounts"""
    dfs = []
    
    if 'EUR' in accounts and not st.session_state.df_eur.empty:
        df_eur = st.session_state.df_eur.copy()
        df_eur['currency'] = 'EUR'
        df_eur['account'] = 'EUR Account'
        df_eur = convert_to_usd(df_eur, 'EUR', exchange_rates)
        dfs.append(df_eur)
    
    if 'USD' in accounts and not st.session_state.df_usd.empty:
        df_usd = st.session_state.df_usd.copy()
        df_usd['currency'] = 'USD'
        df_usd['account'] = 'USD Account'
        df_usd = convert_to_usd(df_usd, 'USD', exchange_rates)
        dfs.append(df_usd)
    
    if 'PEN' in accounts and not st.session_state.df_pen.empty:
        df_pen = st.session_state.df_pen.copy()
        df_pen['currency'] = 'PEN'
        df_pen['account'] = 'PEN Account'
        df_pen = convert_to_usd(df_pen, 'PEN', exchange_rates)
        dfs.append(df_pen)
    
    if not dfs:
        return pd.DataFrame()
    
    combined = pd.concat(dfs, ignore_index=True)
    combined['date'] = pd.to_datetime(combined['date'])
    combined = categorize_transactions(combined, st.session_state.vendor_categories)
    
    return combined.sort_values('date')

# Sidebar
st.sidebar.title("⚙️ Settings")

# Exchange Rates Section
st.sidebar.header("💱 Exchange Rates (to USD)")
st.sidebar.caption("Update the exchange rates below")

new_eur_rate = st.sidebar.number_input(
    "EUR → USD",
    min_value=0.01,
    value=st.session_state.exchange_rates['EUR'],
    step=0.01,
    format="%.4f"
)

new_pen_rate = st.sidebar.number_input(
    "PEN → USD",
    min_value=0.01,
    value=st.session_state.exchange_rates['PEN'],
    step=0.01,
    format="%.4f"
)

if st.sidebar.button("Update Exchange Rates"):
    st.session_state.exchange_rates['EUR'] = new_eur_rate
    st.session_state.exchange_rates['PEN'] = new_pen_rate
    st.sidebar.success("✅ Exchange rates updated!")

st.sidebar.divider()

# Account Selection
st.sidebar.header("🏦 Select Accounts")
selected_accounts = st.sidebar.multiselect(
    "Choose accounts to analyze",
    options=['EUR', 'USD', 'PEN'],
    default=['EUR', 'USD', 'PEN']
)

st.sidebar.divider()

# CSV Upload Section
st.sidebar.header("📁 Upload CSV Files")

uploaded_eur = st.sidebar.file_uploader("EUR Transactions", type=['csv'], key='eur')
if uploaded_eur:
    st.session_state.df_eur = pd.read_csv(uploaded_eur)
    st.sidebar.success("✅ EUR file uploaded!")

uploaded_usd = st.sidebar.file_uploader("USD Transactions", type=['csv'], key='usd')
if uploaded_usd:
    st.session_state.df_usd = pd.read_csv(uploaded_usd)
    st.sidebar.success("✅ USD file uploaded!")

uploaded_pen = st.sidebar.file_uploader("PEN Transactions", type=['csv'], key='pen')
if uploaded_pen:
    st.session_state.df_pen = pd.read_csv(uploaded_pen)
    st.sidebar.success("✅ PEN file uploaded!")

uploaded_categories = st.sidebar.file_uploader("Vendor Categories", type=['csv'], key='categories')
if uploaded_categories:
    st.session_state.vendor_categories = pd.read_csv(uploaded_categories)
    st.sidebar.success("✅ Categories file uploaded!")

st.sidebar.divider()

# Net Worth Section
st.sidebar.header("💼 Net Worth Tracker")
st.sidebar.caption("Enter your balances manually")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.write("**Initial**")
    initial_eur = st.number_input("EUR", value=5000.0, step=100.0, key='init_eur')
    initial_usd = st.number_input("USD", value=8000.0, step=100.0, key='init_usd')
    initial_pen = st.number_input("PEN", value=15000.0, step=100.0, key='init_pen')

with col2:
    st.write("**Current**")
    current_eur = st.number_input("EUR", value=4200.0, step=100.0, key='curr_eur')
    current_usd = st.number_input("USD", value=7300.0, step=100.0, key='curr_usd')
    current_pen = st.number_input("PEN", value=12500.0, step=100.0, key='curr_pen')

# Main content
st.title("💰 Multi-Currency Expense Tracker")
st.caption("Track and analyze your expenses across multiple currencies")

if not selected_accounts:
    st.warning("⚠️ Please select at least one account from the sidebar to view data.")
else:
    # Get combined data
    df = get_combined_data(selected_accounts, st.session_state.exchange_rates)
    
    if df.empty:
        st.warning("⚠️ No transaction data available for the selected accounts.")
    else:
        # Summary Metrics
        st.header("📊 Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Transactions", len(df))
        
        with col2:
            total_usd = df['amount_usd'].sum()
            st.metric("Total Spent (USD)", f"${abs(total_usd):,.2f}")
        
        with col3:
            date_range = f"{df['date'].min().date()} to {df['date'].max().date()}"
            st.metric("Date Range", f"{(df['date'].max() - df['date'].min()).days} days")
        
        with col4:
            avg_transaction = df['amount_usd'].mean()
            st.metric("Avg Transaction", f"${abs(avg_transaction):,.2f}")
        
        st.divider()
        
        # Tabs for different visualizations
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 By Category", 
            "📅 Over Time", 
            "🏦 By Account", 
            "💼 Net Worth",
            "📋 Transaction Details"
        ])
        
        with tab1:
            st.subheader("Expenses by Category")
            category_totals = df.groupby('category')['amount_usd'].sum().abs().sort_values(ascending=True)
            
            fig = px.bar(
                x=category_totals.values,
                y=category_totals.index,
                orientation='h',
                labels={'x': 'Total Amount (USD)', 'y': 'Category'},
                title=f"Total Expenses by Category ({', '.join(selected_accounts)})",
                color=category_totals.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Category breakdown table
            col1, col2 = st.columns([2, 1])
            with col1:
                category_stats = df.groupby('category').agg({
                    'amount_usd': ['sum', 'count', 'mean']
                }).round(2)
                category_stats.columns = ['Total (USD)', 'Transactions', 'Avg (USD)']
                category_stats['Total (USD)'] = category_stats['Total (USD)'].abs()
                category_stats['Avg (USD)'] = category_stats['Avg (USD)'].abs()
                category_stats = category_stats.sort_values('Total (USD)', ascending=False)
                st.dataframe(category_stats, use_container_width=True)
            
            with col2:
                # Pie chart
                fig_pie = px.pie(
                    values=category_totals.values,
                    names=category_totals.index,
                    title="Category Distribution"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with tab2:
            st.subheader("Expenses Over Time")
            
            # Monthly aggregation
            df['month'] = df['date'].dt.to_period('M').astype(str)
            monthly = df.groupby('month')['amount_usd'].sum().abs()
            
            fig = px.line(
                x=monthly.index,
                y=monthly.values,
                labels={'x': 'Month', 'y': 'Total Amount (USD)'},
                title=f"Monthly Expenses Trend ({', '.join(selected_accounts)})",
                markers=True
            )
            fig.update_traces(line_color='#FF6B6B', line_width=3)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Category over time
            st.subheader("Category Trends")
            category_monthly = df.groupby(['month', 'category'])['amount_usd'].sum().abs().reset_index()
            
            fig2 = px.line(
                category_monthly,
                x='month',
                y='amount_usd',
                color='category',
                labels={'amount_usd': 'Amount (USD)', 'month': 'Month'},
                title="Expense Trends by Category"
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            st.subheader("Comparison by Account")
            
            account_totals = df.groupby('account')['amount_usd'].sum().abs()
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            fig = px.bar(
                x=account_totals.index,
                y=account_totals.values,
                labels={'x': 'Account', 'y': 'Total Amount (USD)'},
                title="Total Expenses by Account (in USD)",
                color=account_totals.index,
                color_discrete_sequence=colors
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Account breakdown
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("By Currency (Original)")
                currency_summary = df.groupby('currency')['amount'].sum().abs()
                for curr, amount in currency_summary.items():
                    st.metric(f"{curr} Total", f"{amount:,.2f} {curr}")
            
            with col2:
                st.subheader("By Account (USD)")
                for account, amount in account_totals.items():
                    st.metric(account, f"${amount:,.2f}")
        
        with tab4:
            st.subheader("Net Worth Evolution")
            
            # Calculate net worth in USD
            initial_usd_total = (
                initial_eur * st.session_state.exchange_rates['EUR'] +
                initial_usd * st.session_state.exchange_rates['USD'] +
                initial_pen * st.session_state.exchange_rates['PEN']
            )
            
            current_usd_total = (
                current_eur * st.session_state.exchange_rates['EUR'] +
                current_usd * st.session_state.exchange_rates['USD'] +
                current_pen * st.session_state.exchange_rates['PEN']
            )
            
            # Create visualization
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['Initial Balance', 'Current Balance'],
                y=[initial_usd_total, current_usd_total],
                marker_color=['#3498DB', '#2ECC71' if current_usd_total >= initial_usd_total else '#E74C3C'],
                text=[f'${initial_usd_total:,.2f}', f'${current_usd_total:,.2f}'],
                textposition='outside',
            ))
            
            fig.update_layout(
                title="Net Worth Evolution (in USD)",
                yaxis_title="Amount (USD)",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Net worth metrics
            difference = current_usd_total - initial_usd_total
            percentage_change = (difference / initial_usd_total * 100) if initial_usd_total != 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Initial Net Worth", f"${initial_usd_total:,.2f}")
            with col2:
                st.metric("Current Net Worth", f"${current_usd_total:,.2f}")
            with col3:
                st.metric("Change", f"${difference:,.2f}", f"{percentage_change:.1f}%")
            
            # Breakdown by currency
            st.subheader("Balance Breakdown")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Initial Balances**")
                st.write(f"🇪🇺 EUR: €{initial_eur:,.2f} (${initial_eur * st.session_state.exchange_rates['EUR']:,.2f})")
                st.write(f"🇺🇸 USD: ${initial_usd:,.2f}")
                st.write(f"🇵🇪 PEN: S/{initial_pen:,.2f} (${initial_pen * st.session_state.exchange_rates['PEN']:,.2f})")
            
            with col2:
                st.write("**Current Balances**")
                st.write(f"🇪🇺 EUR: €{current_eur:,.2f} (${current_eur * st.session_state.exchange_rates['EUR']:,.2f})")
                st.write(f"🇺🇸 USD: ${current_usd:,.2f}")
                st.write(f"🇵🇪 PEN: S/{current_pen:,.2f} (${current_pen * st.session_state.exchange_rates['PEN']:,.2f})")
        
        with tab5:
            st.subheader("Transaction Details")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_categories = st.multiselect(
                    "Filter by Category",
                    options=sorted(df['category'].unique()),
                    default=sorted(df['category'].unique())
                )
            
            with col2:
                selected_currencies = st.multiselect(
                    "Filter by Currency",
                    options=sorted(df['currency'].unique()),
                    default=sorted(df['currency'].unique())
                )
            
            with col3:
                sort_by = st.selectbox(
                    "Sort by",
                    options=['date', 'amount_usd', 'vendor', 'category'],
                    index=0
                )
            
            # Apply filters
            filtered_df = df[
                (df['category'].isin(selected_categories)) &
                (df['currency'].isin(selected_currencies))
            ].sort_values(sort_by, ascending=False)
            
            # Display table
            display_df = filtered_df[['date', 'vendor', 'description', 'amount', 'currency', 'amount_usd', 'category']].copy()
            display_df['date'] = display_df['date'].dt.date
            display_df['amount'] = display_df['amount'].round(2)
            display_df['amount_usd'] = display_df['amount_usd'].round(2)
            display_df.columns = ['Date', 'Vendor', 'Description', 'Amount', 'Currency', 'Amount (USD)', 'Category']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Download button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# Footer
st.divider()
st.caption("💡 Tip: Upload new CSV files in the sidebar to update your data. Use the exchange rate inputs to keep conversions accurate.")
