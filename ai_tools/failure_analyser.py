"""
AI-powered Failure Analyser.

Takes pytest failure output and uses AI to identify
root cause, explain the issue, and suggest a fix.

Usage:
    python ai_tools/failure_analyser.py failure_output.txt
    pytest tests/ -v 2>&1 > /tmp/output.txt
    python ai_tools/failure_analyser.py /tmp/output.txt
"""

import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = (
    "You are a senior QA automation engineer debugging "
    "Playwright + pytest tests against Odoo ERP. "
    "When given a test failure output, provide: "
    "1. ROOT CAUSE: What exactly went wrong (one sentence). "
    "2. EXPLANATION: Why this happened in plain English. "
    "3. SUGGESTED FIX: The exact code change needed. "
    "4. PREVENTION: How to avoid this in future tests. "
    "Be specific and practical."
)


def analyse_failure(failure_text):
    """Analyse a pytest failure output using AI."""
    client = OpenAI()

    prompt = (
        "Analyse this test failure and provide "
        "root cause, explanation, fix, and prevention:\n\n" + failure_text
    )

    response = client.responses.create(
        model="gpt-5.4-mini",
        instructions=SYSTEM_PROMPT,
        input=prompt,
    )

    return response.output_text


def main():
    """Entry point for CLI usage."""
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        print(f"Reading failure from: {filepath}")
        with open(filepath) as f:
            failure_text = f.read()
    else:
        print("Usage: python ai_tools/failure_analyser.py <failure_file>")
        print("Example: python ai_tools/failure_analyser.py /tmp/failure.txt")
        sys.exit(1)

    print("Analysing failure with AI...\n")
    analysis = analyse_failure(failure_text)

    print("=" * 60)
    print("AI FAILURE ANALYSIS")
    print("=" * 60)
    print(analysis)
    print("=" * 60)


if __name__ == "__main__":
    main()
