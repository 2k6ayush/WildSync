from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Forest, ForestData, Analysis
from ..services.analysis import analyze_forest_data, compute_completeness

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.post("/start")
@login_required
def start_analysis():
    data = request.get_json(force=True)
    forest_id = data.get("forest_id")
    forest = Forest.query.get(forest_id)
    if not forest or forest.user_id != current_user.user_id:
        return jsonify({"error": "Forest not found"}), 404

    fd = ForestData.query.filter_by(forest_id=forest_id).first()
    if not fd:
        return jsonify({"error": "No data uploaded for this forest"}), 400

    completeness = compute_completeness(fd)
    if completeness["percent"] < 70:
        return jsonify({
            "status": "insufficient",
            "completeness": completeness,
            "prompt": "Additional data needed for accurate analysis.",
            "missing": completeness["missing"],
        }), 422

    analysis = analyze_forest_data(fd)
    db.session.add(analysis)
    db.session.commit()

    return jsonify({
        "status": "ok",
        "analysis_id": analysis.analysis_id,
        "heat_map_data": analysis.heat_map_data,
        "recommendations": analysis.recommendations,
    })
