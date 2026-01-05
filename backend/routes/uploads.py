import os
import re
from typing import Dict, Any, Optional, Tuple, List
import pandas as pd
from PIL import Image, ExifTags
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ..extensions import db
from ..models import User, Forest, ForestData
from ..services.location import detect_location, parse_coordinates

try:
    import PyPDF2  # type: ignore
    _PDF_OK = True
except Exception:
    _PDF_OK = False

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "pdf", "png", "jpg", "jpeg"}

uploads_bp = Blueprint("uploads", __name__)

_COLUMN_ALIASES = {
    "location": "location",
    "area": "area",
    "coordinates": "coordinates",
    "coord": "coordinates",
    "treecount": "tree_count",
    "trees": "tree_count",
    "tree_count": "tree_count",
    "soilhealth": "soil_health",
    "soilhealthindex": "soil_health",
    "soilquality": "soil_health",
    "soilph": "soil_ph",
    "ph": "soil_ph",
    "soilmoisture": "soil_moisture",
    "moisture": "soil_moisture",
    "animalactivity": "animal_activity",
    "wildlifeactivity": "animal_activity",
    "activity": "animal_activity",
    "speciesrichness": "species_richness",
    "fires": "fires",
    "floods": "floods",
    "lat": "lat",
    "latitude": "lat",
    "lon": "lon",
    "lng": "lon",
    "longitude": "lon",
}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _normalize_col(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, float) and pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.strip().replace(",", "").replace("%", "")
    try:
        return float(value)
    except Exception:
        return None


def _to_int(value: Any) -> Optional[int]:
    val = _to_float(value)
    if val is None:
        return None
    return int(val)


def _derive_soil_health(
    soil_health: Optional[float],
    soil_ph: Optional[float],
    soil_moisture: Optional[float],
) -> Optional[float]:
    if soil_health is not None:
        return max(0.0, min(1.0, soil_health))
    components: List[float] = []
    if soil_ph is not None:
        components.append(max(0.0, 1.0 - abs(soil_ph - 6.5) / 6.5))
    if soil_moisture is not None:
        components.append(max(0.0, min(1.0, soil_moisture / 100.0)))
    if components:
        return max(0.0, min(1.0, sum(components) / len(components)))
    return None


