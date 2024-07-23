# Lightspark Python SDK

The Lightspark Python SDK provides a convenient way to interact with the Lightspark services from applications written in the Python language.

## Installation

To install the SDK, simply run:

```bash
pip install lightspark
```

## Documentation

The documentation for this SDK (installation, usage, etc.) is available at https://docs.lightspark.com/lightspark-sdk/getting-started?language=Python

## Sample code

For your convenience, we included an example that shows you how to use the SDK.
Open the file `example.py` and make sure to update the variables at the top of the page with your information, then run it using pipenv:

```python
pipenv install
pipenv run python -m examples.example
```

There are also a few examples of webservers for demonstrating webhooks and LNURLs. These can similarly be run through Flask:

```python
pipenv install -d
pipenv run flask --app examples.flask_lnurl_server run
```

Note that Flask requires Python >= 3.8, so these examples will not work if running Python 3.7.
