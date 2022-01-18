import os
import re


def check_for_attachments(message):
    if message.attachments:
        return True
    return False


def is_image(file):
    if re.search(r"(\.jpg|\.jpeg|\.png)$", file.filename, flags=re.IGNORECASE):
        return True
    return False


def delete_images_after(f):
    async def wrapper(ctx, *args):
        g = await f(ctx, *args)
        if ctx.message.attachments:
            if os.path.exists(f"files/images/{ctx.message.attachments[0].filename}"):
                os.remove(f"files/images/{ctx.message.attachments[0].filename}")
        ref = ctx.message.reference
        if ref is not None and ref.resolved.attachments:
            if os.path.exists(f"files/images/{ref.resolved.attachments[0].filename}"):
                os.remove(f"files/images/{ref.resolved.attachments[0].filename}")
        return g
    return wrapper


async def save_image(message, depth=0):
    if check_for_attachments(message):
        img = message.attachments[0]
        if is_image(img):
            path = f"files/images/{img.filename}"
            await img.save(fp=path)
            return path
    if depth == 0:
        ref = message.reference
        if ref is not None:
            return await save_image(ref.resolved, depth=depth+1)
    return None



