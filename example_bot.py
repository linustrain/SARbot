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
        stats_request = requests.get(url = 'https://royale.pet/api/player/76561198106196691/stats')
        summary_request = requests.get(url = 'https://royale.pet/api/player/76561198106196691/summary')
        data = stats_request.json()
        summary_data = summary_request.json()
        print(summary_data)
        stats = data['stats']
        embed = discord.Embed(title='Player Stats for ' + summary_data['summary']['personaname'], colour = discord.Colour.blue())
        embed.add_field(name='Kills', value=stats['Kills']['value'], inline=False)
        embed.add_field(name='Deaths', value=stats['Deaths']['value'], inline=False)
        embed.add_field(name='Games', value=stats['Games']['value'], inline=False)
        embed.add_field(name='Time Played', value=stats['TimePlayedSeconds']['value'], inline=False)
        embed.add_field(name='Health Juice Drank', value=stats['HealthJuiceDrank']['value'], inline=False)
        embed.add_field(name='Damage Dealt', value=stats['DamageDealt']['value'], inline=False)

        await message.channel.send(embed=embed) 

client.run(str(os.getenv("TOKEN")))