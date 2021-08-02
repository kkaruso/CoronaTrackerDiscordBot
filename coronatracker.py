import discord
import requests

from tokenDC import CITIES, DISCORDTOKEN

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        # await message.add_reaction('<:weich:806915319209656321>')
        return

    if message.content.startswith('!corona'):
        user_request = message.content.split(maxsplit=1)[1]

        if user_request.lower() == 'help':
            await help(message)
        elif user_request.lower() == 'germany':
            await corona_germany(message)
        elif user_request.lower() == 'all':
            await all(message)
        elif user_request.lower() in CITIES:
            await corona_city(message, user_request)


async def corona_city(message, requested_city):
    data_cities = requests.get(
        'https://api.corona-zahlen.org/districts').json()['data']
    requested_city_lower = requested_city.lower()

    for _, data_city in data_cities.items():
        if data_city['name'].lower() == requested_city_lower:
            await message.channel.send(f"{requested_city} neue Fälle: {data_city['delta']['cases']} \n{requested_city} R-Wert: {round(data_city['weekIncidence'], 2)}")
            return

    await message.channel.send(f"Could not retrive any data for {requested_city}")


async def corona_germany(message):
    data_germany = requests.get('https://api.corona-zahlen.org/germany').json()

    await message.channel.send(f"Deutschland neue Fälle: {data_germany['delta']['cases']} \nDeutschland R-Wert: {round(data_germany['weekIncidence'], 2)}")


async def all(message):
    newJsonCity = requests.get(
        'https://api.corona-zahlen.org/districts').json()['data']
    newJsonGermany = requests.get(
        'https://api.corona-zahlen.org/germany').json()
    cityNames = ["Mannheim", "Ludwigshafen am Rhein",
                 "Alzey-Worms", "Neustadt an der Weinstraße", "München", "Worms"]

    for _, value in newJsonCity.items():
        if value['name'] in cityNames:
            cityNames.remove(value['name'])
            await message.channel.send(f"{value['name']} neue Fälle: {value['delta']['cases']} | r-Wert: {round(value['weekIncidence'], 2)}")

    await message.channel.send(f"Deutschland neue Fälle: {newJsonGermany['delta']['cases']} | r-Wert: {round(newJsonGermany['weekIncidence'], 2)}")


async def help(message):
    await message.channel.send(f"No help!")

client.run(DISCORDTOKEN)
