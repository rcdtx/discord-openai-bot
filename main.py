import configparser

import openai
import discord
from discord.ext import commands

config = configparser.ConfigParser()
config.read("credentials.ini")

# Set up the OpenAI API
openai.api_key = config["Credentials"]["openai_api_key"]
discord_bot_key = config["Credentials"]["discord_bot_key"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!gpt'):
        # Use the OpenAI API to generate a response to the message
        response = openai.Completion.create(engine="text-davinci-002",
                                            prompt=message.content[5:],
                                            max_tokens=1024,
                                            n=1,
                                            stop=["[STOP]"])

    try:
        await message.channel.send(response["choices"][0]["text"])
    except discord.errors.HTTPException:
        await message.channel.send(response["choices"][0]["text"][:1999])


bot.run(discord_bot_key)
