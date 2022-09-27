# Quotes-API
> Unofficial API for fetching quotes from Goodreads. Originally created by CW4RRIOR, modified by nynxa.

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[API docs](https://github.com/CW4RR10R/Quotes-API/wiki/API-Docs)

#### Sample Response
```json
{
  "author": "Lao Tzu", 
  "image": "https://images.gr-assets.com/authors/1435903703p2/2622245.jpg", 
  "tags": [
    "courage", 
    "deeply-loved", 
    "love", 
    "strength", 
    "widely-misattributed"
  ], 
  "text": "\u201cBeing deeply loved by someone gives you strength, while loving someone deeply gives you courage.\u201d    \u2015      Lao Tzu"
}
```

### Installation
* Cloning the repository
``` bash
git clone https://github.com/nynxa/Quotes-API
cd Quotes-API
```

* Setting up a virtual environment
``` bash
pip3 install virtualenv
virtualenv quotesapi
source quotesapi/bin/activate
```

* Installing the requirements and run your flask application
``` bash
pip3 install -r requirements.txt
python3 main.py
```

#### Contact Me
[![Telegram](https://img.shields.io/badge/Telegram-blue?style=for-the-badge&logo=telegram)](https://t.me/W4RR10R/)
[![Mail](https://img.shields.io/badge/Mail-grey?style=for-the-badge&logo=gmail)](mailto:arunpt@hi2.in?subject=Quotes-API)