import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_llm_explanation(company_data, risk_analysis, loan_terms):
    """
    Generate AI-powered explanation using OpenAI
    Falls back to rule-based if API key not available
    """
    
    try:
        import openai
        
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            return generate_fallback_explanation(company_data, risk_analysis, loan_terms)
        
        openai.api_key = api_key
        
        prompt = f"""
You are a senior credit analyst at a commercial bank. Analyze the following loan application and provide a detailed, professional explanation of the credit decision.

Company Information:
- Name: {company_data.get('company_name')}
- Industry: {company_data.get('industry')}
- Annual Revenue: ${company_data.get('revenue')}M
- Years in Business: {company_data.get('years_in_business')}
- Loan Amount Requested: ${company_data.get('loan_amount')}M
- Purpose: {company_data.get('purpose')}

Risk Assessment:
- Risk Level: {risk_analysis['risk_level']}
- Risk Score: {risk_analysis['risk_score']}/100
- Key Risk Factors:
{chr(10).join('  - ' + factor for factor in risk_analysis['risk_factors'])}

Proposed Loan Terms:
- Tenor: {loan_terms['tenor']}
- Interest Rate: {loan_terms['interest_margin']}
- Amortization: {loan_terms['amortization']}
- Covenants: {', '.join(loan_terms['covenants'])}

Please provide:
1. Executive Summary (2-3 sentences)
2. Detailed Risk Analysis
3. Rationale for Each Term (Tenor, Interest Rate, Covenants)
4. Final Recommendation

Use professional banking terminology. Be concise but thorough.
"""
        
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo" for faster/cheaper
            messages=[
                {"role": "system", "content": "You are an expert commercial credit analyst with 20 years of experience in corporate lending."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"LLM Error: {e}")
        return generate_fallback_explanation(company_data, risk_analysis, loan_terms)


def generate_fallback_explanation(company_data, risk_analysis, loan_terms):
    """
    Fallback rule-based explanation when LLM not available
    """
    
    risk_level = risk_analysis["risk_level"]
    risk_score = risk_analysis["risk_score"]
    
    explanation = f"""
## Credit Decision Analysis

### Executive Summary

Based on our comprehensive analysis of **{company_data['company_name']}**, we have assessed the credit risk as **{risk_level}** with a risk score of **{risk_score}/100**. The proposed loan structure balances risk mitigation with competitive market terms appropriate for the {company_data['industry']} sector.

---

### Detailed Risk Analysis

**Company Profile:**
- {company_data['company_name']} operates in the {company_data['industry']} industry with annual revenue of ${company_data['revenue']}M
- The company is seeking ${company_data['loan_amount']}M for {company_data['purpose']}
- Loan-to-revenue ratio: {(company_data['loan_amount'] / company_data['revenue'] * 100):.1f}%

**Key Risk Factors:**

"""
    
    for factor in risk_analysis["risk_factors"]:
        explanation += f"- {factor}\n"
    
    explanation += f"""

---

### Term Structure Rationale

#### 1. Tenor: {loan_terms['tenor']}

"""
    
    if risk_score > 60:
        explanation += """
The shorter tenor is appropriate given the elevated risk profile. This structure:
- Reduces long-term exposure to credit risk
- Allows for more frequent covenant monitoring
- Enables earlier principal recovery
- Provides flexibility to reassess terms at maturity
"""
    elif risk_score > 35:
        explanation += """
A moderate tenor balances several considerations:
- Provides adequate time for business performance
- Maintains reasonable payment obligations
- Allows for comprehensive monitoring
- Aligns with industry standard for similar credits
"""
    else:
        explanation += """
The extended tenor reflects the strong credit profile:
- Demonstrates lender confidence in long-term viability
- Provides borrower with strategic flexibility
- Supports business planning and investment
- Competitive positioning in the market
"""
    
    explanation += f"""

#### 2. Interest Rate: {loan_terms['interest_margin']}

"""
    
    if risk_score > 60:
        explanation += """
The premium pricing reflects:
- Higher probability of default
- Industry volatility considerations
- Elevated leverage metrics
- Need for risk-adjusted returns
- Compensation for intensive monitoring requirements
"""
    elif risk_score > 35:
        explanation += """
Market-standard pricing for moderate-risk commercial credits:
- Competitive with peer transactions
- Appropriate for the risk-return profile
- Reflects current market conditions
- Balances borrower affordability with lender requirements
"""
    else:
        explanation += """
Favorable pricing reflecting strong credit fundamentals:
- Low probability of default
- Strong financial metrics
- Stable industry characteristics
- Conservative leverage position
- Established operating history
"""
    
    explanation += f"""

#### 3. Financial Covenants

The covenant package serves multiple purposes:

**Monitoring & Control:**
"""
    
    for covenant in loan_terms["covenants"]:
        explanation += f"- {covenant}\n"
    
    explanation += """

These covenants provide:
- Early warning indicators of financial deterioration
- Triggers for lender intervention if necessary
- Incentives for maintaining financial discipline
- Protection of lender's security position

---

### Collateral & Security

**First lien position on all company assets** provides:
- Priority claim in event of default
- Comprehensive asset coverage
- Enhanced recovery prospects
- Negotiating leverage for covenant modifications

---

### Final Recommendation

"""
    
    if risk_score > 60:
        explanation += f"""
**Proceed with Enhanced Monitoring**

While {company_data['company_name']} presents elevated risk, the proposed structure incorporates appropriate safeguards:
- Shorter tenor limits exposure
- Premium pricing compensates for risk
- Stringent covenants enable close monitoring
- Strong collateral position protects downside

**Conditions Precedent:**
- Completion of full due diligence
- Satisfactory legal documentation
- Environmental assessment (if applicable)
- Insurance requirements confirmation
- Personal guarantees (if required)

**Ongoing Monitoring:**
- Quarterly financial statement review
- Annual site visits
- Covenant compliance testing
- Industry trend analysis
"""
    elif risk_score > 35:
        explanation += f"""
**Proceed with Standard Terms**

{company_data['company_name']} represents an acceptable credit risk with moderate fundamentals. The proposed terms are appropriate for the risk profile:
- Balanced tenor and pricing
- Standard covenant package
- Adequate collateral coverage
- Routine monitoring requirements

**Conditions Precedent:**
- Standard due diligence completion
- Execution of loan documentation
- Insurance verification
- Legal opinions

**Ongoing Monitoring:**
- Semi-annual financial reviews
- Annual covenant testing
- Periodic management discussions
"""
    else:
        explanation += f"""
**Proceed - Recommended Credit**

{company_data['company_name']} represents a high-quality credit with strong fundamentals:
- Low default probability
- Stable cash flows
- Conservative financial management
- Favorable industry dynamics

The proposed terms reflect this strong profile while maintaining prudent credit standards.

**Conditions Precedent:**
- Customary due diligence
- Standard documentation
- Insurance confirmation

**Ongoing Monitoring:**
- Annual financial review
- Covenant compliance verification
- Relationship management meetings
"""
    
    explanation += """

---

*This analysis was generated by AURA's AI Credit Decision Engine, incorporating quantitative risk models and qualitative credit assessment methodologies consistent with industry best practices.*
"""
    
    return explanation


def generate_chat_response(user_message, context=None):
    """
    Generate chatbot responses for user queries
    """
    
    try:
        import openai
        
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            return "I'm currently operating in offline mode. Please configure your OpenAI API key to enable AI-powered responses."
        
        openai.api_key = api_key
        
        system_prompt = """
You are AURA (AI Unified Risk & Loan Origination Assistant), an expert AI assistant for commercial lending and credit analysis.

You help users with:
- Credit risk assessment questions
- Loan structuring guidance
- Financial covenant explanations
- Industry-specific lending insights
- Regulatory compliance questions

Provide clear, professional, and actionable advice. Use banking terminology appropriately.
"""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})
        
        messages.append({"role": "user", "content": user_message})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"