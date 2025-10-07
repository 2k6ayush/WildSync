from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..services.chatbot import chat_with_context

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.post("")
@login_required
def chat():
    data = request.get_json(force=True)
    message = data.get("message", "")
    forest_id = data.get("forest_id")
    if not message:
        return jsonify({"error": "Message required"}), 400
    reply, meta = chat_with_context(user_id=current_user.user_id, message=message, forest_id=forest_id)
    return jsonify({"response": reply, "meta": meta})
