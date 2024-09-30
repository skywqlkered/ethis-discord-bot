import os
import json
import discord
import shutil


async def download_attach(attach: discord.Attachment, model_name: str, state: bool):
    # state = True is a png
    # state = False is a json
    if state: 
        await attach.save(model_name + ".png")
        if attach.filename.endswith(".png"):
            if not move_texture(model_name):
                return False
            else:
                return True
    if not state:
        await attach.save(model_name + ".json")
        if attach.filename.endswith(".json"):
            if not move_model(model_name):
                return False
            else:
                return True

def get_path():
    dirname = os.path.dirname(__file__)
    dirname = dirname.split("functions")[0]

    return dirname

def move_texture(filename: str):
    dirname = get_path()
    src = os.path.join(dirname, filename + ".png")
    item_dir = os.path.join(
        dirname, "server_pack", "assets", "minecraft", "textures", "item"
    )

    destination_path = os.path.join(item_dir, filename + ".png")

    if not os.path.exists(destination_path):
        shutil.move(src, destination_path)
        return True
    else:
        return False

    


def move_model(model_name: str):
    dirname = get_path()
    src = os.path.join(dirname, model_name + ".json")
    item_dir = os.path.join(
        dirname, "server_pack", "assets", "minecraft", "models", "item"
    )

    destination_path = os.path.join(item_dir, model_name + ".json")

    if not os.path.exists(destination_path):
        shutil.move(src, destination_path)
        return True

    else:
        return False
    


def generate_model_json(parent, placeholder_model):
    data = {
        "parent": f"minecraft:item/{parent}",
        "textures": {"layer0": f"minecraft:item/{placeholder_model}"},
    }

    with open(placeholder_model + ".json", "w") as file:
        json.dump(data, file, indent=4)


# Example usage


def generate_item_json(parent, placeholder_texture, placeholder_model):
    data = {
        "parent": f"minecraft:item/{parent}",
        "textures": {"layer0": f"minecraft:item/{placeholder_texture}"},
        "overrides": [
            {
                "predicate": {"custom_model_data": 0},
                "model": f"minecraft:item/{placeholder_model}",
            }
        ],
    }
    with open(placeholder_texture + ".json", "w") as file:
        json.dump(data, file, indent=4)


# # Generate JSON structure
# json_output = generate_json(parent, placeholder_texture, placeholder_id, placeholder_model)
def create_new(parent, placeholder_texture, placeholder_model):
    generate_model_json(parent, placeholder_model)
    move_model(placeholder_model)
    generate_item_json(parent, placeholder_texture, placeholder_model)
    move_model(placeholder_texture)


def edit_existing_override(parent, placeholder_texture: str, placeholder_model):
    path = get_path()
    model_path = os.path.join(
        path,
        "server_pack",
        "assets",
        "minecraft",
        "models",
        "item",
        placeholder_texture,
    )

    with open(model_path + ".json", "r") as file:
        data = json.load(file)

    prev_id = int(data["overrides"][0]["predicate"]["custom_model_data"])
    new_id = prev_id + 1
    # create a new override
    new_override = {
        "predicate": {"custom_model_data": new_id},
        "model": f"minecraft:item/{placeholder_model}",
    }
    data["overrides"].append(new_override)

    with open(model_path + ".json", "w") as file:
        json.dump(data, file, indent=4)


def edit_or_create(parent, placeholder_texture, placeholder_model):
    # check if the model already exists in models/item
    path: str = get_path()
    model_path = os.path.join(
        path, "server_pack", "assets", "minecraft", "models", "item"
    )

    if os.path.exists(f"{model_path}/{placeholder_texture}.json"):
        edit_existing_override(
            parent=None,
            placeholder_texture=placeholder_texture,
            placeholder_model=placeholder_model,
        )
    else:
        create_new(parent, placeholder_texture, placeholder_model)

def create_new_override_with_john(parent, placeholder_texture, placeholder_model):
    move_model(placeholder_model)
    generate_item_json(parent, placeholder_texture, placeholder_model)
    move_model(placeholder_texture)