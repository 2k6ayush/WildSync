import os
import pandas as pd
from PIL import Image, ExifTags
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ..services.location import detect_location

try:
    import PyPDF2  # type: ignore
    _PDF_OK = True
except Exception:
    _PDF_OK = False

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "pdf", "png", "jpg", "jpeg"}

uploads_bp = Blueprint("uploads", __name__)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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

    location_guess = detect_location(file_path=path, exif_coords=coords_from_exif)

    return jsonify({
        "message": "File uploaded",
        "file": {"name": filename},
        "preview": preview,
        "location_guess": location_guess,
    }), 201
