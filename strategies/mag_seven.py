from lumibot.strategies.strategy import Strategy


class MagSeven(Strategy):
    """
    Buys the 'Magnificent Seven' tech stocks with equal weighting.
    Demonstrates multi-asset order execution.
    """

    parameters = {
        # The Mag 7 Tickers
        "symbols": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"],
        # 1.0 = 100% of the portfolio is invested
        "cash_at_risk": 0.95,
    }

    def initialize(self):
        self.sleeptime = "1D"
        self.symbols = self.parameters["symbols"]

    def on_trading_iteration(self):
        # 1. Calculate Target Value per Asset
        # If we have $10,000 and 7 assets, we want ~$1,350 per asset
        cash = self.get_cash()
        portfolio_value = self.get_portfolio_value()

        # If we already hold positions, we don't want to keep buying.
        # For a simple Buy-and-Hold, we check if we are mostly in cash.

        # Simple Logic: If cash is > 10% of portfolio, we probably need to buy.
        if cash > (portfolio_value * 0.10):

            weight = self.parameters["cash_at_risk"] / len(self.symbols)
            target_value_per_asset = portfolio_value * weight

            self.log_message(f"Portfolio Value: ${portfolio_value:,.2f}")
            self.log_message(f"Target per Asset: ${target_value_per_asset:,.2f}")

            for symbol in self.symbols:
                # Check if we already own it
                position = self.get_position(symbol)

                if position is None:
                    last_price = self.get_last_price(symbol)
                    quantity = int(target_value_per_asset // last_price)

                    if quantity > 0:
                        order = self.create_order(symbol, quantity, "buy")
                        self.submit_order(order)
                        self.log_message(f"BUYING {quantity} {symbol} @ {last_price}")

        else:
            self.log_message("Portfolio is fully invested. Sleeping...")
