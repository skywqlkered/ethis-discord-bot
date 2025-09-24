import configparser
import discord
import discord.gateway
import requests


def request_option(config_option: str):
    config: configparser.ConfigParser = gather_configini()
    return config.get("CHANNEL", config_option)


def gather_configini():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def add_staff(id: int, role_name: str):
    if role_name.startswith("\"") and role_name.endswith("\""):
        role_name = role_name.removeprefix("\"").removesuffix("\"")
    if role_name.startswith("\'") and role_name.endswith("\'"):
        role_name = role_name.removeprefix("\'").removesuffix("\'")
    config = gather_configini()
    # add new adiiotns rather than replace
    config.read("config.ini")
    if config.get("CHANNEL", "staff_roles") == "":
        staff_str = str((id, role_name))
    else:
        staff_str = config.get("CHANNEL", "staff_roles") + \
            "," + str(id, role_name)
    config.set("CHANNEL", "staff_roles", staff_str)
    with open("config.ini", "w") as configfile:
        config.write(configfile)


def remove_staff(id: int, name: str):
    config = gather_configini()
    # add new adiiotns rather than replace
    config.read("config.ini")
    staff_str = config.get("CHANNEL", "staff_roles")
    rem_staff = staff_str.replace(str(id, name), "")
    if rem_staff.startswith("."):
        rem_staff = rem_staff[1:]
    if rem_staff.endswith("."):
        rem_staff = rem_staff[:-1]
    config.set("CHANNEL", "staff_roles", rem_staff)

    with open("config.ini", "w") as configfile:
        config.write(configfile)


def get_staff_roles() -> list[int, str]:
    config = gather_configini()
    roles = config.get("CHANNEL", "staff_roles")
    staff_list = []
    for i in roles.split("|"):
        x, y = i.split(",")
        staff_list.append((int(x), str(y)))
    return staff_list


def set_texture_category(category: discord.CategoryChannel):
    config = gather_configini()
    config.set("CHANNEL", "texture_category", str(category.id))
    with open("config.ini", "w") as configfile:
        config.write(configfile)


async def perm_check(userman: discord.User, message: discord.Message):
    if userman.id == message.guild.owner_id:
        return True
    for role in userman.roles:
        x = str(role.id)
        if x in get_staff_roles():
            return True
    return False


def get_online_players() -> list:
    data = requests.get(
        "https://api.mcsrvstat.us/3/66.59.209.46"
    )
    online = []
    # check if (data.json()["players"])["list"] exits
    if "list" not in (data.json()["players"]):
        return "No players online"

    player_list: dict = (data.json()["players"])["list"]
    for i in player_list:
        online.append(i["name"] + "\n")

    if len(online) == 0:
        return "No players online"

    names = "".join(online)

    return names
