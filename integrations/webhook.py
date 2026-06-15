#!/usr/bin/env python3
"""Minimal, dependency-free webhook forwarder for Cognis findings.

Reads JSON findings on stdin and POSTs them to a URL (SIEM/Slack/Jira bridge).
Usage:  <tool> scan . --format json | python integrations/webhook.py --url URL
"""
from __future__ import annotations

import argparse
import sys
import urllib.request
from urllib.parse import urlparse


def _validate_url(url: str) -> None:
    """Raise ValueError if url is not a valid http/https URL."""
    try:
        parsed = urlparse(url)
    except Exception as exc:
        raise ValueError(f"Cannot parse URL: {exc}") from exc
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"URL scheme must be http or https, got {parsed.scheme!r}."
        )
    if not parsed.netloc:
        raise ValueError("URL has no host.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Destination URL (http/https)")
    ap.add_argument("--header", action="append", default=[], help="Key: Value")
    args = ap.parse_args()

    try:
        _validate_url(args.url)
    except ValueError as exc:
        print(f"error: invalid --url: {exc}", file=sys.stderr)
        return 2

    payload_str = sys.stdin.read()
    if not payload_str.strip():
        print("error: stdin is empty — nothing to post.", file=sys.stderr)
        return 2

    payload = payload_str.encode("utf-8")

    req = urllib.request.Request(args.url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    for h in args.header:
        if ":" not in h:
            print(
                f"error: --header {h!r} must be in 'Key: Value' format.",
                file=sys.stderr,
            )
            return 2
        k, _, v = h.partition(":")
        req.add_header(k.strip(), v.strip())

    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"posted {len(payload)} bytes -> {r.status}")
        return 0
    except urllib.error.HTTPError as exc:
        print(f"webhook HTTP error: {exc.code} {exc.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"webhook connection error: {exc.reason}", file=sys.stderr)
        return 1
    except TimeoutError:
        print("webhook error: connection timed out.", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"webhook error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
