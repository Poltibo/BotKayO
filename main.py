import logging

from constants import TOKEN, DEV_CHANNEL, PROD_CHANNEL
from views import botkayo

logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] BotKayO: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    botkayo.channel_id = PROD_CHANNEL  # DEV_CHANNEL / PROD_CHANNEL
    botkayo.run(TOKEN)
