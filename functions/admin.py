import configparser
import discord

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
    print ("staff added")
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
    print ("staff removed")
    
    with open("config.ini", "w") as configfile:
        config.write(configfile)

async def check_if_owner(Message: discord.Message) -> bool:
    if Message.author.id == Message.guild.owner_id:

        return True

    else:  
        return False


async def check_if_staff(user: discord.user, message: discord.Message) -> bool:
    roles = (await message.guild.fetch_member(user.id)).roles
    config = gather_configini()
    staff_list = (config.get("CHANNEL", "staff_roles")).split(",")
    for role in roles:
        if str(role.id) in staff_list:
            return True

    return False

async def staff_checker(message):
    return await check_if_owner(message) or await check_if_staff(message.author, message)

