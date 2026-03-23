# Financial Advisor Bot
# Rule-based chatbot for basic financial guidance
# Features:
# - Saving advice
# - Budgeting advice
# - Income breakdown

import re
import random
import csv
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="Financial Advisor Bot", page_icon="💬", layout="centered")


# Extract numerical value from user input using regex
def extract_amount(text: str):
    match = re.search(r'(-?\d+(?:,\d{3})*(?:\.\d+)?)', text)
    if match:
        amount_str = match.group(1).replace(",", "")
        try:
            return float(amount_str)
        except:
            return None
    return None

# Log chatbot interactions for simple evaluation evidence
def log_interaction(user_input: str, bot_reply: str):
    with open("chat_log.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), user_input, bot_reply])


# Detect user intent using keyword matching
def detect_intent(user_input: str):
    text = user_input.lower()

    if any(x in text for x in ["save", "saving", "savings"]):
        return "saving_advice"

    if any(x in text for x in ["budget", "budgeting", "spend", "spending", "expense", "expenses"]):
        return "budget_advice"

    if any(x in text for x in ["break", "breakdown", "split", "divide", "allocation", "allocate"]):
        return "income_breakdown"

    return "unknown"


# Validate extracted income values
def validate_income(income):
    if income is None:
        return "missing"
    if income <= 0:
        return "non_positive"
    if income > 100000:
        return "too_large"
    return "valid"


# Generate saving recommendation using 20% rule
def saving_response(user_input: str):
    try:
        income = extract_amount(user_input)
    except Exception:
        return "There was an error processing your input."

    status = validate_income(income)

    if status == "missing":
        return (
            "I can help with saving advice. Please include your monthly income, for example: "
            "'How much should I save if I earn 2000 per month?'"
        )
    if status == "non_positive":
        return "Income must be a positive number."
    if status == "too_large":
        return "Please enter a realistic monthly income."

    recommended_saving = income * 0.20
    opening = random.choice([
        "A simple saving guideline is 20% of income.",
        "One common rule is to save around 20% of what you earn.",
        "A basic approach is to put aside about 20% each month."
    ])

    return (
        f"{opening}\n\n"
        f"For an income of ${income:,.2f}:\n"
        f"- Suggested savings: ${recommended_saving:,.2f} per month\n\n"
        "This can help build savings over time."
    )


# Generate budgeting advice using 50/30/20 rule
def budget_response(user_input: str):
    try:
        income = extract_amount(user_input)
    except Exception:
        return "There was an error processing your input."

    status = validate_income(income)

    if status == "missing":
        return (
            "A simple budgeting rule is the 50/30/20 method:\n\n"
            "- 50% for needs\n"
            "- 30% for wants\n"
            "- 20% for savings\n\n"
            "If you include your monthly income, I can estimate the amounts."
        )
    if status == "non_positive":
        return "Income must be a positive number."
    if status == "too_large":
        return "Please enter a realistic monthly income."

    needs = income * 0.50
    wants = income * 0.30
    savings = income * 0.20

    opener = random.choice([
        "A simple budgeting rule is the 50/30/20 method.",
        "One common budgeting approach is the 50/30/20 method.",
        "A basic way to budget is the 50/30/20 split."
    ])

    return (
        f"{opener}\n\n"
        f"For a monthly income of ${income:,.2f}:\n"
        f"- Needs: ${needs:,.2f}\n"
        f"- Wants: ${wants:,.2f}\n"
        f"- Savings: ${savings:,.2f}\n\n"
        "This is a basic guideline and can be adjusted."
    )


# Generate simple income breakdown into categories
def breakdown_response(user_input: str):
    try:
        income = extract_amount(user_input)
    except Exception:
        return "There was an error processing your input."

    status = validate_income(income)

    if status == "missing":
        return (
            "I can help break down an income into categories. "
            "Please include your monthly income, for example: "
            "'Can you break down 2500 for me?'"
        )

    if status == "non_positive":
        return "Income must be a positive number."

    if status == "too_large":
        return "Please enter a realistic monthly income."

    # STOP execution if invalid
    if status != "valid":
        return "Invalid input."

    # Only runs if VALID
    rent = income * 0.30
    food = income * 0.15
    transport = income * 0.10
    savings = income * 0.20
    other = income - (rent + food + transport + savings)

    return (
        f"Here is one simple example breakdown for ${income:,.2f} per month:\n\n"
        f"- Housing/Rent: ${rent:,.2f}\n"
        f"- Food: ${food:,.2f}\n"
        f"- Transport: ${transport:,.2f}\n"
        f"- Savings: ${savings:,.2f}\n"
        f"- Other expenses: ${other:,.2f}\n\n"
        "This is only an example and should be adjusted to your own situation."
    )


# Route user input to correct response based on detected intent
def chatbot_reply(user_input: str):
    intent = detect_intent(user_input)

    if intent == "saving_advice":
        return saving_response(user_input)
    elif intent == "budget_advice":
        return budget_response(user_input)
    elif intent == "income_breakdown":
        return breakdown_response(user_input)
    else:
        return (
            "I can currently help with three things:\n\n"
            "1. Saving advice\n"
            "2. Budgeting advice\n"
            "3. Simple income breakdown\n\n"
            "Try asking something like:\n"
            "- How much should I save if I earn 2000 per month?\n"
            "- Can you give me budgeting advice?\n"
            "- Can you break down 2500 for me?\n"
            "- I earn 3000, how should I budget?"
        )


st.title("💬 Financial Advisor Bot")
st.caption("Basic budgeting and saving guidance using a simple rule-based chatbot")

st.markdown(
    """
This prototype provides:
- saving advice
- budgeting advice
- simple income breakdowns

**Important:** This is an educational prototype only.  
It does **not** provide professional financial advice.
"""
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello. I am a Financial Advisor Bot prototype. "
                "Ask me about saving, budgeting, or a simple income breakdown."
            ),
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    reply = chatbot_reply(user_input)
    log_interaction(user_input, reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

st.divider()
st.subheader("Suggested test prompts")
st.markdown(
    """
- How much should I save if I earn 2000 per month?
- Can you give me budgeting advice?
- Can you break down 2500 for me?
- I earn 3000, how should I budget?
- save
- budget 0
- break down -500
"""
)