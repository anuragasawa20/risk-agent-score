import requests
import os
import dotenv
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class QuicknodeClient:

    def __init__(self) -> None:
        """Initialize the QuicknodeClient"""
        # self.API_KEY = os.getenv("QUICKNODE_API_KEY")
        # if not self.API_KEY:
        #     raise ValueError("QUICKNODE_API_KEY environment variable is required")

        self.base_url = "https://orbital-proportionate-slug.quiknode.pro/71c12b7ae395e620531c4a4f7855f73b4c16c85e/"
        self.headers = {"Content-Type": "application/json"}

        try:
            # Create a session for connection pooling and better performance
            self.session = requests.Session()
            self.session.headers.update(self.headers)

            # Test the connection with a simple call
            test_payload = {
                "method": "eth_blockNumber",
                "params": [],
                "id": 1,
                "jsonrpc": "2.0",
            }
            response = self.session.post(self.base_url, json=test_payload)
            response.raise_for_status()
            print(f"Connection test successful. Current block: {response.json()}")

        except Exception as e:
            print(f"Error initializing QuicknodeClient: {e}")
            raise e

    def get_balance(self, address: str) -> dict:
        """Get balance for an ethereum address"""
        payload = {
            "method": "eth_getBalance",
            "params": [address, "latest"],
            "id": 1,
            "jsonrpc": "2.0",
        }

        try:
            response = self.session.post(self.base_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result
        except Exception as e:
            print(f"Error getting balance: {e}")
            raise e

    def get_balance_wei_to_eth(self, address: str) -> float:
        """Get balance and convert from Wei to ETH"""
        balance_data = self.get_balance(address)

        if "result" in balance_data:
            balance_wei = int(balance_data["result"], 16)  # Convert hex to int
            balance_eth = balance_wei / 10**18
            return balance_eth
        return 0.0

    def get_transactions(self, address: str, page: int = 1, per_page: int = 20) -> dict:
        """Get transactions for an address using QuickNode's enhanced API"""
        payload = {
            "method": "qn_getTransactionsByAddress",
            "params": [{"address": address, "page": page, "perPage": per_page}],
            "id": 1,
            "jsonrpc": "2.0",
        }

        try:
            response = self.session.post(self.base_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return {"result": {"transactions": []}}

    def get_transaction_count(self, address: str) -> int:
        """Get total transaction count for an address"""
        payload = {
            "method": "eth_getTransactionCount",
            "params": [address, "latest"],
            "id": 1,
            "jsonrpc": "2.0",
        }

        try:
            response = self.session.post(self.base_url, json=payload)
            response.raise_for_status()
            result = response.json()

            if "result" in result:
                return int(result["result"], 16)  # Convert hex to int
            return 0
        except Exception as e:
            print(f"Error getting transaction count: {e}")
            return 0

    def get_block_number(self) -> int:
        """Get current block number"""
        payload = {
            "method": "eth_blockNumber",
            "params": [],
            "id": 1,
            "jsonrpc": "2.0",
        }

        try:
            response = self.session.post(self.base_url, json=payload)
            response.raise_for_status()
            result = response.json()

            if "result" in result:
                return int(result["result"], 16)
            return 0
        except Exception as e:
            print(f"Error getting block number: {e}")
            return 0

    def get_transaction_by_hash(self, tx_hash: str) -> Dict[str, Any]:
        """Get detailed transaction information by hash"""
        payload = {
            "method": "eth_getTransactionByHash",
            "params": [tx_hash],
            "id": 1,
            "jsonrpc": "2.0",
        }

        try:
            response = self.session.post(self.base_url, json=payload)
            response.raise_for_status()
            result = response.json()

            return result.get("result", {})
        except Exception as e:
            print(f"Error getting transaction {tx_hash}: {e}")
            return {}

    def get_transaction_receipt(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction receipt by hash"""
        payload = {
            "method": "eth_getTransactionReceipt",
            "params": [tx_hash],
            "id": 1,
            "jsonrpc": "2.0",
        }

        try:
            response = self.session.post(self.base_url, json=payload)
            response.raise_for_status()
            result = response.json()

            return result.get("result", {})
        except Exception as e:
            print(f"Error getting transaction receipt {tx_hash}: {e}")
            return {}

    def get_code(self, address: str) -> str:
        """Get code at address (to check if it's a contract)"""
        payload = {
            "method": "eth_getCode",
            "params": [address, "latest"],
            "id": 1,
            "jsonrpc": "2.0",
        }

        try:
            response = self.session.post(self.base_url, json=payload)
            response.raise_for_status()
            result = response.json()

            return result.get("result", "0x")
        except Exception as e:
            print(f"Error getting code for {address}: {e}")
            return "0x"

    def is_contract(self, address: str) -> bool:
        """Check if address is a smart contract"""
        code = self.get_code(address)
        return code != "0x" and len(code) > 2

    def get_gas_price(self) -> int:
        """Get current gas price"""
        payload = {
            "method": "eth_gasPrice",
            "params": [],
            "id": 1,
            "jsonrpc": "2.0",
        }

        try:
            response = self.session.post(self.base_url, json=payload)
            response.raise_for_status()
            result = response.json()

            if "result" in result:
                return int(result["result"], 16)
            return 0
        except Exception as e:
            print(f"Error getting gas price: {e}")
            return 0

    def analyze_address_type(self, address: str) -> Dict[str, Any]:
        """Analyze address to determine if it's EOA or contract and gather basic info"""
        is_contract_addr = self.is_contract(address)
        balance_eth = self.get_balance_wei_to_eth(address)
        tx_count = self.get_transaction_count(address)

        analysis = {
            "address": address,
            "is_contract": is_contract_addr,
            "address_type": (
                "Contract" if is_contract_addr else "Externally Owned Account (EOA)"
            ),
            "eth_balance": balance_eth,
            "transaction_count": tx_count,
            "analysis_timestamp": datetime.now().isoformat(),
        }

        return analysis

    def batch_get_balances(self, addresses: List[str]) -> Dict[str, float]:
        """Get balances for multiple addresses efficiently"""
        balances = {}

        for address in addresses:
            try:
                balance = self.get_balance_wei_to_eth(address)
                balances[address] = balance
            except Exception as e:
                print(f"Error getting balance for {address}: {e}")
                balances[address] = 0.0

        return balances

    def get_enhanced_transaction_data(
        self, address: str, limit: int = 50
    ) -> Dict[str, Any]:
        """Get enhanced transaction data with additional QuickNode features"""
        # Get basic transactions
        tx_data = self.get_transactions(address, per_page=limit)

        if not tx_data.get("result") or not tx_data["result"].get("transactions"):
            return {"error": "No transaction data available"}

        transactions = tx_data["result"]["transactions"]

        enhanced_data = {
            "address": address,
            "total_transactions": len(transactions),
            "enhanced_transactions": [],
            "analysis": {
                "contract_interactions": 0,
                "unique_counterparties": set(),
                "total_gas_used": 0,
                "total_value_transferred": 0.0,
            },
        }

        for tx in transactions:
            # Enhanced transaction with additional data
            enhanced_tx = {
                "hash": tx.get("hash", ""),
                "from": tx.get("from", ""),
                "to": tx.get("to", ""),
                "value_wei": int(tx.get("value", "0"), 16) if tx.get("value") else 0,
                "value_eth": (
                    int(tx.get("value", "0"), 16) / 10**18 if tx.get("value") else 0
                ),
                "gas": int(tx.get("gas", "0"), 16) if tx.get("gas") else 0,
                "gas_price": (
                    int(tx.get("gasPrice", "0"), 16) if tx.get("gasPrice") else 0
                ),
                "block_number": (
                    int(tx.get("blockNumber", "0"), 16) if tx.get("blockNumber") else 0
                ),
                "input_data": tx.get("input", "0x"),
                "timestamp": tx.get("timestamp", ""),
                "is_contract_interaction": len(tx.get("input", "0x")) > 2,
            }

            enhanced_data["enhanced_transactions"].append(enhanced_tx)

            # Update analysis
            if enhanced_tx["is_contract_interaction"]:
                enhanced_data["analysis"]["contract_interactions"] += 1

            enhanced_data["analysis"]["unique_counterparties"].add(enhanced_tx["from"])
            enhanced_data["analysis"]["unique_counterparties"].add(enhanced_tx["to"])
            enhanced_data["analysis"]["total_gas_used"] += enhanced_tx["gas"]
            enhanced_data["analysis"]["total_value_transferred"] += enhanced_tx[
                "value_eth"
            ]

        # Convert set to count
        enhanced_data["analysis"]["unique_counterparties"] = len(
            enhanced_data["analysis"]["unique_counterparties"]
        )

        return enhanced_data

    def close(self):
        """Close the HTTP Client"""
        if hasattr(self, "session"):
            self.session.close()


if __name__ == "__main__":
    dotenv.load_dotenv()

    try:
        client = QuicknodeClient()

        # Test address
        address = "0x51dB92258A3ab0F81de0FEAB5D59a77e49B57275"

        # Get balance
        balance_result = client.get_balance(address)

        # Get transaction count
        tx_count_result = client.get_transactions(address)

        client.close()

    except ValueError as ve:
        print(f"Configuration error: {ve}")
    except Exception as e:
        print(f"Error: {e}")
