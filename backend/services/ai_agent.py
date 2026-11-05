import os
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

    # Google Gemini GenAI Integration
    ai_explanation = None
    ai_api_key = current_app.config.get('AI_API_KEY') or os.getenv('AI_API_KEY')
    if ai_api_key and "your_" not in ai_api_key:
        try:
            genai.configure(api_key=ai_api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = (
                f"You are PayGuard AI, an intelligent fintech security auditor. "
                f"Review this autonomous payment attempt:\n"
                f"- Merchant: {transaction_data.get('merchant', 'Unknown')}\n"
                f"- Amount: ${transaction_data.get('amount', 0)} {transaction_data.get('currency', 'USD')}\n"
                f"- Category: {transaction_data.get('category', 'General')}\n"
                f"- Intent Context: {transaction_data.get('context', 'None provided')}\n"
                f"- Calculated Risk Score: {risk_assessment['score']}/100 ({risk_assessment['level']})\n"
                f"- System Decision: {decision}\n\n"
                f"Provide a concise, professional 1-sentence explanation summarizing why this transaction was {decision.lower()}."
            )
            response = model.generate_content(prompt)
            if response and response.text:
                ai_explanation = response.text.strip()
        except Exception as e:
            print(f"Gemini generation notice: {e}")

    return {
        "risk_score": risk_assessment["score"],
        "risk_level": risk_assessment["level"],
        "decision": decision,
        "recommendation": recommendation,
        "reasons": risk_assessment["reasons"],
        "ai_explanation": ai_explanation
    }
