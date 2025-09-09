import os
from typing import Dict, Any, List
import asyncio
from datetime import datetime
import json
import time

# Import our custom clients and components
try:
    # Try relative imports first (when run as module)
    from .Etherscan_client import EtherscanClient
    from .QuickNode_client import QuicknodeClient
    from .defillama_client import DeFiLlamaClient
    from .risk_scoring_engine import RiskScoringEngine
except ImportError:
    # Fallback to direct imports (when run as script)
    from Etherscan_client import EtherscanClient
    from QuickNode_client import QuicknodeClient
    from defillama_client import DeFiLlamaClient
    from risk_scoring_engine import RiskScoringEngine


class RiskAgent:
    """
    Main Risk Agent that orchestrates wallet risk analysis
    Provides comprehensive risk scores (0-100) based on multiple factors:
    - Transaction patterns and behavior
    - DeFi protocol interactions
    - Asset concentration and diversification
    - Activity patterns and failure rates
    """

    def __init__(self):
        """Initialize all client components"""
        try:
            self.etherscan_client = EtherscanClient()
            self.quicknode_client = QuicknodeClient()
            self.defillama_client = DeFiLlamaClient()
            # Using direct contract address mapping instead of signature analysis
            self.risk_engine = RiskScoringEngine()

            print("✅ Risk Agent initialized successfully")
            print(f"   - Etherscan client: Ready")
            print(f"   - QuickNode client: Ready")
            print(f"   - DeFiLlama client: Ready")
            print(f"   - Risk scoring engine: Ready")

        except Exception as e:
            print(f"❌ Error initializing Risk Agent: {e}")
            raise

    def analyze_wallet_comprehensive(self, wallet_address: str) -> Dict[str, Any]:
        """
        Comprehensive wallet analysis with risk scoring

        Args:
            wallet_address: Ethereum wallet address to analyze

        Returns:
            Dict with comprehensive risk analysis
        """
        print(f"🔍 Analyzing wallet: {wallet_address}")
        analysis_start_time = time.time()

        try:
            # Step 1: Get comprehensive blockchain data
            print("📊 Fetching transaction patterns and blockchain data...")

            # Use Etherscan for detailed analysis
            transaction_patterns = self.etherscan_client.analyze_transaction_patterns(
                wallet_address
            )
            # print("")
            eth_balance = self.etherscan_client.get_eth_balance(wallet_address)
            token_balances = self.etherscan_client.get_token_balances(wallet_address)
            contract_interactions = self.etherscan_client.get_contract_interactions(
                wallet_address
            )

            # Use QuickNode for additional verification and data
            quicknode_analysis = self.quicknode_client.analyze_address_type(
                wallet_address
            )

            print(
                f"   ✓ Found {transaction_patterns.get('total_transactions', 0)} transactions"
            )
            print(f"   ✓ ETH Balance: {eth_balance:.4f} ETH")
            print(f"   ✓ Token Types: {len(token_balances)}")
            print(f"   ✓ Contract Interactions: {len(contract_interactions)}")

            # Step 2: Analyze protocol interactions for DeFi risk assessment
            print("🏦 Analyzing DeFi protocol interactions...")

            # Extract protocol names from contract interactions
            protocol_names = self._extract_protocol_names(contract_interactions)
            print(f"   ✓ Identified protocols: {protocol_names}")

            # Get protocol risk data from DeFiLlama
            protocol_analysis = self.defillama_client.analyze_protocol_interactions(
                protocol_names
            )

            # Step 3: Prepare balance data for risk analysis
            balance_data = {
                "eth_balance": eth_balance,
                "tokens": token_balances,
                "quicknode_data": quicknode_analysis,
            }

            # Step 4: Calculate comprehensive risk score
            print("🎯 Calculating comprehensive risk score...")
            risk_analysis = self.risk_engine.calculate_overall_risk_score(
                transaction_patterns, protocol_analysis, balance_data
            )

            # Step 5: Compile comprehensive report
            analysis_time = time.time() - analysis_start_time

            comprehensive_report = {
                # Basic Information
                "wallet_address": wallet_address,
                "analysis_timestamp": datetime.now().isoformat(),
                "analysis_duration_seconds": round(analysis_time, 2),
                # Core Risk Assessment
                "risk_score": risk_analysis["overall_risk_score"],
                "risk_level": risk_analysis["risk_level"],
                "risk_description": risk_analysis["risk_description"],
                # Detailed Risk Breakdown
                "component_scores": risk_analysis["component_scores"],
                "component_weights": risk_analysis["component_weights"],
                "risk_factors": risk_analysis["risk_factors"],
                "recommendations": risk_analysis["recommendations"],
                "risk_distribution": risk_analysis["risk_distribution"],
                # NEW: All Three Scoring Methods 🎯
                "scoring_methods": risk_analysis.get("scoring_methods", {}),
                # Transaction Analysis Summary
                "transaction_summary": {
                    "total_transactions": transaction_patterns.get(
                        "total_transactions", 0
                    ),
                    "success_rate": (
                        transaction_patterns.get("successful_transactions", 0)
                        / max(transaction_patterns.get("total_transactions", 1), 1)
                        * 100
                    ),
                    "recent_activity": transaction_patterns.get("recent_activity", 0),
                    "contract_interactions": transaction_patterns.get(
                        "contract_interactions", 0
                    ),
                    "unique_addresses": transaction_patterns.get("unique_addresses", 0),
                    "high_value_transactions": transaction_patterns.get(
                        "high_value_transactions", 0
                    ),
                    "activity_frequency": transaction_patterns.get(
                        "time_analysis", {}
                    ).get("activity_frequency", 0),
                    "avg_gas_price": transaction_patterns.get("gas_analysis", {}).get(
                        "avg_gas_price", 0
                    ),
                    "total_fees_paid": transaction_patterns.get("gas_analysis", {}).get(
                        "total_fees", 0
                    ),
                },
                # Protocol Interaction Summary
                "protocol_summary": {
                    "protocols_identified": len(protocol_names),
                    "protocols_interacted": len(protocol_analysis.get("protocols", [])),
                    "high_risk_protocols": protocol_analysis.get(
                        "high_risk_protocols", 0
                    ),
                    "average_protocol_risk": protocol_analysis.get("average_risk", 0),
                    "diversification_score": protocol_analysis.get(
                        "diversification_score", 0
                    ),
                    "total_tvl_exposure": protocol_analysis.get(
                        "total_tvl_interacted", 0
                    ),
                    "protocol_categories": protocol_analysis.get("categories", []),
                    "risk_distribution": protocol_analysis.get("risk_distribution", {}),
                },
                # Asset and Balance Summary
                "asset_summary": {
                    "eth_balance": eth_balance,
                    "token_types": len(token_balances),
                    "is_contract": quicknode_analysis.get("is_contract", False),
                    "address_type": quicknode_analysis.get("address_type", "Unknown"),
                    "quicknode_tx_count": quicknode_analysis.get(
                        "transaction_count", 0
                    ),
                },
                # Detailed Component Analysis (for advanced users)
                "detailed_analysis": {
                    "transaction_risk_details": risk_analysis.get(
                        "detailed_analysis", {}
                    ).get("transaction_analysis", {}),
                    "protocol_risk_details": risk_analysis.get(
                        "detailed_analysis", {}
                    ).get("protocol_analysis", {}),
                    "asset_risk_details": risk_analysis.get(
                        "detailed_analysis", {}
                    ).get("concentration_analysis", {}),
                    "behavioral_risk_details": risk_analysis.get(
                        "detailed_analysis", {}
                    ).get("behavioral_analysis", {}),
                },
                # Raw Data (for debugging/advanced analysis)
                "raw_data": {
                    "transaction_patterns": transaction_patterns,
                    "protocol_analysis": protocol_analysis,
                    "balance_data": balance_data,
                    "contract_interactions_sample": contract_interactions[
                        :5
                    ],  # First 5 for space
                },
            }

            print(f"✅ Analysis completed in {analysis_time:.2f} seconds")
            return comprehensive_report

        except Exception as e:
            print(f"❌ Error during wallet analysis: {e}")
            return {
                "wallet_address": wallet_address,
                "error": str(e),
                "analysis_timestamp": datetime.now().isoformat(),
                "status": "failed",
            }

    def batch_analyze_wallets(
        self, wallet_addresses: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Analyze multiple wallets in batch

        Args:
            wallet_addresses: List of wallet addresses to analyze

        Returns:
            Dict mapping addresses to their risk analyses
        """
        results = {}
        total_wallets = len(wallet_addresses)

        print(f"🚀 NUVOLARI SAFE SCORE - BATCH RISK ANALYSIS")
        print("=" * 70)
        print(f"Analyzing {total_wallets} wallets...")
        print("=" * 70)

        for i, address in enumerate(wallet_addresses, 1):
            try:
                print(f"\n📍 WALLET {i}/{total_wallets}: {address}")
                print("-" * 50)

                analysis = self.analyze_wallet_comprehensive(address)
                results[address] = analysis

                if "error" not in analysis:
                    # Print summary
                    risk_score = analysis["risk_score"]
                    risk_level = analysis["risk_level"]

                    print(f"✅ ANALYSIS COMPLETE")
                    print(f"   Risk Score: {risk_score}/100 ({risk_level})")
                    print(
                        f"   Total Transactions: {analysis['transaction_summary']['total_transactions']}"
                    )
                    print(
                        f"   Success Rate: {analysis['transaction_summary']['success_rate']:.1f}%"
                    )
                    print(
                        f"   Protocols: {analysis['protocol_summary']['protocols_identified']}"
                    )
                    print(
                        f"   ETH Balance: {analysis['asset_summary']['eth_balance']:.4f} ETH"
                    )

                    # Show top risk factors
                    if analysis["risk_factors"]:
                        print(f"   Top Risk Factors:")
                        for factor in analysis["risk_factors"][:3]:
                            print(f"     • {factor}")
                else:
                    print(
                        f"❌ ANALYSIS FAILED: {analysis.get('error', 'Unknown error')}"
                    )

                # Brief pause to avoid rate limits
                time.sleep(1)

            except Exception as e:
                print(f"❌ Error analyzing {address}: {e}")
                results[address] = {
                    "error": str(e),
                    "wallet_address": address,
                    "analysis_timestamp": datetime.now().isoformat(),
                }

        return results

    def _extract_protocol_names(
        self, contract_interactions: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Extract protocol names from contract interactions using DIRECT ADDRESS MAPPING
        Uses DeFiLlama's contract address database - NO STATIC DATA OR GUESSING
        """
        if not contract_interactions:
            return ["No DeFi Interactions"]

        protocols = set()

        # Build contract address mapping from DeFiLlama (DIRECT APPROACH - NO GUESSING)
        address_mapping = self.defillama_client.build_contract_address_mapping()

        print(
            f"🔍 Built mapping for {len(address_mapping)} contract addresses from DeFiLlama"
        )

        # Direct address lookup for each contract interaction
        for interaction in contract_interactions:
            contract_address = interaction.get("to_address", "").lower()

            if contract_address and contract_address in address_mapping:
                protocol_name = address_mapping[contract_address]
                protocols.add(protocol_name)
                print(f"✅ Found protocol: {protocol_name} at {contract_address}")
            else:
                # Check if it's a token transfer vs unknown contract
                input_data = interaction.get("input_data", "0x")
                if input_data == "0x":
                    protocols.add("Token Transfer")
                else:
                    protocols.add("Unknown Protocol")

        # Return found protocols or fallback
        if protocols:
            return list(protocols)
        else:
            return ["No DeFi Interactions"]

    # OLD STATIC METHODS REMOVED ✅
    # - _analyze_function_signatures: Used hardcoded method signatures (0x38ed1739, etc.)
    # - _match_pattern_to_protocols: Used static pattern matching
    # REPLACED WITH: Direct contract address to protocol name mapping from DeFiLlama

    def generate_risk_report(
        self, analysis_results: Dict[str, Dict[str, Any]], output_file: str = None
    ) -> str:
        """Generate a comprehensive risk report from analysis results"""

        report_lines = []
        report_lines.append("🎯 NUVOLARI SAFE SCORE - COMPREHENSIVE RISK REPORT")
        report_lines.append("=" * 80)
        report_lines.append(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_lines.append(f"Wallets Analyzed: {len(analysis_results)}")
        report_lines.append("")

        # Filter successful analyses
        successful_analyses = {
            addr: data for addr, data in analysis_results.items() if "error" not in data
        }
        failed_analyses = {
            addr: data for addr, data in analysis_results.items() if "error" in data
        }

        if failed_analyses:
            report_lines.append(f"⚠️ Failed Analyses: {len(failed_analyses)}")
            for addr, data in failed_analyses.items():
                report_lines.append(f"   {addr}: {data.get('error', 'Unknown error')}")
            report_lines.append("")

        if not successful_analyses:
            report_lines.append("❌ No successful analyses to report")
            return "\n".join(report_lines)

        # Sort wallets by risk score (highest first)
        sorted_wallets = sorted(
            successful_analyses.items(),
            key=lambda x: x[1].get("risk_score", 0),
            reverse=True,
        )

        # Executive Summary
        report_lines.append("📊 EXECUTIVE SUMMARY")
        report_lines.append("-" * 40)

        risk_scores = [data["risk_score"] for _, data in successful_analyses.items()]
        avg_risk = sum(risk_scores) / len(risk_scores)
        max_risk = max(risk_scores)
        min_risk = min(risk_scores)

        high_risk_count = sum(1 for score in risk_scores if score >= 60)
        medium_risk_count = sum(1 for score in risk_scores if 40 <= score < 60)
        low_risk_count = sum(1 for score in risk_scores if score < 40)

        report_lines.append(f"Average Risk Score: {avg_risk:.1f}/100")
        report_lines.append(f"Risk Range: {min_risk:.1f} - {max_risk:.1f}")
        report_lines.append(f"Risk Distribution:")
        report_lines.append(f"  • High Risk (≥60): {high_risk_count} wallets")
        report_lines.append(f"  • Medium Risk (40-59): {medium_risk_count} wallets")
        report_lines.append(f"  • Low Risk (<40): {low_risk_count} wallets")
        report_lines.append("")

        # Detailed Wallet Analysis
        report_lines.append("🔍 DETAILED WALLET ANALYSIS")
        report_lines.append("=" * 40)

        for i, (address, analysis) in enumerate(sorted_wallets, 1):
            risk_score = analysis["risk_score"]
            risk_level = analysis["risk_level"]

            report_lines.append(f"\n{i}. WALLET: {address}")
            report_lines.append(f"   Risk Score: {risk_score}/100 ({risk_level})")
            report_lines.append(f"   Description: {analysis['risk_description']}")

            # Transaction summary
            tx_summary = analysis["transaction_summary"]
            report_lines.append(
                f"   Transactions: {tx_summary['total_transactions']} (Success: {tx_summary['success_rate']:.1f}%)"
            )
            report_lines.append(
                f"   ETH Balance: {analysis['asset_summary']['eth_balance']:.4f} ETH"
            )
            report_lines.append(
                f"   Token Types: {analysis['asset_summary']['token_types']}"
            )

            # Protocol summary
            protocol_summary = analysis["protocol_summary"]
            report_lines.append(
                f"   Protocols: {protocol_summary['protocols_identified']} identified"
            )

            # Component scores
            report_lines.append(f"   Component Scores:")
            for component, score in analysis["component_scores"].items():
                report_lines.append(
                    f"     • {component.replace('_', ' ').title()}: {score:.1f}/100"
                )

            # Top risk factors
            if analysis["risk_factors"]:
                report_lines.append(f"   Key Risk Factors:")
                for factor in analysis["risk_factors"][:3]:
                    report_lines.append(f"     • {factor}")

            # Top recommendations
            if analysis["recommendations"]:
                report_lines.append(f"   Recommendations:")
                for rec in analysis["recommendations"][:2]:
                    report_lines.append(f"     • {rec}")

        report_content = "\n".join(report_lines)

        # Save to file if specified
        if output_file:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(report_content)
                print(f"📄 Report saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error saving report: {e}")

        return report_content

    def close(self):
        """Close all client connections"""
        try:
            self.etherscan_client.close()
            self.quicknode_client.close()
            self.defillama_client.close()
            print("✅ All connections closed successfully")
        except Exception as e:
            print(f"⚠️ Error closing connections: {e}")


# Main execution function for testing and demonstration
def main():
    """
    Main function to test the risk agent with the provided wallet addresses
    This demonstrates the complete Risk Agent functionality
    """

    # Load environment variables from services/.env
    import dotenv
    import os

    # Load .env file from the same directory as this script
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    dotenv.load_dotenv(env_path)

    # Test wallet addresses provided by user
    test_wallets = [
        "0x7a29aE65Bf25Dfb6e554BF0468a6c23ed99a8DC2",
        "0x3feC8fd95b122887551c19c73F6b2bbf445B8C87",
        "0x38e247893BbC8517a317c54Ed34F9C62cb5F26c0",
        "0x51db92258a3ab0f81de0feab5d59a77e49b57275",
    ]

    print("🚀 NUVOLARI SAFE SCORE - RISK AGENT DEMONSTRATION")
    print("=" * 80)
    print(f"Initializing Risk Agent for {len(test_wallets)} wallets...")
    print("=" * 80)

    agent = RiskAgent()

    try:
        # Analyze all wallets
        results = agent.batch_analyze_wallets(test_wallets)

        # Generate comprehensive report
        print(f"\n" + "=" * 80)
        print("📋 GENERATING COMPREHENSIVE REPORT")
        print("=" * 80)

        report = agent.generate_risk_report(
            results, "nuvolari_risk_analysis_report.txt"
        )

        # Display summary statistics
        successful_results = {k: v for k, v in results.items() if "error" not in v}

        if successful_results:
            print(f"\n🎯 FINAL RISK ASSESSMENT SUMMARY")
            print("=" * 80)

            sorted_wallets = sorted(
                successful_results.items(),
                key=lambda x: x[1].get("risk_score", 0),
                reverse=True,
            )

            for i, (address, analysis) in enumerate(sorted_wallets, 1):
                risk_score = analysis["risk_score"]
                risk_level = analysis["risk_level"]

                print(f"{i}. {address[:10]}...{address[-8:]}")
                print(f"   🎯 Risk Score: {risk_score}/100 ({risk_level})")
                print(
                    f"   📊 Transactions: {analysis['transaction_summary']['total_transactions']}"
                )
                print(
                    f"   ✅ Success Rate: {analysis['transaction_summary']['success_rate']:.1f}%"
                )
                print(
                    f"   🏦 Protocols: {analysis['protocol_summary']['protocols_identified']}"
                )
                print(
                    f"   💰 ETH Balance: {analysis['asset_summary']['eth_balance']:.4f} ETH"
                )
                print("")

        # Save detailed results to JSON
        json_filename = "nuvolari_detailed_analysis.json"
        try:
            with open(json_filename, "w") as f:
                json.dump(results, f, indent=2, default=str)
            print(f"💾 Detailed JSON results saved to: {json_filename}")
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")

        print(
            f"\n✨ Analysis complete! Check the generated files for detailed insights."
        )

    except Exception as e:
        print(f"❌ Error during analysis: {e}")

    finally:
        agent.close()


if __name__ == "__main__":
    main()
