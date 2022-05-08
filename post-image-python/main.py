import logging
import os
from datetime import datetime
from time import sleep

import requests
from picamera import PiCamera

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

SYSTEM_ID = '<SYSTEM_ID>'
DEVICE_ID = '<DEVICE_ID>'
url = f'https://api.fruitful.ag/v1/systems/{SYSTEM_ID}/devices/{DEVICE_ID}/image'
X_API_KEY = '<X-API-KEY>'


def take_picture(local_img_path):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    camera = PiCamera()
    camera.resolution = (1440, 1080)
    camera.iso = 100
    sleep(3)
    try:
        camera.start_preview()
        camera.annotate_text = str(current_time)
        sleep(2)
        camera.capture(local_img_path)
        camera.stop_preview()
        logger.info(f'Picture taken and saved under {local_img_path}')
    except Exception as e:
        logger.error(f'Error in taking a picture: {e}')
        raise e


def main():
    local_img_path = os.path.join(DIR_PATH, 'plant.jpg')
    take_picture(local_img_path)

    try:
        header = {'X-API-KEY': X_API_KEY}
        with open(local_img_path, 'rb') as img:
            files = {'image': img}
            r = requests.post(url, files=files, headers=header)
        logger.info(f'Request status: {r.status_code}, {r.text}')
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
