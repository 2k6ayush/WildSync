from flask import Blueprint, jsonify
from flask_login import login_required, current_user

profile_bp = Blueprint("profile", __name__)


@profile_bp.get("")
@login_required
def profile():
    u = current_user
    return jsonify({
        "user": {
            "name": u.name,
            "email": u.email,
            "department": u.department,
            "role": u.role,
        }
    })
