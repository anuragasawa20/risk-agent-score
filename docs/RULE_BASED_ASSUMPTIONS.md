# 📋 Rule-Based Risk Analysis Assumptions & Edge Cases

This document comprehensively outlines all rule-based assumptions made in the Nuvolari Safe Score risk assessment system, along with their potential edge cases and limitations.

## 🏗️ System Architecture

### Overall Scoring Methodology
- **Base Risk Score**: Each component starts with a base score of 50/100
- **Weighted Combination**: Component scores are weighted and combined
- **Score Range**: Final scores are clamped between 0-100

**Weights Distribution:**
```
Transaction Patterns: 25%
Protocol Interactions: 30%
Asset Concentration: 20%
Activity Frequency: 15%
Failure Rate: 10%
```

---

## 1. 📊 Transaction Pattern Analysis (25% Weight)

### Core Assumptions

#### 1.1 Success Rate Analysis
**Assumption**: Higher transaction success rates indicate safer, more experienced users.

**Rules:**
- Success Rate < 70% → +25 risk penalty ("Low success rate")
- Success Rate < 85% → +10 risk penalty ("Moderate success rate")  
- Success Rate > 95% → -10 risk bonus ("High success rate")

**Rationale**: Failed transactions suggest poor planning, insufficient funds, or interaction with problematic contracts.

**Edge Cases & Limitations:**
- ❌ **New Users**: Legitimate new users learning DeFi may have lower success rates
- ❌ **Network Congestion**: High gas periods cause legitimate transactions to fail
- ❌ **MEV/Arbitrage**: Professional traders may accept higher failure rates for profit opportunities
- ❌ **Experimental Activity**: Power users testing new protocols may have lower success rates
- ❌ **Gas Estimation Issues**: Some wallets/interfaces have poor gas estimation

#### 1.2 Activity Frequency Analysis
**Assumption**: Extremely high or extremely low activity indicates higher risk.

**Rules:**
- Frequency > 20 tx/day → +15 risk penalty ("Very high activity")
- Frequency > 10 tx/day → +5 risk penalty ("High activity")
- Frequency < 0.1 tx/day → +15 risk penalty ("Very low activity")
- 1-5 tx/day → -5 risk bonus ("Normal activity")

**Rationale**: Very high activity suggests bot activity or desperate trading; very low activity suggests abandoned wallets.

**Edge Cases & Limitations:**
- ❌ **Professional Traders**: Legitimate high-frequency traders flagged as risky
- ❌ **Arbitrage Bots**: Legitimate MEV/arbitrage operations penalized
- ❌ **Seasonal Activity**: Users with seasonal DeFi participation patterns
- ❌ **Batch Operations**: Smart contract interactions creating burst activity
- ❌ **HODLers**: Long-term holders unfairly penalized for low activity
- ❌ **Multi-Wallet Users**: Users spreading activity across multiple wallets

#### 1.3 High-Value Transaction Analysis
**Assumption**: High proportion of high-value transactions indicates higher risk.

**Rules:**
- High-value ratio > 50% → +15 risk penalty
- High-value ratio > 30% → +5 risk penalty

**Rationale**: Many high-value transactions suggest whale activity or suspicious fund movement.

**Edge Cases & Limitations:**
- ❌ **Institutional Users**: Large institutions conducting legitimate business
- ❌ **Whale Traders**: Legitimate large-scale traders
- ❌ **Real Estate/NFT**: Large legitimate purchases
- ❌ **DeFi Yield Farming**: Large capital deployment in farming strategies
- ❌ **Threshold Definition**: "High-value" threshold may not adjust for market conditions

#### 1.4 Smart Contract Interaction Analysis
**Assumption**: Very high contract interaction ratios suggest higher risk exposure.

**Rules:**
- Contract ratio > 90% → +15 risk penalty ("Very high DeFi usage")
- Contract ratio > 70% → +5 risk penalty ("High DeFi usage")
- Contract ratio < 10% → -5 risk bonus ("Low DeFi usage")

**Rationale**: Heavy DeFi usage exposes users to smart contract risks.

**Edge Cases & Limitations:**
- ❌ **DeFi Power Users**: Experienced DeFi users unfairly penalized
- ❌ **Yield Farmers**: Professional yield farming strategies
- ❌ **Protocol Developers**: Developers testing contracts
- ❌ **DeFi Integrators**: Services requiring many contract interactions
- ❌ **GameFi Users**: Gaming protocols requiring frequent interactions

#### 1.5 Recent Activity Analysis
**Assumption**: No recent activity in active wallets suggests abandonment or compromise.

**Rules:**
- 0 transactions in 30 days (for wallets with >10 historical transactions) → +20 risk penalty
- >50 recent transactions → +10 risk penalty

**Edge Cases & Limitations:**
- ❌ **Seasonal Users**: Users with cyclical activity patterns
- ❌ **Market Timing**: Users waiting for better market conditions
- ❌ **HODLers**: Long-term holders with infrequent activity
- ❌ **Multi-Wallet Rotation**: Users rotating between different wallets
- ❌ **Regulatory Concerns**: Users pausing activity due to regulatory uncertainty

#### 1.6 Gas Price Analysis
**Assumption**: Consistently high gas prices suggest desperate or risky behavior.

**Rules:**
- Average gas > 100 Gwei → +10 risk penalty

**Edge Cases & Limitations:**
- ❌ **Network Congestion**: Users forced to pay high gas during congestion
- ❌ **Time-Sensitive Operations**: Legitimate urgent transactions
- ❌ **MEV Protection**: Users paying higher gas for MEV protection
- ❌ **Arbitrage Opportunities**: Time-sensitive arbitrage requiring high gas
- ❌ **Gas Token Usage**: Historical gas token redemptions

#### 1.7 Address Diversity Analysis
**Assumption**: Low address diversity suggests concentrated, potentially risky interactions.

**Rules:**
- Address diversity < 10% → +10 risk penalty

**Edge Cases & Limitations:**
- ❌ **Protocol Loyalty**: Users preferring specific trusted protocols
- ❌ **Automated Strategies**: Bots interacting with limited contract sets
- ❌ **Yield Farming**: Focused farming strategies
- ❌ **Recurring Payments**: Legitimate recurring payment patterns

---

## 2. 🏦 Protocol Risk Assessment (30% Weight)

### Core Assumptions

#### 2.1 Protocol Risk Scoring
**Assumption**: Protocols can be assigned risk scores based on TVL, audits, and age.

**Rules:**
- Base risk = average protocol risk score
- Interaction with high-risk protocols adds penalty

**Edge Cases & Limitations:**
- ❌ **New Innovation**: New protocols may be high-risk but innovative
- ❌ **Risk Score Accuracy**: Protocol risk scoring methodology may be flawed
- ❌ **Temporal Changes**: Protocol risk changes over time
- ❌ **Subjective Metrics**: Risk assessment involves subjective elements

#### 2.2 Diversification Analysis
**Assumption**: Protocol diversification reduces risk through spreading exposure.

**Rules:**
- Single protocol category → +15 risk penalty
- <3 categories → +5 risk penalty  
- ≥3 categories → -10 risk bonus

**Edge Cases & Limitations:**
- ❌ **Specialization Strategy**: Users specializing in specific protocol types
- ❌ **Risk Correlation**: Different protocols may have correlated risks
- ❌ **Category Definitions**: Protocol categorization may be arbitrary
- ❌ **Forced Specialization**: Some strategies require protocol focus

#### 2.3 TVL (Total Value Locked) Analysis
**Assumption**: Higher TVL protocols are generally safer and more established.

**Rules:**
- TVL > $50B → -15 risk bonus
- TVL > $10B → -10 risk bonus  
- TVL > $1B → -5 risk bonus
- TVL < $100M → +15 risk penalty

**Edge Cases & Limitations:**
- ❌ **TVL Manipulation**: TVL can be artificially inflated
- ❌ **New Protocols**: High-quality new protocols start with low TVL
- ❌ **Market Cycles**: TVL fluctuates with market conditions
- ❌ **Protocol Utility**: Some protocols don't require high TVL
- ❌ **TVL Concentration**: High TVL may indicate concentration risk

#### 2.4 Risk Distribution Analysis
**Assumption**: Interaction with "very high risk" protocols is particularly dangerous.

**Rules:**
- Each very high-risk protocol → +5 risk penalty

**Edge Cases & Limitations:**
- ❌ **Risk Classification**: "Very high risk" classification may be incorrect
- ❌ **Experimental Protocols**: Users testing new innovations
- ❌ **Risk/Reward Trade-offs**: High-risk protocols may offer proportional rewards
- ❌ **Time-Sensitive Opportunities**: Brief interactions for specific opportunities

---

## 3. 💰 Asset Concentration Analysis (20% Weight)

### Core Assumptions

#### 3.1 Portfolio Diversification Analysis
**Assumption**: Diversified portfolios are safer than concentrated ones.

**Rules:**
- 0 tokens (ETH only) → -15 risk bonus (if ETH > 0)
- 0 assets → +30 risk penalty
- 1 token → +20 risk penalty ("Single token concentration")
- <3 tokens → +10 risk penalty ("Low diversification")
- <10 tokens → -5 risk bonus ("Good diversification")
- ≥10 tokens → -10 risk bonus ("High diversification")

