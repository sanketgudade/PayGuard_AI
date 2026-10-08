import google.generativeai as genai
from flask import current_app
from .policy_engine import evaluate_policy
from .risk_engine import calculate_risk
import json

def analyze_transaction(transaction_data, policy):
    # Rule-based parts
    policy_reasons = evaluate_policy(transaction_data, policy)
    risk_assessment = calculate_risk(transaction_data, policy_reasons)
    
    decision = "APPROVE"
    recommendation = "Safe to proceed autonomously."
    
    if risk_assessment["level"] in ["HIGH", "CRITICAL"] or policy_reasons:
        decision = "REQUIRE_APPROVAL"
        recommendation = "Human approval required due to high risk or policy rules."
        
    if risk_assessment["level"] == "CRITICAL" and policy.high_risk_block:
        decision = "BLOCK"
        recommendation = "Transaction blocked automatically due to critical risk."

    # In a full hackathon version, we would call Gemini here to enrich the response
    # and generate a natural language explanation.
    # For now, we simulate the AI output structure to keep it robust.

    # ai_explanation = "..." 

    return {
        "risk_score": risk_assessment["score"],
        "risk_level": risk_assessment["level"],
        "decision": decision,
        "recommendation": recommendation,
        "reasons": risk_assessment["reasons"]
    }
