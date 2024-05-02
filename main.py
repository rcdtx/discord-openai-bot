import os

from openai import OpenAI
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

bot = commands.Bot()

discord_bot_key = os.environ["DISCORD_BOT_KEY"]
client = OpenAI(api_key=os.environ["OPEN_AI_KEY"])


@bot.slash_command(description="Ping command")
async def ping(interaction: Interaction):
    await interaction.response.send_message("Pong!")


@bot.slash_command(description="Repeats your message")
async def gpt(interaction: Interaction, arg: str = SlashOption(description="Prompt")):
    # Use the OpenAI API to generate a response to the message
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": arg},
        ],
        max_tokens=200,
        n=1,
        stop=["[STOP]"],
    )

    await interaction.response.send_message(response.choices[0].message.content)


if __name__ == "__main__":
    bot.run(discord_bot_key)
