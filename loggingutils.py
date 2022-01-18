

def log_command(f):
    async def wrapper(ctx, *args):
        return await f(ctx, *args)
    return wrapper
