# utils.py
from datetime import datetime
from typing import Optional, Dict


def parse_date(date_str: Optional[str]) -> Optional[datetime.date]:
    """
    Parse a string date (YYYY-MM-DD) into a date object.
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None


def format_date(date_obj: Optional[datetime.date]) -> Optional[str]:
    """
    Format a date object into a string (YYYY-MM-DD).
    """
    if not date_obj:
        return None
    return date_obj.strftime("%Y-%m-%d")


def parse_coordinates(coord_str: Optional[str]) -> Optional[Dict[str, float]]:
    """
    Convert a string "lat,lng" into a dict {"latitude": float, "longitude": float}.
    """
    if not coord_str or "," not in coord_str:
        return None
    try:
        lat_str, lng_str = coord_str.split(",")
        return {"latitude": float(lat_str.strip()), "longitude": float(lng_str.strip())}
    except Exception:
        return None


def format_coordinates(coords: Optional[Dict[str, float]]) -> str:
    """
    Convert a dict {"latitude": x, "longitude": y} into a string "x,y".
    """
    if not coords or "latitude" not in coords or "longitude" not in coords:
        return ""
    return f"{coords['latitude']},{coords['longitude']}"

def parse_time(time_str: Optional[str]) -> Optional[datetime.time]:
    """
    Parse a string time ("HH:MM" or "HH:MM:SS") into a time object.
    """
    if not time_str:
        return None
    try:
        return datetime.strptime(time_str, "%H:%M:%S").time()
    except ValueError:
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except Exception:
            return None


def format_time(time_obj: Optional[datetime.time]) -> Optional[str]:
    """
    Format a time object into a string (HH:MM:SS).
    """
    if not time_obj:
        return None
    return time_obj.strftime("%H:%M:%S")

