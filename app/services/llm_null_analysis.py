import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(temperature=0, model_name="gpt-4")

def check_null_hypothesis(claim: str, top_articles: list) -> str:
    context = "\n\n".join(
        f"Title: {a['title']}\nAbstract: {a['abstract']}" for a in top_articles
    )

    prompt = (
        f"You are an expert biomedical researcher.\n"
        f"Given the scientific claim: \"{claim}\"\n"
        f"and the following article abstracts, determine whether the research:\n"
        f"- Supports the claim (verdict = supported)\n"
        f"- Contradicts or fails to support it (verdict = null_result)\n"
        f"- Or is inconclusive (verdict = unclear)\n\n"
        f"Return the answer in the following JSON format:\n\n"
        f"""{{
    "verdict": "supported | null_result | unclear",
    "summary": "<summary of findings>",
    "reasoning": "<Detailed explanation of how each article contributed to the overall verdict. Refer to each article by its index and explain why it supports, contradicts, or is inconclusive.>"
    }}\n\n"""
        f"Abstracts:\n{context}"
    )

    response = llm([HumanMessage(content=prompt)]).content

    # Try parsing JSON using regex
    try:
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            import json
            return json.loads(match.group())
        else:
            return {
                "verdict": "unclear",
                "summary": "Unable to parse structured result",
                "reasoning": response
            }
    except Exception:
        return {
            "verdict": "unclear",
            "summary": "Parsing failed",
            "reasoning": response
        }