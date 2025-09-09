"""
Risk Recommendations Generator
Generates actionable recommendations based on risk analysis results.
"""

from typing import Dict, List


def generate_recommendations(
    overall_risk: float, component_risks: Dict[str, float], reasons: List[str]
) -> List[str]:
    """
    Generate actionable recommendations based on risk analysis.

    Args:
        overall_risk: Overall risk score (0-100)
        component_risks: Dictionary of component risk scores
        reasons: List of risk reasons/factors

    Returns:
        List of recommendation strings
    """
    recommendations = []

    # Overall risk recommendations
    if overall_risk > 80:
        recommendations.append(
            "🚨 CRITICAL: Extreme caution advised - multiple high-risk factors detected"
        )
    elif overall_risk > 60:
        recommendations.append(
            "⚠️ HIGH RISK: Significant caution required before any interactions"
        )
    elif overall_risk < 25:
        recommendations.append(
            "✅ LOW RISK: Generally safe wallet with conservative behavior"
        )

    # Component-specific recommendations
    if component_risks.get("transaction", 0) > 70:
        recommendations.append(
            "📊 Transaction Patterns: Review transaction success rates and activity patterns"
        )

    if component_risks.get("protocol", 0) > 70:
        recommendations.append(
            "🏦 Protocol Risk: Wallet interacts with high-risk DeFi protocols"
        )
        recommendations.append(
            "💡 Suggestion: Research protocol security audits and TVL stability"
        )

    if component_risks.get("concentration", 0) > 70:
        recommendations.append(
            "💰 Asset Concentration: Consider portfolio diversification"
        )
        recommendations.append(
            "🎯 Tip: Spread holdings across multiple assets and protocols"
        )

    if component_risks.get("behavioral", 0) > 70:
        recommendations.append(
            "🎭 Behavioral Risk: Unusual transaction patterns detected"
        )
        recommendations.append(
            "🔍 Recommendation: Verify wallet ownership and transaction authenticity"
        )

    # Specific recommendations based on reasons
    if any("gas" in reason.lower() for reason in reasons):
        recommendations.append(
            "⛽ Gas Optimization: Consider using lower gas prices during off-peak hours"
        )

    if any("new wallet" in reason.lower() for reason in reasons):
        recommendations.append(
            "🆕 New Wallet: Monitor activity patterns as wallet establishes history"
        )

    if any(
        "large" in reason.lower() and "transaction" in reason.lower()
        for reason in reasons
    ):
        recommendations.append(
            "💎 Large Transactions: Verify transaction authenticity for high-value transfers"
        )

    if any("stablecoin" in reason.lower() for reason in reasons):
        recommendations.append(
            "💵 Stablecoin Holdings: Good risk mitigation through stable assets"
        )

    if any("diversification" in reason.lower() for reason in reasons):
        recommendations.append(
            "📈 Portfolio Management: Continue maintaining diversified holdings"
        )

    if any("high-value" in reason.lower() for reason in reasons):
        recommendations.append(
            "💰 High-Value Activity: Implement additional security measures for large transactions"
        )

    if any(
        "inactive" in reason.lower() or "activity" in reason.lower()
        for reason in reasons
    ):
        recommendations.append(
            "⏰ Activity Monitoring: Regular activity helps establish trust patterns"
        )

    return recommendations[:10]  # Limit to top 10 recommendations
