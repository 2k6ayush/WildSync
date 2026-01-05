import os
from typing import Tuple, Dict, Optional
import requests
from ..extensions import db
from ..models import ChatHistory, ForestData, Analysis

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except Exception:
    _OPENAI_AVAILABLE = False


def rule_based_reply(message: str, context: Dict) -> str:
    msg = message.lower()
    analysis = context.get("analysis") or {}
    tree_count = context.get("tree_count")
    soil = context.get("soil") or {}
    animals = context.get("animals") or {}

    if "analysis" in msg or "insight" in msg:
        if analysis:
            severity = analysis.get("severity", "Unknown")
            risk_score = analysis.get("risk_score")
            timeline = analysis.get("timeline")
            steps = analysis.get("steps") or []
            parts = []
            if risk_score is not None:
                parts.append(f"Current risk score: {risk_score:.2f} ({severity}).")
            else:
                parts.append(f"Current severity: {severity}.")
            if timeline:
                parts.append(f"Timeline: {timeline}.")
            if steps:
                parts.append("Top actions: " + "; ".join(steps[:3]) + ".")
            return " ".join(parts)
        return "No analysis found for this forest yet. Run an analysis to generate insights."

    if "recommend" in msg or "best practice" in msg or "conservation" in msg:
        steps = analysis.get("steps") or []
        if steps:
            return "Recommended actions: " + "; ".join(steps[:4]) + "."
        return "Please run an analysis first so I can tailor recommendations to your data."

    if "risk" in msg or "heat" in msg or "map" in msg:
        severity = analysis.get("severity")
        risk_score = analysis.get("risk_score")
        if risk_score is not None and severity:
            return f"Risk score is {risk_score:.2f} ({severity}). Heat map uses this score to color the region."
        if severity:
            return f"Risk severity is {severity}. Run analysis to compute a score and heat map."
        return "No risk analysis found yet. Upload data and start an analysis."

    if "species" in msg:
        return (
            "Native species suited to your soil profile and climate are recommended. "
            "Prioritize soil-stabilizing trees."
        )

    if "data" in msg or "forest" in msg:
        parts = []
        if tree_count is not None:
            parts.append(f"tree count: {tree_count}")
        if soil.get("health") is not None:
            parts.append(f"soil health: {soil.get('health')}")
        if soil.get("ph") is not None:
            parts.append(f"soil pH: {soil.get('ph')}")
        if animals.get("activity") is not None:
            parts.append(f"wildlife activity: {animals.get('activity')}")
        if parts:
            return "Current data includes " + ", ".join(parts) + "."
        return "I do not have forest data in context yet. Upload data and run analysis."

    return "Please provide more details about your question or the forest data you're analyzing."


def _ollama_generate(prompt: str, model: str, host: str) -> Optional[str]:
    base = host or "ollama:11434"
    if base.startswith("http"):
        url = f"{base.rstrip('/')}/api/generate"
    else:
        url = f"http://{base}/api/generate"
    resp = requests.post(url, json={"model": model, "prompt": prompt, "stream": False}, timeout=120)
    if resp.ok:
        j = resp.json()
        return j.get("response")
    return None


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
        analysis = (
            Analysis.query.filter_by(forest_id=forest_id)
            .order_by(Analysis.created_at.desc())
            .first()
        )
        if analysis:
            recs = analysis.recommendations or {}
            context["analysis"] = {
                "risk_score": (analysis.risk_zones or {}).get("overall"),
                "severity": recs.get("severity"),
                "timeline": recs.get("timeline"),
                "steps": recs.get("steps") or [],
            }

    reply = rule_based_reply(message, context)

    # Optional: use local Ollama model if enabled
    if os.getenv("OLLAMA_ENABLED", "0").lower() in ("1", "true", "yes", "y"):
        try:
            model = os.getenv("OLLAMA_MODEL", "mistral")
            host = os.getenv("OLLAMA_HOST", "ollama:11434")
            sys = "You are an AI assistant for forest management. Be concise and practical."
            prompt = f"{sys}\nContext: {context}\nQuestion: {message}\nAnswer:"
            out = _ollama_generate(prompt, model=model, host=host)
            if out:
                reply = out.strip()
        except Exception:
            # silently fall back
            pass

    # Optional: use OpenAI if key provided
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
