# Money project

This project contains `BrandFetch.py` which queries the BrandFetch API for brand categories.

Quick start (Windows, cmd.exe):

```
# Create a virtual environment named "venv"
python -m venv venv

# Activate it
venv\Scripts\activate

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Set your API key inside BrandFetch.py (replace the placeholder) or export it to the environment and run the script
python BrandFetch.py
```

Notes:
- Add your BrandFetch API key in `BrandFetch.py` at the top of the file (API_KEY variable).
- The `requirements.txt` currently contains `requests` which the script needs.
