"""Upload every image in a folder to the Fruitful API, one at a time."""

import argparse
import sys
from pathlib import Path

import requests

# The public API still names the client segment `systems` (legacy naming).
IMAGE_URL = "https://api.fruitful.ag/v1/systems/{client_id}/devices/{device_id}/image"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}


def upload_image(url: str, api_key: str, image_path: Path) -> bool:
    with image_path.open("rb") as image:
        response = requests.post(
            url, headers={"X-API-KEY": api_key}, files={"image": image}, timeout=30
        )
    if response.ok:
        print(f"Uploaded {image_path}")
        return True
    print(f"Failed {image_path}: {response.status_code} {response.text}",
        file=sys.stderr)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload images to the Fruitful API.")
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--device-id", required=True)
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--images-folder", required=True, type=Path)
    args = parser.parse_args()

    url = IMAGE_URL.format(client_id=args.client_id, device_id=args.device_id)
    images = sorted(
        p for p in args.images_folder.rglob("*") if p.suffix.lower() in IMAGE_SUFFIXES
    )
    failures = sum(not upload_image(url, args.api_key, path) for path in images)
    print(f"Uploaded {len(images) - failures}/{len(images)} images")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
