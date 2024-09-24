import logging
import requests
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import argparse

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(ch)

def post_image(image_path, url, header):
    try:
        with open(image_path, 'rb') as img:
            files = {'image': img}
            r = requests.post(url, files=files, headers=header)

            if r.status_code > 201:
                logger.error(f"Failed to upload {image_path.name}: {r.status_code} - {r.text}")
    except Exception as e:
        logger.exception(f"Failed to upload {image_path.name}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Upload images to the server.')
    parser.add_argument('--system-id', required=True, help='System ID')
    parser.add_argument('--device-id', required=True, help='Device ID')
    parser.add_argument('--api-key', required=True, help='API Key')
    parser.add_argument('--images-folder', required=True, help='Folder containing images to upload')
    parser.add_argument('--max-workers', type=int, default=10, help='Maximum number of worker threads')

    args = parser.parse_args()

    images_folder = Path(args.images_folder)
    header = {'X-API-KEY': args.api_key}

    # Construct the URL
    url = f'https://api.fruitful.ag/v1/systems/{args.system_id}/devices/{args.device_id}/image'

    # List all PNG images in the folder
    images = list(images_folder.rglob("*.png"))

    if not images:
        logger.info("No images found to upload.")
        return

    max_workers = min(args.max_workers, len(images))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(tqdm(
            executor.map(lambda img: post_image(img, url, header), images),
            total=len(images),
            desc="Uploading images",
            unit="image"
        ))

if __name__ == '__main__':
    main()
