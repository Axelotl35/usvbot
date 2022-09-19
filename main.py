from discord.ext.commands import Bot
from random import random
import discord
from bs4 import BeautifulSoup
import chess
import chess.svg
import sys
from tabulate import tabulate

import read_token


import urllib.request
from datetime import datetime
def passed(d):
    return datetime.now() < datetime(*d[::-1])
    #return datetime(2022,9,30) < datetime(*d[::-1])

client = Bot(command_prefix="$", intents=discord.Intents.all())

# IGNORE UNTIL HERE

@client.event
async def on_ready():
    print("ready")
    #"It's not about winning, it's about sending a message"

@client.command()
async def ping(ctx):
    await ctx.send("pong")


@client.slash_command(description="Zeigt den nächsten Gegner in der Liga an.")
async def nextgame(ctx):
    league = 2
    site = str(urllib.request.urlopen(f'https://schachligen.de/cgi-bin/admin/hp.cgi?action=termine_anzeigen&liga_id={league}').readlines())
    soup = BeautifulSoup(site,"html.parser")
    table = soup.find_all("table")[2].find("table").find("table").find("table").find("table").find("table").find_all("tr")

    team = "USV Potsdam I"
    opponent = ""
    id = ""

    found = False
    for col in table:
        if col.has_attr("bgcolor"):
            if col.attrs["bgcolor"] == "silver":
                datestr = str(col.contents[0].contents[0]).split(" ")[1]
                date = list(map(int,datestr.split(".")))
                if passed(date):
                    found = True
            elif found and team in str(col):
                opponent = list(filter(lambda x:x!=team,[col.contents[0].contents[0], col.contents[1].contents[0]]))[0]
                break
    site = str(urllib.request.urlopen(f'https://schachligen.de/cgi-bin/admin/hp.cgi?action=mannschaft_liga&liga_id={league}').readlines())
    soup = BeautifulSoup(site,"html.parser")
    teams = soup.find_all(attrs={"type":"radio"})
    for t in teams:
        if str(t.next_element) == opponent:
            id = t.attrs["value"]
            break
    site = str(urllib.request.urlopen(f'https://schachligen.de/cgi-bin/admin/hp.cgi?liga_id={league}&mannschaft_id={id}&action=mannschaft_anzeigen').readlines())
    soup = BeautifulSoup(site,"html.parser")
    players = soup.find("tr",attrs={"bgcolor":"silver"}).find_next("tr").find_all_next("tr")
    playerlist = []
    for player in players:
        if not player.has_attr("bgcolor"):break
        if player.attrs["bgcolor"]!="white":break
        playerlist.append(list(map(lambda x:str(x.contents[0].contents[0]),player.contents[:4]+[player.contents[-1]])))
        playerlist[-1][-1]+=str(player.contents[-1].contents[0].contents[1].contents[0])
    #print()
    await ctx.send(f"Das nächste Spiel ist ein {'Heimspiel' if col.contents[0].contents[0]==team else 'Auswärtsspiel'} am {datestr} gegen {opponent}.")
    await ctx.send("Gegnerische Aufstellung:\n```"+tabulate(playerlist, headers=['Brett', 'Vorname', 'Nachname', 'DWZ', 'Punkte'], tablefmt='orgtbl')+"```")

# @client.command()
# async def genFEN(ctx,FEN):
#     pass

# IGNORE FROM HERE

# ALWAYS COPY THE LAST LINE
# ALWAYS SHARE TOKEN WITH OTHERS
TOKEN = read_token.read("token.txt")
client.run(TOKEN)