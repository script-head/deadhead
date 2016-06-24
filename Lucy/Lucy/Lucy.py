import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    await client.change_status(game=discord.Game(name = "Nyu!", url = "https://www.twitch.tv/directory", type = 1))

@client.event
async def on_message(message):
     if message.channel.is_private == True:
        if message.author.bot == True:
            return
        await client.send_message(message.channel, "Sorry I can't respond to private messages")
     if message.content.startswith("/say"):
        if message.content == "/say":
            await client.send_message(message.channel, "Pardon bitch? I need a message!")
        elif message.content == "/say":
            await client.send_message(message.channel, "Pardon bitch? I need a message!")
        else:
            await client.send_message(message.channel, message.content.replace("/say ", ""))
        await client.send_message(message.channel, msg)
     elif message.content.startswith("/info"):
        await client.send_message(message.channel, "```\nCreator: CreeperSeth\nVersion: 1.0```")
     elif message.content.startswith("/hangout"):
        await client.send_message(message.author, "Hangout invite link: discord.gg/014lbMgnygx1IoH6s")
     elif message.content.startswith("/invite"):
        await client.send_message(message.author, "Invite link: https://discordapp.com/oauth2/authorize?&client_id=185800598933733377&scope=bot&permissions=16886814s")

client.run("NoFuckYouMyToken:p")