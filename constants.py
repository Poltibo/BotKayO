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

WEAPONS = {
    "1": "classic",
    "2": "ghost",
    "3": "bucky",
    "4": "guardian",
    "5": "vandal",
    "6": "odin",
    "7": "operator",
}

PLAYER_AGENTS = {
    "LuluGub": "reyna",
    "Tomygub": "chamber",
    "Poltibo": "kayo",
    "BetaKakarotene": "killjoy",
    "Lambabar": "skye",
    "Clavelloux": "cypher",
    "ChokDi": "brimstone",
}

SPRAYS = {
    "kayo": {"win": ["data/img/sprays/kayo/kayo_win1.gif"]},
    "cypher": {"win": ["data/img/sprays/cypher/cypher_win1.png"]},
    "brimstone": {"win": ["data/img/sprays/brimstone/brimstone_win1.png"]},
    "chamber": {"win": ["data/img/sprays/chamber/chamber_win1.png"]},
    "reyna": {"win": ["data/img/sprays/reyna/reyna_win1.png"]},
    "killjoy": {"win": ["data/img/sprays/killjoy/killjoy_win1.png"]},
    "skye": {"win": ["data/img/sprays/skye/skye_win1.png"]},
    "misc": {
        "rank": "https://static.wikia.nocookie.net/valorant/images/c/cb/Winner%27s_Ribbon_Spray.png"
    },
}
