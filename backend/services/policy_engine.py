def evaluate_policy(transaction_data, policy):
    reasons = []
    
    amount = float(transaction_data.get('amount', 0))
    autonomous_limit = float(policy.autonomous_limit) if policy.autonomous_limit else 100.0
    
    if amount > autonomous_limit:
        reasons.append({
            "type": "POLICY",
            "severity": "HIGH",
            "description": f"Transaction exceeds autonomous spending limit of ${autonomous_limit:.2f}."
        })
    
    # We could check daily and monthly limits here...
    
    is_new_merchant = True # Mock logic
    if is_new_merchant and policy.new_merchant_approval:
        reasons.append({
            "type": "POLICY",
            "severity": "MEDIUM",
            "description": "Merchant is new and requires approval based on policy."
        })
        
    return reasons
