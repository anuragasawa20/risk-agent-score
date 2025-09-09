"""
DEPRECATED: This file is maintained for backward compatibility.
Please use the new modular risk scoring system from services.risk_scoring

New usage:
    from services.risk_scoring import RiskScoringEngine
"""

import warnings
from typing import Dict, Any

# Handle both direct execution and module imports
try:
    # Try relative import first (when run as module)
    from .risk_scoring import RiskScoringEngine as ModularRiskScoringEngine
except ImportError:
    # Fallback to direct import (when run as script)
    from risk_scoring import RiskScoringEngine as ModularRiskScoringEngine

# Issue deprecation warning
warnings.warn(
    "services.risk_scoring_engine is deprecated. "
    "Use 'from services.risk_scoring import RiskScoringEngine' instead.",
    DeprecationWarning,
    stacklevel=2,
)


# Backward compatibility - redirect to new modular system
class RiskScoringEngine(ModularRiskScoringEngine):
    """
    DEPRECATED: Backward compatibility wrapper.

    This class inherits from the new modular RiskScoringEngine.
    Please migrate to: from services.risk_scoring import RiskScoringEngine
    """

    def __init__(self):
        super().__init__()
        # Legacy attribute names for backward compatibility
        self.risk_thresholds = {
            "very_low": 20,
            "low": 40,
            "medium": 60,
            "high": 80,
            "very_high": 100,
        }

    # Legacy method names for backward compatibility
    def _should_use_llm_analysis(self) -> bool:
        """Check if LLM analysis should be used (legacy compatibility)"""
        return self.llm_analyzer.is_available()

    def calculate_llm_risk_score(
        self,
        patterns: Dict[str, Any],
        protocol_analysis: Dict[str, Any],
        balances: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Legacy compatibility method"""
        return self.llm_analyzer.analyze_wallet_risk(
            patterns, protocol_analysis, balances
        )

    def calculate_transaction_pattern_risk(
        self, patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Legacy compatibility method"""
        return self.transaction_analyzer.calculate_risk(patterns)

    def calculate_protocol_risk(
        self, protocol_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Legacy compatibility method"""
        return self.protocol_analyzer.calculate_risk(protocol_analysis)

    def calculate_asset_concentration_risk(
        self, balances: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Legacy compatibility method"""
        return self.asset_analyzer.calculate_risk(balances)

    def calculate_behavioral_risk(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy compatibility method"""
        return self.behavioral_analyzer.calculate_risk(patterns)


if __name__ == "__main__":
    """Test the Risk Scoring Engine with real data"""
    import dotenv

    dotenv.load_dotenv()

    print("🎯 Risk Scoring Engine - Real Data Testing")
    print("=" * 60)
    print("Note: This module requires real transaction data from Etherscan client")
    print("Use the main risk_agent.py to test with real wallet data")
    print("=" * 60)
