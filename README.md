# Dropbox Upload

Script to upload all contents to dropbox and create sharable links for each file.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
python -m venv venv
# For Linux: 
source venv/bin/activate
pip install -r requirements.txt
```

## Environment Configuration:
- Generate DropBox access token and assign value in DropBoxCustom file for `DROPBOX_ACCESS_TOKEN`
- Assign app directory of DropBox where you want to upload the contents using `DROPBOX_ROOT_PATH` variable
- In `main.py` configure your media file location in `BASE_DIR` variable

## Usage

- Run `python main.py`
- Script will scan for resources in media location
- Script will upload all the files one by one
- Script will print a sharable link for each uploaded file