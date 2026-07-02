from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from retriever import search_assessments

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]



@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    user_message = " ".join(
        [msg.content.lower() for msg in request.messages if msg.role == "user"]
    )

    if (
        "compare" in user_message
        or "difference" in user_message
        or "vs" in user_message
    ):

        cleaned_message = (
            user_message.replace("compare", "")
            .replace("difference between", "")
        )

        if " and " in cleaned_message:
            parts = cleaned_message.split("and")
        elif " vs " in cleaned_message:
            parts = cleaned_message.split("vs")
        else:
            parts = []

        if len(parts) >= 2:
            first_query = parts[0].strip()
            second_query = parts[1].strip()

            first_results = search_assessments(first_query, top_k=1)
            second_results = search_assessments(second_query, top_k=1)

            if first_results and second_results:
                first_result = first_results[0]
                second_result = second_results[0]

                return {
                    "reply": (
                        f"Here’s a quick comparison: {first_result['name']} is primarily designed for "
                        f"{', '.join(first_result.get('keys', []))}, while {second_result['name']} "
                        f"is better suited for {', '.join(second_result.get('keys', []))}."
                    ),
                    "recommendations": [
                        {
                            "name": first_result["name"],
                            "url": first_result["link"]
                        },
                        {
                            "name": second_result["name"],
                            "url": second_result["link"]
                        }
                    ],
                    "end_of_conversation": True
                }

    blocked_keywords = [
        "salary", "weather", "hack", "capital",
        "ipl", "football", "cricket", "movie",
        "news", "politics", "stocks"
    ]

    if any(word in user_message for word in blocked_keywords):
        return {
            "reply": "I’m designed to help with SHL assessment recommendations, comparisons, and hiring-related evaluation guidance. Could you share your hiring requirement?",
            "recommendations": [],
            "end_of_conversation": False
        }

    allowed_keywords = [
        "developer", "engineer", "assessment", "test",
        "java", "python", "sql", "leadership",
        "personality", "reasoning", "manager", "analyst",
        "coding", "technical", "behavioral", "cognitive","screening",
        "evaluation", "benchmark", "executive", "talent"    ]

    if not any(keyword in user_message for keyword in allowed_keywords):
        return {
            "reply": "I’m designed to help with SHL assessment recommendations, comparisons, and hiring-related evaluation guidance. Could you share your hiring requirement?",
            "recommendations": [],
            "end_of_conversation": False
        }

    if any(role in user_message for role in ["developer", "engineer", "analyst", "manager"]) and not any(
        level in user_message for level in ["entry", "mid", "senior"]
    ):
        return {
            "reply": "Happy to help. Could you tell me the role and seniority level you’re hiring for (for example: Entry-level, Mid-level, or Senior)?",
            "recommendations": [],
            "end_of_conversation": False
        }

    vague_terms = [
    "leadership",
    "solution",
    "assessment",
    "test",
    "evaluation",
    "screening",
    "benchmark",
    "capability",
    "talent",
    "development",
    "executive",
    "potential"
]

    if any(term in user_message for term in vague_terms) and len(user_message.split()) <= 8:
        return {
            "reply": "Happy to help narrow this down. Who is the target group (for example, managers, directors, or executives), and is this for hiring or development purposes?",
            "recommendations": [],
            "end_of_conversation": False
        }

    results = search_assessments(user_message)

    if not results:
        return {
            "reply": "I couldn’t find a strong assessment match for that requirement yet. Could you share more details about the role, skills, or seniority?",
            "recommendations": [],
            "end_of_conversation": False
        }

    recommendations = []

    for r in results:
        matched_keys = [
            key for key in r.get("keys", [])
            if key.lower() in user_message
        ]

        reason = ", ".join(matched_keys) if matched_keys else ", ".join(r.get("keys", []))

        recommendations.append({
            "name": r["name"],
            "url": r["link"],
            "test_type": ", ".join(r.get("keys", [])),
            "why": f"Recommended because it matches your requirement for {reason}."
        })

    return {
        "reply": "Based on your hiring requirements, here are the most relevant SHL assessments:",
        "recommendations": recommendations,
        "end_of_conversation": True
    }