import logging

import discord
import requests
from discord.ext import commands

from constants import PLAYERS, PODIUM_EMOJIS, DEV_CHANNEL
from core import (
    get_ranks_from_image,
    update_score,
    get_weapons,
    duel_result,
    get_points,
)


class BotKayO(commands.Bot):
    def __init__(
        self,
        player_list: list[str],
        channel_id: int,
    ):
        self.player_list = player_list
        self.channel_id = channel_id

        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(intents=intents, command_prefix="!")


def my_channel_only(func):
    def func_wrapper(ctx, *args, **kwargs):
        logging.info(f"{ctx.channel.id}, {botkayo.channel_id}")
        if ctx.channel.id == botkayo.channel_id:
            return func(*args, **kwargs)
        else:
            raise ValueError

    return func_wrapper


botkayo = BotKayO(player_list=PLAYERS, channel_id=DEV_CHANNEL)


# noinspection PyUnresolvedReferences
class Button(discord.ui.View):
    def __init__(self, player_list: list[str]):
        super().__init__()
        self.player_list = player_list

    @discord.ui.button(label="Valider", style=discord.ButtonStyle.green)
    async def val_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        update_score(self.player_list)

        await interaction.response.send_message(
            f"{interaction.user} a validé ce classement."
        )

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.red)
    async def cancel_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            f"{interaction.user} a refusé ce classement."
        )


@botkayo.event
async def on_message(message):
    if message.attachments and message.channel.id == botkayo.channel_id:
        img_data = requests.get(message.attachments[0].url).content

        with open("data/img/last_game.jpg", "wb") as handler:
            handler.write(img_data)

        embedVar = discord.Embed(
            title=f"Classement :",
            description="Est-ce que c'est correct ? ",
            color=0x001C81,
        )

        player_ranks = get_ranks_from_image("data/img/last_game.jpg")
        rank = 1

        for player in player_ranks:
            embedVar.add_field(
                name=f"{str(rank) + '.' if rank > 3 else PODIUM_EMOJIS[str(rank)]}",
                value="",
                inline=True,
            )
            embedVar.add_field(name=":", value="", inline=True)
            embedVar.add_field(
                name=f"{player}",
                value="",
                inline=True,
            )
            rank += 1

        # embedVar.set_image(url=message.attachments[0].url)
        await message.channel.send(
            embed=embedVar, view=Button(player_list=player_ranks)
        )

    await botkayo.process_commands(message)


@my_channel_only
@botkayo.command(name="next_game")
async def next_game(ctx, *players):
    if ctx.channel.id == botkayo.channel_id:
        weapons = get_weapons([player for player in players])

        embedVar = discord.Embed(
            title=f"Armes pour la prochaine game :",
            color=0x001C81,
        )

        for player in weapons.keys():
            embedVar.add_field(
                name=f"{player}",
                value="",
                inline=True,
            )
            embedVar.add_field(name=":", value="", inline=True)
            embedVar.add_field(
                name=f"{weapons[player]}",
                value="",
                inline=True,
            )

        await ctx.send(embed=embedVar)


@my_channel_only
@botkayo.command(name="duel")
async def duel(ctx, player1, player2):
    if ctx.channel.id == botkayo.channel_id:
        res = duel_result(player1, player2)
        if res:
            await ctx.send(
                f"{player1} et {player2} ont échangé leur place au classement!"
            )
        else:
            await ctx.send(
                f"{player1} est déjà plus haut que  {player2} dans le classement. Pas d'échange."
            )


@my_channel_only
@botkayo.command(name="ranking")
async def ranking(ctx):
    if ctx.channel.id == botkayo.channel_id:
        scores = get_points()
        weapons = get_weapons()
        embedVar = discord.Embed()
        embedVar.set_author(name="Classement")
        # embedVar.set_thumbnail(url=RANKINGS_ICON)
        rank = 1
        for key in scores.keys():
            embedVar.add_field(
                name=f"{str(rank) + '.' if rank > 3 else PODIUM_EMOJIS[str(rank)]} {key}",
                value="",
                inline=True,
            )
            embedVar.add_field(
                name=f"{int(scores[key])}pts",
                value="",
                inline=True,
            )
            embedVar.add_field(name=f"{weapons[key]}", value="", inline=True)
            rank += 1
        await ctx.send(embed=embedVar)


@my_channel_only
@botkayo.command(name="guide")
async def guide(ctx):
    if ctx.channel.id == botkayo.channel_id:
        embedVar = discord.Embed(
            title=f"Manuel d'utilisation :",
            color=0x001C81,
        )
        embedVar.add_field(
            name=f"!next_game Player1 ... PlayerN",
            value="Attribue les armes à tous les joueurs mentionnés pour la prochaine game selon leur classement.",
            inline=False,
        )
        embedVar.add_field(
            name=f"!duel PlayerWin PlayerLose",
            value="Enregistre le résultat d'un duel. Si PlayerWin est en dessous de PlayerLose au classement, "
            "inverse les classements des 2 joueurs.",
            inline=False,
        )
        embedVar.add_field(
            name=f"!ranking",
            value="Affiche le classement global et les armes actuellement attribuées.",
            inline=False,
        )
        embedVar.add_field(
            name=f"Envoi d'un screenshot de fin de game",
            value="Définit le classement de la game et demande validation pour éviter les erreurs. Si validation, "
            "met à jour le classement des joueurs impliqués.",
            inline=False,
        )

        await ctx.send(embed=embedVar)


@botkayo.event
async def on_ready():
    logging.info("Ready")
    await botkayo.user.edit(username="BotKayO")
    await botkayo.change_presence(
        activity=discord.Activity(type=discord.ActivityType.competing, name="Valorant")
    )
