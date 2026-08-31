"""Upload every image in a folder to the Fruitful API, in parallel."""

import argparse
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

API_BASE_URL = "https://api.fruitful.ag/v1"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
REQUEST_TIMEOUT_SECONDS = 30

logger = logging.getLogger(__name__)


def build_image_url(client_id: str, device_id: str) -> str:
    # The public API still names the client segment `systems` (legacy naming).
    return f"{API_BASE_URL}/systems/{client_id}/devices/{device_id}/image"


def build_session(api_key: str, max_workers: int) -> requests.Session:
    """One session shared across threads is safe: headers set once, no cookies."""
    session = requests.Session()
    session.headers["X-API-KEY"] = api_key
    # Default pool size is 10; above that, connections are discarded per request.
    session.mount("https://", HTTPAdapter(pool_maxsize=max_workers))
    return session


def find_images(folder: Path) -> list[Path]:
    return sorted(
        p
        for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )


def upload_image(session: requests.Session, url: str, image_path: Path) -> bool:
    """Return True on success; on any failure log it and return False."""
    try:
        with image_path.open("rb") as image:
            response = session.post(
                url, files={"image": image}, timeout=REQUEST_TIMEOUT_SECONDS
            )
    except (OSError, requests.RequestException) as error:
        logger.error("Failed to upload %s: %s", image_path, error)
        return False
    if response.ok:
        return True
    logger.error(
        "Failed to upload %s: %s %s",
        image_path,
        response.status_code,
        response.text[:200],
    )
    return False


def upload_all(
    session: requests.Session, url: str, images: list[Path], max_workers: int
) -> int:
    """Return the number of uploads that failed."""
    with ThreadPoolExecutor(max_workers=min(max_workers, len(images))) as executor:
        results = tqdm(
            executor.map(lambda path: upload_image(session, url, path), images),
            total=len(images),
            desc="Uploading images",
            unit="image",
        )
        return sum(1 for ok in results if not ok)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload images to the Fruitful API.")
    parser.add_argument(
        "--client-id", required=True, help="Client ID from the Fruitful app"
    )
    parser.add_argument(
        "--device-id", required=True, help="Unique ID of the uploading device"
    )
    parser.add_argument(
        "--api-key", required=True, help="API key from the Fruitful app"
    )
    parser.add_argument(
        "--images-folder", required=True, type=Path, help="Folder searched recursively"
    )
    parser.add_argument("--max-workers", type=int, default=10, help="Parallel uploads")
    args = parser.parse_args()
    if args.max_workers < 1:
        parser.error("--max-workers must be at least 1")
    if not args.images_folder.is_dir():
        parser.error(f"--images-folder is not a folder: {args.images_folder}")
    return args


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    args = parse_args()

    images = find_images(args.images_folder)
    if not images:
        logger.info("No images found in %s", args.images_folder)
        return 0

    url = build_image_url(args.client_id, args.device_id)
    with build_session(
        args.api_key, args.max_workers
    ) as session, logging_redirect_tqdm():
        failures = upload_all(session, url, images, args.max_workers)

    logger.info("Uploaded %d/%d images", len(images) - failures, len(images))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
