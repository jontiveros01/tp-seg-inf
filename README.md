# TokenSnare - HoneyTokens Implementation

## 💻 Management (API)

This API has been designed to manage honeytokens, both to register new tokens and to receive their callbacks.

### 🕹️ Execution Instructions

There are two ways to run the API locally: using python (with a virtual environment) or using docker.

#### 🐍 Using Python
1. Create venv: `python3 -m venv venv`
2. Activate venv: `source ./venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run application: `python3 api/main.py`

#### 🐳 Using Docker
1. Build docker image: `docker build -t honeytokens-manager-api .`
2. Run docker image: `docker run -p 8080:8080 honeytokens-manager-api`

### 👨‍💻 Devs
If you are developing new features, be sure to record all dependencies in the [requirements.txt](./requirements.txt) file. You can follow the steps below if you are not familiar with python:
1. Make sure you are in the active virtual environment, if you don't know how to do this, go [here](#🐍-using-python) (steps 1 and 2)
2. Install all new dependencies if you haven't already: `pip install dep1 dep2 ...`
3. Update the `requirements.txt` file: `pip freeze > requirements.txt`

Do not forget to apply code formatter: `black . && isort .`

## 🍯 HoneyTokens Generator (CLI)

### To create a new honeytoken:
- Make sure you are on the path `/tp-seg-inf`
- Make sure you are running the API
- Run the following command: `python3 -m cli.main generate [token-type] -param value`

### Token Types & CLI Parameters

The system supports multiple types of honeytokens, each with different customizations or parameters.

| Token Type   | Command                  | Parameters                                |
|--------------|--------------------------|-------------------------------------------|
| `QR`         | `generate qr`            | `--message -m`                            |
| `PDF`        | `generate pdf`           | -                                         |

---

### Examples of use
```bash
# QR token with optional message
python3 -m cli.main generate qr -m "Page not found"

# PDF token
python3 -m cli.main generate pdf
```