def _extract_tabular_data(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {}
    row = df.iloc[0].to_dict()
    extracted: Dict[str, Any] = {}
    for col, val in row.items():
        key = _COLUMN_ALIASES.get(_normalize_col(col))
        if key:
            extracted[key] = val

    lat = _to_float(extracted.get("lat"))
    lon = _to_float(extracted.get("lon"))
    if extracted.get("coordinates"):
        extracted["coordinates"] = str(extracted.get("coordinates"))
    elif lat is not None and lon is not None:
        extracted["coordinates"] = f"{lat},{lon}"

    extracted["area"] = _to_float(extracted.get("area"))
    extracted["tree_count"] = _to_int(extracted.get("tree_count"))
    extracted["soil_health"] = _to_float(extracted.get("soil_health"))
    extracted["soil_ph"] = _to_float(extracted.get("soil_ph"))
    extracted["soil_moisture"] = _to_float(extracted.get("soil_moisture"))
    extracted["animal_activity"] = _to_float(extracted.get("animal_activity"))
    extracted["species_richness"] = _to_int(extracted.get("species_richness"))
    extracted["fires"] = _to_int(extracted.get("fires"))
    extracted["floods"] = _to_int(extracted.get("floods"))
    return extracted


def _parse_pdf_text(text: str) -> Dict[str, Any]:
    extracted: Dict[str, Any] = {}
    if not text:
        return extracted

    area_match = re.search(r"area of (?:approximately )?([0-9,.]+)\s*km", text, re.IGNORECASE)
    if area_match:
        extracted["area"] = _to_float(area_match.group(1))

    for pattern in (r"Tree Count\s*[:\-]\s*([0-9,]+)", r"Trees\s*[:\-]\s*([0-9,]+)"):
        tree_match = re.search(pattern, text, re.IGNORECASE)
        if tree_match:
            extracted["tree_count"] = _to_int(tree_match.group(1))
            break

    ph_match = re.search(r"Soil pH:\s*([0-9.]+)", text, re.IGNORECASE)
    if ph_match:
        extracted["soil_ph"] = _to_float(ph_match.group(1))

    soil_health_match = re.search(r"Soil (Health|Quality)\s*[:\-]\s*([0-9.]+)", text, re.IGNORECASE)
    if soil_health_match:
        extracted["soil_health"] = _to_float(soil_health_match.group(2))

    moisture_match = re.search(r"Soil Moisture:\s*([0-9.]+)%", text, re.IGNORECASE)
    if moisture_match:
        extracted["soil_moisture"] = _to_float(moisture_match.group(1))

    location_match = re.search(r"Location:\s*(.+)", text, re.IGNORECASE)
    if location_match:
        location_line = location_match.group(1).strip()
        extracted["location"] = location_line
        coord_match = re.search(
            r"(\d+(?:\.\d+)?)\s*([NS])\s*,\s*(\d+(?:\.\d+)?)\s*([EW])",
            location_line,
            re.IGNORECASE,
        )
        if coord_match:
            lat = float(coord_match.group(1))
            lon = float(coord_match.group(3))
            if coord_match.group(2).upper() == "S":
                lat = -lat
            if coord_match.group(4).upper() == "W":
                lon = -lon
            extracted["coordinates"] = f"{lat},{lon}"
        if not extracted.get("coordinates"):
            coord_any = parse_coordinates(location_line)
            if coord_any:
                extracted["coordinates"] = f"{coord_any['lat']},{coord_any['lon']}"
        if "(" in location_line and location_line.endswith(")"):
            extracted["location"] = location_line.split("(")[-1].strip(")")

    lat_match = re.search(r"Lat(?:itude)?\s*[:\-]\s*([0-9.\-]+)", text, re.IGNORECASE)
    lon_match = re.search(r"(Lon(?:gitude)?|Lng)\s*[:\-]\s*([0-9.\-]+)", text, re.IGNORECASE)
    if lat_match and lon_match and not extracted.get("coordinates"):
        extracted["coordinates"] = f"{_to_float(lat_match.group(1))},{_to_float(lon_match.group(2))}"

    if not extracted.get("coordinates"):
        dms = _parse_dms_coordinates(text)
        if dms:
            extracted["coordinates"] = f"{dms['lat']},{dms['lon']}"

    animal_match = re.search(r"Animal (Activity|Index)\s*[:\-]\s*([0-9.]+)", text, re.IGNORECASE)
    if animal_match:
        extracted["animal_activity"] = _to_float(animal_match.group(2))

    sightings = re.findall(r":\s*([0-9]+)\s*sighting", text, re.IGNORECASE)
    if sightings:
        total = sum(int(s) for s in sightings)
        extracted["animal_activity"] = min(1.0, total / 20.0)
        extracted["species_richness"] = len(sightings)

    if not extracted.get("coordinates"):
        coord_any = parse_coordinates(text)
        if coord_any:
            extracted["coordinates"] = f"{coord_any['lat']},{coord_any['lon']}"

    return extracted


def _parse_dms_coordinates(text: str) -> Optional[Dict[str, float]]:
    def to_decimal(deg: str, minutes: str, direction: str) -> float:
        value = float(deg) + float(minutes) / 60.0
        if direction.upper() in ("S", "W"):
            value = -value
        return value

    deg_sym = r"(?:\u00b0|deg)"
    min_sym = r"(?:\u2032|\'|\u2019)?"

    lat_range = re.search(
        rf"latitudes?\s+(\d{{1,2}})\s*{deg_sym}\s*(\d{{1,2}})\s*{min_sym}\s*to\s*(\d{{1,2}})\s*{deg_sym}\s*(\d{{1,2}})\s*{min_sym}\s*([NS])",
        text,
        re.IGNORECASE,
    )
    lon_range = re.search(
        rf"longitudes?\s+(\d{{1,3}})\s*{deg_sym}\s*(\d{{1,2}})\s*{min_sym}\s*to\s*(\d{{1,3}})\s*{deg_sym}\s*(\d{{1,2}})\s*{min_sym}\s*([EW])",
        text,
        re.IGNORECASE,
    )
    if lat_range and lon_range:
        lat1 = to_decimal(lat_range.group(1), lat_range.group(2), lat_range.group(5))
        lat2 = to_decimal(lat_range.group(3), lat_range.group(4), lat_range.group(5))
        lon1 = to_decimal(lon_range.group(1), lon_range.group(2), lon_range.group(5))
        lon2 = to_decimal(lon_range.group(3), lon_range.group(4), lon_range.group(5))
        lat = (lat1 + lat2) / 2.0
        lon = (lon1 + lon2) / 2.0
        if abs(lat) <= 90 and abs(lon) <= 180:
            return {"lat": lat, "lon": lon}

    lat_single = re.search(
        rf"latitude\s+(\d{{1,2}})\s*{deg_sym}\s*(\d{{1,2}})\s*{min_sym}\s*([NS])",
        text,
        re.IGNORECASE,
    )
    lon_single = re.search(
        rf"longitude\s+(\d{{1,3}})\s*{deg_sym}\s*(\d{{1,2}})\s*{min_sym}\s*([EW])",
        text,
        re.IGNORECASE,
    )
    if lat_single and lon_single:
        lat = to_decimal(lat_single.group(1), lat_single.group(2), lat_single.group(3))
        lon = to_decimal(lon_single.group(1), lon_single.group(2), lon_single.group(3))
        if abs(lat) <= 90 and abs(lon) <= 180:
            return {"lat": lat, "lon": lon}

    return None


def _parse_pdf(path: str) -> Dict[str, Any]:
    if not _PDF_OK:
        return {}
    text_chunks = []
    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for i in range(min(2, len(reader.pages))):
                try:
                    txt = reader.pages[i].extract_text() or ""
                except Exception:
                    txt = ""
                if txt:
                    text_chunks.append(txt)
    except Exception:
        return {}
    return _parse_pdf_text("\n".join(text_chunks))


def _build_payload(parsed: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any], List[str]]:
    forest_fields: Dict[str, Any] = {}
    data_fields: Dict[str, Any] = {}
    warnings: List[str] = []

    if parsed.get("location"):
        forest_fields["location"] = parsed["location"]
    if parsed.get("area") is not None:
        forest_fields["area"] = parsed["area"]
    if parsed.get("coordinates"):
        forest_fields["coordinates"] = parsed["coordinates"]

    tree_count = parsed.get("tree_count")
    if tree_count is None:
        warnings.append("Tree count missing; defaulting to 500.")
        tree_count = 500
    data_fields["tree_count"] = tree_count

    soil_health = _derive_soil_health(
        parsed.get("soil_health"),
        parsed.get("soil_ph"),
        parsed.get("soil_moisture"),
    )
    soil_data: Dict[str, Any] = {}
    if soil_health is None:
        warnings.append("Soil health missing; defaulting to 0.5.")
        soil_health = 0.5
    soil_data["health"] = soil_health
    if parsed.get("soil_ph") is not None:
        soil_data["ph"] = parsed["soil_ph"]
    if parsed.get("soil_moisture") is not None:
        soil_data["moisture"] = parsed["soil_moisture"]
    data_fields["soil_data"] = soil_data

    animal_data: Dict[str, Any] = {}
    animal_activity = parsed.get("animal_activity")
    if animal_activity is None:
        warnings.append("Animal activity missing; defaulting to 0.5.")
        animal_activity = 0.5
    animal_data["activity"] = animal_activity
    if parsed.get("species_richness") is not None:
        animal_data["species_richness"] = parsed["species_richness"]
    data_fields["animal_data"] = animal_data

    calamity: Dict[str, Any] = {}
    if parsed.get("fires") is not None:
        calamity["fires"] = parsed["fires"]
    if parsed.get("floods") is not None:
        calamity["floods"] = parsed["floods"]
    if calamity:
        data_fields["calamity_history"] = calamity

    return forest_fields, data_fields, warnings


