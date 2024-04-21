# bunkr-downloader
Downloads all files contained in a bunkr album (16 parallel downloads)

Tested on archlinux with python 3.10.13

Should work on binbows, Feel free to confirm or report otherwise. macOS support not guaranteed.

### Prerequisites

- cURL

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage

`python downloader.py https://bunkr.link.to/album`