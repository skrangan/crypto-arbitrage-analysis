# Cryptocurrency Arbitrage Detection System
## Bellman-Ford vs Triangle Arbitrage Analysis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive system for detecting and analyzing cryptocurrency arbitrage opportunities using two algorithms: **Bellman-Ford** and **Triangle Arbitrage**.

> ⚠️ **Important Finding**: After 1,644 market scans over 4 days, **zero arbitrage opportunities** were detected. This project demonstrates that retail cryptocurrency arbitrage is not viable in 2026 due to extreme market efficiency. See [Final Report](FINAL_REPORT.md) for full analysis.

---

## 📊 Project Overview

This project compares two algorithmic approaches to cryptocurrency arbitrage detection:

1. **Bellman-Ford Algorithm** - Detects negative cycles in exchange rate graphs (any cycle length)
2. **Triangle Arbitrage** - Tests all 3-currency combinations (fixed 3-trade cycles)

### Key Results

- **1,644 market scans** across 4 days
- **Zero opportunities found** by either algorithm
- **Conclusion**: Modern crypto markets are too efficient for retail arbitrage
- **Value**: Excellent educational project, poor financial strategy

---

## 🎯 Features

### Core Algorithms
- ✅ Bellman-Ford negative cycle detection
- ✅ Triangle arbitrage enumeration
- ✅ Real-time market data from Binance.us
- ✅ Volume and liquidity filtering
- ✅ Fee and slippage estimation

### Data Collection
- ✅ Automated continuous monitoring
- ✅ Scheduled data collection (X times/day for Y days)
- ✅ Batch analysis of historical data
- ✅ Statistical comparison and reporting

### Trading Capabilities
- ✅ Wallet-aware detection (uses actual balances)
- ✅ Auto-execution mode (⚠️ use with caution)
- ✅ Testnet support for safe testing
- ✅ Detailed execution logging

---

## 📁 Repository Structure

```
arbitrage-detection/
├── README.md                           # This file
├── FINAL_REPORT.md                     # Comprehensive analysis report
├── LICENSE                             # MIT License
│
├── Core Detection/
│   ├── algorithm_comparison.py         # Main comparison engine
│   ├── bellman_ford_arbitrage.py       # Bellman-Ford implementation
│   └── triangle_arbitrage.py           # Triangle arbitrage implementation
│
├── Data Collection/
│   ├── data_collector.py               # Automated data collection
│   ├── batch_analysis.py               # Batch statistical analysis
│   └── analyze_results.py              # Individual result analyzer
│
├── Trading/
│   ├── wallet_aware_detector.py        # Wallet-integrated detector
│   ├── auto_executing_monitor.py       # Auto-trading system
│   └── continuous_monitor.py           # Continuous monitoring
│
├── Documentation/
│   ├── ALGORITHM_COMPARISON_GUIDE.md   # Algorithm comparison guide
│   ├── DATA_COLLECTION_GUIDE.md        # Data collection instructions
│   ├── AUTO_EXECUTE_SETUP.md           # Auto-execution setup
│   ├── TROUBLESHOOTING_EXECUTION.md    # Troubleshooting guide
│   └── NEGATIVE_RETURNS_EXPLAINED.md   # Understanding negative returns
│
└── Data/ (not included in repo)
    └── comparison_data/                 # Collected comparison results
        ├── comparison_*.json            # Individual scan results
        ├── collection_log.txt           # Collection log
        └── batch_analysis_summary.txt   # Analysis summary
```

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8 or higher
python3 --version

# Install dependencies
pip install requests --break-system-packages
```

### Option 1: Single Comparison (5 minutes)

```bash
# Run one comparison
python3 algorithm_comparison.py

# View results
cat arbitrage_comparison.json
```

### Option 2: Automated Data Collection (Recommended)

```bash
# Start automated collection
python3 data_collector.py

