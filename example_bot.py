#example bot code

import discord
import os
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$getinfo'):
        r = requests.get(url = 'https://royale.pet/api/player/76561198106196691/summary')
        data = r.json()
        print(data)
        summary = data['summary']
        print(summary)
        embed = discord.Embed(title='Player Stats for ' + summary['personaname'], colour = discord.Colour.blue())
        for key, value in summary.items():
            embed.add_field(name=key, value=value, inline=False)
        await message.channel.send(embed=embed) 

client.run(str(os.getenv("TOKEN")))