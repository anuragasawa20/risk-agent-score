import httpx
import os
import dotenv
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class EtherscanClient:

    def __init__(self) -> None:
        """Initialize the EtherscanClient"""
        self.API_KEY = os.getenv("ETHERSCAN_API_KEY")
        if not self.API_KEY:
            raise ValueError("ETHERSCAN_API_KEY environment variable is required")

        try:
            self.client = httpx.Client(
                base_url="https://api.etherscan.io/api",
                timeout=15.0,
            )
        except Exception as e:
            print(f"Error initializing EtherscanClient: {e}")
            raise e

    def get_transactions(self, address: str, limit: int = 100) -> dict:
        """Get transactions list for an address"""
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": limit,
            "sort": "desc",  # Most recent first
            "apikey": self.API_KEY,
        }
        response = self.client.get("", params=params)
        return response.json()

    def get_token_transactions(self, address: str, limit: int = 100) -> dict:
        """Get ERC-20 token transactions"""
        params = {
            "module": "account",
            "action": "tokentx",
            "address": address,
            "page": 1,
            "offset": limit,
            "sort": "desc",
            "apikey": self.API_KEY,
        }
        try:
            response = self.client.get("", params=params)
            return response.json()
        except Exception as e:
            print(f"Error fetching token transactions: {e}")
            return {"status": "0", "result": []}

    def get_eth_balance(self, address: str) -> float:
        """Get ETH balance for address"""
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest",
            "apikey": self.API_KEY,
        }
        try:
            response = self.client.get("", params=params)
            data = response.json()
            if data.get("status") == "1":
                balance_wei = int(data.get("result", "0"))
                return balance_wei / 10**18
            return 0.0
        except Exception as e:
            print(f"Error fetching ETH balance: {e}")
            return 0.0

    def get_token_balances(self, address: str) -> List[Dict[str, Any]]:
        """Get ERC-20 token balances by analyzing token transactions"""
        token_txs_data = self.get_token_transactions(address, 200)

        if token_txs_data.get("status") != "1":
            return []

        token_txs = token_txs_data.get("result", [])

        # Extract unique token contracts
        tokens = {}
        for tx in token_txs:
            contract_address = tx.get("contractAddress", "")
            if contract_address and contract_address not in tokens:
                tokens[contract_address] = {
                    "contract_address": contract_address,
                    "token_name": tx.get("tokenName", ""),
                    "token_symbol": tx.get("tokenSymbol", ""),
                    "token_decimal": tx.get("tokenDecimal", "18"),
                    "last_transaction": tx.get("timeStamp", "0"),
                }

        return list(tokens.values())

    def analyze_transaction_patterns(self, address: str) -> Dict[str, Any]:
        """Comprehensive transaction pattern analysis for risk assessment"""
        tx_data = self.get_transactions(address, 200)

        if tx_data.get("status") != "1":
            return {"error": "No transaction data available"}

        transactions = tx_data.get("result", [])

        if not transactions:
            return {"error": "No transactions found"}

        patterns = {
            "total_transactions": len(transactions),
            "successful_transactions": 0,
            "failed_transactions": 0,
            "unique_addresses": set(),
            "contract_interactions": 0,
            "high_value_transactions": 0,  # >1 ETH
            "recent_activity": 0,  # Last 30 days
            "gas_analysis": {"total_gas_used": 0, "avg_gas_price": 0, "total_fees": 0},
            "time_analysis": {
                "first_transaction": None,
                "last_transaction": None,
                "activity_frequency": 0,
            },
            "value_analysis": {
                "total_value_in": 0,
                "total_value_out": 0,
                "largest_transaction": 0,
                "avg_transaction_value": 0,
            },
            "address_interactions": {
                "most_frequent_addresses": {},
                "interaction_diversity": 0,
            },
        }

        current_time = datetime.now().timestamp()
        thirty_days_ago = current_time - (30 * 24 * 60 * 60)

        gas_prices = []
        transaction_times = []
        address_frequency = defaultdict(int)
        transaction_values = []

        for tx in transactions:
            # Basic counts
            if tx.get("txreceipt_status") == "1":
                patterns["successful_transactions"] += 1
            else:
                patterns["failed_transactions"] += 1

            # Address tracking
            from_addr = tx.get("from", "").lower()
            to_addr = tx.get("to", "").lower()
            patterns["unique_addresses"].add(from_addr)
            patterns["unique_addresses"].add(to_addr)

            # Address frequency analysis
            if from_addr != address.lower():
                address_frequency[from_addr] += 1
            if to_addr != address.lower():
                address_frequency[to_addr] += 1

            # Contract interactions
            if tx.get("input", "0x") != "0x":
                patterns["contract_interactions"] += 1

            # Value analysis
            value_wei = int(tx.get("value", "0"))
            value_eth = value_wei / 10**18
            transaction_values.append(value_eth)

            if value_eth > 1:
                patterns["high_value_transactions"] += 1

            patterns["value_analysis"]["largest_transaction"] = max(
                patterns["value_analysis"]["largest_transaction"], value_eth
            )

            # Direction-based value tracking
            if from_addr == address.lower():
                patterns["value_analysis"]["total_value_out"] += value_eth
            else:
                patterns["value_analysis"]["total_value_in"] += value_eth

            # Time analysis
            timestamp = int(tx.get("timeStamp", "0"))
            transaction_times.append(timestamp)

            if timestamp > thirty_days_ago:
                patterns["recent_activity"] += 1

            # Gas analysis
            gas_used = int(tx.get("gasUsed", "0"))
            gas_price = int(tx.get("gasPrice", "0"))

            patterns["gas_analysis"]["total_gas_used"] += gas_used
            gas_prices.append(gas_price)
            patterns["gas_analysis"]["total_fees"] += (gas_used * gas_price) / 10**18

        # Calculate derived metrics
        if gas_prices:
            patterns["gas_analysis"]["avg_gas_price"] = (
                sum(gas_prices) / len(gas_prices) / 10**9
            )  # In Gwei

        if transaction_values:
            patterns["value_analysis"]["avg_transaction_value"] = sum(
                transaction_values
            ) / len(transaction_values)

        patterns["unique_addresses"] = len(patterns["unique_addresses"])

        # Address interaction analysis
        patterns["address_interactions"]["most_frequent_addresses"] = dict(
            sorted(address_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        patterns["address_interactions"]["interaction_diversity"] = len(
            address_frequency
        )

        if transaction_times:
            patterns["time_analysis"]["first_transaction"] = min(transaction_times)
            patterns["time_analysis"]["last_transaction"] = max(transaction_times)

            # Activity frequency (transactions per day)
            time_span = max(transaction_times) - min(transaction_times)
            if time_span > 0:
                patterns["time_analysis"]["activity_frequency"] = len(transactions) / (
                    time_span / (24 * 60 * 60)
                )

        return patterns

    def get_contract_interactions(self, address: str) -> List[Dict[str, Any]]:
        """Get detailed contract interaction analysis"""
        tx_data = self.get_transactions(address, 100)

        if tx_data.get("status") != "1":
            return []

        transactions = tx_data.get("result", [])
        contract_interactions = []

        for tx in transactions:
            if tx.get("input", "0x") != "0x":
                contract_interactions.append(
                    {
                        "hash": tx.get("hash", ""),
                        "to": tx.get("to", ""),
                        "function_name": tx.get("functionName", ""),
                        "method_id": tx.get("methodId", ""),
                        "input_data": tx.get("input", ""),
                        "value": int(tx.get("value", "0")) / 10**18,
                        "gas_used": int(tx.get("gasUsed", "0")),
                        "gas_price": int(tx.get("gasPrice", "0")),
                        "timestamp": int(tx.get("timeStamp", "0")),
                        "status": tx.get("txreceipt_status", "0"),
                        "block_number": int(tx.get("blockNumber", "0")),
                    }
                )

        return contract_interactions

    def get_wallet_summary(self, address: str) -> Dict[str, Any]:
        """Get comprehensive wallet summary"""
        print(f"📊 Analyzing wallet: {address}")

        # Get all data
        eth_balance = self.get_eth_balance(address)
        token_balances = self.get_token_balances(address)
        transaction_patterns = self.analyze_transaction_patterns(address)
        contract_interactions = self.get_contract_interactions(address)

        return {
            "wallet_address": address,
            "eth_balance": eth_balance,
            "token_count": len(token_balances),
            "tokens": token_balances,
            "transaction_patterns": transaction_patterns,
            "contract_interactions": len(contract_interactions),
            "contract_details": contract_interactions[:10],  # First 10 for summary
        }

    def close(self):
        """close the HTTP Client"""
        self.client.close()


if __name__ == "__main__":
    dotenv.load_dotenv()

    try:
        client = EtherscanClient()
        client.get_transactions("0x51dB92258A3ab0F81de0FEAB5D59a77e49B57275")
        client.close()
    except ValueError as ve:
        print(f"Configuration error: {ve}")
    except Exception as e:
        print(f"Error: {e}")
