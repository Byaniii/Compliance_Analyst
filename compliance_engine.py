"""
AML/KYC Compliance Review Engine for Money Transfers
Implements rule-based risk assessment with optional OpenAI-enhanced analysis
Supports configurable rules via RulesManager
"""

from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
import json
from rules_manager import RulesManager


class RiskLevel(Enum):
    """Risk levels for transactions"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class CustomerType(Enum):
    """Customer classification levels"""
    LOW = "low"  # freelancer
    MEDIUM = "medium"  # SMB
    HIGH = "high"  # PEP/NGO


@dataclass
class Transaction:
    """Transaction data for compliance review"""
    amount_usd: float
    origin_country: str
    destination_country: str
    purpose: str
    customer_type: CustomerType
    has_structuring_signals: bool = False


class ComplianceEngine:
    """Compliance review engine with AML/KYC rules"""

    def __init__(self, openai_client=None, rules_manager=None):
        self.triggered_rules: List[str] = []
        self.risk_score: int = 0
        self.openai_client = openai_client
        self.rules_manager = rules_manager or RulesManager()
        self._load_rules()
    
    def _load_rules(self):
        """Load rules from RulesManager"""
        rules = self.rules_manager.get_rules()
        
        # Geographic risk classifications
        self.HIGH_RISK_COUNTRIES = set(rules.get("high_risk_countries", []))
        self.MEDIUM_RISK_COUNTRIES = set(rules.get("medium_risk_countries", []))
        self.LOW_RISK_COUNTRIES = set(rules.get("low_risk_countries", []))
        
        # Transaction purpose risk classifications
        self.HIGH_RISK_PURPOSES = set(rules.get("high_risk_purposes", []))
        self.MEDIUM_RISK_PURPOSES = set(rules.get("medium_risk_purposes", []))
        self.LOW_RISK_PURPOSES = set(rules.get("low_risk_purposes", []))
        
        # Risk scoring base values
        self.COUNTRY_RISK_SCORES = rules.get("country_risk_scores", {
            "high": 35,
            "medium": 18,
            "low": 5,
        })
        
        self.PURPOSE_RISK_SCORES = rules.get("purpose_risk_scores", {
            "high": 28,
            "medium": 15,
            "low": 3,
        })
        
        customer_scores = rules.get("customer_type_scores", {
            "low": 5,
            "medium": 15,
            "high": 40,
        })
        self.CUSTOMER_TYPE_SCORES = {
            CustomerType.LOW: customer_scores.get("low", 5),
            CustomerType.MEDIUM: customer_scores.get("medium", 15),
            CustomerType.HIGH: customer_scores.get("high", 40),
        }
        
        # Thresholds
        thresholds = rules.get("amount_thresholds", {})
        self.HIGH_RISK_ORIGIN_THRESHOLD = thresholds.get("high_risk_origin_threshold", 10000)
        self.GENERAL_HIGH_THRESHOLD = thresholds.get("general_high_threshold", 25000)
        self.MODERATE_THRESHOLD = thresholds.get("moderate_threshold", 15000)
        
        score_thresholds = rules.get("risk_score_thresholds", {})
        self.LOW_MAX_SCORE = score_thresholds.get("low_max", 30)
        self.MEDIUM_MAX_SCORE = score_thresholds.get("medium_max", 70)
    
    def reload_rules(self):
        """Reload rules from configuration"""
        self._load_rules()

    def review(self, transaction: Transaction) -> Dict:
        """
        Perform compliance review on a transaction
        Returns JSON-formatted risk assessment
        """
        self.triggered_rules = []
        self.risk_score = 0
        checklist_items = []

        # Rule 1: Check country risk
        country_risk = self._assess_country_risk(transaction.origin_country)
        
        # Rule 2: Check purpose risk
        purpose_risk = self._assess_purpose_risk(transaction.purpose)

        # Rule 3: Customer type assessment
        customer_risk = self._assess_customer_risk(transaction.customer_type)

        # Rule 4: Amount threshold checks
        amount_risk = self._assess_amount_risk(
            transaction.amount_usd, 
            transaction.origin_country
        )

        # Rule 5: Structuring signals
        structuring_risk = self._assess_structuring(transaction.has_structuring_signals)

        # Calculate base risk score
        self.risk_score = (
            self.COUNTRY_RISK_SCORES[country_risk] +
            self.PURPOSE_RISK_SCORES[purpose_risk] +
            self.CUSTOMER_TYPE_SCORES[transaction.customer_type] +
            amount_risk
        )

        # Apply structuring adjustment (raises by one level)
        if structuring_risk > 0:
            self.risk_score += structuring_risk

        # Cap score at 100
        self.risk_score = min(self.risk_score, 100)

        # Determine risk level
        risk_level = self._score_to_level(self.risk_score)

        # Generate rationale
        rationale = self._generate_rationale(transaction, country_risk, purpose_risk)

        # Generate checklist
        checklist_items = self._generate_checklist(transaction, risk_level)

        # Enhance with OpenAI analysis if available
        ai_analysis = None
        if self.openai_client:
            try:
                ai_analysis = self._get_ai_risk_analysis(transaction, self.risk_score, risk_level)
            except Exception as e:
                print(f"OpenAI analysis failed: {e}")
                # Continue with rule-based assessment

        result = {
            "risk_score": self.risk_score,
            "risk_level": risk_level,
            "triggered_rules": self.triggered_rules,
            "rationale": rationale,
            "checklist_items": checklist_items,
        }

        # Add AI insights if available
        if ai_analysis:
            result["ai_insights"] = ai_analysis

        return result

    def _assess_country_risk(self, country: str) -> str:
        """Assess risk level of origin country"""
        if country in self.HIGH_RISK_COUNTRIES:
            self.triggered_rules.append(
                f"Origin country '{country}' classified as high-risk"
            )
            return "high"
        elif country in self.MEDIUM_RISK_COUNTRIES:
            self.triggered_rules.append(
                f"Origin country '{country}' classified as medium-risk"
            )
            return "medium"
        elif country in self.LOW_RISK_COUNTRIES:
            return "low"
        else:
            self.triggered_rules.append(
                f"Origin country '{country}' not in known risk database"
            )
            return "medium"  # Default to medium for unknown countries

    def _assess_purpose_risk(self, purpose: str) -> str:
        """Assess risk level of transaction purpose"""
        purpose_lower = purpose.lower()
        
        if purpose_lower in self.HIGH_RISK_PURPOSES:
            self.triggered_rules.append(
                f"Transaction purpose '{purpose}' classified as high-risk"
            )
            return "high"
        elif purpose_lower in self.MEDIUM_RISK_PURPOSES:
            self.triggered_rules.append(
                f"Transaction purpose '{purpose}' classified as medium-risk"
            )
            return "medium"
        elif purpose_lower in self.LOW_RISK_PURPOSES:
            return "low"
        else:
            self.triggered_rules.append(
                f"Transaction purpose '{purpose}' not in known database"
            )
            return "medium"  # Default to medium for unknown purposes

    def _assess_customer_risk(self, customer_type: CustomerType) -> str:
        """Assess risk based on customer type"""
        if customer_type == CustomerType.HIGH:
            self.triggered_rules.append(
                "Customer classified as PEP/NGO (high-risk profile)"
            )
            return "high"
        elif customer_type == CustomerType.MEDIUM:
            return "medium"
        else:
            return "low"

    def _assess_amount_risk(self, amount: float, country: str) -> int:
        """Assess risk based on transaction amount"""
        score = 0

        # Rule: If amount > threshold USD from a high-risk origin → High
        if amount > self.HIGH_RISK_ORIGIN_THRESHOLD and country in self.HIGH_RISK_COUNTRIES:
            self.triggered_rules.append(
                f"Amount ${amount:,.2f} exceeds ${self.HIGH_RISK_ORIGIN_THRESHOLD:,.0f} from high-risk country"
            )
            score += 40

        # Rule: If amount > general high threshold USD → High
        if amount > self.GENERAL_HIGH_THRESHOLD:
            self.triggered_rules.append(
                f"Amount ${amount:,.2f} exceeds ${self.GENERAL_HIGH_THRESHOLD:,.0f} threshold"
            )
            score += 40

        # Moderate threshold
        elif amount > self.MODERATE_THRESHOLD:
            self.triggered_rules.append(
                f"Amount ${amount:,.2f} is above moderate threshold (${self.MODERATE_THRESHOLD:,.0f})"
            )
            score += 15

        return score

    def _assess_structuring(self, has_signals: bool) -> int:
        """Assess structuring risk - raises risk by one level"""
        if has_signals:
            self.triggered_rules.append(
                "Structuring signals detected (multiple small transactions)"
            )
            return 15  # Raises risk by approximately one level
        return 0

    def _score_to_level(self, score: int) -> str:
        """Convert risk score to risk level"""
        if score <= self.LOW_MAX_SCORE:
            return RiskLevel.LOW.value
        elif score <= self.MEDIUM_MAX_SCORE:
            return RiskLevel.MEDIUM.value
        else:
            return RiskLevel.HIGH.value

    def _generate_rationale(
        self, transaction: Transaction, country_risk: str, purpose_risk: str
    ) -> str:
        """Generate human-readable rationale for the risk assessment"""
        parts = []

        # Country context
        if country_risk == "high":
            parts.append(
                f"Origin country {transaction.origin_country} is on the high-risk list."
            )
        elif country_risk == "medium":
            parts.append(
                f"Origin country {transaction.origin_country} is on the medium-risk list."
            )

        # Purpose context
        if purpose_risk == "high":
            parts.append(
                f"Transaction purpose '{transaction.purpose}' is classified as high-risk."
            )
        elif purpose_risk == "medium":
            parts.append(
                f"Transaction purpose '{transaction.purpose}' is classified as medium-risk."
            )

        # Amount context
        if transaction.amount_usd > 25000:
            parts.append(f"Transaction amount (${transaction.amount_usd:,.2f}) exceeds $25,000.")
        elif transaction.amount_usd > 10000:
            parts.append(f"Transaction amount (${transaction.amount_usd:,.2f}) exceeds $10,000.")

        # Customer context
        if transaction.customer_type == CustomerType.HIGH:
            parts.append("Customer classified as PEP/NGO profile (elevated risk).")

        # Structuring context
        if transaction.has_structuring_signals:
            parts.append("Potential structuring behavior detected.")

        rationale = " ".join(parts) if parts else "Transaction meets low-risk criteria."
        return rationale

    def _generate_checklist(self, transaction: Transaction, risk_level: str) -> List[str]:
        """Generate compliance checklist items based on risk level"""
        checklist = []

        # Universal checks
        checklist.append("Verify customer identity (KYC)")
        checklist.append("Confirm transaction purpose")
        checklist.append("Check sanctions lists (OFAC, UN, EU)")

        # Risk-based checks
        if risk_level == RiskLevel.HIGH.value:
            checklist.append("Escalate to compliance officer for manual review")
            checklist.append("Verify source of funds")
            checklist.append("Perform enhanced due diligence (EDD)")
            checklist.append("Check beneficial ownership information")
            checklist.append("Document business rationale")

        elif risk_level == RiskLevel.MEDIUM.value:
            checklist.append("Perform simplified due diligence (SDD)")
            checklist.append("Verify destination country compliance")
            if transaction.amount_usd > 10000:
                checklist.append("Document transaction rationale")

        else:  # LOW
            checklist.append("Standard AML checks sufficient")

        # Geographic checks
        if transaction.origin_country not in self.LOW_RISK_COUNTRIES:
            checklist.append(
                f"Research sanctions and regulatory status of {transaction.origin_country}"
            )

        # Purpose-specific checks
        if transaction.purpose.lower() in self.HIGH_RISK_PURPOSES:
            checklist.append(f"Verify legitimacy of {transaction.purpose} activity")

        return checklist

    def _get_ai_risk_analysis(
        self, 
        transaction: Transaction, 
        calculated_score: int, 
        calculated_level: str
    ) -> Optional[Dict]:
        """
        Use OpenAI to provide enhanced risk analysis and recommendations
        
        Returns:
            Dictionary with AI insights including:
            - enhanced_rationale: Deeper analysis of the risk factors
            - additional_red_flags: Potential concerns to investigate
            - recommendations: Specific actions to take
            - risk_adjustment: Suggested score adjustment (if any)
        """
        if not self.openai_client:
            return None

        # Construct prompt for OpenAI
        prompt = self._build_ai_prompt(transaction, calculated_score, calculated_level)

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert AML/KYC compliance officer with 15+ years of experience. "
                            "Your role is to provide insightful risk analysis for money transfer transactions. "
                            "Be thorough, professional, and focus on practical compliance considerations."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent, focused responses
                max_tokens=800,
                response_format={"type": "json_object"}
            )

            # Parse the response
            ai_response = json.loads(response.choices[0].message.content)
            
            return {
                "enhanced_rationale": ai_response.get("enhanced_rationale", ""),
                "additional_red_flags": ai_response.get("additional_red_flags", []),
                "recommendations": ai_response.get("recommendations", []),
                "risk_adjustment": ai_response.get("risk_adjustment", None),
                "confidence_level": ai_response.get("confidence_level", "medium")
            }

        except Exception as e:
            print(f"Error getting AI analysis: {e}")
            return None

    def _build_ai_prompt(
        self, 
        transaction: Transaction, 
        calculated_score: int, 
        calculated_level: str
    ) -> str:
        """Build the prompt for OpenAI analysis"""
        
        return f"""Analyze this money transfer transaction for AML/KYC compliance risks:

