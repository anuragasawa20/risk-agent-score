"""
Core Risk Scoring Engine
Main orchestrator that coordinates all risk analysis components.
"""

from typing import Dict, Any
from .config import RISK_WEIGHTS, LLM_CONFIG
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


class RiskScoringEngine:
    """
    Advanced risk scoring engine with multiple risk factors.

    Combines rule-based analysis with optional AI-powered insights
    to provide comprehensive wallet risk assessment.
    """

    def __init__(self):
        """Initialize the risk scoring engine with all component analyzers"""
        # Component analyzers
        self.transaction_analyzer = TransactionPatternAnalyzer()
        self.protocol_analyzer = ProtocolRiskAnalyzer()
        self.asset_analyzer = AssetConcentrationAnalyzer()
        self.behavioral_analyzer = BehavioralPatternAnalyzer()

        # LLM analyzer (optional)
        self.llm_analyzer = GeminiRiskAnalyzer()

        # Configuration
        self.risk_weights = RISK_WEIGHTS
        self.llm_config = LLM_CONFIG

    def calculate_overall_risk_score(
        self,
        patterns: Dict[str, Any],
        protocol_analysis: Dict[str, Any],
        balances: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive risk score with detailed breakdown including LLM analysis.

        Args:
            patterns: Transaction patterns data
            protocol_analysis: Protocol interaction analysis
            balances: Wallet balance data

        Returns:
            Comprehensive risk analysis results
        """
        print("🎯 Starting comprehensive risk analysis...")

        # STEP 1: Calculate RULE-BASED component scores
        print("📊 STEP 1: Calculating rule-based risk components...")
        transaction_result = self.transaction_analyzer.calculate_risk(patterns)
        protocol_result = self.protocol_analyzer.calculate_risk(protocol_analysis)
        concentration_result = self.asset_analyzer.calculate_risk(balances)
        behavioral_result = self.behavioral_analyzer.calculate_risk(patterns)

        # Extract rule-based risk scores
        transaction_risk = transaction_result["risk_score"]
        protocol_risk = protocol_result["risk_score"]
        concentration_risk = concentration_result["risk_score"]
        behavioral_risk = behavioral_result["risk_score"]

        print(f"   📈 Transaction patterns risk: {transaction_risk:.1f}/100")
        print(f"   🏦 Protocol interactions risk: {protocol_risk:.1f}/100")
        print(f"   💰 Asset concentration risk: {concentration_risk:.1f}/100")
        print(f"   🎭 Behavioral patterns risk: {behavioral_risk:.1f}/100")

        # Calculate rule-based weighted overall score
        rule_based_risk = (
            transaction_risk * self.risk_weights["transaction_patterns"]
            + protocol_risk * self.risk_weights["protocol_interactions"]
            + concentration_risk * self.risk_weights["asset_concentration"]
            + behavioral_risk
            * (
                self.risk_weights["activity_frequency"]
                + self.risk_weights["failure_rate"]
            )
        )

        print(f"   🔢 Rule-based overall score: {rule_based_risk:.2f}/100")

        # STEP 2: Calculate LLM-BASED risk score
        print("🤖 STEP 2: Starting Gemini AI Analysis...")
        try:
            llm_result = self.llm_analyzer.analyze_wallet_risk(
                patterns, protocol_analysis, balances
            )
            llm_risk_score = llm_result.get("llm_risk_score")
            llm_component_scores = llm_result.get("component_scores", {})

            if llm_risk_score is not None:
                print(f"   ✅ Gemini AI analysis completed successfully!")
                print(f"   📊 Gemini score: {llm_risk_score}/100")
            else:
                print("   ⚠️  Gemini AI analysis returned None (no API key or failed)")

        except Exception as e:
            print(f"   ❌ ERROR in Gemini AI analysis: {e}")
            print(f"   🔧 Falling back to rule-based scoring only")
            llm_result = {
                "llm_risk_score": None,
                "reasoning": f"Gemini analysis failed: {str(e)}",
                "component_scores": {},
            }
            llm_risk_score = None
            llm_component_scores = {}

        # STEP 3: Calculate HYBRID score (combining rule-based + LLM)
        print("🔀 STEP 3: Calculating Hybrid Score...")
        try:
            if llm_risk_score is not None:
                print(
                    f"   🎯 Creating hybrid: {self.llm_config['rule_based_weight']*100:.0f}% rule-based ({rule_based_risk:.1f}) + {self.llm_config['llm_weight']*100:.0f}% Gemini ({llm_risk_score:.1f})"
                )

                # Weighted combination
                hybrid_risk = (
                    self.llm_config["rule_based_weight"] * rule_based_risk
                    + self.llm_config["llm_weight"] * llm_risk_score
                )
                print(f"   📊 Hybrid overall score calculated: {hybrid_risk:.2f}")

                # Combine component scores intelligently
                print("   🔧 Combining component scores...")
                hybrid_components = {
                    "transaction_patterns": (
                        0.7 * transaction_risk
                        + 0.3
                        * llm_component_scores.get(
                            "transaction_patterns", transaction_risk
                        )
                    ),
                    "protocol_interactions": (
                        0.5 * protocol_risk
                        + 0.5
                        * llm_component_scores.get(
                            "protocol_interactions", protocol_risk
                        )
                    ),
                    "asset_concentration": (
                        0.6 * concentration_risk
                        + 0.4
                        * llm_component_scores.get(
                            "asset_concentration", concentration_risk
                        )
                    ),
                    "behavioral_patterns": (
                        0.7 * behavioral_risk
                        + 0.3
                        * llm_component_scores.get(
                            "behavioral_patterns", behavioral_risk
                        )
                    ),
                }

                # Use hybrid as primary score
                overall_risk = hybrid_risk
                primary_components = hybrid_components
                print(f"   ✅ Hybrid scoring complete: {hybrid_risk:.2f}/100")

            else:
                print("   🔄 No Gemini data available, using 100% rule-based scoring")
                # Fallback to rule-based if LLM failed
                overall_risk = rule_based_risk
                primary_components = {
                    "transaction_patterns": transaction_risk,
                    "protocol_interactions": protocol_risk,
                    "asset_concentration": concentration_risk,
                    "behavioral_patterns": behavioral_risk,
                }
                print(f"   📊 Using pure rule-based score: {rule_based_risk:.2f}/100")

        except Exception as e:
            print(f"   ❌ ERROR in hybrid calculation: {e}")
            print("   🔧 Falling back to pure rule-based scoring")
            overall_risk = rule_based_risk
            primary_components = {
                "transaction_patterns": transaction_risk,
                "protocol_interactions": protocol_risk,
                "asset_concentration": concentration_risk,
                "behavioral_patterns": behavioral_risk,
            }

        # Determine risk level and description
        risk_level, risk_description = get_risk_level_description(overall_risk)
        print(f"🎯 Final Risk Assessment: {risk_level} ({overall_risk:.2f}/100)")

        # Combine all reasons
        all_reasons = []
        all_reasons.extend(transaction_result.get("reasons", []))
        all_reasons.extend(protocol_result.get("reasons", []))
        all_reasons.extend(concentration_result.get("reasons", []))
        all_reasons.extend(behavioral_result.get("reasons", []))

        # Generate recommendations
        recommendations = generate_recommendations(
            overall_risk,
            {
                "transaction": transaction_risk,
                "protocol": protocol_risk,
                "concentration": concentration_risk,
                "behavioral": behavioral_risk,
            },
            all_reasons,
        )

        return {
            # PRIMARY (HYBRID) SCORES - used by main system
            "overall_risk_score": round(overall_risk, 2),
            "risk_level": risk_level,
            "risk_description": risk_description,
            "component_scores": {
                "transaction_patterns": round(
                    primary_components["transaction_patterns"], 2
                ),
                "protocol_interactions": round(
                    primary_components["protocol_interactions"], 2
                ),
                "asset_concentration": round(
                    primary_components["asset_concentration"], 2
                ),
                "behavioral_patterns": round(
                    primary_components["behavioral_patterns"], 2
                ),
            },
            # ALL THREE SCORING METHODS 🎯
            "scoring_methods": {
                "rule_based": {
                    "overall_score": round(rule_based_risk, 2),
                    "risk_level": get_risk_level_description(rule_based_risk)[0],
                    "components": {
                        "transaction_patterns": round(transaction_risk, 2),
                        "protocol_interactions": round(protocol_risk, 2),
                        "asset_concentration": round(concentration_risk, 2),
                        "behavioral_patterns": round(behavioral_risk, 2),
                    },
                },
                "llm_based": {
                    "overall_score": (
                        round(llm_risk_score, 2) if llm_risk_score else None
                    ),
                    "risk_level": (
                        get_risk_level_description(llm_risk_score)[0]
                        if llm_risk_score
                        else "N/A"
                    ),
                    "components": llm_component_scores,
                    "reasoning": llm_result.get(
                        "reasoning", "Gemini analysis not available"
                    ),
                    "key_insights": llm_result.get("key_insights", []),
                },
                "hybrid": {
                    "overall_score": round(overall_risk, 2),
                    "risk_level": risk_level,
                    "components": {
                        "transaction_patterns": round(
                            primary_components["transaction_patterns"], 2
                        ),
                        "protocol_interactions": round(
                            primary_components["protocol_interactions"], 2
                        ),
                        "asset_concentration": round(
                            primary_components["asset_concentration"], 2
                        ),
                        "behavioral_patterns": round(
                            primary_components["behavioral_patterns"], 2
                        ),
                    },
                    "methodology": (
                        f"{self.llm_config['rule_based_weight']*100:.0f}% rule-based + {self.llm_config['llm_weight']*100:.0f}% Gemini"
                        if llm_risk_score
                        else "100% rule-based (Gemini unavailable)"
                    ),
                },
            },
            # EXISTING STRUCTURE (for compatibility)
            "component_weights": self.risk_weights,
            "detailed_analysis": {
                "transaction_analysis": transaction_result,
                "protocol_analysis": protocol_result,
                "concentration_analysis": concentration_result,
                "behavioral_analysis": behavioral_result,
                "llm_analysis": llm_result,
            },
            "risk_factors": all_reasons,
            "recommendations": recommendations,
            "risk_distribution": categorize_risk_components(
                {
                    "transaction": primary_components["transaction_patterns"],
                    "protocol": primary_components["protocol_interactions"],
                    "concentration": primary_components["asset_concentration"],
                    "behavioral": primary_components["behavioral_patterns"],
                }
            ),
        }
