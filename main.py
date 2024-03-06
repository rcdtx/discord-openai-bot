import os

from openai import OpenAI

import discord
from discord.ext import commands

discord_bot_key = os.environ["DISCORD_BOT_KEY"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)

client = OpenAI(api_key=os.environ["OPEN_AI_KEY"])


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!gpt"):
        # Use the OpenAI API to generate a response to the message
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.content[5:]},
            ],
            max_tokens=200,
            n=1,
            stop=["[STOP]"],
        )

        try:
            # await message.channel.send(response.choices[0].text)
            await message.channel.send(response.choices[0].message.content)
        except discord.errors.HTTPException:
            await message.channel.send(response.choices[0])


if __name__ == "__main__":
    try:
        bot.run(discord_bot_key)
    except:
        os.system("kill 1")