TRANSACTION DETAILS:
- Amount: ${transaction.amount_usd:,.2f} USD
- Origin Country: {transaction.origin_country}
- Destination Country: {transaction.destination_country}
- Purpose: {transaction.purpose}
- Customer Type: {transaction.customer_type.value}
- Structuring Signals: {"Yes" if transaction.has_structuring_signals else "No"}

RULE-BASED ASSESSMENT:
- Calculated Risk Score: {calculated_score}/100
- Risk Level: {calculated_level}
- Triggered Rules: {", ".join(self.triggered_rules) if self.triggered_rules else "None"}

Please provide a detailed compliance analysis in JSON format with the following structure:
{{
    "enhanced_rationale": "A detailed explanation of the risk factors, considering geopolitical context, transaction patterns, and compliance best practices",
    "additional_red_flags": ["List of specific concerns or patterns that warrant investigation"],
    "recommendations": ["Specific actionable steps the compliance team should take"],
    "risk_adjustment": {{
        "suggested_score": (number between 0-100, or null if rule-based score is appropriate),
        "justification": "Brief explanation if adjustment is suggested"
    }},
    "confidence_level": "high/medium/low - your confidence in this assessment"
}}

Focus on:
1. Contextual factors that rules-based systems might miss
2. Current geopolitical considerations for these countries
3. Industry-specific red flags related to the stated purpose
4. Pattern indicators that suggest legitimate vs. suspicious activity"""
