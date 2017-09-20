# pixutils

Scripts Python pour interroger Airtable dans PIX.

## Installation

    git clone https://github.com/jilljenn/pixutils
    cd pixutils
    echo 'AIRTABLE_BASE=XXX' >> .env
    echo 'AIRTABLE_API_KEY=XXX' >> .env
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

## Usage

Pour rafraîchir les tests adaptatifs, faites :

    python quickstart.py
