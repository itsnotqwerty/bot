import discord
from discord.ext import commands
from files import \
    save_image, \
    delete_images_after
from images import \
    execute_image_operation, \
    caption
from utils import log
import errors
from errors import error


@commands.command(name="echo")
async def _echo(ctx, *args):
    try:
        await ctx.send(' '.join(args))
    except discord.errors.HTTPException:
        await ctx.send("echo!")


@commands.command(name="caption")
@delete_images_after
async def _caption(ctx, *args):
    filepath = await save_image(ctx.message)
    if filepath is None:
        err = error(errors.NO_ATTACHMENT_ERROR)
        log(err)
        return await ctx.send(err)
    if execute_image_operation(filepath, caption, ' '.join(args)):
        file = discord.File(filepath)
        return await ctx.send(file=file)
    err = error(errors.OPERATION_FAILED_ERROR)
    log(err)
    return await ctx.send(err)


def create_image_command(name, operation):

    @commands.command(name=name)
    @delete_images_after
    async def _operation(ctx, *args):
        if not args:
            err = error(errors.NO_ARGUMENTS_ERROR)
            log(err)
            return await ctx.send(err)
        filepath = await save_image(ctx.message)
        if filepath is None:
            err = error(errors.NO_ATTACHMENT_ERROR)
            log(err)
            return await ctx.send(err)
        if execute_image_operation(filepath, operation, args[0]):
            file = discord.File(filepath)
            return await ctx.send(file=file)
        err = error(errors.OPERATION_FAILED_ERROR)
        log(err)
        return await ctx.send(err)

    return _operation
