def get_share_price(symbol: str) -> float:
    """
    Retrieves the current price of the specified share.
    Test implementation with fixed prices.
    """
    prices = {
        'AAPL': 150.00,
        'TSLA': 700.00,
        'GOOGL': 2800.00
    }
    return prices.get(symbol, 0.0)


class Account:
    """
    Account management system for trading simulation platform.
    """
    
    def __init__(self, username: str):
        """
        Initializes a new account with a username.
        
        Args:
            username: The username of the account holder.
        """
        self.username = username
        self.balance = 0.0
        self.holdings = {}
        self.transactions = []
        self._total_deposited = 0.0
    
    def deposit(self, amount: float):
        """
        Allows the user to deposit funds into their account.
        
        Args:
            amount: The amount to deposit (must be > 0).
            
        Raises:
            ValueError: If amount <= 0.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero")
        
        self.balance += amount
        self._total_deposited += amount
        self.transactions.append({
            'type': 'deposit',
            'amount': amount,
            'balance_after': self.balance
        })
    
    def withdraw(self, amount: float):
        """
        Allows the user to withdraw funds from their account.
        
        Args:
            amount: The amount to withdraw (must be > 0 and <= balance).
            
        Raises:
            ValueError: If amount <= 0 or amount > balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero")
        
        if amount > self.balance:
            raise ValueError("Insufficient funds: cannot withdraw more than current balance")
        
        self.balance -= amount
        self.transactions.append({
            'type': 'withdrawal',
            'amount': amount,
            'balance_after': self.balance
        })
    
    def buy_shares(self, symbol: str, quantity: int):
        """
        Allows the user to buy shares of a given stock symbol.
        
        Args:
            symbol: The stock symbol to buy.
            quantity: The number of shares to buy (must be > 0).
            
        Raises:
            ValueError: If quantity <= 0 or insufficient funds.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        price = get_share_price(symbol)
        if price == 0.0:
            raise ValueError(f"Invalid stock symbol: {symbol}")
        
        total_cost = price * quantity
        
        if total_cost > self.balance:
            raise ValueError(f"Insufficient funds: need {total_cost:.2f}, but only have {self.balance:.2f}")
        
        self.balance -= total_cost
        
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        self.transactions.append({
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total_cost': total_cost,
            'balance_after': self.balance
        })
    
    def sell_shares(self, symbol: str, quantity: int):
        """
        Allows the user to sell shares of a given stock symbol.
        
        Args:
            symbol: The stock symbol to sell.
            quantity: The number of shares to sell (must be > 0).
            
        Raises:
            ValueError: If quantity <= 0 or insufficient shares.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            current_holdings = self.holdings.get(symbol, 0)
            raise ValueError(f"Insufficient shares: trying to sell {quantity} shares, but only have {current_holdings}")
        
        price = get_share_price(symbol)
        if price == 0.0:
            raise ValueError(f"Invalid stock symbol: {symbol}")
        
        total_revenue = price * quantity
        
        self.balance += total_revenue
        self.holdings[symbol] -= quantity
        
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self.transactions.append({
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total_revenue': total_revenue,
            'balance_after': self.balance
        })
    
    def total_portfolio_value(self) -> float:
        """
        Calculates the total current value of the user's portfolio.
        
        Returns:
            The total portfolio value (cash + current value of all holdings).
        """
        portfolio_value = self.balance
        
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            portfolio_value += price * quantity
        
        return portfolio_value
    
    def profit_or_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit.
        
        Returns:
            The profit (positive) or loss (negative) as a float.
        """
        current_value = self.total_portfolio_value()
        return current_value - self._total_deposited
    
    def get_holdings(self) -> dict:
        """
        Returns a dictionary of the user's current holdings.
        
        Returns:
            A dictionary with stock symbols as keys and quantities as values.
        """
        return self.holdings.copy()
    
    def get_transactions(self) -> list:
        """
        Returns a list of the user's transaction history.
        
        Returns:
            A list of transaction dictionaries.
        """
        return self.transactions.copy()