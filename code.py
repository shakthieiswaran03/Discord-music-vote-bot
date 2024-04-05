import discord
import discord.ext
import re
import random
import time
from apiclient.discovery import build

global songs
songs = [[],[],[],[],[],[],[]]

def getyt(song):
    try:
        apikey = "" # insert Youtube API key
        youtube = build('youtube','v3',developerKey=apikey)
        request = youtube.search().list(q=song, part="snippet", type="video", maxResults=1, safeSearch="none")
        result = request.execute()
        url = "https://www.youtube.com/watch?v="+str(result["items"][0]['id']['videoId'])
        thumbnail = result["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        song = result["items"][0]["snippet"]["title"]
        return(url, song, thumbnail)
    except:
        print("[-] Youtube Error")

client = discord.Client()
@client.event
async def on_ready():
    try:
        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name='+b songname'))
        print('Logged in as {0.user}'.format(client))
    except:
        print("[-] Startup Error")

@client.event
async def on_message(message):
    try:
        if message.content.startswith('+b '):
            song = message.content[3:]
            url,song,thumbnail = getyt(song)
            embed = discord.Embed(title=song, description=(url+"\nRequested by "+str(message.author.mention).format(message)), color=0x8a003f)
            embed.set_thumbnail(url=thumbnail)
            embed.set_author(name="Is this a banger?", icon_url="https://i.imgur.com/m7NdXzj.png")
            post = await message.channel.send(embed=embed)
            await post.add_reaction("\U0001F525")
            await post.add_reaction("\U0001F5D1")
            songs[0].append(url)
            songs[1].append(song)
            songs[2].append(message.author)
            songs[3].append(1)
            songs[4].append(1)
            songs[5].append(post.id)
            songs[6].append(post)
            await message.delete()
        if message.content.startswith('+info'):
            embed = discord.Embed(title="Bot Info", description="This bot was made for voting on music. It will only work in #bangers and is hosted locally so it may not always be online.", color=0x8a003f)
            embed.add_field(name="+b songname", value="Command for adding a song to the voting pool.‎", inline=True)
            embed.set_image(url="https://i.imgur.com/m7NdXzj.png")
            await message.channel.send(embed=embed)
            await message.delete()
    except:
        print("[-] Message Error")

@client.event
async def on_raw_reaction_add(payload):
    try:
        message_id = payload.message_id
        user_id = payload.user_id
        if message_id in songs[5] and str(user_id) != "": # insert the bot's UID
            songs_id = songs[5].index(message_id)
            if payload.emoji.name == "🔥":
                songs[3][songs_id] += 1
            elif payload.emoji.name == "🗑":
                songs[4][songs_id] += 1
            if songs[3][songs_id] >= 4:
                print("banger :", str(songs[1][songs_id]).lower())
                await (songs[2][songs_id]).send("your suggestion "+songs[1][songs_id].lower()+" is officially a banger!")
                await (songs[6][songs_id]).delete()
                embed = discord.Embed(title=songs[1][songs_id], description=(songs[0][songs_id]+"\nRequested by "+str(songs[2][songs_id].mention)), color=0x8a003f)
                embed.set_author(name="Confirmed Banger", icon_url="https://i.imgur.com/eb22nnS.jpg")
                await songs[6][songs_id].channel.send(embed=embed)
            elif songs[4][songs_id] >= 4:
                await (songs[2][songs_id]).send("your suggestion "+songs[1][songs_id].lower()+" is not a banger!")
                await (songs[6][songs_id]).delete()
    except:
        print("[-] Add Reaction Error")

@client.event
async def on_raw_reaction_remove(payload):
    try:
        message_id = payload.message_id
        user_id = payload.user_id
        if message_id in songs[5] and str(user_id) != "": # insert the bot's UID
            songs_id = songs[5].index(message_id)
            if payload.emoji.name == "🔥":
                songs[3][songs_id] -= 1
            elif payload.emoji.name == "🗑":
                songs[4][songs_id] -= 1
    except:
        print("[-] Remove Reaction Error")

client.run('') # insert Discord token
