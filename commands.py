import discord
from discord.ext import commands
from files import \
    save_image, \
    delete_images_after
from images import \
    execute_image_operation, \
    caption
import errors
from errors import report_error


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
        return await ctx.send(report_error(errors.NO_ATTACHMENT_ERROR))
    if execute_image_operation(filepath, caption, ' '.join(args)):
        file = discord.File(filepath)
        return await ctx.send(file=file)
    return await ctx.send(report_error(errors.OPERATION_FAILED_ERROR))


def create_image_command(name, operation):

    @commands.command(name=name)
    @delete_images_after
    async def _operation(ctx, *args):
        filepath = await save_image(ctx.message)
        if filepath is None:
            return await ctx.send(report_error(errors.NO_ATTACHMENT_ERROR))
        if execute_image_operation(filepath, operation, args[0]):
            file = discord.File(filepath)
            return await ctx.send(file=file)
        return await ctx.send(report_error(errors.OPERATION_FAILED_ERROR))

    return _operation
