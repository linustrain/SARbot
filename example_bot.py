#example bot code

import discord
import os
import requests


steam_id = {}

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

    if message.content.startswith('$setID'):
        split_message = message.content.split()
        if len(split_message) > 1:
            steam_id[message.author.name] = split_message[1]
            await message.channel.send('Successfully set Steam ID for ' + message.author.name + ': ' + steam_id[message.author.name])
        else:
            await message.channel.send('Error setting Steam ID')

    if message.content.startswith('$getInfo'):
        if message.author.name not in steam_id.keys():
            await message.channel.send('Please set Steam ID using $setID <SteamID>')
            return
        stats_request = requests.get(url = 'https://royale.pet/api/player/' + steam_id[message.author.name] + '/stats')
        summary_request = requests.get(url = 'https://royale.pet/api/player/' + steam_id[message.author.name] + '/summary')
        stats_data = stats_request.json()
        summary_data = summary_request.json()
        print(stats_data)
        print(summary_data)
        stats = stats_data['stats']
        solos_stats = {
            'Games': stats['Games']['value'],
            'Kills': stats['Kills']['value'], 
            'MostKills': stats['MostKills']['value'],
            'Top': stats['Top5']['value'],
            'Deaths': stats['Deaths']['value'],
            'Wins': stats['Wins']['value']
        }
        duos_stats = {
            'Games': stats['GamesDuos']['value'],
            'Kills': stats['KillsDuos']['value'], 
            'MostKills': stats['MostKillsDuos']['value'],
            'Top': stats['Top3Duos']['value'],
            'Deaths': stats['DeathsDuos']['value'],
            'Wins': stats['WinsDuos']['value']
        }
        squads_stats = {
            'Games': stats['GamesSquads']['value'],
            'Kills': stats['KillsSquads']['value'], 
            'MostKills': stats['MostKillsSquads']['value'],
            'Top': stats['Top2Squads']['value'],
            'Deaths': stats['DeathsSquads']['value'],
            'Wins': stats['WinsSquads']['value']
        }
        kills_total = solos_stats['Kills'] + duos_stats['Kills'] + squads_stats['Kills']
        deaths_total = solos_stats['Deaths'] + duos_stats['Deaths'] + squads_stats['Deaths']
        games_total = solos_stats['Games'] + duos_stats['Games'] + squads_stats['Games']
        time_played = str(int(stats['TimePlayedSeconds']['value'] / 3600)) + " hours"
        print(time_played)
        embed = discord.Embed(title='Player Stats for ' + summary_data['summary']['personaname'], colour = discord.Colour.blue())
        embed.add_field(name='Kills', value=kills_total, inline=False)
        embed.add_field(name='Deaths', value=deaths_total, inline=False)
        embed.add_field(name='Games', value=games_total, inline=False)
        embed.add_field(name='Time Played (In-match)', value=time_played, inline=False)
        embed.add_field(name='Health Juice Drank', value=stats['HealthJuiceDrank']['value'], inline=False)
        embed.add_field(name='Damage Dealt', value=stats['DamageDealt']['value'], inline=False)

        await message.channel.send(embed=embed) 

client.run(str(os.getenv("TOKEN")))