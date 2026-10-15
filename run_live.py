import os
from dotenv import load_dotenv
from lumibot.brokers import Alpaca
from lumibot.traders import Trader
from strategies.mag_seven import MagSeven

# Load .env file
load_dotenv()

# Parse Credentials
ALPACA_CREDS = {
    "API_KEY": os.getenv("ALPACA_API_KEY"),
    "API_SECRET": os.getenv("ALPACA_API_SECRET"),
    "PAPER": os.getenv("ALPACA_IS_PAPER", "True").lower() == "true",
}

if not ALPACA_CREDS["API_KEY"]:
    raise ValueError("Missing API Keys. Please check your .env file.")

# 1. Setup Broker
broker = Alpaca(ALPACA_CREDS)

# 2. Setup Strategy
strategy = MagSeven(broker=broker)

# 3. Run Trader
trader = Trader()
trader.add_strategy(strategy)

print("Starting Mag7 Bot... (Press Ctrl+C to stop)")
trader.run_all()
