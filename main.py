import os

import openai
import discord
from discord.ext import commands

openai.api_key = os.environ["OPEN_AI_KEY"]
discord_bot_key = os.environ["DISCORD_BOT_KEY"]

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


if __name__ == "__main__":
  try:
    bot.run(discord_bot_key)
  except:
    os.system("kill 1")
