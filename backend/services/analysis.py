from typing import Dict, Any
import numpy as np
from ..models import Analysis, ForestData


def compute_completeness(fd: ForestData) -> Dict[str, Any]:
    missing = []
    if fd.tree_count is None:
        missing.append("tree_count")
    if not fd.soil_data:
        missing.append("soil_data")
    if not fd.animal_data:
        missing.append("animal_data")
    present = 3 - len(missing)
    percent = int((present / 3) * 100)
    return {"percent": percent, "missing": missing}


def risk_score(tree_count: int, soil_health: float, animal_index: float) -> float:
    base = 0
    base += (1000 - min(tree_count or 0, 1000)) / 1000 * 0.4
    base += (1.0 - min(max(soil_health or 0, 0.0), 1.0)) * 0.4
    base += abs((animal_index or 0) - 0.5) * 0.2
    return float(np.clip(base, 0.0, 1.0))


def severity_label(score: float) -> str:
    if score >= 0.75:
        return "Critical"
    if score >= 0.6:
        return "High"
    if score >= 0.4:
        return "Moderate"
    return "Low"


def generate_recommendations(score: float) -> Dict[str, Any]:
    if score >= 0.75:
        timeline = "Critical: Action within 3 months"
        steps = [
            "Immediate erosion control with geo-textiles",
            "Deploy patrols to protect habitats",
            "Replant 500+ native trees",
        ]
        resources = {"budget": 50000, "manpower": 20, "materials": ["saplings", "tools", "geotextile"]}
    elif score >= 0.6:
        timeline = "High: Action within 3-6 months"
        steps = [
            "Targeted reforestation (200-300 trees)",
            "Soil enrichment program",
            "Habitat monitoring",
        ]
        resources = {"budget": 20000, "manpower": 10, "materials": ["saplings", "fertilizer"]}
    elif score >= 0.4:
        timeline = "Moderate: Action within 6 months"
        steps = [
            "Selective planting (100-200 trees)",
            "Soil assessment and maintenance",
        ]
        resources = {"budget": 10000, "manpower": 6, "materials": ["saplings"]}
    else:
        timeline = "Low: Routine monitoring"
        steps = ["Maintain current conservation efforts"]
        resources = {"budget": 2000, "manpower": 2, "materials": []}

    return {
        "severity": severity_label(score),
        "timeline": timeline,
        "steps": steps,
        "resources": resources,
        "expected_outcomes": ["Improved canopy cover", "Stabilized soil", "Balanced wildlife activity"],
        "metrics": ["tree_survival_rate", "soil_health_index", "wildlife_activity_index"],
    }


def analyze_forest_data(fd: ForestData) -> Analysis:
    tree_count = fd.tree_count or 0
    soil_health = (fd.soil_data or {}).get("health", 0.5)
    animal_index = (fd.animal_data or {}).get("activity", 0.5)

    score = risk_score(tree_count, soil_health, animal_index)

    layer = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "risk": score,
                    "severity": severity_label(score),
                    "details": {
                        "tree_count": tree_count,
                        "soil_health": soil_health,
                        "animal_activity": animal_index,
                    },
                },
                "geometry": {"type": "Point", "coordinates": [0, 0]},
            }
        ],
    }

    recs = generate_recommendations(score)

    analysis = Analysis(
        forest_id=fd.forest_id,
        risk_zones={"overall": score},
        recommendations=recs,
        heat_map_data={
            "layers": {"risk": layer},
            "legend": {
                "0.0-0.3": "Green (healthy)",
                "0.3-0.6": "Yellow (moderate)",
                "0.6-1.0": "Red (high-risk)",
            },
        },
    )
    return analysis
