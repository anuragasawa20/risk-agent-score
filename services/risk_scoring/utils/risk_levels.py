"""
Risk Level Utilities
Functions for determining risk levels and categorizing risk components.
"""

from typing import Dict, List, Tuple
from ..config import RISK_LEVEL_DESCRIPTIONS


def get_risk_level_description(risk_score: float) -> Tuple[str, str]:
    """
    Get risk level and description based on score.

    Args:
        risk_score: Risk score from 0-100

    Returns:
        Tuple of (risk_level, description)
    """
    if risk_score >= 80:
        return "VERY_HIGH", RISK_LEVEL_DESCRIPTIONS["VERY_HIGH"]
    elif risk_score >= 60:
        return "HIGH", RISK_LEVEL_DESCRIPTIONS["HIGH"]
    elif risk_score >= 40:
        return "MEDIUM", RISK_LEVEL_DESCRIPTIONS["MEDIUM"]
    elif risk_score >= 20:
        return "LOW", RISK_LEVEL_DESCRIPTIONS["LOW"]
    else:
        return "VERY_LOW", RISK_LEVEL_DESCRIPTIONS["VERY_LOW"]


def categorize_risk_components(
    component_risks: Dict[str, float],
) -> Dict[str, List[str]]:
    """
    Categorize risk components by severity.

    Args:
        component_risks: Dictionary mapping component names to risk scores

    Returns:
        Dictionary with 'high', 'medium', 'low' categories containing component names
    """
    categorized = {"high": [], "medium": [], "low": []}

    for component, risk in component_risks.items():
        if risk >= 70:
            categorized["high"].append(component)
        elif risk >= 40:
            categorized["medium"].append(component)
        else:
            categorized["low"].append(component)

    return categorized