# Choose mode:
# - Scheduled: 3x/day for 7 days (21 runs)
# - Continuous: Every X minutes
# - Quick test: 3 runs, 5 min apart

# After collection completes:
python3 batch_analysis.py
```

### Option 3: Live Monitoring

```bash
# Detection only (safe)
python3 continuous_monitor.py

# With auto-execution (⚠️ requires API keys)
python3 auto_executing_monitor.py
```

---

## 📈 Algorithms Explained

### Bellman-Ford Algorithm

```python
# How it works:
1. Build graph of exchange rates (negative log transformation)
2. Run Bellman-Ford to find negative cycles
3. Extract profitable arbitrage path
4. Calculate actual profit after fees/slippage

# Example opportunity:
USD → ETH → USDC → BTC → SOL → USD (5 trades)
Theoretical: 2.5% profit
After costs: 0.3% profit
```

**Pros**: Finds any-length cycles, comprehensive search  
**Cons**: More trades = higher costs, complex execution

### Triangle Arbitrage

```python
# How it works:
1. Generate all 3-currency combinations
2. Test each triangle: A → B → C → A
3. Calculate profit for each valid triangle
4. Filter by profitability threshold

# Example opportunity:
BTC → ETH → USDT → BTC (3 trades)
Theoretical: 1.8% profit
After costs: 0.4% profit
```

**Pros**: Simple execution, lower costs (3 trades)  
**Cons**: Misses longer cycles, less comprehensive

---

## 🔧 Configuration

### Detection Parameters

```python
# algorithm_comparison.py

# Currencies to scan
self.whitelist = {
    'BTC', 'ETH', 'USDT', 'USD', 'USDC', 
    'BNB', 'SOL', 'ADA', 'AVAX', ...
}

# Volume filter
self.min_24h_volume_usd = 100000  # $100k minimum

# Profitability thresholds
self.min_profit_threshold = 0.5   # 0.5% minimum
self.max_profit_threshold = 10.0  # 10% maximum (reject as error)

# Cost assumptions
self.trading_fee_rate = 0.001     # 0.1% per trade
self.estimated_slippage_rate = 0.003  # 0.3% per trade
```

### Data Collection Schedule

```python
# data_collector.py

# Scheduled mode
times_per_day = 3  # Scan 3x daily
days = 7           # For 7 days
# Total: 21 comparisons

# Continuous mode
interval_minutes = 60  # Scan every 60 minutes
```

---

## 📊 Results & Findings

### Our Test Results (March 12-16, 2026)

| Metric | Value |
|--------|-------|
| **Total Scans** | 1,644 |
| **Duration** | 4 days (96 hours) |
| **Bellman-Ford Opportunities** | 0 |
| **Triangle Opportunities** | 0 |
| **Winner** | Tie (neither found anything) |

### Why Zero Opportunities?

1. **Market Efficiency**: High-frequency bots eliminate arbitrage in milliseconds
2. **Infrastructure Limitations**: Retail systems too slow (Python, REST API)
3. **Conservative Thresholds**: Required 0.5%+ profit after 1.6% costs
4. **Single Exchange**: Binance.us internal matching prevents inefficiencies

### Key Insights

✅ **Both algorithms work correctly** (validated implementation)  
❌ **No profitable opportunities exist** for retail traders  
📚 **High educational value** despite zero financial returns  
⚠️ **Not recommended** as a money-making strategy

Read the [Full Report](FINAL_REPORT.md) for detailed analysis.

---

## 💻 API Integration

### Binance.us API

```python
# Public endpoints (no authentication)
GET /api/v3/ticker/24hr        # Get all ticker prices
GET /api/v3/exchangeInfo       # Get trading rules

