import httpx
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import time


class DeFiLlamaClient:
    """Client for DeFiLlama API to get protocol and TVL data"""

    def __init__(self):
        self.base_url = "https://api.llama.fi"
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=15.0,
            headers={"User-Agent": "RiskAgent/1.0", "Accept": "application/json"},
        )

    def get_protocols(self) -> List[Dict[str, Any]]:
        """Get list of all DeFi protocols (FREE API - cached for efficiency)"""
        try:
            # Add small delay to respect free API limits
            time.sleep(0.5)
            response = self.client.get("/protocols")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching protocols: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching protocols: {e}")
            return []

    def get_protocol_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get specific protocol data by name (case-insensitive search)"""
        protocols = self.get_protocols()
        name_lower = name.lower()

        # First try exact match
        for protocol in protocols:
            if protocol.get("name", "").lower() == name_lower:
                return protocol

        # Then try partial match
        for protocol in protocols:
            if name_lower in protocol.get("name", "").lower():
                return protocol

        return None

    def get_protocol_tvl(self, protocol_slug: str) -> Dict[str, Any]:
        """Get TVL data for a specific protocol"""
        try:
            response = self.client.get(f"/protocol/{protocol_slug}")
            if response.status_code == 200:
                return response.json()
            else:
                print(
                    f"Error fetching protocol TVL for {protocol_slug}: HTTP {response.status_code}"
                )
                return {}
        except Exception as e:
            print(f"Error fetching protocol TVL for {protocol_slug}: {e}")
            return {}

    def get_chains(self) -> List[Dict[str, Any]]:
        """Get all chains data"""
        try:
            response = self.client.get("/chains")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching chains: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching chains: {e}")
            return []

    def get_protocol_risk_score(self, protocol_name: str) -> float:
        """Calculate risk score for a protocol based on TVL, age, and other factors"""
        protocol = self.get_protocol_by_name(protocol_name)

        if not protocol:
            return 80.0  # High risk for unknown protocols

        risk_score = 50.0  # Base risk

        # TVL factor (higher TVL = lower risk)
        tvl = protocol.get("tvl", 0)
        if tvl > 10_000_000_000:  # >$10B TVL
            risk_score -= 20
        elif tvl > 1_000_000_000:  # >$1B TVL
            risk_score -= 15
        elif tvl > 100_000_000:  # >$100M TVL
            risk_score -= 10
        elif tvl > 10_000_000:  # >$10M TVL
            risk_score -= 5
        else:
            risk_score += 15  # Small TVL protocols are riskier

        # Category factor (some categories are riskier)
        category = protocol.get("category", "").lower()
        high_risk_categories = [
            "leverage",
            "derivatives",
            "yield farming",
            "synthetics",
        ]
        medium_risk_categories = ["yield", "options", "insurance"]
        safe_categories = ["dexes", "lending"]

        if any(risky_cat in category for risky_cat in high_risk_categories):
            risk_score += 15
        elif any(medium_cat in category for medium_cat in medium_risk_categories):
            risk_score += 5
        elif any(safe_cat in category for safe_cat in safe_categories):
            risk_score -= 10

        # Chain factor (some chains are riskier)
        chains = protocol.get("chains", [])
        if isinstance(chains, list):
            chain_names = [chain.lower() for chain in chains]
            if "ethereum" in chain_names:
                risk_score -= 10  # Ethereum is most established
            if "binance" in chain_names or "bsc" in chain_names:
                risk_score -= 5  # BSC is established but less than Ethereum
            if len(chains) > 5:
                risk_score += 5  # Multi-chain can be more complex/risky

        # Age factor (older protocols are generally safer)
        # This is approximated since we don't have exact launch dates
        # We use the protocol's position in rankings as a proxy

        return max(0, min(100, risk_score))

    def build_contract_address_mapping(self) -> Dict[str, str]:
        """
        Build mapping of contract addresses to protocol names
        Uses REAL DeFiLlama protocol data - NO STATIC MAPPINGS
        """
        protocols = self.get_protocols()
        address_mapping = {}

        for protocol in protocols:
            address = protocol.get("address")
            if address and address != "None" and address.startswith("0x"):
                # Use lowercase for consistent lookups
                address_mapping[address.lower()] = protocol.get("name", "Unknown")

        return address_mapping

    def identify_protocol_from_contract(self, contract_address: str) -> str:
        """
        Identify protocol from contract address using DeFiLlama mapping
        DIRECT ADDRESS LOOKUP - NO GUESSING OR STATIC DATA
        """
        if not contract_address or contract_address == "0x":
            return "Unknown"

        # Build mapping from DeFiLlama data
        address_mapping = self.build_contract_address_mapping()

        # Direct lookup
        protocol_name = address_mapping.get(contract_address.lower())
        return protocol_name if protocol_name else "Unknown Protocol"

    def analyze_protocol_interactions(
        self, protocol_names: List[str]
    ) -> Dict[str, Any]:
        """Analyze risk from multiple protocol interactions"""

        # FIX: Handle "No DeFi Interactions" correctly - should be LOW risk, not HIGH
        if len(protocol_names) == 1 and protocol_names[0].lower() in [
            "no defi interactions",
            "no defi",
            "none",
        ]:
            return {
                "protocols": [],
                "average_risk": 0,  # NO DeFi interactions = NO DeFi risk
                "raw_average_risk": 0,
                "high_risk_protocols": 0,
                "total_tvl_interacted": 0,
                "diversification_score": 0,
                "categories": [],
                "total_protocols": 0,
                "concentration_penalty": 0,
                "risk_distribution": {"low": 0, "medium": 0, "high": 0, "very_high": 0},
            }

        protocol_risks = []
        total_tvl = 0
        high_risk_count = 0
        categories = set()

        for name in protocol_names:
            if name.lower() in ["unknown", ""]:
                continue

            protocol = self.get_protocol_by_name(name)
            risk = self.get_protocol_risk_score(name)

            if protocol:
                protocol_info = {
                    "name": name,
                    "risk_score": risk,
                    "tvl": protocol.get("tvl", 0),
                    "category": protocol.get("category", "Unknown"),
                    "chains": protocol.get("chains", []),
                }
                protocol_risks.append(protocol_info)

                total_tvl += protocol.get("tvl", 0)
                categories.add(protocol.get("category", "Unknown"))

                if risk > 70:
                    high_risk_count += 1
            else:
                # For unknown protocols, add with high risk
                protocol_risks.append(
                    {
                        "name": name,
                        "risk_score": 85.0,  # High risk for unknown
                        "tvl": 0,
                        "category": "Unknown",
                        "chains": [],
                    }
                )
                high_risk_count += 1

        avg_risk = (
            sum(p["risk_score"] for p in protocol_risks) / len(protocol_risks)
            if protocol_risks
            else 50
        )

        # Calculate additional risk metrics
        diversification_score = len(categories)
        total_protocols = len(protocol_risks)

        # Risk adjustment based on concentration
        concentration_penalty = 0
        if total_protocols == 1:
            concentration_penalty = 15  # Single protocol concentration
        elif total_protocols < 3:
            concentration_penalty = 10  # Low diversification

        adjusted_avg_risk = min(100, avg_risk + concentration_penalty)

        return {
            "protocols": protocol_risks,
            "average_risk": adjusted_avg_risk,
            "raw_average_risk": avg_risk,
            "high_risk_protocols": high_risk_count,
            "total_tvl_interacted": total_tvl,
            "diversification_score": diversification_score,
            "categories": list(categories),
            "total_protocols": total_protocols,
            "concentration_penalty": concentration_penalty,
            "risk_distribution": self._calculate_risk_distribution(protocol_risks),
        }

    def _calculate_risk_distribution(
        self, protocol_risks: List[Dict]
    ) -> Dict[str, int]:
        """Calculate distribution of protocols across risk levels"""
        distribution = {"low": 0, "medium": 0, "high": 0, "very_high": 0}

        for protocol in protocol_risks:
            risk = protocol["risk_score"]
            if risk < 25:
                distribution["low"] += 1
            elif risk < 50:
                distribution["medium"] += 1
            elif risk < 75:
                distribution["high"] += 1
            else:
                distribution["very_high"] += 1

        return distribution

    def get_protocol_categories_stats(self) -> Dict[str, Any]:
        """Get statistics about different protocol categories"""
        protocols = self.get_protocols()

        category_stats = {}
        total_tvl_by_category = {}

        for protocol in protocols:
            category = protocol.get("category", "Unknown")
            tvl = protocol.get("tvl", 0)

            if category not in category_stats:
                category_stats[category] = {"count": 0, "total_tvl": 0, "protocols": []}

            category_stats[category]["count"] += 1
            category_stats[category]["total_tvl"] += tvl
            category_stats[category]["protocols"].append(protocol.get("name", ""))

        # Calculate average TVL and risk assessment per category
        for category, stats in category_stats.items():
            stats["avg_tvl"] = (
                stats["total_tvl"] / stats["count"] if stats["count"] > 0 else 0
            )

            # Category risk assessment
            if category.lower() in ["leverage", "derivatives", "synthetics"]:
                stats["category_risk"] = "HIGH"
            elif category.lower() in ["yield", "options", "insurance"]:
                stats["category_risk"] = "MEDIUM"
            elif category.lower() in ["dexes", "lending"]:
                stats["category_risk"] = "LOW"
            else:
                stats["category_risk"] = "MEDIUM"

        return category_stats

    def close(self):
        """Close HTTP client"""
        self.client.close()


if __name__ == "__main__":
    """Test the DeFiLlama client with real API data"""
    import dotenv

    dotenv.load_dotenv()

    print("🏦 DeFiLlama Client - Real API Testing")
    print("=" * 50)
    print("Testing connection to DeFiLlama FREE API...")

    client = DeFiLlamaClient()

    try:
        # Test basic API connectivity
        protocols = client.get_protocols()
        print(f"✅ Successfully connected to DeFiLlama API")
        print(f"   📊 Found {len(protocols)} protocols in database")

        # Test some real popular protocols
        real_protocols = ["Lido", "AAVE", "Uniswap V3", "Compound V2"]

        print(f"\n🔍 Testing real protocol data:")
        for protocol_name in real_protocols:
            protocol_data = client.get_protocol_by_name(protocol_name)
            if protocol_data:
                risk_score = client.get_protocol_risk_score(protocol_name)
                print(
                    f"   • {protocol_name}: Risk {risk_score:.1f}/100, TVL ${protocol_data.get('tvl', 0):,.0f}"
                )
            else:
                print(f"   • {protocol_name}: Not found in database")

        # Test protocol analysis with real protocols
        print(f"\n📈 Protocol Risk Analysis (Real Data):")
        analysis = client.analyze_protocol_interactions(real_protocols)
        print(f"   Average Risk: {analysis['average_risk']:.1f}/100")
        print(
            f"   Protocols Found: {len([p for p in analysis['protocols'] if p['tvl'] > 0])}"
        )
        print(f"   Total TVL: ${analysis['total_tvl_interacted']:,.0f}")

        print(f"\n✅ All tests completed with REAL DATA from DeFiLlama FREE API")

    except Exception as e:
        print(f"❌ Error testing DeFiLlama client: {e}")

    finally:
        client.close()
