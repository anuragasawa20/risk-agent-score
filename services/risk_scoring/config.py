"""
Risk Scoring Configuration
Contains all configuration constants and thresholds used across the risk scoring system.
"""

# Risk component weights (must sum to 1.0)
RISK_WEIGHTS = {
    "transaction_patterns": 0.25,  # Transaction behavior analysis
    "protocol_interactions": 0.30,  # DeFi protocol risk assessment
    "asset_concentration": 0.20,  # Portfolio diversification
    "activity_frequency": 0.15,  # Activity and behavioral patterns
    "failure_rate": 0.10,  # Transaction failure patterns
}

# Risk thresholds for different categories
RISK_THRESHOLDS = {
    "very_low": 20,
    "low": 40,
    "medium": 60,
    "high": 80,
    "very_high": 100,
}

# Transaction pattern analysis thresholds
TRANSACTION_THRESHOLDS = {
    "low_success_rate": 0.7,
    "moderate_success_rate": 0.85,
    "high_success_rate": 0.95,
    "high_activity_frequency": 10.0,
    "very_high_activity_frequency": 20.0,
    "low_activity_frequency": 0.1,
    "high_value_tx_ratio": 0.3,
    "very_high_value_tx_ratio": 0.5,
    "high_contract_ratio": 0.7,
    "very_high_contract_ratio": 0.9,
    "low_contract_ratio": 0.1,
    "recent_activity_threshold": 50,
    "inactive_days": 30,
    "high_gas_price": 100.0,
    "very_high_gas_price": 200.0,
    "low_address_diversity": 0.1,
}

# Protocol risk thresholds
PROTOCOL_THRESHOLDS = {
    "single_protocol_penalty": 15,
    "low_diversification_penalty": 5,
    "diversification_bonus": 10,
    "low_diversification_threshold": 3,
    "very_high_tvl": 50_000_000_000,  # $50B
    "high_tvl": 10_000_000_000,  # $10B
    "medium_tvl": 1_000_000_000,  # $1B
    "low_tvl": 100_000_000,  # $100M
    "very_high_tvl_bonus": 15,
    "high_tvl_bonus": 10,
    "medium_tvl_bonus": 5,
    "low_tvl_penalty": 15,
    "very_high_risk_penalty": 5,
}

# Asset concentration thresholds
ASSET_THRESHOLDS = {
    "single_token_penalty": 20,
    "low_diversification_penalty": 10,
    "good_diversification_bonus": 5,
    "high_diversification_bonus": 10,
    "low_diversification_count": 3,
    "good_diversification_count": 10,
    "very_large_eth_holdings": 1000.0,  # ETH
    "large_eth_holdings": 100.0,  # ETH
    "significant_eth_holdings": 10.0,  # ETH
    "very_low_eth_balance": 0.01,  # ETH
    "very_large_eth_penalty": 25,
    "large_eth_penalty": 15,
    "significant_eth_penalty": 5,
    "very_low_eth_penalty": 10,
    "stablecoin_bonus_max": 15,
    "stablecoin_bonus_per_token": 5,
}

# Behavioral pattern thresholds
BEHAVIORAL_THRESHOLDS = {
    "very_high_gas_price": 200.0,  # Gwei
    "high_gas_price": 100.0,  # Gwei
    "low_gas_price": 20.0,  # Gwei
    "very_high_gas_penalty": 20,
    "high_gas_penalty": 10,
    "low_gas_bonus": 5,
    "heavy_outflow_ratio": 3.0,
    "moderate_outflow_ratio": 1.5,
    "accumulation_ratio": 2.0,
    "heavy_outflow_penalty": 20,
    "moderate_outflow_penalty": 5,
    "accumulation_bonus": 5,
    "very_large_transaction": 100.0,  # ETH
    "large_transaction": 10.0,  # ETH
    "very_large_tx_penalty": 15,
    "large_tx_penalty": 5,
    "very_concentrated_interactions": 0.1,
    "concentrated_interactions": 0.3,
    "diverse_interactions": 0.7,
    "very_concentrated_penalty": 15,
    "concentrated_penalty": 5,
    "diverse_bonus": 5,
    "very_new_wallet_days": 30,
    "new_wallet_days": 90,
    "old_wallet_days": 730,
    "very_new_wallet_penalty": 15,
    "new_wallet_penalty": 5,
    "old_wallet_bonus": 10,
}

# LLM (Gemini) configuration
LLM_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 0.1,
    "max_output_tokens": 500,
    "timeout_seconds": 30,
    "rule_based_weight": 0.6,
    "llm_weight": 0.4,
}

# Stablecoin identifiers
STABLECOIN_SYMBOLS = ["usdt", "usdc", "dai", "busd", "frax", "tusd", "usdp", "gusd"]

# Risk level descriptions
RISK_LEVEL_DESCRIPTIONS = {
    "VERY_HIGH": "Extremely risky wallet with multiple severe red flags",
    "HIGH": "High-risk wallet requiring significant caution",
    "MEDIUM": "Medium risk with some concerning factors",
    "LOW": "Low risk with generally safe behavior patterns",
    "VERY_LOW": "Very low risk, highly conservative wallet behavior",
}
