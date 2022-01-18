from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from utils import i_floor, attempt_cast


def execute_image_operation(filepath, operation, *args):
    print("Executing image operation...")
    img = Image.open(filepath)
    img = img.convert("RGB")
    img = operation(img, *args)
    if img is None:
        return False
    img.save(filepath)
    img.close()
    return True


def rescale(img, scale):
    return img.resize(
        (
            i_floor(img.width * scale[0]),
            i_floor(img.height * scale[1])
        ),
        resample=Image.BILINEAR
    )


def brighten(img, brightness):
    if attempt_cast(float, brightness):
        brightness = float(brightness)
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(brightness)
    return None


def saturate(img, saturation):
    if attempt_cast(float, saturation):
        saturation = float(saturation)
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(saturation)
    return None


def deepfry(img, crispiness):
    if attempt_cast(float, crispiness):
        crispiness = float(crispiness)
        img = brighten(img, crispiness * 0.6)
        img = saturate(img, crispiness * 2.0)
        return img
    return None


def squish(img, squish_factor):
    img = img.convert("RGB")
    if attempt_cast(float, squish_factor):
        squish_factor = float(squish_factor)
        if squish_factor > 0:
            img = rescale(img, (1, 1 / squish_factor))
        if squish_factor < 0:
            img = rescale(img, (abs(1 / squish_factor), 1))
        return img
    return None


def text_fill(text, size, font_path=f"files/fonts/Roboto.ttf"):
    caption_height = i_floor(size[1] / 4)
    text_margin = (size[0] / 6, caption_height / 4)
    font_size = 1
    fnt = ImageFont.truetype(font_path, font_size)
    # Increment font size until it would otherwise overflow its boundaries
    while fnt.getsize(text)[1] < (size[1] - text_margin[1]) and fnt.getsize(text)[0] < (size[0] - text_margin[0]):
        font_size += 1
        fnt = ImageFont.truetype(font_path, font_size)
    return font_size


def caption(img, text):
    # Cast attached image to RGBA
    img = img.convert("RGBA")
    # Initialize a blank base template and define caption boundaries
    caption_size = (img.width, i_floor(img.height / 4))
    base = Image.new(
        "RGB",
        (img.width, 5 * caption_size[1]),
        (255, 255, 255)
    )
    # Fit caption to boundaries
    font_path = f"files/fonts/Roboto.ttf"
    font_size = text_fill(text, caption_size)
    fnt = ImageFont.truetype(font_path, font_size)
    # Start drawing on base
    d = ImageDraw.Draw(base)
    # Set variables
    fill = (0, 0, 0)
    # Paste caption
    d.text(
        (
            # Center text inside caption boundaries
            i_floor((img.width - d.textsize(text, font=fnt)[0]) / 2),
            i_floor((caption_size[1] - d.textsize(text, font=fnt)[1]) / 2)
        ),
        text,
        font=fnt,
        fill=fill
    )
    # Paste original image onto base
    base.paste(img, (0, i_floor(img.height / 4)))
    return base
