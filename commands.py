import discord
from discord.ext import commands
import re
import numpy as np
from files import \
    save_image, \
    delete_images_after
from images import \
    execute_image_operation, \
    caption, \
    tribute
from utils import \
    log,\
    attempt_cast, \
    random_within_range
import errors
from errors import error


@commands.command(name="echo")
async def _echo(ctx, *args):
    try:
        await ctx.send(' '.join(args))
    except discord.errors.HTTPException:
        await ctx.send("echo!")


@commands.command(name="roll")
async def _roll(ctx, *args):
    if not args:
        return await ctx.send(random_within_range(1, 20))
    if attempt_cast(int, args[0]):
        n = int(args[0])
        if n >= 1:
            return await ctx.send(random_within_range(1, n))
        if n <= -1:
            return await ctx.send(random_within_range(-1, n))
        return await ctx.send(0)
    try:
        if re.match(r"^[0-9]{1,3}d[0-9]{1,8}$", args[0]):
            k, n = args[0].split('d')
            if k == 1:
                return await ctx.send(random_within_range(1, n))
            y = []
            for i in range(0, int(k)):
                y.append(random_within_range(1, int(n)))
            return await ctx.send(f"{y}: {np.sum(y)}")
    except discord.errors.HTTPException:
        return await ctx.send("Error: Too many parameters")
    if attempt_cast(float, args[0]):
        return await ctx.send("Sorry! Floating point numbers aren't supported!")
    return await ctx.send("Error: One or more invalid arguments")


@commands.command(name="caption")
@delete_images_after
async def _caption(ctx, *args):
    if not args:
        err = error(errors.NO_ARGUMENTS_ERROR)
        log(err)
        return await ctx.send(err)
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


@commands.command(name="tribute")
@delete_images_after
async def _tribute(ctx, *args):
    filepath = await save_image(ctx.message)
    if filepath is None:
        err = error(errors.NO_ATTACHMENT_ERROR)
        log(err)
        return await ctx.send(err)
    if execute_image_operation(filepath, tribute):
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
