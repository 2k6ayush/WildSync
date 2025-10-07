import os
from typing import Tuple, Dict, Optional
from ..extensions import db
from ..models import ChatHistory, ForestData

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except Exception:
    _OPENAI_AVAILABLE = False


def rule_based_reply(message: str, context: Dict) -> str:
    if "risk" in message.lower():
        tc = context.get("tree_count", "unknown")
        return (
            f"Based on available data (tree count: {tc}), risk factors include canopy loss and soil health. "
            "Consider targeted reforestation and soil enrichment."
        )
    if "species" in message.lower():
        return (
            "Native species suited to your soil profile and climate are recommended. "
            "Prioritize soil-stabilizing trees."
        )
    return "Please provide more details about your question or the forest data you're analyzing."


def chat_with_context(user_id: int, message: str, forest_id: Optional[int] = None) -> Tuple[str, Dict]:
    context: Dict = {}
    if forest_id:
        fd = ForestData.query.filter_by(forest_id=forest_id).first()
        if fd:
            context = {
                "tree_count": fd.tree_count,
                "soil": fd.soil_data,
                "animals": fd.animal_data,
            }

    reply = rule_based_reply(message, context)

    if _OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI assistant for forest management."},
                    {"role": "user", "content": f"Context: {context}\nQuestion: {message}"},
                ],
                temperature=0.2,
            )
            reply = completion.choices[0].message.content
        except Exception:
            pass

    ch = ChatHistory(user_id=user_id, message=message, response=reply)
    db.session.add(ch)
    db.session.commit()

    return reply, {"forest_id": forest_id}
