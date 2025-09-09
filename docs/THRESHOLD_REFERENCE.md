# 🔧 Risk Assessment Threshold Reference

Complete reference of all numerical thresholds used in the rule-based risk assessment system.

## 📊 Component Weights

```python
RISK_WEIGHTS = {
    "transaction_patterns": 0.25,    # 25%
    "protocol_interactions": 0.30,   # 30%  
    "asset_concentration": 0.20,     # 20%
    "activity_frequency": 0.15,      # 15%
    "failure_rate": 0.10,           # 10%
}
```

## 🎯 Risk Level Boundaries

```python
RISK_LEVELS = {
    "VERY_LOW":   0-20,     # Highly conservative wallet behavior
    "LOW":       20-40,     # Generally safe behavior patterns  
    "MEDIUM":    40-60,     # Some concerning factors
    "HIGH":      60-80,     # Significant caution required
    "VERY_HIGH": 80-100,    # Multiple severe red flags
}
```

---

## 1. 📊 Transaction Pattern Thresholds

### Success Rate Analysis
```python
LOW_SUCCESS_RATE = 0.70        # <70% = +25 penalty
MODERATE_SUCCESS_RATE = 0.85   # <85% = +10 penalty  
HIGH_SUCCESS_RATE = 0.95       # >95% = -10 bonus
```

### Activity Frequency Analysis  
```python
VERY_HIGH_ACTIVITY = 20.0      # >20 tx/day = +15 penalty
HIGH_ACTIVITY = 10.0           # >10 tx/day = +5 penalty
LOW_ACTIVITY = 0.1             # <0.1 tx/day = +15 penalty
NORMAL_ACTIVITY = 1.0-5.0      # 1-5 tx/day = -5 bonus
```

### High-Value Transaction Analysis
```python
VERY_HIGH_VALUE_RATIO = 0.50   # >50% high-value = +15 penalty
HIGH_VALUE_RATIO = 0.30        # >30% high-value = +5 penalty
```

### Contract Interaction Analysis
```python
VERY_HIGH_CONTRACT_RATIO = 0.90  # >90% contracts = +15 penalty
HIGH_CONTRACT_RATIO = 0.70       # >70% contracts = +5 penalty  
LOW_CONTRACT_RATIO = 0.10        # <10% contracts = -5 bonus
```

### Recent Activity Analysis
```python
INACTIVE_DAYS = 30             # 0 tx in 30 days = +20 penalty
RECENT_ACTIVITY_THRESHOLD = 50 # >50 recent tx = +10 penalty
```

### Gas Usage Analysis
```python
HIGH_GAS_PRICE = 100.0         # >100 Gwei = +10 penalty
```

### Address Diversity Analysis
```python
LOW_ADDRESS_DIVERSITY = 0.10   # <10% diversity = +10 penalty
```

---

## 2. 🏦 Protocol Risk Thresholds

### Diversification Analysis
```python
SINGLE_PROTOCOL_PENALTY = 15      # 1 category = +15 penalty
LOW_DIVERSIFICATION_PENALTY = 5   # <3 categories = +5 penalty
DIVERSIFICATION_BONUS = 10        # ≥3 categories = -10 bonus  
LOW_DIVERSIFICATION_THRESHOLD = 3
```

### TVL Analysis (USD)
```python
VERY_HIGH_TVL = 50_000_000_000    # $50B+ = -15 bonus
HIGH_TVL = 10_000_000_000         # $10B+ = -10 bonus
MEDIUM_TVL = 1_000_000_000        # $1B+ = -5 bonus
LOW_TVL = 100_000_000             # <$100M = +15 penalty
```

### Risk Distribution Analysis
```python
VERY_HIGH_RISK_PENALTY = 5        # +5 per very high-risk protocol
```

---

## 3. 💰 Asset Concentration Thresholds

### Diversification Analysis
```python
SINGLE_TOKEN_PENALTY = 20           # 1 token = +20 penalty
LOW_DIVERSIFICATION_PENALTY = 10    # <3 tokens = +10 penalty
GOOD_DIVERSIFICATION_BONUS = 5      # <10 tokens = -5 bonus
HIGH_DIVERSIFICATION_BONUS = 10     # ≥10 tokens = -10 bonus
LOW_DIVERSIFICATION_COUNT = 3
GOOD_DIVERSIFICATION_COUNT = 10
```

### ETH Holdings Analysis (ETH)
```python
VERY_LARGE_ETH_HOLDINGS = 1000.0    # >1000 ETH = +25 penalty
LARGE_ETH_HOLDINGS = 100.0          # >100 ETH = +15 penalty  
SIGNIFICANT_ETH_HOLDINGS = 10.0     # >10 ETH = +5 penalty
VERY_LOW_ETH_BALANCE = 0.01         # <0.01 ETH = +10 penalty
```

