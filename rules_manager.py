"""
Rules Manager for Configurable Compliance Rules
Handles loading, saving, and managing risk assessment rules
"""

import json
from pathlib import Path
from typing import Dict, List

RULES_FILE = Path(__file__).parent / "rules_config.json"

class RulesManager:
    """Manages compliance rules configuration"""
    
    def __init__(self):
        self.rules = self.load_rules()
    
    def load_rules(self) -> Dict:
        """Load rules from JSON file"""
        try:
            if RULES_FILE.exists():
                with open(RULES_FILE, 'r') as f:
                    return json.load(f)
            else:
                return self._get_default_rules()
        except Exception as e:
            print(f"Error loading rules: {e}")
            return self._get_default_rules()
    
    def save_rules(self, rules: Dict) -> bool:
        """Save rules to JSON file"""
        try:
            with open(RULES_FILE, 'w') as f:
                json.dump(rules, f, indent=2)
            self.rules = rules
            return True
        except Exception as e:
            print(f"Error saving rules: {e}")
            return False
    
    def get_rules(self) -> Dict:
        """Get current rules"""
        return self.rules.copy()
    
    def update_rules(self, updates: Dict) -> bool:
        """Update specific rules"""
        try:
            self.rules.update(updates)
            return self.save_rules(self.rules)
        except Exception as e:
            print(f"Error updating rules: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset rules to default values"""
        return self.save_rules(self._get_default_rules())
    
    def _get_default_rules(self) -> Dict:
        """Get default rules configuration"""
        return {
            "high_risk_countries": [
                "Cayman Islands",
                "Nigeria",
                "Syria",
                "Iran",
                "North Korea"
            ],
            "medium_risk_countries": [
                "Vietnam",
                "Indonesia",
                "India"
            ],
            "low_risk_countries": [
                "Singapore",
                "United Kingdom",
                "Philippines",
                "United States"
            ],
            "high_risk_purposes": [
                "investment",
                "gambling",
                "crypto trading"
            ],
            "medium_risk_purposes": [
                "trade finance",
                "remittance"
            ],
            "low_risk_purposes": [
                "payroll",
                "services"
            ],
            "amount_thresholds": {
                "high_risk_origin_threshold": 10000,
                "general_high_threshold": 25000,
                "moderate_threshold": 15000
            },
            "risk_score_thresholds": {
                "low_max": 30,
                "medium_max": 70
            },
            "country_risk_scores": {
                "high": 35,
                "medium": 18,
                "low": 5
            },
            "purpose_risk_scores": {
                "high": 28,
                "medium": 15,
                "low": 3
            },
            "customer_type_scores": {
                "low": 5,
                "medium": 15,
                "high": 40
            }
        }
    
    def add_country(self, country: str, risk_level: str) -> bool:
        """Add a country to a risk level list"""
        key = f"{risk_level}_risk_countries"
        if key in self.rules and country not in self.rules[key]:
            self.rules[key].append(country)
            return self.save_rules(self.rules)
        return False
    
    def remove_country(self, country: str, risk_level: str) -> bool:
        """Remove a country from a risk level list"""
        key = f"{risk_level}_risk_countries"
        if key in self.rules and country in self.rules[key]:
            self.rules[key].remove(country)
            return self.save_rules(self.rules)
        return False
    
    def add_purpose(self, purpose: str, risk_level: str) -> bool:
        """Add a purpose to a risk level list"""
        key = f"{risk_level}_risk_purposes"
        if key in self.rules and purpose not in self.rules[key]:
            self.rules[key].append(purpose)
            return self.save_rules(self.rules)
        return False
    
    def remove_purpose(self, purpose: str, risk_level: str) -> bool:
        """Remove a purpose from a risk level list"""
        key = f"{risk_level}_risk_purposes"
        if key in self.rules and purpose in self.rules[key]:
            self.rules[key].remove(purpose)
            return self.save_rules(self.rules)
        return False

