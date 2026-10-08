def calculate_risk(transaction_data, policy_reasons):
    amount = float(transaction_data.get('amount', 0))
    score = 0
    reasons = list(policy_reasons)
    
    # Amount risk
    if amount <= 50:
        score += 5
    elif amount <= 100:
        score += 15
    else:
        score += 30
        
    # Merchant risk (mocked)
    merchant = transaction_data.get('merchant', '').lower()
    if 'unknown' in merchant:
        score += 30
        reasons.append({
            "type": "MERCHANT",
            "severity": "HIGH",
            "description": "Unknown or high-risk merchant."
        })
    elif 'new' in merchant:
        score += 15
        
    # Policy risk
    if policy_reasons:
        score += 25
        
    score = min(score, 100)
    
    level = "VERY LOW"
    if score > 20: level = "LOW"
    if score > 40: level = "MEDIUM"
    if score > 60: level = "HIGH"
    if score > 80: level = "CRITICAL"
    
    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }
