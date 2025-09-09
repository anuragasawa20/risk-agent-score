"""
Protocol Risk Analysis
Analyzes DeFi protocol interactions for risk assessment.
"""

from typing import Dict, Any
from ..config import PROTOCOL_THRESHOLDS


class ProtocolRiskAnalyzer:
    """Analyzes DeFi protocol interaction risks"""

    def __init__(self):
        self.thresholds = PROTOCOL_THRESHOLDS

    def calculate_risk(self, protocol_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate risk based on protocol interactions.

        Args:
            protocol_analysis: Protocol interaction data

        Returns:
            Risk analysis results with score and reasons
        """
        if not protocol_analysis or "protocols" not in protocol_analysis:
            return {
                "risk_score": 0.0,  # No DeFi interactions = No DeFi risk
                "reasons": ["No DeFi protocol interactions detected - Low Risk"],
                "metrics": {},
            }

        protocols = protocol_analysis["protocols"]
        if not protocols:
            return {
                "risk_score": 0.0,  # No protocols = No protocol risk
                "reasons": ["No DeFi protocol interactions - Low Risk"],
                "metrics": {},
            }

        reasons = []

        # Base protocol risk from average
        avg_risk = protocol_analysis.get("raw_average_risk", 50)
        risk_score = avg_risk

        # Analyze high-risk protocols
        risk_score, reasons = self._analyze_high_risk_protocols(
            protocol_analysis, risk_score, reasons
        )

        # Analyze diversification
        risk_score, reasons = self._analyze_diversification(
            protocol_analysis, risk_score, reasons
        )

        # Analyze TVL (Total Value Locked)
        risk_score, reasons = self._analyze_tvl_factor(
            protocol_analysis, risk_score, reasons
        )

        # Analyze protocol concentration
        risk_score, reasons = self._analyze_concentration(
            protocol_analysis, risk_score, reasons
        )

        # Analyze risk distribution
        risk_score, reasons = self._analyze_risk_distribution(
            protocol_analysis, risk_score, reasons
        )

        # Calculate metrics for return
        high_risk_count = protocol_analysis.get("high_risk_protocols", 0)
        total_protocols = protocol_analysis.get("total_protocols", 1)
        diversification = protocol_analysis.get("diversification_score", 1)
        total_tvl = protocol_analysis.get("total_tvl_interacted", 0)
        risk_dist = protocol_analysis.get("risk_distribution", {})

        return {
            "risk_score": max(0, min(100, risk_score)),
            "reasons": reasons,
            "metrics": {
                "average_protocol_risk": avg_risk,
                "high_risk_protocol_ratio": (
                    high_risk_count / total_protocols if total_protocols > 0 else 0
                ),
                "diversification_score": diversification,
                "total_tvl": total_tvl,
                "risk_distribution": risk_dist,
            },
        }

    def _analyze_high_risk_protocols(
        self, protocol_analysis: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze high-risk protocol exposure"""
        high_risk_count = protocol_analysis.get("high_risk_protocols", 0)
        total_protocols = protocol_analysis.get("total_protocols", 1)

        if high_risk_count > 0:
            high_risk_ratio = high_risk_count / total_protocols
            penalty = min(high_risk_ratio * 30, 30)
            risk_score += penalty
            reasons.append(f"High-risk protocols: {high_risk_count}/{total_protocols}")

        return risk_score, reasons

    def _analyze_diversification(
        self, protocol_analysis: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze protocol diversification"""
        diversification = protocol_analysis.get("diversification_score", 1)

        if diversification == 1:
            risk_score += self.thresholds["single_protocol_penalty"]
            reasons.append("Single protocol category")
        elif diversification < self.thresholds["low_diversification_threshold"]:
            risk_score += self.thresholds["low_diversification_penalty"]
            reasons.append(f"Low diversification: {diversification} categories")
        else:
            risk_score -= self.thresholds["diversification_bonus"]
            reasons.append(f"Good diversification: {diversification} categories")

        return risk_score, reasons

    def _analyze_tvl_factor(
        self, protocol_analysis: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze TVL (Total Value Locked) factor"""
        total_tvl = protocol_analysis.get("total_tvl_interacted", 0)

        if total_tvl > self.thresholds["very_high_tvl"]:  # >$50B
            risk_score -= self.thresholds["very_high_tvl_bonus"]
            reasons.append(f"Very high TVL protocols: ${total_tvl/1e9:.1f}B")
        elif total_tvl > self.thresholds["high_tvl"]:  # >$10B
            risk_score -= self.thresholds["high_tvl_bonus"]
            reasons.append(f"High TVL protocols: ${total_tvl/1e9:.1f}B")
        elif total_tvl > self.thresholds["medium_tvl"]:  # >$1B
            risk_score -= self.thresholds["medium_tvl_bonus"]
            reasons.append(f"Medium TVL protocols: ${total_tvl/1e9:.1f}B")
        elif total_tvl < self.thresholds["low_tvl"]:  # <$100M
            risk_score += self.thresholds["low_tvl_penalty"]
            reasons.append(f"Low TVL protocols: ${total_tvl/1e6:.1f}M")

        return risk_score, reasons

    def _analyze_concentration(
        self, protocol_analysis: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze protocol concentration penalty"""
        concentration_penalty = protocol_analysis.get("concentration_penalty", 0)
        if concentration_penalty > 0:
            reasons.append("Protocol concentration risk")

        return risk_score, reasons

    def _analyze_risk_distribution(
        self, protocol_analysis: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze risk distribution across protocols"""
        risk_dist = protocol_analysis.get("risk_distribution", {})
        very_high_count = risk_dist.get("very_high", 0)

        if very_high_count > 0:
            risk_score += very_high_count * self.thresholds["very_high_risk_penalty"]
            reasons.append(f"Very high-risk protocols: {very_high_count}")

        return risk_score, reasons
