# Post Images (Python)

Uploads every `.png` / `.jpg` / `.jpeg` (any case) found recursively in a folder to the
Fruitful API, using a thread pool for parallel uploads.

## Run

```sh
pip install -r requirements.txt
python main.py \
  --client-id YOUR_CLIENT_ID \
  --device-id YOUR_DEVICE_ID \
  --api-key "$FRUITFUL_API_KEY" \
  --images-folder /path/to/images \
  --max-workers 5   # optional, default 10
```

Get `CLIENT_ID` (called *System ID* in the Swagger docs) and `API_KEY` from the
[Fruitful App](https://app.fruitful.ag) settings. `DEVICE_ID` is any unique string you
choose per device.

Exit codes: `0` all uploaded (or no images found), `1` at least one upload failed
(each failure is logged with its path), `2` bad arguments.

See the [Swagger docs](https://api.fruitful.ag/v1/docs/) for the full API.
