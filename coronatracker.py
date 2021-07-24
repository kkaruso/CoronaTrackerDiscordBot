import requests, discord
from tokenDC import DISCORDTOKEN

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    newJsonCity = coronaCity()
    newJsonGermany = coronaGermany()

    if message.author == client.user:
        return

    if message.content.startswith('!corona'):
        test = message.content.split(maxsplit=1)[1]
        city = ""
        for _, value in newJsonCity['data'].items():
            if value['name'] == test:
                city = value
        await message.channel.send(f"{test} neue Fälle: {city['delta']['cases']} \n{test} R-Wert: {round(city['weekIncidence'], 2)}")
    
    if message.content.startswith('deutschland'):
        await message.channel.send(f"Deutschland neue Fälle: {newJsonGermany['delta']['cases']} \nDeutschland R-Wert: {round(newJsonGermany['weekIncidence'], 2)}")

def coronaCity():

    r = requests.get('https://api.corona-zahlen.org/districts').json()
    newJsonCity = r

    return newJsonCity

def coronaGermany():

    r = requests.get('https://api.corona-zahlen.org/germany').json()
    newJsonGermany = r

    return newJsonGermany

client.run(DISCORDTOKEN)