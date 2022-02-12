import discord
from discord.ext import commands
from commands import create_image_command, _caption, _echo, _tribute, _roll
from images import \
    squish, \
    brighten, \
    saturate, \
    deepfry
from files import check_for_attachments
from utils import log
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
bot.add_command(_tribute)
bot.add_command(_roll)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    log(f"{message.created_at} in #{message.channel} || {message.author} ({message.author.id}): {message.content}")
    if check_for_attachments(message):
        for attachment in message.attachments:
            log(
                "Attachment: ["
                f"\n\tFilename: {attachment.filename}"
                f"\n\tMedia Type: {attachment.content_type}"
                f"\n\tURL: {attachment.url}"
                "\n]"
            )
    await bot.process_commands(message)


print("Starting bot")
bot.run(token())
