# TokenSnare - HoneyTokens Implementation

## 💻 Management (API)

This API has been designed to manage honeytokens, both to register new tokens and to receive their callbacks.

### 🕹️ Execution Instructions

There are two ways to run the API locally: using python (with a virtual environment) or using docker.

#### 🐍 Using Python
1. Create venv: `python3 -m venv venv`
2. Activate venv: 
- On Windows, run: `venv\Scripts\activate.bat`
- On Linux/MacOS, run: `./venv/bin/activate` 
3. Install dependencies: `pip install -r requirements.txt`
4. Run application: `python api/main.py`

#### 🐳 Using Docker
1. Build docker image: `docker build -t honeytokens-manager-api .`
2. Run docker image: `docker run -p 8080:8080 honeytokens-manager-api`

## 🍯 HoneyTokens Generator (CLI)

### To create a new honeytoken:
- Make sure you are on the path `/tp-seg-inf`
- Make sure you are running the API
- Run the following command: `python3 -m cli.main generate [token-type] -param value`

### Token Types & CLI Parameters

The system supports multiple types of honeytokens, each with different customizations or parameters.

| Token Type   | Command                  | Parameters                                | Values                                     |
|--------------|--------------------------|-------------------------------------------|--------------------------------------------|
| `QR`         | `generate qr`            | `--message -m`                            | string                                     |
| `PDF`        | `generate pdf`           | -                                         | -                                          |
| `HTML`       | `generate html`          | `--strategy -s`                           | `fetch-script` `css-bg` `remote-css`       |

---

### Examples of use
```bash
# QR token with optional message
python3 -m cli.main generate qr -m "Page not found"

# PDF token
python3 -m cli.main generate pdf

# HTML token
python3 -m cli.main generate html -s remote-css
```