import numpy as np

def analyze_risk(labor_cost, material_cost, equipment_cost, miscellaneous_cost, duration):
    """Analyze potential cost overrun risks based on input parameters."""
    
    risk_score = 0

    # High labor & material cost → Higher risk
    if labor_cost > 15000 or material_cost > 30000:
        risk_score += 3
    elif labor_cost > 10000 or material_cost > 20000:
        risk_score += 2
    else:
        risk_score += 1

    # Long project duration → Higher risk of delays
    if duration > 12:
        risk_score += 3
    elif duration > 6:
        risk_score += 2
    else:
        risk_score += 1

    # Equipment cost impact
    if equipment_cost > 10000:
        risk_score += 2

    # Miscellaneous costs above $3000 indicate unexpected expenses
    if miscellaneous_cost > 3000:
        risk_score += 2

    # Assign risk levels
    if risk_score >= 7:
        risk_level = "🔴 High Risk: Cost Overrun Likely!"
    elif risk_score >= 4:
        risk_level = "🟠 Medium Risk: Some Overruns Possible."
    else:
        risk_level = "🟢 Low Risk: Project Costs are Stable."

    return risk_level, risk_score