**Edge Cases & Limitations:**
- ❌ **Strategic Concentration**: Intentional concentration in high-conviction assets
- ❌ **ETH Maximalism**: Legitimate preference for ETH-only exposure
- ❌ **Market Conditions**: Bear market conditions may favor concentration
- ❌ **Gas Efficiency**: Managing fewer tokens is more gas-efficient
- ❌ **Quality vs Quantity**: Few high-quality assets vs many low-quality ones

#### 3.2 ETH Holdings Size Analysis (Whale Risk)
**Assumption**: Very large ETH holdings create whale risk and attack vectors.

**Rules:**
- >1000 ETH → +25 risk penalty ("Very large ETH holdings")
- >100 ETH → +15 risk penalty ("Large ETH holdings")
- >10 ETH → +5 risk penalty ("Significant ETH holdings")
- <0.01 ETH → +10 risk penalty ("Very low ETH balance")

**Edge Cases & Limitations:**
- ❌ **Institutional Holdings**: Legitimate institutional ETH holdings
- ❌ **Staking Operations**: ETH held for staking purposes
- ❌ **Market Making**: ETH held for market making activities
- ❌ **Price Appreciation**: Holdings that grew due to price appreciation
- ❌ **Multi-Sig Operations**: Shared custody arrangements
- ❌ **Threshold Relativity**: Fixed thresholds don't adjust for market conditions

#### 3.3 Stablecoin Holdings Analysis
**Assumption**: Stablecoin holdings reduce portfolio risk.

**Rules:**
- Each stablecoin → -5 risk bonus (max -15 total)

**Edge Cases & Limitations:**
- ❌ **Stablecoin Risk**: Stablecoins have their own risks (depeg, regulatory)
- ❌ **Centralized Stablecoins**: USDC/USDT have centralization risks
- ❌ **Yield Farming**: Stablecoins used in risky yield farming
- ❌ **Market Timing**: Stablecoins held during market uncertainty
- ❌ **Stablecoin Quality**: Not all stablecoins are equally stable

---

## 4. 🎭 Behavioral Pattern Analysis (25% Weight)

### Core Assumptions

#### 4.1 Gas Usage Pattern Analysis
**Assumption**: Extreme gas usage patterns indicate risky or desperate behavior.

**Rules:**
- Average gas > 200 Gwei → +20 risk penalty ("Very high gas usage")
- Average gas > 100 Gwei → +10 risk penalty ("High gas usage")
- Average gas < 20 Gwei → -5 risk bonus ("Efficient gas usage")

**Edge Cases & Limitations:**
- ❌ **Network Conditions**: Gas prices vary significantly with network congestion
- ❌ **Time-Sensitive Operations**: Legitimate urgent transactions requiring high gas
- ❌ **MEV Protection**: Paying premium gas for MEV protection
- ❌ **Historical Bias**: Past gas usage may not reflect current behavior
- ❌ **Wallet Gas Settings**: Some wallets have poor gas estimation defaults

#### 4.2 Value Flow Analysis
**Assumption**: Heavy outflows suggest fund drainage or liquidation pressure.

**Rules:**
- Outflow > 3x Inflow → +20 risk penalty ("Heavy fund outflow")
- Outflow > 1.5x Inflow → +5 risk penalty ("Moderate outflow")
- Inflow > 2x Outflow → -5 risk bonus ("Accumulation pattern")

**Edge Cases & Limitations:**
- ❌ **Profit Taking**: Legitimate profit realization during bull markets
- ❌ **Rebalancing**: Portfolio rebalancing operations
- ❌ **Investment Strategies**: DCA or systematic investment strategies
- ❌ **Liquidity Provision**: Adding/removing liquidity from pools
- ❌ **Multi-Wallet Management**: Moving funds between personal wallets

#### 4.3 Transaction Size Analysis
**Assumption**: Very large transactions indicate higher risk exposure.

**Rules:**
- Largest transaction > 100 ETH → +15 risk penalty ("Very large transaction")
- Largest transaction > 10 ETH → +5 risk penalty ("Large transaction")

**Edge Cases & Limitations:**
- ❌ **Legitimate Large Transactions**: House purchases, business transactions
- ❌ **Institutional Operations**: Corporate treasury management
- ❌ **Arbitrage Operations**: Large-scale arbitrage requiring significant capital
- ❌ **Liquidity Provision**: Large LP positions
- ❌ **Price Appreciation**: Transactions that became large due to price increases

#### 4.4 Interaction Diversity Analysis
**Assumption**: Low interaction diversity suggests concentrated, potentially risky behavior.

**Rules:**
- Diversity ratio < 10% → +15 risk penalty ("Very concentrated interactions")
- Diversity ratio < 30% → +5 risk penalty ("Somewhat concentrated")
- Diversity ratio > 70% → -5 risk bonus ("Diverse interactions")

