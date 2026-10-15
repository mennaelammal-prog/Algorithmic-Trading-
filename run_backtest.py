from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from strategies.mag_seven import MagSeven

start_date = datetime(2021, 1, 1)
end_date = datetime(2026, 1, 1)

print("Starting Backtest...")

MagSeven.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    benchmark_asset="SPY",  # Compare vs S&P 500
)
