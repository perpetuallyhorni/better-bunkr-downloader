# This is buggy and sometimes corrupts videos... I recommend using [CyberDrop-DL](https://github.com/Jules-WinnfieldX/CyberDropDownloader), however that doesn't download multiple files at once, so it can be much slower. Overall it should be faster to delete corrupted videos and retrigger a download with this than using Cyberdrop. I suspect the bug comes from downloading the same file multiple times but I don't have time to debug it. Feel free to open an issue/PR if you identify or fix the bug.


# better-bunkr-downloader

### Forked from [Saertox/bunkr-downloader](https://github.com/Saertox/bunkr-downloader)

Downloads all files contained in a bunkr album (16 parallel downloads)

Tested on archlinux with python 3.10.13

Should work on binbows, Feel free to confirm or report otherwise. macOS support not guaranteed.

## Prerequisites

- cURL

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

`python downloader.py https://bunkr.link.to/album`
