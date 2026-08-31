# Fruitful API Examples

![Fruitful logo](fixtures/logo_ffai.png)

Small, self-contained examples for the [Fruitful API](https://api.fruitful.ag/v1/docs/).

| Example | What it does |
|---|---|
| [`post-image-python`](post-image-python/) | Upload a folder of images |

## Setup

Python 3.9+.

```sh
git clone git@github.com:fruitful-farming/fruitful-api-examples.git
cd fruitful-api-examples/post-image-python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Get your `CLIENT_ID` and `API_KEY` from the [Fruitful App](https://app.fruitful.ag).
Each example's README shows how to run it.
