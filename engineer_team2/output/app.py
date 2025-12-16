import gradio as gr
from accounts import Account

# Initialize a single account for demo purposes
account = Account("demo_user")

def deposit_funds(amount):
    try:
        account.deposit(float(amount))
        return f"Successfully deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def withdraw_funds(amount):
    try:
        account.withdraw(float(amount))
        return f"Successfully withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def buy_shares_action(symbol, quantity):
    try:
        account.buy_shares(symbol, int(quantity))
        return f"Successfully bought {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def sell_shares_action(symbol, quantity):
    try:
        account.sell_shares(symbol, int(quantity))
        return f"Successfully sold {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def show_balance():
    return f"Current cash balance: ${account.balance:.2f}"

def show_portfolio_value():
    total = account.total_portfolio_value()
    return f"Total portfolio value (cash + holdings): ${total:.2f}"

def show_profit_loss():
    pnl = account.profit_or_loss()
    if pnl >= 0:
        return f"Profit: ${pnl:.2f}"
    else:
        return f"Loss: ${abs(pnl):.2f}"

def show_holdings():
    holdings = account.get_holdings()
    if not holdings:
        return "No holdings"
    
    result = "Current Holdings:\n"
    for symbol, quantity in holdings.items():
        result += f"  {symbol}: {quantity} shares\n"
    return result

def show_transactions():
    transactions = account.get_transactions()
    if not transactions:
        return "No transactions"
    
    result = "Transaction History:\n"
    for i, txn in enumerate(transactions, 1):
        result += f"\n{i}. Type: {txn['type']}\n"
        if txn['type'] == 'deposit':
            result += f"   Amount: ${txn['amount']:.2f}\n"
        elif txn['type'] == 'withdrawal':
            result += f"   Amount: ${txn['amount']:.2f}\n"
        elif txn['type'] == 'buy':
            result += f"   Symbol: {txn['symbol']}, Quantity: {txn['quantity']}, Price: ${txn['price']:.2f}, Total: ${txn['total_cost']:.2f}\n"
        elif txn['type'] == 'sell':
            result += f"   Symbol: {txn['symbol']}, Quantity: {txn['quantity']}, Price: ${txn['price']:.2f}, Total: ${txn['total_revenue']:.2f}\n"
        result += f"   Balance after: ${txn['balance_after']:.2f}\n"
    return result

def show_account_summary():
    balance = account.balance
    holdings = account.get_holdings()
    portfolio_value = account.total_portfolio_value()
    pnl = account.profit_or_loss()
    
    summary = f"Account Summary for {account.username}\n"
    summary += f"{'='*50}\n"
    summary += f"Cash Balance: ${balance:.2f}\n\n"
    
    summary += "Holdings:\n"
    if holdings:
        for symbol, quantity in holdings.items():
            summary += f"  {symbol}: {quantity} shares\n"
    else:
        summary += "  No holdings\n"
    
    summary += f"\nTotal Portfolio Value: ${portfolio_value:.2f}\n"
    summary += f"Profit/Loss: ${pnl:.2f}\n"
    
    return summary

# Create Gradio interface
with gr.Blocks(title="Trading Account Demo") as demo:
    gr.Markdown("# Trading Account Management System")
    gr.Markdown("Demo account for single user. Available stocks: AAPL ($150), TSLA ($700), GOOGL ($2800)")
    
    with gr.Tab("Account Overview"):
        summary_output = gr.Textbox(label="Account Summary", lines=10)
        refresh_btn = gr.Button("Refresh Summary")
        refresh_btn.click(show_account_summary, outputs=summary_output)
    
    with gr.Tab("Deposit/Withdraw"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Deposit Funds")
                deposit_amount = gr.Number(label="Amount to Deposit", value=1000)
                deposit_btn = gr.Button("Deposit")
                deposit_output = gr.Textbox(label="Result")
                deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)
            
            with gr.Column():
                gr.Markdown("### Withdraw Funds")
                withdraw_amount = gr.Number(label="Amount to Withdraw", value=100)
                withdraw_btn = gr.Button("Withdraw")
                withdraw_output = gr.Textbox(label="Result")
                withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
    
    with gr.Tab("Buy/Sell Shares"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Buy Shares")
                buy_symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Stock Symbol", value="AAPL")
                buy_quantity = gr.Number(label="Quantity", value=10)
                buy_btn = gr.Button("Buy")
                buy_output = gr.Textbox(label="Result")
                buy_btn.click(buy_shares_action, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
            
            with gr.Column():
                gr.Markdown("### Sell Shares")
                sell_symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Stock Symbol", value="AAPL")
                sell_quantity = gr.Number(label="Quantity", value=5)
                sell_btn = gr.Button("Sell")
                sell_output = gr.Textbox(label="Result")
                sell_btn.click(sell_shares_action, inputs=[sell_symbol, sell_quantity], outputs=sell_output)
    
    with gr.Tab("Portfolio Info"):
        with gr.Row():
            with gr.Column():
                balance_output = gr.Textbox(label="Cash Balance")
                balance_btn = gr.Button("Show Balance")
                balance_btn.click(show_balance, outputs=balance_output)
            
            with gr.Column():
                portfolio_output = gr.Textbox(label="Portfolio Value")
                portfolio_btn = gr.Button("Show Portfolio Value")
                portfolio_btn.click(show_portfolio_value, outputs=portfolio_output)
        
        with gr.Row():
            with gr.Column():
                pnl_output = gr.Textbox(label="Profit/Loss")
                pnl_btn = gr.Button("Show Profit/Loss")
                pnl_btn.click(show_profit_loss, outputs=pnl_output)
            
            with gr.Column():
                holdings_output = gr.Textbox(label="Holdings", lines=5)
                holdings_btn = gr.Button("Show Holdings")
                holdings_btn.click(show_holdings, outputs=holdings_output)
    
    with gr.Tab("Transaction History"):
        transactions_output = gr.Textbox(label="All Transactions", lines=15)
        transactions_btn = gr.Button("Show Transactions")
        transactions_btn.click(show_transactions, outputs=transactions_output)

if __name__ == "__main__":
    demo.launch()