**Edge Cases & Limitations:**
- ❌ **Protocol Specialization**: Users specializing in specific protocols
- ❌ **Automated Strategies**: Bots with focused interaction patterns
- ❌ **Recurring Operations**: Legitimate recurring transaction patterns
- ❌ **Preferred Protocols**: Users sticking to trusted, familiar protocols

#### 4.5 Wallet Lifecycle Analysis
**Assumption**: Very new wallets are riskier due to lack of established patterns.

**Rules:**
- Age < 30 days → +15 risk penalty ("Very new wallet")
- Age < 90 days → +5 risk penalty ("New wallet")
- Age > 2 years → -10 risk bonus ("Established wallet")

**Edge Cases & Limitations:**
- ❌ **Privacy Practices**: Experienced users creating new wallets for privacy
- ❌ **Wallet Migration**: Users migrating from old to new wallets
- ❌ **Multi-Wallet Strategies**: Users employing multiple wallets for different purposes
- ❌ **Security Practices**: Regular wallet rotation for security
- ❌ **Platform-Specific Wallets**: Creating wallets for specific platforms/purposes

---

## 🚨 System-Wide Edge Cases & Limitations

### 1. Context Insensitivity
- **Market Conditions**: Rules don't adjust for bull/bear market conditions
- **Network State**: Ethereum network congestion not factored into scoring
- **Temporal Context**: Historical vs current behavior not weighted differently
- **Regulatory Environment**: Changing regulatory landscape not considered

### 2. User Archetype Bias
- **Professional Traders**: Many legitimate professional behaviors flagged as risky
- **Institutional Users**: Corporate/institutional patterns differ from retail expectations
- **Privacy-Conscious Users**: Privacy practices may trigger false positives
- **Multi-Wallet Users**: Sophisticated users with multiple wallet strategies
- **International Users**: Different usage patterns across jurisdictions

### 3. Technical Limitations
- **Data Quality**: Relies on accurate and complete blockchain data
- **Protocol Recognition**: May not recognize new or niche protocols
- **Transaction Parsing**: Complex transactions may be misinterpreted
- **MEV Activity**: MEV-related activities may be misclassified

### 4. Threshold Rigidity
- **Fixed Thresholds**: Most thresholds are static and don't adapt to market conditions
- **Binary Classifications**: Many rules use binary high/low classifications
- **Relative vs Absolute**: Most measures are absolute rather than relative to peer groups
- **Currency Fluctuations**: ETH-denominated thresholds don't adjust for price changes

### 5. Behavioral Model Assumptions
- **Rational Actor Model**: Assumes users always act rationally
- **Risk Aversion**: Assumes lower risk is always better
- **Western Financial Models**: Biased toward Western financial behavior patterns
- **Individual vs Institutional**: Doesn't distinguish between individual and institutional users

### 6. Data Completeness
- **Off-Chain Activity**: Cannot see centralized exchange interactions
- **Cross-Chain Activity**: Limited visibility into other blockchain activity  
- **Private Transactions**: Cannot analyze privacy-focused transaction methods
- **Layer 2 Activity**: Limited visibility into L2 transaction patterns

---

## 🔧 Recommendations for Improvement

### 1. Dynamic Thresholds
- Implement market-condition-aware thresholds
- Use percentile-based scoring relative to peer groups
- Adjust thresholds based on network conditions

### 2. User Archetypes
- Develop scoring models for different user types
- Implement machine learning to identify user patterns
- Create institutional vs retail user classifications

### 3. Contextual Analysis
- Factor in market conditions and timing
- Consider transaction sequencing and patterns
- Implement temporal weighting of historical behavior

### 4. Enhanced Data Sources
- Integrate additional on-chain data sources
- Include cross-chain activity analysis
- Incorporate off-chain reputation signals

### 5. Probabilistic Scoring
- Move from binary to probabilistic risk assessments
- Implement confidence intervals for risk scores
- Provide uncertainty quantification

---

## 📊 Impact Assessment Matrix

| Risk Category | False Positive Risk | False Negative Risk | Severity |
|---------------|-------------------|-------------------|----------|
| Professional Traders | HIGH | LOW | MEDIUM |
| New Users | HIGH | MEDIUM | HIGH |
| Institutional Users | HIGH | LOW | HIGH |
| Privacy Users | MEDIUM | HIGH | MEDIUM |
| Seasonal Users | MEDIUM | LOW | LOW |
| Multi-Wallet Users | HIGH | MEDIUM | MEDIUM |
| MEV/Arbitrage | HIGH | LOW | LOW |
| Whale Users | MEDIUM | LOW | MEDIUM |

This comprehensive analysis provides the foundation for understanding and improving the rule-based risk assessment system while acknowledging its current limitations and edge cases.
