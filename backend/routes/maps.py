from flask import Blueprint, jsonify, request
from ..models import Analysis

maps_bp = Blueprint("maps", __name__)


@maps_bp.get("/layers")
def layers():
    analysis_id = request.args.get("analysis_id", type=int)
    analysis = Analysis.query.get(analysis_id)
    if not analysis:
        return {"error": "Analysis not found"}, 404
    return jsonify(analysis.heat_map_data or {})
