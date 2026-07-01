import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_explanation(bottlenecks: list) -> str:
    bottleneck_text = "\n".join([
        f"- {b['item']} (severity: {b['severity']}, sources: {b['sources']})"
        for b in bottlenecks
    ])

    prompt = f"""You are an expert mentor for open source contributors and GSoC aspirants.

Based on the following evidence-based bottleneck analysis, provide a clear, actionable explanation:

{bottleneck_text}

For each bottleneck:
1. Explain why it is a bottleneck
2. Give 2-3 specific actionable steps to fix it

Be direct, encouraging, and practical.Do not use casual emojies."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content