### Stablecoin Analysis
```python
STABLECOIN_BONUS_PER_TOKEN = 5      # -5 bonus per stablecoin
STABLECOIN_BONUS_MAX = 15           # Max -15 total bonus
```

### Stablecoin Symbols
```python
STABLECOIN_SYMBOLS = [
    "usdt", "usdc", "dai", "busd", 
    "frax", "tusd", "usdp", "gusd"
]
```

---

## 4. 🎭 Behavioral Pattern Thresholds

### Gas Usage Analysis (Gwei)
```python
VERY_HIGH_GAS_PRICE = 200.0     # >200 Gwei = +20 penalty
HIGH_GAS_PRICE = 100.0          # >100 Gwei = +10 penalty
LOW_GAS_PRICE = 20.0            # <20 Gwei = -5 bonus
```

### Value Flow Analysis (Ratios)
```python
HEAVY_OUTFLOW_RATIO = 3.0       # Outflow > 3x Inflow = +20 penalty
MODERATE_OUTFLOW_RATIO = 1.5    # Outflow > 1.5x Inflow = +5 penalty
ACCUMULATION_RATIO = 2.0        # Inflow > 2x Outflow = -5 bonus
```

### Transaction Size Analysis (ETH)
```python
VERY_LARGE_TRANSACTION = 100.0  # >100 ETH = +15 penalty
LARGE_TRANSACTION = 10.0        # >10 ETH = +5 penalty
```

### Interaction Diversity Analysis
```python
VERY_CONCENTRATED_INTERACTIONS = 0.10  # <10% = +15 penalty
CONCENTRATED_INTERACTIONS = 0.30       # <30% = +5 penalty  
DIVERSE_INTERACTIONS = 0.70            # >70% = -5 bonus
```

### Wallet Lifecycle Analysis (Days)
```python
VERY_NEW_WALLET_DAYS = 30       # <30 days = +15 penalty
NEW_WALLET_DAYS = 90            # <90 days = +5 penalty
OLD_WALLET_DAYS = 730           # >730 days (2 years) = -10 bonus
```

---

## 5. 🤖 LLM Configuration

### Gemini AI Settings
```python
LLM_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 0.1,
    "max_output_tokens": 500,
    "timeout_seconds": 30,
    "rule_based_weight": 0.6,      # 60% rule-based
    "llm_weight": 0.4,             # 40% AI-based
}
```

---

## 📈 Penalty/Bonus Summary

### High Impact Changes (≥15 points)
```
+25: Very low transaction success rate (<70%)
+20: Single token concentration  
+20: No recent activity (inactive wallet)
+20: Very high gas usage (>200 Gwei)
+20: Heavy fund outflow (>3x inflow)
+15: Very high activity (>20 tx/day)
+15: Very low activity (<0.1 tx/day)
+15: Very high DeFi usage (>90% contracts)
+15: Very high value tx ratio (>50%)
+15: Single protocol category
+15: Low TVL protocols (<$100M)
+15: Very large ETH holdings (>1000 ETH)
+15: Very concentrated interactions (<10%)
+15: Very new wallet (<30 days)
+15: Very large transaction (>100 ETH)
-15: ETH-only portfolio (conservative)
-15: Very high TVL protocols (>$50B)
-15: High diversification (≥10 tokens)
```

### Medium Impact Changes (5-14 points)
```
+10: Moderate success rate (<85%)
+10: High activity (>10 tx/day)
+10: High DeFi usage (>70% contracts)
+10: High gas usage (>100 Gwei)
+10: Large ETH holdings (>100 ETH)
+10: Very low ETH balance (<0.01 ETH)
+10: Very active recently (>50 txs)
+10: Low address diversity (<10%)
+10: Low diversification (<3 tokens)
-10: High success rate (>95%)
-10: Diversification bonus (≥3 categories)
-10: High TVL protocols (>$10B)
-10: Old wallet (>2 years)
```

### Low Impact Changes (≤5 points)
```
+5: Various moderate risk factors
-5: Various low-risk bonuses
```

---

## ⚙️ Configuration File Locations

- **Main Config**: `services/risk_scoring/config.py`
- **Component Configs**: Individual analyzer classes
- **LLM Config**: `services/risk_scoring/llm/gemini_client.py`

## 🔧 Modifying Thresholds

To adjust thresholds:
1. Edit `services/risk_scoring/config.py`
2. Update relevant `*_THRESHOLDS` dictionaries
3. Restart the application
4. Test with known wallets to validate changes

---

**⚠️ Important**: Threshold changes can significantly impact risk scores. Always test changes thoroughly before production deployment.
