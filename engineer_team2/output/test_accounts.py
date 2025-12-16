import unittest
from accounts import Account, get_share_price


class TestGetSharePrice(unittest.TestCase):
    """Test cases for the get_share_price function."""
    
    def test_get_share_price_valid_symbols(self):
        """Test retrieving prices for valid stock symbols."""
        self.assertEqual(get_share_price('AAPL'), 150.00)
        self.assertEqual(get_share_price('TSLA'), 700.00)
        self.assertEqual(get_share_price('GOOGL'), 2800.00)
    
    def test_get_share_price_invalid_symbol(self):
        """Test retrieving price for an invalid stock symbol."""
        self.assertEqual(get_share_price('INVALID'), 0.0)
        self.assertEqual(get_share_price('XYZ'), 0.0)


class TestAccountInitialization(unittest.TestCase):
    """Test cases for Account initialization."""
    
    def test_account_creation(self):
        """Test creating a new account."""
        account = Account('testuser')
        self.assertEqual(account.username, 'testuser')
        self.assertEqual(account.balance, 0.0)
        self.assertEqual(account.holdings, {})
        self.assertEqual(account.transactions, [])
        self.assertEqual(account._total_deposited, 0.0)


class TestAccountDeposit(unittest.TestCase):
    """Test cases for the deposit method."""
    
    def setUp(self):
        """Set up a fresh account for each test."""
        self.account = Account('testuser')
    
    def test_deposit_valid_amount(self):
        """Test depositing a valid amount."""
        self.account.deposit(1000.0)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account._total_deposited, 1000.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['type'], 'deposit')
        self.assertEqual(self.account.transactions[0]['amount'], 1000.0)
    
    def test_deposit_multiple_times(self):
        """Test multiple deposits."""
        self.account.deposit(500.0)
        self.account.deposit(300.0)
        self.assertEqual(self.account.balance, 800.0)
        self.assertEqual(self.account._total_deposited, 800.0)
        self.assertEqual(len(self.account.transactions), 2)
    
    def test_deposit_zero_amount(self):
        """Test depositing zero amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(0)
        self.assertIn('must be greater than zero', str(context.exception))
    
    def test_deposit_negative_amount(self):
        """Test depositing negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-100.0)
        self.assertIn('must be greater than zero', str(context.exception))


