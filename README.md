# 📈 Algorithmic Trading Lab (Template)

A professional, reproducible environment for researching, backtesting, and executing algorithmic trading strategies.

This repository bridges the gap between **Data Science** (Vectorized Backtesting) and **Live Execution** (Event-Driven Trading). It is designed for developers and researchers who want to move beyond "spaghetti code" scripts into a robust trading infrastructure.

Check out the corresponding blog post:

* [Algorithmic Trading with VectorBT and Lumibot](https://www.cbrincoveanu.com/notes/algorithmic-trading-with-vectorbt-and-lumibot/)

## ⚡ Key Technologies

*   **Research (Phase 1):** [VectorBT](https://vectorbt.dev/) — High-performance, vectorized backtesting using NumPy/Pandas broadcasting. Used for hypothesis testing and parameter optimization.
*   **Execution (Phase 2):** [Lumibot](https://lumibot.lumiwealth.com/) — Event-driven framework for realistic simulation and live trading. Handles order management, slippage, and broker connection.
*   **Broker:** [Alpaca](https://alpaca.markets/) — Commission-free API for stock trading (Paper & Live).
*   **Environment:** **VSCode Dev Containers** — A fully Dockerized Python environment ensuring code runs exactly the same on every machine.

## 📂 Project Structure

```text
.
├── .devcontainer/       # Docker configuration for VSCode
├── notebooks/           # Phase 1: Research & VectorBT experiments
│   └── example.ipynb    # Demo: From "Buy & Hold" to "Golden Cross" optimization
├── strategies/          # Phase 2: Production-ready Strategy Classes
│   └── mag_seven.py     # Example: "Magnificent Seven" Rebalancing Strategy
├── run_backtest.py      # Script to simulate strategies with Lumibot
├── run_live.py          # Script to deploy strategies to Alpaca (Paper/Live)
├── .env.example         # Template for API keys
└── requirements.txt     # Python dependencies
```

## 🚀 Getting Started

### 1. Prerequisites
*   [Docker Desktop](https://www.docker.com/products/docker-desktop) (Running)
*   [VSCode](https://code.visualstudio.com/)
*   VSCode Extension: **Dev Containers** (ms-vscode-remote.remote-containers)

### 2. Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/cbrincoveanu/algo-trading-template.git
    cd algo-trading-template
    ```
2.  **Open in VSCode:**
    Open the folder in VSCode. You should see a popup: *"Folder contains a Dev Container configuration file. Reopen to folder to develop in a container."*
3.  **Build the Environment:**
    Click **"Reopen in Container"**.
    *   *Note: This may take a few minutes the first time as it pulls the Docker image and installs Python libraries.*

### 3. Configuration (Optional / For Live Trading)
1.  Get your **Paper Trading API Keys** from the [Alpaca Dashboard](https://app.alpaca.markets/paper/dashboard/overview).
2.  Rename `.env.example` to `.env`:
    ```bash
    mv .env.example .env
    ```
3.  Paste your keys into `.env`:
    ```ini
    ALPACA_API_KEY=PKxxxxxxxxxxxxxxxxxx
    ALPACA_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ALPACA_IS_PAPER=True
    ```

---

## 🧪 Workflow

### Phase 1: Research (VectorBT)
Use Jupyter Notebooks to rapidly test hypotheses.
1.  Open `notebooks/example.ipynb`.
2.  Select the **`base (conda)`** kernel (or `/opt/conda/bin/python`).
3.  Run the cells to see how **VectorBT** can test thousands of parameter combinations in seconds.

### Phase 2: Strategy Development (Lumibot)
Once you have a robust idea, implement it as a class in `strategies/`.
*   See `strategies/mag_seven.py` for an example of a multi-asset buy-and-hold strategy.

### Phase 3: Backtesting (Event-Driven)
Verify your strategy handles realistic constraints (fees, slippage, sequential data).
```bash
python run_backtest.py
```
*   *Output:* A browser window will open with a tear sheet (CAGR, Sharpe, Drawdown).

### Phase 4: Live / Paper Trading
Deploy the bot to trade in real-time.
```bash
python run_live.py
```
*   *Output:* The bot will connect to Alpaca and wait for market open.

---

## ⚠️ Disclaimer

**This software is for educational and research purposes only.**

*   Algorithmic trading involves significant risk.
*   Past performance is not indicative of future results.
*   Do not trade with money you cannot afford to lose.
*   The authors and contributors are not financial advisors.
