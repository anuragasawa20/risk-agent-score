"""
Transaction Pattern Risk Analysis
Analyzes wallet transaction patterns for risk indicators.
"""

from typing import Dict, Any
from ..config import TRANSACTION_THRESHOLDS


class TransactionPatternAnalyzer:
    """Analyzes transaction patterns for risk assessment"""

    def __init__(self):
        self.thresholds = TRANSACTION_THRESHOLDS

    def calculate_risk(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze transaction patterns for risk indicators.

        Args:
            patterns: Transaction patterns data

        Returns:
            Risk analysis results with score and reasons
        """
        if "error" in patterns:
            return {"risk_score": 90.0, "reasons": ["No transaction data available"]}

        risk_score = 50.0  # Base risk
        reasons = []

        total_txs = patterns.get("total_transactions", 0)
        if total_txs == 0:
            return {
                "risk_score": 90.0,
                "reasons": ["Inactive wallet - no transactions"],
            }

        # Success rate analysis
        risk_score, reasons = self._analyze_success_rate(
            patterns, total_txs, risk_score, reasons
        )

        # Activity frequency analysis
        risk_score, reasons = self._analyze_activity_frequency(
            patterns, risk_score, reasons
        )

        # High-value transaction analysis
        risk_score, reasons = self._analyze_high_value_transactions(
            patterns, total_txs, risk_score, reasons
        )

        # Contract interaction analysis
        risk_score, reasons = self._analyze_contract_interactions(
            patterns, total_txs, risk_score, reasons
        )

        # Recent activity analysis
        risk_score, reasons = self._analyze_recent_activity(
            patterns, total_txs, risk_score, reasons
        )

        # Gas price analysis
        risk_score, reasons = self._analyze_gas_usage(patterns, risk_score, reasons)

        # Address diversity analysis
        risk_score, reasons = self._analyze_address_diversity(
            patterns, total_txs, risk_score, reasons
        )

        # Calculate derived metrics
        success_txs = patterns.get("successful_transactions", 0)
        success_rate = success_txs / total_txs if total_txs > 0 else 0
        frequency = patterns.get("time_analysis", {}).get("activity_frequency", 0)
        high_value_txs = patterns.get("high_value_transactions", 0)
        high_value_ratio = high_value_txs / total_txs if total_txs > 0 else 0
        contract_interactions = patterns.get("contract_interactions", 0)
        contract_ratio = contract_interactions / total_txs if total_txs > 0 else 0
        recent_activity = patterns.get("recent_activity", 0)

        return {
            "risk_score": max(0, min(100, risk_score)),
            "reasons": reasons,
            "metrics": {
                "success_rate": success_rate,
                "activity_frequency": frequency,
                "high_value_ratio": high_value_ratio,
                "contract_interaction_ratio": contract_ratio,
                "recent_activity": recent_activity,
            },
        }

    def _analyze_success_rate(
        self, patterns: Dict[str, Any], total_txs: int, risk_score: float, reasons: list
    ) -> tuple:
        """Analyze transaction success rate"""
        success_txs = patterns.get("successful_transactions", 0)
        success_rate = success_txs / total_txs if total_txs > 0 else 0

        if success_rate < self.thresholds["low_success_rate"]:
            risk_score += 25
            reasons.append(f"Low success rate: {success_rate:.1%}")
        elif success_rate < self.thresholds["moderate_success_rate"]:
            risk_score += 10
            reasons.append(f"Moderate success rate: {success_rate:.1%}")
        elif success_rate > self.thresholds["high_success_rate"]:
            risk_score -= 10
            reasons.append(f"High success rate: {success_rate:.1%}")

        return risk_score, reasons

    def _analyze_activity_frequency(
        self, patterns: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze wallet activity frequency"""
        frequency = patterns.get("time_analysis", {}).get("activity_frequency", 0)

        if frequency > self.thresholds["very_high_activity_frequency"]:
            risk_score += 15
            reasons.append(f"Very high activity: {frequency:.1f} tx/day")
        elif frequency > self.thresholds["high_activity_frequency"]:
            risk_score += 5
            reasons.append(f"High activity: {frequency:.1f} tx/day")
        elif frequency < self.thresholds["low_activity_frequency"]:
            risk_score += 15
            reasons.append(f"Very low activity: {frequency:.3f} tx/day")
        elif 1 <= frequency <= 5:  # Normal human activity
            risk_score -= 5
            reasons.append(f"Normal activity: {frequency:.1f} tx/day")

        return risk_score, reasons

    def _analyze_high_value_transactions(
        self, patterns: Dict[str, Any], total_txs: int, risk_score: float, reasons: list
    ) -> tuple:
        """Analyze high-value transaction patterns"""
        high_value_txs = patterns.get("high_value_transactions", 0)
        high_value_ratio = high_value_txs / total_txs if total_txs > 0 else 0

        if high_value_ratio > self.thresholds["very_high_value_tx_ratio"]:
            risk_score += 15
            reasons.append(f"High value transaction ratio: {high_value_ratio:.1%}")
        elif high_value_ratio > self.thresholds["high_value_tx_ratio"]:
            risk_score += 5
            reasons.append(f"Moderate high-value transactions: {high_value_ratio:.1%}")

        return risk_score, reasons

    def _analyze_contract_interactions(
        self, patterns: Dict[str, Any], total_txs: int, risk_score: float, reasons: list
    ) -> tuple:
        """Analyze smart contract interaction patterns"""
        contract_interactions = patterns.get("contract_interactions", 0)
        contract_ratio = contract_interactions / total_txs if total_txs > 0 else 0

        if contract_ratio > self.thresholds["very_high_contract_ratio"]:
            risk_score += 15
            reasons.append(f"Very high DeFi usage: {contract_ratio:.1%}")
        elif contract_ratio > self.thresholds["high_contract_ratio"]:
            risk_score += 5
            reasons.append(f"High DeFi usage: {contract_ratio:.1%}")
        elif contract_ratio < self.thresholds["low_contract_ratio"]:
            risk_score -= 5
            reasons.append(f"Low DeFi usage: {contract_ratio:.1%}")

        return risk_score, reasons

    def _analyze_recent_activity(
        self, patterns: Dict[str, Any], total_txs: int, risk_score: float, reasons: list
    ) -> tuple:
        """Analyze recent wallet activity"""
        recent_activity = patterns.get("recent_activity", 0)

        if recent_activity == 0 and total_txs > 10:  # Inactive wallet
            risk_score += 20
            reasons.append(
                f"No recent activity ({self.thresholds['inactive_days']} days)"
            )
        elif recent_activity > self.thresholds["recent_activity_threshold"]:
            risk_score += 10
            reasons.append(f"Very active recently: {recent_activity} txs")

        return risk_score, reasons

    def _analyze_gas_usage(
        self, patterns: Dict[str, Any], risk_score: float, reasons: list
    ) -> tuple:
        """Analyze gas price patterns"""
        avg_gas_price = patterns.get("gas_analysis", {}).get("avg_gas_price", 0)

        if avg_gas_price > self.thresholds["high_gas_price"]:
            risk_score += 10
            reasons.append(f"High gas prices: {avg_gas_price:.1f} Gwei")

        return risk_score, reasons

    def _analyze_address_diversity(
        self, patterns: Dict[str, Any], total_txs: int, risk_score: float, reasons: list
    ) -> tuple:
        """Analyze address interaction diversity"""
        unique_addresses = patterns.get("unique_addresses", 0)

        if total_txs > 0:
            address_diversity = unique_addresses / total_txs
            if address_diversity < self.thresholds["low_address_diversity"]:
                risk_score += 10
                reasons.append(f"Low address diversity: {address_diversity:.2f}")

        return risk_score, reasons
