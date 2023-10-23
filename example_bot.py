#example bot code

import discord
import os
import requests

# git status
# git add .
# git commit -m "commit message"
# git push

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

    if message.content.startswith('$getStats'):
        if message.author.name not in steam_id.keys():
            # Get input from user for steam ID
            await message.channel.send('Please set Steam ID using $setID <SteamID>')
            return
        
        # Get API data from SAR API
        stats_data, summary_data = player_info(steam_id[message.author.name])
        
        # print(stats_data)
        # print(summary_data)
        
        # Gets data for each gamemode and inserts into var
        stats = stats_data['stats']
        solos_stats = format_solo_data(stats)
        duos_stats = format_duos_data(stats)
        squads_stats = format_squads_data(stats)
        kills_total = solos_stats['Kills'] + duos_stats['Kills'] + squads_stats['Kills']
        deaths_total = solos_stats['Deaths'] + duos_stats['Deaths'] + squads_stats['Deaths']
        games_total = solos_stats['Games'] + duos_stats['Games'] + squads_stats['Games']
        time_played = str(int(stats['TimePlayedSeconds']['value'] / 3600)) + " hours"
        # print(time_played)
        
        embed = create_stats_embed('Total', summary_data['summary']['personaname'], kills_total, deaths_total, games_total, time_played)

        await message.channel.send(embed=embed) 

    if message.content.startswith('$getSoloStats'):
        if message.author.name not in steam_id.keys():
            # Get input from user for steam ID
            await message.channel.send('Please set Steam ID using $setID <SteamID>')
            return
        stats_data, summary_data = player_info(steam_id[message.author.name])
        stats = stats_data['stats']
        solos_stats = format_solo_data(stats)
        time_played = str(int(stats['TimePlayedSeconds']['value'] / 3600)) + " hours"
        embed = create_stats_embed('Solo', summary_data['summary']['personaname'], solos_stats['Kills'], solos_stats['Deaths'], solos_stats['Games'], time_played)
        await message.channel.send(embed=embed)

def create_stats_embed(gamemode, playername, kills, deaths, games, time):
# Embed totals data into fields
        title = gamemode + " Stats for " + playername
        embed = discord.Embed(title=title, colour = discord.Colour.blue())
        embed.add_field(name='Kills', value=kills, inline=False)
        embed.add_field(name='Deaths', value=deaths, inline=False)
        embed.add_field(name='Games', value=games, inline=False)
        embed.add_field(name='Time Played (In-match)', value=time, inline=False)
        return embed

def player_info(playername): 
# Get API data from SAR API
        stats_request = requests.get(url = 'https://royale.pet/api/player/' + playername + '/stats')
        summary_request = requests.get(url = 'https://royale.pet/api/player/' + playername + '/summary')
        stats_data = stats_request.json()
        summary_data = summary_request.json()
        return stats_data, summary_data

# Each function gets API data from SAR API and returns dictionary
def format_solo_data(stats):
    return {
        'Games': stats['Games']['value'],
        'Kills': stats['Kills']['value'], 
        'MostKills': stats['MostKills']['value'],
        'Top': stats['Top5']['value'],
        'Deaths': stats['Deaths']['value'],
        'Wins': stats['Wins']['value']
    }
def format_duos_data(stats):
    return {
        'Games': stats['GamesDuos']['value'],
        'Kills': stats['KillsDuos']['value'], 
        'MostKills': stats['MostKillsDuos']['value'],
        'Top': stats['Top3Duos']['value'],
        'Deaths': stats['DeathsDuos']['value'],
        'Wins': stats['WinsDuos']['value']
    }
def format_squads_data(stats):
    return {
        'Games': stats['GamesSquads']['value'],
        'Kills': stats['KillsSquads']['value'], 
        'MostKills': stats['MostKillsSquads']['value'],
        'Top': stats['Top2Squads']['value'],
        'Deaths': stats['DeathsSquads']['value'],
        'Wins': stats['WinsSquads']['value']
    }
client.run(str(os.getenv("TOKEN")))