import os

from pathlib import Path
from dotenv import load_dotenv

import json

import ufobit

WORKDIR = Path(__file__).parent
I18N_DOMAIN = "ufo_bot"
LOCALES_DIR = WORKDIR / "locales"

with open('config.env', 'r') as env_file:
    load_dotenv(stream=env_file)

TOKEN = os.getenv("TOKEN")

WALLET = os.getenv("WALLET")

wallet_private = os.getenv("PRIVATE_KEY")

main_wallet = ufobit.Key(wallet_private)

SUPPORT_ID = 5802571273