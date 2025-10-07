import re
import requests
from typing import Optional, Dict

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "WildSync/1.0 (contact: admin@wildsync.ai)"}


def parse_coordinates(text: Optional[str]) -> Optional[Dict[str, float]]:
    if not text:
        return None
    match = re.search(r"(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)", str(text))
    if match:
        return {"lat": float(match.group(1)), "lon": float(match.group(2))}
    return None


def geocode_place(place: str) -> Optional[Dict[str, float]]:
    try:
        resp = requests.get(NOMINATIM_URL, params={"q": place, "format": "json", "limit": 1}, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data:
            return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"]) }
    except Exception:
        return None
    return None


def detect_location(file_path: Optional[str] = None, exif_coords: Optional[str] = None, place_name: Optional[str] = None):
    coords = parse_coordinates(exif_coords)
    if coords:
        return {"method": "exif", "coordinates": coords}
    if place_name:
        gc = geocode_place(place_name)
        if gc:
            return {"method": "geocoding", "coordinates": gc}
    return {"method": "manual_required", "message": "Unable to detect location. Please provide exact area and coordinates."}

import os
import re
import requests
from typing import Optional, Dict

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "WildSync/1.0 (contact: admin@wildsync.ai)"}


def parse_coordinates(text: Optional[str]) -> Optional[Dict[str, float]]:
    if not text:
        return None
    # rudimentary lat, lon parser
    match = re.search(r"(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)", str(text))
    if match:
        return {"lat": float(match.group(1)), "lon": float(match.group(2))}
    return None


def geocode_place(place: str) -> Optional[Dict[str, float]]:
    try:
        resp = requests.get(NOMINATIM_URL, params={"q": place, "format": "json", "limit": 1}, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data:
            return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"]) }
    except Exception:
        return None
    return None


def detect_location(file_path: Optional[str] = None, exif_coords: Optional[str] = None, place_name: Optional[str] = None):
    # Try coords from EXIF
    coords = parse_coordinates(exif_coords)
    if coords:
        return {"method": "exif", "coordinates": coords}
    # Try place name
    if place_name:
        gc = geocode_place(place_name)
        if gc:
            return {"method": "geocoding", "coordinates": gc}
    # No detection
    return {"method": "manual_required", "message": "Unable to detect location. Please provide exact area and coordinates."}