# Private endpoints (requires API key)
GET /api/v3/account            # Get account balances
POST /api/v3/order             # Place order
```

### API Key Setup (Optional)

For wallet-aware detection or auto-execution:

1. Create account on Binance.us
2. Complete KYC verification
3. Generate API keys:
   - Enable "Reading" for detection
   - Enable "Trading" for execution (⚠️ risky)
   - **Never enable "Withdrawals"**
4. Add keys to code:
```python
API_KEY = "your_key_here"
API_SECRET = "your_secret_here"
```

---

## 🎓 Educational Use

This project is excellent for learning:

### Algorithms & Data Structures
- Graph theory (Bellman-Ford)
- Negative cycle detection
- Combinatorial optimization
- Dynamic programming

### Software Engineering
- REST API integration
- Error handling and retries
- Asynchronous data collection
- Batch processing and analysis

### Finance & Trading
- Market microstructure
- Transaction costs (fees, slippage)
- Order book dynamics
- Market efficiency hypothesis

### Data Science
- Statistical analysis
- Time series patterns
- Trend detection
- Batch vs real-time processing

---

## ⚠️ Risks & Disclaimers

### Financial Risks

- ❌ **No profitable opportunities found** in our testing
- ❌ **Market efficiency** eliminates retail arbitrage
- ❌ **Transaction costs** often exceed theoretical profits
- ❌ **Execution risk** (slippage, failed orders, market moves)

### Technical Risks

- ⚠️ API rate limits (can get temporary bans)
- ⚠️ Network failures (lose opportunities mid-execution)
- ⚠️ Bugs in execution logic (could lose money)
- ⚠️ Exchange downtime (stuck mid-cycle)

### Legal & Tax

- 📋 Every trade is a taxable event
- 📋 Must track all transactions for taxes
- 📋 Frequent trading = complex tax reporting
- 📋 Consult tax professional before trading

**DISCLAIMER**: This is educational software. Use at your own risk. No guarantees of profitability. Authors not liable for financial losses.

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Cross-exchange arbitrage (Binance ↔ Coinbase)
- [ ] WebSocket streaming (faster data)
- [ ] C++/Rust implementation (lower latency)
- [ ] Machine learning for pattern detection
- [ ] Visualization tools (graphs, charts)
- [ ] Additional exchanges (Kraken, Gemini)

### How to Contribute

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📚 Documentation

- [📊 Final Report](FINAL_REPORT.md) - Comprehensive analysis of 1,644 scans
- [🔬 Algorithm Comparison Guide](Documentation/ALGORITHM_COMPARISON_GUIDE.md)
- [📅 Data Collection Guide](Documentation/DATA_COLLECTION_GUIDE.md)
- [⚡ Auto-Execution Setup](Documentation/AUTO_EXECUTE_SETUP.md)
- [🔧 Troubleshooting](Documentation/TROUBLESHOOTING_EXECUTION.md)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Binance.us** for providing public API access
- **Richard Bellman & Lester Ford Jr.** for the Bellman-Ford algorithm
- **Cryptocurrency community** for open-source inspiration

---

## 📞 Contact

**Project Author**: [Your Name]  
**Email**: [Your Email]  
**GitHub**: [Your GitHub Profile]

---

## 🎯 Conclusion

### What This Project Proves

✅ **Technical Achievement**: Both algorithms implemented correctly  
✅ **Comprehensive Testing**: 1,644 real market scans  
✅ **Statistical Rigor**: 4-day continuous monitoring  
❌ **Financial Viability**: Zero opportunities found  

### The Bottom Line

**Cryptocurrency arbitrage at retail scale is not viable in 2026.**

But this project still has value as:
- 📚 Educational resource for algorithmic trading
- 💻 Portfolio project demonstrating coding skills
- 🔬 Research into market efficiency
- 🎓 Hands-on learning experience

**Use this code to learn, not to make money.**

---

## 📈 Star History

If you found this project useful for learning, please consider giving it a ⭐!

---

**Last Updated**: March 16, 2026  
**Status**: Complete (no further development planned)  
**Recommendation**: Use for educational purposes only
