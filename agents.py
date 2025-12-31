import google.generativeai as genai
import json
import os
import streamlit as st

# Configure Gemini using environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Correct, supported model from YOUR account
model = genai.GenerativeModel("models/gemini-flash-lite-latest")


from google.api_core.exceptions import ResourceExhausted


def call_llm(system_prompt, user_prompt):
    try:
        response = model.generate_content(
            f"{system_prompt}\n\n{user_prompt}",
            generation_config={"max_output_tokens": 512}
        )
        return response.text
    except Exception as e:
        st.error("LLM call failed. Showing fallback output.")
        return "Analysis unavailable due to API limitations."



# ---------- FUNDAMENTAL AGENT ----------
def fundamental_analyst_agent(ratios):
    prompt = f"""
You are a fundamental equity analyst.

Given these financial ratios:
{json.dumps(ratios, indent=2)}

Provide a qualitative assessment of:
- Profitability
- Liquidity
- Leverage
- Capital efficiency
"""
    return call_llm("Professional equity analyst", prompt)


# ---------- MANAGEMENT QUALITY ----------
def management_quality_agent():
    prompt = """
Analyze management quality and business fundamentals.

Cover:
- Management tone
- Strategic clarity
- Risk disclosure quality
- Capital allocation discipline
- Governance credibility
"""
    return call_llm("Expert management analyst", prompt)


# ---------- TECHNICAL AGENT ----------
def technical_analyst_agent(tech):
    prompt = f"""
You are a technical market analyst.

Indicators:
{json.dumps(tech, indent=2)}

Interpret:
- Trend direction
- Momentum
- Volatility
"""
    return call_llm("Professional technical analyst", prompt)


# ---------- CONTRARIAN AGENT ----------
def contrarian_agent():
    prompt = """
Act as a contrarian investor.

List strong reasons NOT to buy this stock.
Focus on risks, valuation, and uncertainty.
"""
    return call_llm("Contrarian analyst", prompt)


# ---------- CHAIRMAN ----------
def chairman_agent(fundamental, management, technical, contrarian):
    prompt = f"""
You are the chairman of an investment committee.

Inputs:

FUNDAMENTAL ANALYSIS:
{fundamental}

MANAGEMENT QUALITY:
{management}

TECHNICAL ANALYSIS:
{technical}

CONTRARIAN VIEW:
{contrarian}

Synthesize everything and provide:
- Final recommendation (BUY / HOLD / AVOID)
- Confidence level (Low / Medium / High)
- Clear reasoning
"""
    return call_llm("Investment committee chairman", prompt)
