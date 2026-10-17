#!/usr/bin/env python3
"""Dependency-free learning pipeline discovery. Classification is advisory, never executes remote input."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

REGISTRY = Path(__file__).parent / "registry" / "pipelines.json"

def classify(source: str, explicit_type: str | None = None) -> str:
    """Explicit types win; unknown URLs are not silently treated as videos."""
    if explicit_type:
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", explicit_type):
            raise ValueError("Invalid input type")
        return explicit_type
    s = source.strip()
    parsed = urlparse(s)
    if parsed.scheme in ("https", "http") and parsed.hostname:
        host = parsed.hostname.lower()
        if host in ("youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"):
            return "youtube_url"
        if host in ("github.com", "www.github.com"):
            return "repository_url"
        if host in ("instagram.com", "www.instagram.com", "vimeo.com", "www.vimeo.com", "tiktok.com", "www.tiktok.com"):
            return "video_url"
        if parsed.path.lower().endswith((".mp4", ".mov", ".webm", ".mkv")):
            return "video_url"
        return "website_url"
    if s.lower().endswith((".mp4", ".mov", ".webm", ".mkv")):
        return "video_file"
    if len(s.split()) >= 30:
        return "research"
    return "concept"

def route(source: str, explicit_type: str | None = None) -> dict:
    kind = classify(source, explicit_type)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    matches = [p for p in registry["pipelines"] if kind in p["inputs"]]
    if matches:
        return {"input_type": kind, "status": "matched", "pipelines": [p["id"] for p in matches],
                "execution": "not_started", "note": "Routing is not ingestion or verification."}
    return {"input_type": kind, "status": "capability_gap", "pipelines": [],
            "execution": "not_started",
            "proposal": {"input_type": kind, "status": "proposed",
                         "next": "Research existing adapters, compare alternatives, sandbox test, review before registration."}}

def main():
    parser = argparse.ArgumentParser(description="Recognize learning inputs without executing them")
    parser.add_argument("source")
    parser.add_argument("--type", dest="explicit_type")
    args = parser.parse_args()
    print(json.dumps(route(args.source, args.explicit_type), indent=2))

if __name__ == "__main__":
    main()
