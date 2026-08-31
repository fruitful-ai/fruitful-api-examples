# Post Images (Python)

Minimal example: uploads every `.png` / `.jpg` / `.jpeg` in a folder (recursively) to the
Fruitful API, one image at a time.

## Run

```sh
pip install -r requirements.txt
python main.py \
  --client-id YOUR_CLIENT_ID \
  --device-id YOUR_DEVICE_ID \
  --api-key YOUR_API_KEY \
  --images-folder /path/to/images
```

Get `CLIENT_ID` (called *System ID* in the Swagger docs) and `API_KEY` from the
[Fruitful App](https://app.fruitful.ag) settings. `DEVICE_ID` is any unique string you
choose per device.

Exit code is `1` if any upload failed.

See the [Swagger docs](https://api.fruitful.ag/v1/docs/) for the full API.
