# utils.py

import requests
from urllib.parse import urlparse, parse_qs
from dateutil import parser
from config import HEADERS

def request_json(url, params=None):
    """
    Safe wrapper for GET requests.
    Returns (json, response) or (None, response) on error.
    """
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    except Exception as e:
        print("Network error:", e)
        return None, None

    if resp.status_code == 200:
        try:
            return resp.json(), resp
        except ValueError:
            return None, resp

    # errors
    print(f"Error: {resp.status_code} for {url}")
    return None, resp


def extract_last_page(link):
    """
    Extract page number from GitHub Link header (rel='last').
    """
    if not link:
        return None

    parts = link.split(",")
    for p in parts:
        if 'rel="last"' in p:
            start = p.find("<") + 1
            end = p.find(">")
            url = p[start:end]
            qs = parse_qs(urlparse(url).query)
            return int(qs.get("page", [None])[0])

    return None


def format_iso(iso_str):
    if not iso_str:
        return "-"
    try:
        dt = parser.isoparse(iso_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except:
        return iso_str

