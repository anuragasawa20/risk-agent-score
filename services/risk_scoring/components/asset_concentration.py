"""
Asset Concentration Risk Analysis
Analyzes portfolio asset distribution for concentration risks.
"""

from typing import Dict, Any
from ..config import ASSET_THRESHOLDS, STABLECOIN_SYMBOLS


class AssetConcentrationAnalyzer:
    """Analyzes asset concentration and portfolio diversification risks"""

    def __init__(self):
        self.thresholds = ASSET_THRESHOLDS
        self.stablecoin_symbols = STABLECOIN_SYMBOLS

    def calculate_risk(self, balances: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate risk based on asset concentration.

        Args:
            balances: Wallet balance data

        Returns:
            Risk analysis results with score and reasons
        """
        risk_score = 50.0
        reasons = []

        eth_balance = balances.get("eth_balance", 0)
        tokens = balances.get("tokens", [])
        token_count = len(tokens)

        # Analyze asset diversification
        risk_score, reasons = self._analyze_diversification(
            eth_balance, token_count, risk_score, reasons
        )

        # Analyze ETH holdings size (whale risk)
        risk_score, reasons = self._analyze_eth_holdings(
            eth_balance, risk_score, reasons
        )

        # Analyze token composition (stablecoins etc.)
        risk_score, reasons = self._analyze_token_composition(
            tokens, risk_score, reasons
        )

        # Determine asset diversification level
        diversification_level = self._get_diversification_level(token_count)

        return {
            "risk_score": max(0, min(100, risk_score)),
            "reasons": reasons,
            "metrics": {
                "eth_balance": eth_balance,
                "token_count": token_count,
                "asset_diversification": diversification_level,
            },
        }

    def _analyze_diversification(
        self, eth_balance: float, token_count: int, risk_score: float, reasons: list
    ) -> tuple:
        """Analyze portfolio diversification"""
        if token_count == 0:
            if eth_balance > 0:
                risk_score -= 15  # Only ETH is relatively safe
                reasons.append("ETH-only portfolio (conservative)")
            else:
                risk_score += 30  # No assets is risky for active wallet
                reasons.append("No significant assets detected")
        elif token_count == 1:
            risk_score += self.thresholds["single_token_penalty"]
            reasons.append("Single token concentration")
        elif token_count < self.thresholds["low_diversification_count"]:
            risk_score += self.thresholds["low_diversification_penalty"]
            reasons.append(f"Low diversification: {token_count} tokens")
        elif token_count < self.thresholds["good_diversification_count"]:
            risk_score -= self.thresholds["good_diversification_bonus"]
            reasons.append(f"Good diversification: {token_count} tokens")
        else:
            risk_score -= self.thresholds["high_diversification_bonus"]
            reasons.append(f"High diversification: {token_count} tokens")

        return risk_score, reasons

    def _analyze_eth_holdings(
        self, eth_balance: float, risk_score: float, reasons: list
    ) -> tuple:
        """Analyze ETH holdings size for whale risk"""
        if (
            eth_balance > self.thresholds["very_large_eth_holdings"]
        ):  # >1000 ETH (~$2M+)
            risk_score += self.thresholds["very_large_eth_penalty"]
            reasons.append(f"Very large ETH holdings: {eth_balance:.2f} ETH")
        elif eth_balance > self.thresholds["large_eth_holdings"]:  # >100 ETH (~$200K+)
            risk_score += self.thresholds["large_eth_penalty"]
            reasons.append(f"Large ETH holdings: {eth_balance:.2f} ETH")
        elif eth_balance > self.thresholds["significant_eth_holdings"]:  # >10 ETH
            risk_score += self.thresholds["significant_eth_penalty"]
            reasons.append(f"Significant ETH holdings: {eth_balance:.2f} ETH")
        elif eth_balance < self.thresholds["very_low_eth_balance"]:  # <0.01 ETH
            risk_score += self.thresholds["very_low_eth_penalty"]
            reasons.append("Very low ETH balance")

        return risk_score, reasons

    def _analyze_token_composition(
        self, tokens: list, risk_score: float, reasons: list
    ) -> tuple:
        """Analyze token composition for stability factors"""
        if not tokens:
            return risk_score, reasons

        # Look for stablecoins (safer assets)
        stablecoin_count = sum(
            1
            for token in tokens
            if any(
                stable in token.get("token_symbol", "").lower()
                for stable in self.stablecoin_symbols
            )
        )

        if stablecoin_count > 0:
            bonus = min(
                stablecoin_count * self.thresholds["stablecoin_bonus_per_token"],
                self.thresholds["stablecoin_bonus_max"],
            )
            risk_score -= bonus
            reasons.append(f"Stablecoin exposure: {stablecoin_count} tokens")

        return risk_score, reasons

    def _get_diversification_level(self, token_count: int) -> str:
        """Determine diversification level description"""
        if token_count > self.thresholds["good_diversification_count"]:
            return "high"
        elif token_count > self.thresholds["low_diversification_count"]:
            return "medium"
        elif token_count > 0:
            return "low"
        else:
            return "none"
