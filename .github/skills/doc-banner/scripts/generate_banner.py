#!/usr/bin/env python3
"""Generate a doc banner PNG with the Microsoft Foundry MAI image model.

Grounded in: https://learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-mai

Auth: API key (env AZURE_API_KEY) OR Microsoft Entra ID (DefaultAzureCredential).
Constraints (MAI image API): width >= 768, height >= 768, width*height <= 1048576,
output is always PNG.
"""
from __future__ import annotations

import argparse
import base64
import os
import sys

import requests  # pip install requests

DEFAULT_ENDPOINT = "https://project-ai-demos-resource.services.ai.azure.com"
DEFAULT_DEPLOYMENT = "MAI-Image-2.5"
MAX_PIXELS = 1_048_576
MIN_SIDE = 768


def build_headers() -> dict[str, str]:
    """Prefer an API key if present; otherwise fall back to Entra ID."""
    api_key = os.environ.get("AZURE_API_KEY")
    if api_key:
        return {"Content-Type": "application/json", "api-key": api_key}

    try:
        from azure.identity import (  # pip install azure-identity
            DefaultAzureCredential,
            get_bearer_token_provider,
        )
    except ImportError:
        sys.exit(
            "No AZURE_API_KEY set and azure-identity is not installed.\n"
            "Either set $env:AZURE_API_KEY, or run 'pip install azure-identity' "
            "and 'az login' to use Microsoft Entra ID."
        )

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    return {"Content-Type": "application/json", "Authorization": f"Bearer {token_provider()}"}


def validate_size(width: int, height: int) -> None:
    if width < MIN_SIDE or height < MIN_SIDE:
        sys.exit(f"width and height must each be >= {MIN_SIDE} (got {width}x{height}).")
    if width * height > MAX_PIXELS:
        sys.exit(
            f"width*height must be <= {MAX_PIXELS} (got {width * height}). "
            "Try 1344x768 for the widest supported banner."
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a doc banner via MAI-Image-2.5.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", help="Inline text prompt.")
    group.add_argument("--prompt-file", help="Path to a UTF-8 file containing the prompt.")
    parser.add_argument("--out", required=True, help="Output PNG path.")
    parser.add_argument("--width", type=int, default=1344, help="Image width (>=768). Default 1344.")
    parser.add_argument("--height", type=int, default=768, help="Image height (>=768). Default 768.")
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("AZURE_ENDPOINT", DEFAULT_ENDPOINT),
        help=f"Foundry resource endpoint. Default {DEFAULT_ENDPOINT}.",
    )
    parser.add_argument(
        "--deployment",
        default=os.environ.get("DEPLOYMENT_NAME", DEFAULT_DEPLOYMENT),
        help=f"Model deployment name. Default {DEFAULT_DEPLOYMENT}.",
    )
    args = parser.parse_args()

    validate_size(args.width, args.height)

    if args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as handle:
            prompt = handle.read().strip()
    else:
        prompt = args.prompt

    url = f"{args.endpoint.rstrip('/')}/mai/v1/images/generations"
    payload = {
        "model": args.deployment,
        "prompt": prompt,
        "width": args.width,
        "height": args.height,
    }

    print(f"POST {url}  ({args.width}x{args.height}, deployment={args.deployment})")
    response = requests.post(url, headers=build_headers(), json=payload, timeout=180)
    if response.status_code != 200:
        sys.exit(f"Request failed [{response.status_code}]: {response.text}")

    result = response.json()
    images = [item for item in result.get("data", []) if "b64_json" in item]
    if not images:
        sys.exit(f"Unexpected response format: {result}")

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "wb") as handle:
        handle.write(base64.b64decode(images[0]["b64_json"]))

    print(f"Image saved to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
