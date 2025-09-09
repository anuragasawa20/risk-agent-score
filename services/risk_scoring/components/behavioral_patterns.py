"""
Behavioral Pattern Risk Analysis
Analyzes wallet behavioral patterns for risk assessment.
"""

from typing import Dict, Any
from ..config import BEHAVIORAL_THRESHOLDS


class BehavioralPatternAnalyzer:
    """Analyzes wallet behavioral patterns for risk indicators"""

    def __init__(self):
        self.thresholds = BEHAVIORAL_THRESHOLDS

    def calculate_risk(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate risk based on behavioral patterns.

        Args:
            patterns: Transaction patterns data

        Returns:
            Risk analysis results with score and reasons
        """
        if "error" in patterns:
            return {
                "risk_score": 60.0,
                "reasons": ["Unable to analyze behavior"],
                "metrics": {},
            }

        risk_score = 50.0
        reasons = []

        # Analyze gas usage patterns
        risk_score, reasons = self._analyze_gas_patterns(patterns, risk_score, reasons)

        # Analyze value flow patterns
        risk_score, reasons = self._analyze_value_flow(patterns, risk_score, reasons)

        # Analyze transaction sizes
        risk_score, reasons = self._analyze_transaction_sizes(
            patterns, risk_score, reasons
        )

        # Analyze address interaction diversity
        risk_score, reasons = self._analyze_interaction_diversity(
            patterns, risk_score, reasons
        )

        # Analyze wallet age and lifecycle
        risk_score, reasons = self._analyze_wallet_lifecycle(
            patterns, risk_score, reasons
        )

        # Calculate metrics for return
        gas_analysis = patterns.get("gas_analysis", {})
        avg_gas_price = gas_analysis.get("avg_gas_price", 0)

        value_analysis = patterns.get("value_analysis", {})
        value_in = value_analysis.get("total_value_in", 0)
        value_out = value_analysis.get("total_value_out", 0)
        largest_tx = value_analysis.get("largest_transaction", 0)

        address_interactions = patterns.get("address_interactions", {})
        interaction_diversity = address_interactions.get("interaction_diversity", 0)
        total_txs = patterns.get("total_transactions", 1)

        # Calculate derived metrics
        diversity_ratio = interaction_diversity / total_txs if total_txs > 0 else 0
        value_flow_ratio = value_out / max(value_in, 1)

        time_analysis = patterns.get("time_analysis", {})
        first_tx = time_analysis.get("first_transaction")
        last_tx = time_analysis.get("last_transaction")
        wallet_age_days = 0
        if first_tx and last_tx:
            wallet_age_days = (last_tx - first_tx) / (24 * 60 * 60)

        return {
            "risk_score": max(0, min(100, risk_score)),
            "reasons": reasons,
            "metrics": {
                "avg_gas_price": avg_gas_price,
                "value_flow_ratio": value_flow_ratio,
                "largest_transaction": largest_tx,
                "interaction_diversity": diversity_ratio,
                "wallet_age_days": wallet_age_days,
            },
        }

    def _analyze_gas_patterns(
        self, patterns: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze gas usage patterns (high gas = desperation/MEV/arbitrage)"""
        gas_analysis = patterns.get("gas_analysis", {})
        avg_gas_price = gas_analysis.get("avg_gas_price", 0)

        if avg_gas_price > self.thresholds["very_high_gas_price"]:  # >200 Gwei
            risk_score += self.thresholds["very_high_gas_penalty"]
            reasons.append(f"Very high gas usage: {avg_gas_price:.1f} Gwei")
        elif avg_gas_price > self.thresholds["high_gas_price"]:  # >100 Gwei
            risk_score += self.thresholds["high_gas_penalty"]
            reasons.append(f"High gas usage: {avg_gas_price:.1f} Gwei")
        elif avg_gas_price < self.thresholds["low_gas_price"]:  # <20 Gwei
            risk_score -= self.thresholds["low_gas_bonus"]
            reasons.append(f"Efficient gas usage: {avg_gas_price:.1f} Gwei")

        return risk_score, reasons

    def _analyze_value_flow(
        self, patterns: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze value flow patterns"""
        value_analysis = patterns.get("value_analysis", {})
        value_in = value_analysis.get("total_value_in", 0)
        value_out = value_analysis.get("total_value_out", 0)

        if (
            value_out > value_in * self.thresholds["heavy_outflow_ratio"]
        ):  # Heavy outflow
            risk_score += self.thresholds["heavy_outflow_penalty"]
            reasons.append("Heavy fund outflow pattern")
        elif (
            value_out > value_in * self.thresholds["moderate_outflow_ratio"]
        ):  # Moderate outflow
            risk_score += self.thresholds["moderate_outflow_penalty"]
            reasons.append("Moderate outflow pattern")
        elif (
            value_in > value_out * self.thresholds["accumulation_ratio"]
        ):  # Accumulating
            risk_score -= self.thresholds["accumulation_bonus"]
            reasons.append("Accumulation pattern")

        return risk_score, reasons

    def _analyze_transaction_sizes(
        self, patterns: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze transaction size patterns"""
        value_analysis = patterns.get("value_analysis", {})
        largest_tx = value_analysis.get("largest_transaction", 0)

        if largest_tx > self.thresholds["very_large_transaction"]:  # >100 ETH
            risk_score += self.thresholds["very_large_tx_penalty"]
            reasons.append(f"Very large transaction: {largest_tx:.2f} ETH")
        elif largest_tx > self.thresholds["large_transaction"]:  # >10 ETH
            risk_score += self.thresholds["large_tx_penalty"]
            reasons.append(f"Large transaction: {largest_tx:.2f} ETH")

        return risk_score, reasons

    def _analyze_interaction_diversity(
        self, patterns: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze address interaction diversity"""
        address_interactions = patterns.get("address_interactions", {})
        interaction_diversity = address_interactions.get("interaction_diversity", 0)
        total_txs = patterns.get("total_transactions", 1)

        if total_txs > 0:
            diversity_ratio = interaction_diversity / total_txs

            if diversity_ratio < self.thresholds["very_concentrated_interactions"]:
                risk_score += self.thresholds["very_concentrated_penalty"]
                reasons.append("Very concentrated interactions")
            elif diversity_ratio < self.thresholds["concentrated_interactions"]:
                risk_score += self.thresholds["concentrated_penalty"]
                reasons.append("Somewhat concentrated interactions")
            elif diversity_ratio > self.thresholds["diverse_interactions"]:
                risk_score -= self.thresholds["diverse_bonus"]
                reasons.append("Diverse interaction pattern")

        return risk_score, reasons

    def _analyze_wallet_lifecycle(
        self, patterns: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze wallet age and lifecycle patterns"""
        time_analysis = patterns.get("time_analysis", {})
        first_tx = time_analysis.get("first_transaction")
        last_tx = time_analysis.get("last_transaction")

        if first_tx and last_tx:
            wallet_age_days = (last_tx - first_tx) / (24 * 60 * 60)

            if wallet_age_days < self.thresholds["very_new_wallet_days"]:  # <30 days
                risk_score += self.thresholds["very_new_wallet_penalty"]
                reasons.append("Very new wallet (<30 days)")
            elif wallet_age_days < self.thresholds["new_wallet_days"]:  # <90 days
                risk_score += self.thresholds["new_wallet_penalty"]
                reasons.append("New wallet (<90 days)")
            elif wallet_age_days > self.thresholds["old_wallet_days"]:  # >2 years
                risk_score -= self.thresholds["old_wallet_bonus"]
                reasons.append("Established wallet (>2 years)")

        return risk_score, reasons