def _get_or_create_guest_user() -> User:
    email = os.getenv("GUEST_USER_EMAIL", "guest@wildsync.local")
    user = User.query.filter_by(email=email).first()
    if not user:
        name = os.getenv("GUEST_USER_NAME", "Guest")
        user = User(name=name, email=email)
        user.set_password(os.getenv("GUEST_USER_PASSWORD", "ChangeMe123!"))
        db.session.add(user)
        db.session.flush()
    return user


@uploads_bp.post("")
def upload():
    if "file" not in request.files:
        print("DEBUG: No file part in request.files")
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        print("DEBUG: No selected file (empty filename)")
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(file.filename):
        print(f"DEBUG: Unsupported file type: {file.filename}")
        return jsonify({"error": f"Unsupported file type. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"}), 400

    filename = secure_filename(file.filename)
    save_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, filename)
    file.save(path)

    # Extract minimal preview and attempt location detection
    preview = {}
    ext = filename.rsplit(".", 1)[1].lower()
    coords_from_exif = None
    parsed: Dict[str, Any] = {}

    if ext in {"csv", "xlsx", "xls"}:
        try:
            if ext == "csv":
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path)
            preview["columns"] = list(df.columns)[:20]
            preview["rows"] = df.head(10).to_dict(orient="records")
            parsed = _extract_tabular_data(df)
        except Exception as e:
            return jsonify({"error": f"Failed to parse file: {e}"}), 400
    elif ext in {"jpg", "jpeg", "png"}:
        try:
            img = Image.open(path)
            exif = getattr(img, "_getexif", lambda: None)()
            if exif:
                exif_data = {ExifTags.TAGS.get(k, k): v for k, v in exif.items() if k in ExifTags.TAGS}
                gps_info = exif_data.get("GPSInfo")
                if gps_info:
                    coords_from_exif = str(gps_info)
            preview["format"] = img.format
            preview["size"] = img.size
        except Exception as e:
            return jsonify({"error": f"Failed to process image: {e}"}), 400
    elif ext == "pdf":
        if not _PDF_OK:
            return jsonify({"error": "PDF support not installed on server"}), 400
        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                text_chunks = []
                # Extract text from first 2 pages (limited preview)
                for i in range(min(2, num_pages)):
                    try:
                        txt = reader.pages[i].extract_text() or ""
                    except Exception:
                        txt = ""
                    if txt:
                        text_chunks.append(txt)
                preview["pages"] = num_pages
                preview["text_preview"] = ("\n".join(text_chunks))[:1000]
        except Exception:
            # Gracefully handle scanned/unsupported PDFs: save file without text preview
            preview["pages"] = None
            preview["text_preview"] = ""
        parsed = _parse_pdf(path)

    location_guess = detect_location(file_path=path, exif_coords=coords_from_exif)

    warnings: List[str] = []
    forest_id = request.form.get("forest_id", type=int)
    forest_fields, data_fields, defaults_used = _build_payload(parsed)
    warnings.extend(defaults_used)

    forest = None
    if forest_id:
        forest = Forest.query.get(forest_id)
    if not forest:
        guest = _get_or_create_guest_user()
        forest = Forest(
            user_id=guest.user_id,
            location=forest_fields.get("location"),
            area=forest_fields.get("area"),
            coordinates=forest_fields.get("coordinates"),
        )
        db.session.add(forest)
        db.session.flush()
    else:
        for key, val in forest_fields.items():
            setattr(forest, key, val)

    fd = ForestData.query.filter_by(forest_id=forest.forest_id).first()
    if not fd:
        fd = ForestData(forest_id=forest.forest_id)
    if "tree_count" in data_fields:
        fd.tree_count = data_fields["tree_count"]
    if "soil_data" in data_fields:
        fd.soil_data = data_fields["soil_data"]
    if "animal_data" in data_fields:
        fd.animal_data = data_fields["animal_data"]
    if "calamity_history" in data_fields:
        fd.calamity_history = data_fields["calamity_history"]
    db.session.add(fd)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to persist uploaded data", "details": str(e)}), 500

    return jsonify(
        {
            "message": "File uploaded",
            "file": {"name": filename},
            "preview": preview,
            "location_guess": location_guess,
            "forest_id": forest.forest_id,
            "forest": {
                "location": forest.location,
                "area": forest.area,
                "coordinates": forest.coordinates,
            },
            "warnings": warnings,
        }
    ), 201
