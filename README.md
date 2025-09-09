# 🛡️ Nuvolari Safe Score - Advanced Cryptocurrency Wallet Risk Assessment

A comprehensive, modular risk assessment framework for cryptocurrency wallets that combines rule-based analysis with AI-powered insights to provide detailed wallet safety evaluations.

## 🎯 Features

### Multi-Component Risk Analysis
- **Transaction Pattern Analysis** - Evaluates transaction behavior, success rates, and activity patterns
- **Protocol Risk Assessment** - Analyzes DeFi protocol interactions and associated risks  
- **Asset Concentration Analysis** - Assesses portfolio diversification and concentration risks
- **Behavioral Pattern Analysis** - Examines wallet behavioral patterns and lifecycle

### Advanced Scoring Methods
- **Rule-Based Scoring** - Traditional algorithmic risk assessment
- **AI-Powered Analysis** - Google Gemini integration for intelligent risk insights
- **Hybrid Scoring** - Combines rule-based and AI methods for optimal accuracy

### Comprehensive Data Sources
- **Etherscan Integration** - Real-time Ethereum transaction data
- **QuickNode Integration** - Enhanced blockchain data access
- **DefiLlama Integration** - DeFi protocol TVL and risk data

## 🏗️ Architecture

```
services/
├── risk_scoring/              # Modular risk scoring system
│   ├── __init__.py           # Main exports and version info
│   ├── core.py               # Main orchestrator engine
│   ├── config.py             # Configuration constants
│   ├── components/           # Individual risk analyzers
│   │   ├── transaction_patterns.py
│   │   ├── protocol_risk.py
│   │   ├── asset_concentration.py
│   │   └── behavioral_patterns.py
│   ├── llm/                  # AI integration
│   │   └── gemini_client.py
│   └── utils/                # Utility functions
│       ├── risk_levels.py
│       └── recommendations.py
├── risk_agent.py             # Main analysis orchestrator
├── defillama_client.py       # DeFi protocol data
├── Etherscan_client.py       # Ethereum transaction data
└── QuickNode_client.py       # Enhanced blockchain access
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd nuvolari_safe_score

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
# Required
ETHERSCAN_API_KEY=your_etherscan_api_key

# Optional (enables AI analysis)
GEMINI_API_KEY=your_google_gemini_api_key

# Optional (for enhanced data)
QUICKNODE_API_KEY=your_quicknode_api_key
```

### Basic Usage

```python
from services.risk_scoring import RiskScoringEngine
from services.risk_agent import analyze_wallet_comprehensive

# Simple usage with the main agent
results = analyze_wallet_comprehensive("0x742d35Cc6676C5F1E3dDD3e2bFE32cE1579e8894")

# Advanced usage with direct engine access
engine = RiskScoringEngine()
risk_results = engine.calculate_overall_risk_score(
    patterns=transaction_patterns,
    protocol_analysis=protocol_data,
    balances=balance_data
)

print(f"Risk Level: {risk_results['risk_level']}")
print(f"Overall Score: {risk_results['overall_risk_score']}/100")
```

## 📊 Risk Analysis Components

### 1. Transaction Pattern Analysis (25% weight)
- Transaction success rates
- Activity frequency patterns
- High-value transaction ratios
- Smart contract interaction patterns
- Recent activity levels
- Gas usage efficiency
- Address interaction diversity

### 2. Protocol Risk Assessment (30% weight)
- DeFi protocol identification and risk scoring
- TVL (Total Value Locked) analysis
- Protocol diversification assessment
- High-risk protocol exposure
- Protocol concentration penalties

### 3. Asset Concentration Analysis (20% weight)
- Portfolio diversification evaluation
- ETH holdings size analysis (whale risk)
- Token count and distribution
- Stablecoin exposure benefits
- Asset concentration penalties

### 4. Behavioral Pattern Analysis (25% weight)
- Gas price usage patterns
- Value flow analysis (accumulation vs distribution)
- Transaction size patterns
- Address interaction diversity
- Wallet age and lifecycle analysis

## 🤖 AI Integration

The system optionally integrates with Google Gemini for enhanced analysis:

- **Contextual Analysis** - AI evaluates wallet patterns in context
- **Insight Generation** - Provides human-readable risk reasoning
- **Component Scoring** - AI-powered component risk assessment
- **Hybrid Results** - Combines AI insights with rule-based analysis (60% rules + 40% AI)

## 📈 Scoring System

