import yaml

with open("conf/secrets.yml", "r") as file:
    SECRETS = yaml.safe_load(file)

TOKEN = SECRETS["token"]

DEV_CHANNEL = SECRETS["channels"]["dev"]
PROD_CHANNEL = SECRETS["channels"]["prod"]

PLAYERS = [
    "LuluGub",
    "Tomygub",
    "Poltibo",
    "BetaKakarotene",
    "Lambabar",
    "Clavelloux",
    "ChokDi",
]
PODIUM_EMOJIS = {"1": "🏆", "2": "🥈", "3": "🥉"}
