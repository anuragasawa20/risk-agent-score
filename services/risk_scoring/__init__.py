"""
Modular Risk Scoring System
A comprehensive, modular risk assessment framework for cryptocurrency wallets.

This system provides:
- Rule-based risk analysis across multiple components
- AI-powered risk insights via Google Gemini
- Hybrid scoring combining traditional and AI methods
- Detailed risk breakdowns and recommendations

Main Components:
- TransactionPatternAnalyzer: Analyzes transaction behavior patterns
- ProtocolRiskAnalyzer: Evaluates DeFi protocol interaction risks
- AssetConcentrationAnalyzer: Assesses portfolio diversification risks
- BehavioralPatternAnalyzer: Examines wallet behavioral patterns
- GeminiRiskAnalyzer: Provides AI-powered risk insights
- RiskScoringEngine: Main orchestrator combining all analysis

Usage:
    from services.risk_scoring import RiskScoringEngine

    engine = RiskScoringEngine()
    results = engine.calculate_overall_risk_score(
        patterns=transaction_patterns,
        protocol_analysis=protocol_data,
        balances=balance_data
    )
"""

from .core import RiskScoringEngine
from .config import RISK_WEIGHTS, RISK_THRESHOLDS
from .components import (
    TransactionPatternAnalyzer,
    ProtocolRiskAnalyzer,
    AssetConcentrationAnalyzer,
    BehavioralPatternAnalyzer,
)
from .llm import GeminiRiskAnalyzer
from .utils import (
    get_risk_level_description,
    categorize_risk_components,
    generate_recommendations,
)

# Version info
__version__ = "2.0.0"
__author__ = "Risk Analysis Team"

# Main export
__all__ = [
    "RiskScoringEngine",
    "TransactionPatternAnalyzer",
    "ProtocolRiskAnalyzer",
    "AssetConcentrationAnalyzer",
    "BehavioralPatternAnalyzer",
    "GeminiRiskAnalyzer",
    "get_risk_level_description",
    "categorize_risk_components",
    "generate_recommendations",
    "RISK_WEIGHTS",
    "RISK_THRESHOLDS",
]