class TestAccountWithdraw(unittest.TestCase):
    """Test cases for the withdraw method."""
    
    def setUp(self):
        """Set up a fresh account with initial balance for each test."""
        self.account = Account('testuser')
        self.account.deposit(1000.0)
    
    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount."""
        self.account.withdraw(300.0)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'withdrawal')
        self.assertEqual(self.account.transactions[1]['amount'], 300.0)
    
    def test_withdraw_entire_balance(self):
        """Test withdrawing the entire balance."""
        self.account.withdraw(1000.0)
        self.assertEqual(self.account.balance, 0.0)
    
    def test_withdraw_zero_amount(self):
        """Test withdrawing zero amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(0)
        self.assertIn('must be greater than zero', str(context.exception))
    
    def test_withdraw_negative_amount(self):
        """Test withdrawing negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-100.0)
        self.assertIn('must be greater than zero', str(context.exception))
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawing more than balance raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(1500.0)
        self.assertIn('Insufficient funds', str(context.exception))


class TestAccountBuyShares(unittest.TestCase):
    """Test cases for the buy_shares method."""
    
    def setUp(self):
        """Set up a fresh account with initial balance for each test."""
        self.account = Account('testuser')
        self.account.deposit(10000.0)
    
    def test_buy_shares_valid(self):
        """Test buying shares with valid symbol and quantity."""
        self.account.buy_shares('AAPL', 10)
        self.assertEqual(self.account.holdings['AAPL'], 10)
        self.assertEqual(self.account.balance, 10000.0 - (150.0 * 10))
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'buy')
    
    def test_buy_shares_multiple_times_same_symbol(self):
        """Test buying shares of the same symbol multiple times."""
        self.account.buy_shares('AAPL', 5)
        self.account.buy_shares('AAPL', 3)
        self.assertEqual(self.account.holdings['AAPL'], 8)
    
    def test_buy_shares_different_symbols(self):
        """Test buying shares of different symbols."""
        self.account.buy_shares('AAPL', 5)
        self.account.buy_shares('TSLA', 2)
        self.assertEqual(self.account.holdings['AAPL'], 5)
        self.assertEqual(self.account.holdings['TSLA'], 2)
    
    def test_buy_shares_zero_quantity(self):
        """Test buying zero shares raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', 0)
        self.assertIn('must be greater than zero', str(context.exception))
    
    def test_buy_shares_negative_quantity(self):
        """Test buying negative shares raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('AAPL', -5)
        self.assertIn('must be greater than zero', str(context.exception))
    
    def test_buy_shares_invalid_symbol(self):
        """Test buying shares with invalid symbol raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('INVALID', 10)
        self.assertIn('Invalid stock symbol', str(context.exception))
    
    def test_buy_shares_insufficient_funds(self):
        """Test buying shares with insufficient funds raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares('GOOGL', 10)
        self.assertIn('Insufficient funds', str(context.exception))


class TestAccountSellShares(unittest.TestCase):
    """Test cases for the sell_shares method."""
    
    def setUp(self):
        """Set up a fresh account with shares for each test."""
        self.account = Account('testuser')
        self.account.deposit(10000.0)
        self.account.buy_shares('AAPL', 20)
        self.account.buy_shares('TSLA', 5)
    
    def test_sell_shares_valid(self):
        """Test selling shares with valid symbol and quantity."""
        initial_balance = self.account.balance
        self.account.sell_shares('AAPL', 10)
        self.assertEqual(self.account.holdings['AAPL'], 10)
        expected_balance = initial_balance + (150.0 * 10)
        self.assertEqual(self.account.balance, expected_balance)
    
    def test_sell_all_shares_of_symbol(self):
        """Test selling all shares of a symbol removes it from holdings."""
        self.account.sell_shares('AAPL', 20)
        self.assertNotIn('AAPL', self.account.holdings)
        self.assertIn('TSLA', self.account.holdings)
    
    def test_sell_shares_zero_quantity(self):
        """Test selling zero shares raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', 0)
        self.assertIn('must be greater than zero', str(context.exception))
    
    def test_sell_shares_negative_quantity(self):
        """Test selling negative shares raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', -5)
        self.assertIn('must be greater than zero', str(context.exception))
    
    def test_sell_shares_insufficient_holdings(self):
        """Test selling more shares than owned raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('AAPL', 25)
        self.assertIn('Insufficient shares', str(context.exception))
    
    def test_sell_shares_not_owned(self):
        """Test selling shares not in holdings raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('GOOGL', 1)
        self.assertIn('Insufficient shares', str(context.exception))
    
    def test_sell_shares_invalid_symbol(self):
        """Test selling shares with invalid symbol raises ValueError."""
        self.account.holdings['INVALID'] = 10
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares('INVALID', 5)
        self.assertIn('Invalid stock symbol', str(context.exception))


class TestAccountPortfolioValue(unittest.TestCase):
    """Test cases for the total_portfolio_value method."""
    
    def test_portfolio_value_cash_only(self):
        """Test portfolio value with only cash."""
        account = Account('testuser')
        account.deposit(5000.0)
        self.assertEqual(account.total_portfolio_value(), 5000.0)
    
    def test_portfolio_value_with_holdings(self):
        """Test portfolio value with cash and holdings."""
        account = Account('testuser')
        account.deposit(10000.0)
        account.buy_shares('AAPL', 10)
        account.buy_shares('TSLA', 2)
        self.assertEqual(account.total_portfolio_value(), 10000.0)
    
    def test_portfolio_value_no_balance_only_holdings(self):
        """Test portfolio value with no cash balance."""
        account = Account('testuser')
        account.deposit(1500.0)
        account.buy_shares('AAPL', 10)
        self.assertEqual(account.balance, 0.0)
        self.assertEqual(account.total_portfolio_value(), 1500.0)


class TestAccountProfitOrLoss(unittest.TestCase):
    """Test cases for the profit_or_loss method."""
    
    def test_profit_or_loss_no_trading(self):
        """Test profit/loss with only deposits and no trading."""
        account = Account('testuser')
        account.deposit(1000.0)
        self.assertEqual(account.profit_or_loss(), 0.0)
    
    def test_profit_or_loss_with_withdrawal(self):
        """Test profit/loss after withdrawal."""
        account = Account('testuser')
        account.deposit(1000.0)
        account.withdraw(200.0)
        self.assertEqual(account.profit_or_loss(), -200.0)
    
    def test_profit_or_loss_break_even(self):
        """Test profit/loss when breaking even."""
        account = Account('testuser')
        account.deposit(1500.0)
        account.buy_shares('AAPL', 10)
        self.assertEqual(account.profit_or_loss(), 0.0)
    
    def test_profit_or_loss_multiple_deposits(self):
        """Test profit/loss with multiple deposits."""
        account = Account('testuser')
        account.deposit(1000.0)
        account.deposit(500.0)
        self.assertEqual(account._total_deposited, 1500.0)
        self.assertEqual(account.profit_or_loss(), 0.0)


class TestAccountGetHoldings(unittest.TestCase):
    """Test cases for the get_holdings method."""
    
    def test_get_holdings_empty(self):
        """Test getting holdings when account has none."""
        account = Account('testuser')
        self.assertEqual(account.get_holdings(), {})
    
    def test_get_holdings_with_shares(self):
        """Test getting holdings with shares."""
        account = Account('testuser')
        account.deposit(5000.0)
        account.buy_shares('AAPL', 10)
        account.buy_shares('TSLA', 5)
        holdings = account.get_holdings()
        self.assertEqual(holdings['AAPL'], 10)
        self.assertEqual(holdings['TSLA'], 5)
    
    def test_get_holdings_returns_copy(self):
        """Test that get_holdings returns a copy, not reference."""
        account = Account('testuser')
        account.deposit(1500.0)
        account.buy_shares('AAPL', 10)
        holdings = account.get_holdings()
        holdings['AAPL'] = 999
        self.assertEqual(account.holdings['AAPL'], 10)


class TestAccountGetTransactions(unittest.TestCase):
    """Test cases for the get_transactions method."""
    
    def test_get_transactions_empty(self):
        """Test getting transactions when account has none."""
        account = Account('testuser')
        self.assertEqual(account.get_transactions(), [])
    
    def test_get_transactions_with_history(self):
        """Test getting transactions with history."""
        account = Account('testuser')
        account.deposit(1000.0)
        account.withdraw(200.0)
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['type'], 'deposit')
        self.assertEqual(transactions[1]['type'], 'withdrawal')
    
    def test_get_transactions_returns_copy(self):
        """Test that get_transactions returns a copy, not reference."""
        account = Account('testuser')
        account.deposit(1000.0)
        transactions = account.get_transactions()
        transactions.append({'type': 'fake', 'amount': 999})
        self.assertEqual(len(account.transactions), 1)
    
    def test_transactions_include_all_types(self):
        """Test that all transaction types are recorded."""
        account = Account('testuser')
        account.deposit(5000.0)
        account.buy_shares('AAPL', 10)
        account.sell_shares('AAPL', 5)
        account.withdraw(100.0)
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 4)
        self.assertEqual(transactions[0]['type'], 'deposit')
        self.assertEqual(transactions[1]['type'], 'buy')
        self.assertEqual(transactions[2]['type'], 'sell')
        self.assertEqual(transactions[3]['type'], 'withdrawal')


class TestAccount