### Risk Levels
- **VERY_LOW** (0-20): Very low risk, highly conservative wallet behavior
- **LOW** (20-40): Low risk with generally safe behavior patterns
- **MEDIUM** (40-60): Medium risk with some concerning factors
- **HIGH** (60-80): High-risk wallet requiring significant caution
- **VERY_HIGH** (80-100): Extremely risky wallet with multiple severe red flags

### Output Structure
```json
{
  "overall_risk_score": 45.2,
  "risk_level": "MEDIUM",
  "component_scores": {
    "transaction_patterns": 38.5,
    "protocol_interactions": 52.1,
    "asset_concentration": 41.8,
    "behavioral_patterns": 48.3
  },
  "scoring_methods": {
    "rule_based": { "overall_score": 47.1 },
    "llm_based": { "overall_score": 42.8 },
    "hybrid": { "overall_score": 45.2 }
  },
  "recommendations": [
    "✅ LOW RISK: Generally safe wallet with conservative behavior",
    "🏦 Protocol Risk: Consider protocol diversification"
  ]
}
```

## 🔧 Configuration

### Risk Weights
Adjust component weights in `services/risk_scoring/config.py`:

```python
RISK_WEIGHTS = {
    "transaction_patterns": 0.25,
    "protocol_interactions": 0.30,
    "asset_concentration": 0.20,
    "activity_frequency": 0.15,
    "failure_rate": 0.10,
}
```

### Thresholds
Fine-tune risk thresholds for each component in the configuration files.

## 📚 Documentation

### 📋 Rule-Based Analysis Documentation
- **[Complete Assumptions & Edge Cases](docs/RULE_BASED_ASSUMPTIONS.md)** - Comprehensive analysis of all rule-based assumptions and their limitations
- **[Quick Reference Summary](docs/ASSUMPTIONS_SUMMARY.md)** - Concise overview of key assumptions and critical edge cases  
- **[Threshold Reference](docs/THRESHOLD_REFERENCE.md)** - Complete list of all numerical thresholds and configuration values

### 🧠 Machine Learning Enhancement Strategy
- **[ML Improvement Strategy](docs/ML_IMPROVEMENT_STRATEGY.md)** - Comprehensive ML roadmap to address edge cases and false positives
- **[System Architecture](docs/SYSTEM_ARCHITECTURE.md)** - Advanced ML-enhanced architecture with deployment strategies
- **[Algorithm Selection Guide](docs/ALGORITHM_SELECTION_GUIDE.md)** - Detailed algorithm analysis and implementation specifications

### 🔧 API Reference

#### `RiskScoringEngine`
Main orchestrator that coordinates all risk analysis components.

```python
engine = RiskScoringEngine()
results = engine.calculate_overall_risk_score(patterns, protocol_analysis, balances)
```

#### Individual Analyzers
```python
from services.risk_scoring.components import (
    TransactionPatternAnalyzer,
    ProtocolRiskAnalyzer,
    AssetConcentrationAnalyzer,
    BehavioralPatternAnalyzer
)
```

#### AI Integration
```python
from services.risk_scoring.llm import GeminiRiskAnalyzer

gemini = GeminiRiskAnalyzer()
ai_results = gemini.analyze_wallet_risk(patterns, protocol_analysis, balances)
```

## 🧪 Testing

```bash
# Run comprehensive wallet analysis
python services/risk_agent.py

# Test individual components
python test_risk_agent.py

# Test specific wallet
python -c "from services.risk_agent import analyze_wallet_comprehensive; print(analyze_wallet_comprehensive('0x742d35Cc6676C5F1E3dDD3e2bFE32cE1579e8894'))"
```

## 🔄 Migration from Legacy System

The system maintains backward compatibility with the original `risk_scoring_engine.py`:

```python
# Legacy usage (deprecated but still works)
from services.risk_scoring_engine import RiskScoringEngine

# New recommended usage
from services.risk_scoring import RiskScoringEngine
```

## 🛠️ Development

### Adding New Risk Components

1. Create new analyzer in `services/risk_scoring/components/`
2. Follow the interface pattern: `calculate_risk(data) -> Dict[str, Any]`
3. Add to `components/__init__.py` exports
4. Integrate in `core.py` orchestrator
5. Update configuration weights

### Extending AI Integration

1. Add new LLM provider in `services/risk_scoring/llm/`
2. Implement the `analyze_wallet_risk()` interface
3. Update core engine to support multiple AI providers

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for complete dependency list
- API keys for data sources (Etherscan required, others optional)

**⚡ Built for comprehensive wallet risk assessment with modern, modular architecture and AI-powered insights.**
