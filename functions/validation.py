import discord
from PIL import Image
import requests
from io import BytesIO


async def get_content(message: discord.Message) -> tuple[str, str]:
    content = message.content
    split_content = content.split(", ")
    if len(split_content) != 2:
        await message.channel.send(
            "Please include your item like this: **item_name, model_name**"
        )
        return

    if len(split_content) == 2:
        return split_content


def gather_mc_items() -> list[str]:
    file = open("list_of_items.txt", "r")
    mc_items = file.read()
    file.close()
    return list(mc_items.split(", "))


def get_pngs(message: discord.Message) -> discord.Attachment:
    pngs: list = []
    for attach in message.attachments:
        if attach.filename.endswith(".png"):
            pngs.append(attach)

    return pngs


def get_jsons(message: discord.Message) -> list[discord.Attachment]:
    jsons: list = []
    for attach in message.attachments:
        if attach.filename.endswith(".json"):
            jsons.append(attach)

    return jsons


async def validate_suggestion(message: discord.Message) -> bool:
    if len(message.attachments) == 0:
        await message.channel.send("Please attach an image")
        return False

    # Correctly await the coroutine and then perform the operation
    content = await get_content(message)  # Await the coroutine to get the result
    if content is None:  # Check if the result is not None
        return False

    if content is not None:  # Check if the result is not None
        if (
            content[0] not in gather_mc_items()
        ):  # Now you can safely subscript the content
            await message.channel.send(
                "Please include an item in this format: **item_name, model_name**"
            )
            return False

    pngs = get_pngs(message)
    jsons = get_jsons(message)

    if len(pngs) != 1:
        await message.channel.send("Please only attach one image")
        return False

    if len(jsons) > 1:
        await message.channel.send("Please only attach one json")
        return False

    attachment = pngs[0]

    try:
        response = requests.get(attachment.url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        width, height = image.size

        if width != height:
            await message.channel.send("The image is not square.")
            return False

        if not (width & (width - 1) == 0) and width != 0:
            await message.channel.send("The image dimensions are not powers of two.")
            return False

        if image.mode != "RGBA" and image.mode != "RGB":
            await message.channel.send(
                "The image does not have a valid color mode (RGB or RGBA)."
            )
            return False

    except Exception as e:
        await message.channel.send(f"An error occurred while processing the image: {e}")
        return False

    else:
        return True
