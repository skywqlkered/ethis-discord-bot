import configparser
import discord


def request_option(config_option: str):
    config: configparser.ConfigParser = gather_configini()
    return config.get("CHANNEL", config_option)

def gather_configini():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

def set_suggest_channel(id: int):
    config: configparser.ConfigParser = gather_configini()
    config.set("CHANNEL", "suggestions_channel", str(id))
    with open("config.ini", "w") as configfile:
        config.write(configfile)

def set_staff_channel(id: int):
    config = gather_configini()
    config.set("CHANNEL", "staff_channel", str(id))
    with open("config.ini", "w") as configfile:
        config.write(configfile)

def add_staff(id: int):
    config = gather_configini()
    # add new adiiotns rather than replace
    config.read("config.ini")
    staff_str = config.get("CHANNEL", "staff_roles") + "," + str(id)
    config.set("CHANNEL", "staff_roles", staff_str)
    with open("config.ini", "w") as configfile:
        config.write(configfile)

def remove_staff(id: int):
    config = gather_configini()
    # add new adiiotns rather than replace
    config.read("config.ini")
    staff_str = config.get("CHANNEL", "staff_roles")
    rem_staff = staff_str.replace(str(id), "")
    if rem_staff.startswith(","):
        rem_staff = rem_staff[1:]
    if rem_staff.endswith(","):
        rem_staff = rem_staff[:-1]
    config.set("CHANNEL", "staff_roles", rem_staff)
    
    with open("config.ini", "w") as configfile:
        config.write(configfile)

async def perm_check(userman: discord.User, message: discord.Message):
    if userman.id == message.guild.owner_id:
        return True
    for role in userman.roles:
        x = str(role.id)
        if x in request_option("staff_roles").split(","):
            return True
    return False