"""
Google Gemini AI Integration for Risk Analysis
Provides LLM-powered risk assessment capabilities.
"""

import json
import os
import time
from typing import Dict, Any, Optional
import dotenv
from ..config import LLM_CONFIG


class GeminiRiskAnalyzer:
    """Handles Gemini AI integration for wallet risk analysis"""

    def __init__(self):
        """Initialize the Gemini client"""
        self.model_name = LLM_CONFIG["model_name"]
        self.temperature = LLM_CONFIG["temperature"]
        self.max_tokens = LLM_CONFIG["max_output_tokens"]
        self.timeout = LLM_CONFIG["timeout_seconds"]

        # Load environment variables
        env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        dotenv.load_dotenv(env_path)

    def is_available(self) -> bool:
        """Check if Gemini API is available (has API key)"""
        return os.getenv("GEMINI_API_KEY") is not None

    def _call_gemini_api(self, prompt: str) -> Optional[str]:
        """
        Make API call to Gemini.

        Args:
            prompt: The prompt to send to Gemini

        Returns:
            Response text or None if failed
        """
        try:
            print("   🔌 Connecting to Google Gemini API...")
            import google.generativeai as genai

            # Configure Gemini
            print("   🔑 Authenticating with Gemini...")
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

            # Initialize the model
            print(f"   🧠 Loading {self.model_name} model...")
            model = genai.GenerativeModel(self.model_name)

            # Create system prompt
            system_prompt = (
                "You are an expert cryptocurrency risk analyst. "
                "Analyze wallet data and provide risk scores (0-100) with reasoning."
            )
            full_prompt = f"{system_prompt}\n\n{prompt}"

            print("   💭 Sending wallet data to Gemini for analysis...")
            print(f"   📝 Prompt length: {len(full_prompt)} characters")

            # Generate response with timeout
            api_start = time.time()
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                ),
            )
            api_duration = time.time() - api_start

            print(f"   ⚡ Gemini response received in {api_duration:.2f}s")
            print(f"   📤 Response length: {len(response.text)} characters")

            return response.text

        except Exception as e:
            print(f"   ❌ Gemini API call failed: {e}")
            return None

    def _parse_gemini_response(self, response: str) -> Dict[str, Any]:
        """
        Parse Gemini's JSON response.

        Args:
            response: Raw response from Gemini

        Returns:
            Parsed response dictionary
        """
        try:
            # Clean the response - Gemini often returns markdown-wrapped JSON
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]  # Remove ```json
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]  # Remove ending ```
            cleaned_response = cleaned_response.strip()

            print(
                f"   🧹 Cleaned response (first 100 chars): {cleaned_response[:100]}..."
            )

            parsed = json.loads(cleaned_response)

            # Validate required fields
            if "overall_risk_score" not in parsed:
                print("   ⚠️  Warning: Gemini didn't return overall_risk_score")
                parsed["overall_risk_score"] = 50  # Default fallback

            extracted_score = parsed.get("overall_risk_score", 50)
            print(f"   ✅ Successfully parsed Gemini score: {extracted_score}/100")

            return {
                "llm_risk_score": extracted_score,
                "component_scores": parsed.get("component_scores", {}),
                "reasoning": parsed.get("risk_reasoning", "Gemini analysis completed"),
                "key_insights": parsed.get("key_insights", []),
                "raw_response": response,
            }

        except json.JSONDecodeError as json_error:
            print(f"   ❌ JSON parsing failed: {json_error}")
            print(f"   📝 Raw response (first 200 chars): {response[:200]}...")

            # Fallback response
            return {
                "llm_risk_score": 50,
                "reasoning": f"Gemini response could not be parsed: {str(json_error)}",
                "component_scores": {},
                "raw_response": response,
            }

    def analyze_wallet_risk(
        self,
        patterns: Dict[str, Any],
        protocol_analysis: Dict[str, Any],
        balances: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate comprehensive risk assessment using Gemini AI.

        Args:
            patterns: Transaction patterns data
            protocol_analysis: Protocol interaction data
            balances: Wallet balance data

        Returns:
            Risk analysis results from Gemini
        """
        if not self.is_available():
            print("🤖 Gemini AI: Not available (no GEMINI_API_KEY found)")
            return {
                "llm_risk_score": None,
                "reasoning": "Gemini analysis not available (no API key)",
                "component_scores": {},
            }

        print("🤖 Gemini AI: ✅ API key detected, starting AI analysis...")
        print("   📊 Preparing wallet data for Gemini...")

        start_time = time.time()

        # Extract key metrics for analysis
        total_transactions = patterns.get("total_transactions", 0)
        success_rate = (
            patterns.get("successful_transactions", 0)
            / max(total_transactions, 1)
            * 100
        )
        contract_interactions = patterns.get("contract_interactions", 0)

        # Get frequent addresses for protocol identification
        frequent_addresses = patterns.get("address_interactions", {}).get(
            "most_frequent_addresses", {}
        )
        top_addresses = dict(list(frequent_addresses.items())[:5])

        # Get token information
        tokens = balances.get("tokens", [])[:10]  # Top 10 tokens
        token_info = [
            f"{t.get('token_name', 'Unknown')} ({t.get('token_symbol', 'UNK')})"
            for t in tokens
        ]

        # Value flow analysis
        value_analysis = patterns.get("value_analysis", {})
        total_in = value_analysis.get("total_value_in", 0)
        total_out = value_analysis.get("total_value_out", 0)

        # Build comprehensive prompt
        prompt = f"""
        WALLET RISK ANALYSIS REQUEST

        TRANSACTION PATTERNS:
        - Total Transactions: {total_transactions}
        - Success Rate: {success_rate:.1f}%
        - Contract Interactions: {contract_interactions}
        - Value Flow: ${total_out:.2f} out vs ${total_in:.2f} in
        - ETH Balance: {balances.get('eth_balance', 0):.4f} ETH

        MOST FREQUENT CONTRACT INTERACTIONS:
        {json.dumps(top_addresses, indent=2)}

        TOKEN HOLDINGS (Top 10):
        {json.dumps(token_info, indent=2)}

        CURRENT PROTOCOL ANALYSIS:
        - Protocols Identified: {protocol_analysis.get('total_protocols', 0)}
        - Average Protocol Risk: {protocol_analysis.get('average_risk', 0)}

        Please provide a comprehensive risk assessment with scores for each component:

        Respond in this JSON format:
        {{
            "overall_risk_score": <0-100>,
            "component_scores": {{
                "transaction_patterns": <0-100>,
                "protocol_interactions": <0-100>,
                "asset_concentration": <0-100>,
                "behavioral_patterns": <0-100>
            }},
            "risk_reasoning": "<explain the main risk factors and score rationale>",
            "key_insights": [
                "<insight 1>",
                "<insight 2>",
                "<insight 3>"
            ]
        }}
        """

        print("   🚀 Calling Gemini API...")

        try:
            response = self._call_gemini_api(prompt)
            analysis_duration = time.time() - start_time

            if not response:
                print(
                    f"   ❌ Gemini API returned no response after {analysis_duration:.2f}s"
                )
                return {
                    "llm_risk_score": None,
                    "reasoning": "Gemini API call failed",
                    "component_scores": {},
                }

            print(f"   🎯 Gemini analysis completed in {analysis_duration:.2f}s total")
            print("   🔧 Parsing Gemini response...")

            return self._parse_gemini_response(response)

        except Exception as api_error:
            analysis_duration = time.time() - start_time
            print(
                f"   ❌ Gemini API call failed after {analysis_duration:.2f}s: {api_error}"
            )
            return {
                "llm_risk_score": None,
                "reasoning": f"Gemini API error: {str(api_error)}",
                "component_scores": {},
            }
