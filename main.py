import discord
from discord.ext import commands
from commands import create_image_command, _caption, _echo
from imgutils import \
    squish, \
    brighten, \
    saturate, \
    deepfry
from secrets import token


bot = commands.Bot(command_prefix="::")

image_commands = [
    {
        "name": "brightness",
        "operation": brighten
    },
    {
        "name": "saturation",
        "operation": saturate
    },
    {
        "name": "deepfry",
        "operation": deepfry
    },
    {
        "name": "squish",
        "operation": squish
    }
]

for command in image_commands:
    bot.add_command(create_image_command(command["name"], command["operation"]))
bot.add_command(_caption)
bot.add_command(_echo)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    print(f"{message.author}: {message.content}")
    await bot.process_commands(message)


print("Starting bot")
bot.run(token())
