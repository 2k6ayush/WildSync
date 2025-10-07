import os
import pandas as pd
from PIL import Image, ExifTags
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ..services.location import detect_location

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "pdf", "png", "jpg", "jpeg"}

uploads_bp = Blueprint("uploads", __name__)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@uploads_bp.post("")
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    filename = secure_filename(file.filename)
    save_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, filename)
    file.save(path)

    # Extract minimal preview and attempt location detection
    preview = {}
    ext = filename.rsplit(".", 1)[1].lower()
    coords_from_exif = None

    if ext in {"csv", "xlsx", "xls"}:
        try:
            if ext == "csv":
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path)
            preview["columns"] = list(df.columns)[:20]
            preview["rows"] = df.head(10).to_dict(orient="records")
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

    location_guess = detect_location(file_path=path, exif_coords=coords_from_exif)

    return jsonify({
        "message": "File uploaded",
        "file": {"name": filename},
        "preview": preview,
        "location_guess": location_guess,
    }), 201
