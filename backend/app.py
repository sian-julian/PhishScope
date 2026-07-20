"""Flask REST API for PhishScope phishing URL analysis."""

from __future__ import annotations

from typing import Any

from flask import Flask, Response, jsonify, request
from flask_cors import CORS

try:
    from backend.analyzer.feature_extractor import extract_features
    from backend.analyzer.scoring_engine import score_url
    from backend.config import logger
    from hybrid.engine import analyze_url
except ImportError:  # pragma: no cover - supports `python app.py` from backend/
    from analyzer.feature_extractor import extract_features
    from analyzer.scoring_engine import score_url
    from config import logger
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from hybrid.engine import analyze_url

API_NAME = "PhishScope API"
API_VERSION = "0.3"
API_PHASE = "3"
API_AUTHOR = "Sian Julian"

HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

app = Flask(__name__)
CORS(app)


def _error_response(message: str, status_code: int) -> tuple[Response, int]:
    """Build a consistent JSON error response."""
    return jsonify({"error": message}), status_code


@app.get("/")
def index() -> Response:
    """Return API metadata and current service status."""
    logger.info("API metadata requested")
    return jsonify(
        {
            "name": API_NAME,
            "version": API_VERSION,
            "phase": API_PHASE,
            "author": API_AUTHOR,
            "status": "running",
        }
    )


@app.get("/health")
def health() -> Response:
    """Return the health status for deployment and monitoring checks."""
    logger.info("Health check requested")
    return jsonify({"status": "healthy"})


@app.post("/analyze")
def analyze() -> Response | tuple[Response, int]:
    """Extract URL features, calculate a score, and return the verdict."""
    logger.info("Analyze request received")

    if not request.is_json:
        logger.warning("Analyze request rejected: content type is not application/json")
        return _error_response("Unsupported Media Type", 415)

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        logger.warning("Analyze request rejected: JSON body is missing or invalid")
        return _error_response("URL is required.", 400)

    url = payload.get("url")
    if not isinstance(url, str) or not url.strip():
        logger.warning("Analyze request rejected: URL is missing")
        return _error_response("URL is required.", 400)

    benchmark = payload.get("benchmark") is True
    result = analyze_url(url, benchmark=benchmark)
    if "error" in result:
        return _error_response(result["error"], 400)
        
    logger.info("URL: %s", url)
    logger.info("Hybrid Score: %s", result["hybrid"]["score"])
    logger.info("Hybrid Verdict: %s", result["hybrid"]["verdict"])
    return jsonify(result)


@app.errorhandler(400)
def handle_bad_request(_: Exception) -> tuple[Response, int]:
    """Return JSON for unhandled malformed requests."""
    logger.warning("Bad request received")
    return _error_response("Bad Request", 400)


@app.errorhandler(404)
def handle_not_found(_: Exception) -> tuple[Response, int]:
    """Return JSON for unknown routes."""
    logger.warning("Unknown route requested")
    return _error_response("Not Found", 404)


@app.errorhandler(405)
def handle_method_not_allowed(_: Exception) -> tuple[Response, int]:
    """Return JSON for unsupported HTTP methods."""
    logger.warning("Unsupported HTTP method requested")
    return _error_response("Method Not Allowed", 405)


@app.errorhandler(415)
def handle_unsupported_media_type(_: Exception) -> tuple[Response, int]:
    """Return JSON for unsupported request content types."""
    logger.warning("Unsupported media type received")
    return _error_response("Unsupported Media Type", 415)


@app.errorhandler(500)
def handle_internal_server_error(_: Exception) -> tuple[Response, int]:
    """Return JSON for unexpected server failures."""
    logger.exception("Unhandled server error")
    return _error_response("Internal Server Error", 500)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
