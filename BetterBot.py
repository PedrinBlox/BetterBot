# BetterBot made by pe.drin#0
# If you want to give suggestions for BetterBot or got errors, DM me it.
# v3.0.1

#### Config ####

token = "" # Your bot token (required)
prefix = ">" # Your bot's prefix (required)
owner_ids = [""] # The discord account ID for the owners (required for special commands)

# Command Shortcuts
restart_shortcut = ["re"] # this is the shortcut for the restart command, instead of typing ">restart" you just type ">re"
screenshot_shortcut = ["ss"] # this is the shortcut for the screenshot command, instead of typing ">screenshot" you just type ">ss"
run_shortcut = ["r"] # this is the shortcut for the run command, instead of typing ">run" you just type ">r"
kill_shortcut = ["k"] # this is the shortcut for the kill command, instead of typing ">kill" you just type ">k"
details_shortcut = ["d"] # this is the shortcut for the details command, instead of typing ">details" you just type ">d"
autorestart_shortcut = ["aure"] # this is the shortcut for the autorestart command, instead of typing ">autorestart" you just type ">aure"
add_shortcut = ["ad"] # this is the shortcut for the add command, instead of typing ">add" you just type ">add", the command is already short lol
remove_shortcut = ["rem"] # this is the shortcut for the remove command, instead of typing ">remove" you just type ">rem"
checkversion_shortcut = ["cver"] # this is the shortcut for the checkversion command, instead of typing ">checkversion" you just type ">cver"
items_shortcut = ["ite"] # this is the shortcut for the items command, instead of typing ">items" you just type ">ite"
addowner_shortcut = ["addo"] # this is the shortcut for the addowner command, instead of typing ">addowner" you just type ">addo"
cleanids_shortcut = ["cids"] # this is the shortcut for the cleanids command, instead of typing ">cleanids" you just type ">cids"
autosearch_shortcut = ["auto"] # this is the shortcut for the autosearch command, instead of typing ">autosearch" you just type ">auto"

# thanks to floppa6031#0 for the shortcuts

################

try:
    import os
    import asyncio
    import time
    from pystyle import Colorate, Colors, Center
    import discord
    from discord.ext import commands
    import subprocess
    import json 
    import aiohttp
    import requests
    import asyncio
except ModuleNotFoundError:
    a = input(str('Not installed modules detected. Do you want to install them? (y/n) '))
    if a.lower() == 'y':
        os.system('pip install pystyle')
        os.system('pip install discord.py')
        os.system('pip install aiohttp')
        os.system('pip install pillow')

os.system('title BetterBot')
os.system('cls' if os.name == 'nt' else 'clear')

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

version = "3.0.1"
title = f"""
                                                                                                          v{version}
                 /$$$$$$$              /$$     /$$                         /$$$$$$$              /$$    
                | $$__  $$            | $$    | $$                        | $$__  $$            | $$    
                | $$  \ $$  /$$$$$$  /$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$ | $$  \ $$  /$$$$$$  /$$$$$$  
                | $$$$$$$  /$$__  $$|_  $$_/|_  $$_/   /$$__  $$ /$$__  $$| $$$$$$$  /$$__  $$|_  $$_/  
                | $$__  $$| $$$$$$$$  | $$    | $$    | $$$$$$$$| $$  \__/| $$__  $$| $$  \ $$  | $$    
                | $$  \ $$| $$_____/  | $$ /$$| $$ /$$| $$_____/| $$      | $$  \ $$| $$  | $$  | $$ /$$
                | $$$$$$$/|  $$$$$$$  |  $$$$/|  $$$$/|  $$$$$$$| $$      | $$$$$$$/|  $$$$$$/  |  $$$$/
                |_______/  \_______/   \___/   \___/   \_______/|__/      |_______/  \______/    \___/  
                                                                                                        
                                                                                                        

"""

print(Colorate.Vertical(Colors.cyan_to_blue, title))

response = requests.get("https://raw.githubusercontent.com/PedrinBlox/BetterBot/main/version")
if response.status_code != 200:
    pass
if not response.text.rstrip() == version:
    print(f"BETTERBOT HAS A NEW VERSION ({response.text.rstrip()}). PLEASE UPDATE YOUR FILE.")
    print("REPOSITORY FOR BETTERBOT: https://github.com/PedrinBlox/BetterBot")
    print(f"IF YOU PREFER THIS VERSION, IT WILL CONTINUE IN 10 SECONDS.")
    time.sleep(10)

title_printed = False
with open('config.json', 'r') as file:
    config = json.load(file)
    search_cookie = config["cookies"]["search_cookie"]

####### Functions #######
async def print_title(interval):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        buffer = Colorate.Vertical(Colors.cyan_to_blue, title)
        print(buffer, end='', flush=True)
        await asyncio.sleep(interval)
        time.sleep(0.2)

async def create_screenshot():
    from io import BytesIO
    from PIL import ImageGrab

    screenshot = ImageGrab.grab()
    img_bytes = BytesIO()
    screenshot.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    embed = discord.Embed(color=0x1e5dff)
    file = discord.File(img_bytes, filename='ss.png')
    embed.set_image(url='attachment://ss.png')

    return file, embed

async def isowner(id):
    if str(id) in owner_ids:
        return True
    else:
        return False
    
def get_thumbnail(item_id) -> str:
    res = requests.get(
        f'https://thumbnails.roproxy.com/v1/assets?assetIds={item_id}&size=420x420&format=Png'
    ).json()
    return res['data'][0]['imageUrl']

async def get_x_token():
    while True:
        try:
            async with aiohttp.ClientSession(cookies={".ROBLOSECURITY": search_cookie}) as client:
                response = await client.post("https://accountsettings.roblox.com/v1/email", ssl=False)
                xcsrf_token = response.headers.get("x-csrf-token")
                if xcsrf_token is None:
                    raise Exception("An error occurred while getting the X-CSRF-TOKEN. Could be due to an invalid Roblox Cookie")
                return xcsrf_token
        except aiohttp.ClientConnectorError as e:
            print(f"Connection error: {e}")
            await asyncio.sleep(5)

async def get_details(item_id_for_details):
    while True:
        try:
            url = f"https://catalog.roproxy.com/v1/catalog/items/{item_id_for_details}/details?itemType=Asset"
            xcsrf_token = await get_x_token()
            headers = {"x-csrf-token": xcsrf_token, 'Accept': "application/json"}
            cookies = {".ROBLOSECURITY": search_cookie}

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, cookies=cookies, ssl=False) as response:
                    data = await response.json()
                    return data
        except aiohttp.ClientConnectorError as e:
            print(f"Connection error: {e}")
            await asyncio.sleep(5)
##########################

@bot.event
async def on_ready():
    asyncio.create_task(print_title(0.1))

@bot.command()
async def ping(ctx):
    await ctx.reply(f"Pong! {bot.latency}ms")

@bot.command(aliases=screenshot_shortcut)
async def screenshot(ctx):
    if await isowner(ctx.author.id):
        try:
            file, embed = await create_screenshot()
        except ImportError:
            await ctx.reply(":x: Failed to create the screenshot. Check if u have the library Pillow installed.")
            return
        try:
            await ctx.reply(file=file, embed=embed)
        except Exception as e:
            await ctx.reply(f":x: | Failed to send the screenshot. Error {e}")

@bot.command(aliases=restart_shortcut)
async def restart(ctx):
    if await isowner(ctx.author.id):
        try:
            current_pid = os.getpid()
            processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
            programs_to_kill = ['python.exe', 'cmd.exe']

            for process in processes:
                for program in programs_to_kill:
                    if program in process:
                        pid = int(process.split()[1])
                        if pid != current_pid:
                            os.system(f'taskkill /PID {pid} /F')
            os.system(f"start /B start cmd.exe @cmd /k python main.py")
            time.sleep(.5)
            await ctx.reply(":white_check_mark: | Succesfully restarted xolo sniper!")
        except Exception as e:
            await ctx.reply(f":x: | An error occured while trying to restart xolo sniper! Error: {e}")

@bot.command(aliases=run_shortcut)
async def run(ctx):
    if await isowner(ctx.author.id):
        try:
            os.system(f"start /B start cmd.exe @cmd /k python main.py")
            time.sleep(.5)
            await ctx.reply(":white_check_mark: | Succesfully started xolo sniper!")
        except Exception as e:
            time.sleep(.5)
            await ctx.reply(f":x: | An error occured while trying to start xolo sniper! Error: {e}")

@bot.command(aliases=kill_shortcut)
async def kill(ctx):
    if await isowner(ctx.author.id):
        try:
            current_pid = os.getpid()
            processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
            programs_to_kill = ['python.exe', 'cmd.exe']

            for process in processes:
                for program in programs_to_kill:
                    if program in process:
                        pid = int(process.split()[1])
                        if pid != current_pid:
                            os.system(f'taskkill /PID {pid} /F')
            time.sleep(.5)
            await ctx.reply(":white_check_mark: | Succesfully closed xolo sniper!")
        except Exception as e:
            time.sleep(.5)
            await ctx.reply(f":x: | An error occured while trying to close xolo sniper! Error: {e}")

@bot.command(aliases=add_shortcut)
async def add(ctx, id=None):
    if await isowner(ctx.author.id):
        if id is None:
            await ctx.reply(f":x: | You need to specify an ID! Usage: {prefix}add <ID>")
            return

        try:
            id = int(id)
        except ValueError:
            await ctx.reply(f":x: | The ID must be a number! Usage: {prefix}add <ID>")
            return

        with open('config.json', 'r+') as file: 
            config = json.load(file)
            if id in config['items']:
                await ctx.reply(f":x: | ID {id} is already in the list!")
            else:
                config['items'].append(id)
                file.seek(0)
                json.dump(config, file, indent=4)
                file.truncate()

                time.sleep(.5)

                await ctx.reply(f":white_check_mark: | ID {id} added successfully!")

                current_pid = os.getpid()
                processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
                programs_to_kill = ['python.exe', 'cmd.exe']

                for process in processes:
                    for program in programs_to_kill:
                        if program in process:
                            pid = int(process.split()[1])
                            if pid != current_pid:
                                os.system(f'taskkill /PID {pid} /F')

                time.sleep(.5)
                os.system(f"start /B start cmd.exe @cmd /k python main.py")

@bot.command(aliases=remove_shortcut)
async def remove(ctx, id=None):
    if await isowner(ctx.author.id):
        if id is None:
            await ctx.reply(f":x: | You need to specify an ID! Usage: {prefix}remove <ID>")
            return

        try:
            id = int(id)
        except ValueError:
            await ctx.reply(f":x: | The ID must be a number! Usage: {prefix}remove <ID>")
            return

        with open('config.json', 'r+') as file: 
            config = json.load(file)
            if id in config['items']:
                config['items'].remove(id)
                file.seek(0)
                json.dump(config, file, indent=4)
                file.truncate()

                time.sleep(.5)

                await ctx.reply(f":white_check_mark: | ID {id} removed successfully!")

                current_pid = os.getpid()
                processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
                programs_to_kill = ['python.exe', 'cmd.exe']

                for process in processes:
                    for program in programs_to_kill:
                        if program in process:
                            pid = int(process.split()[1])
                            if pid != current_pid:
                                os.system(f'taskkill /PID {pid} /F')

                time.sleep(.5)
                os.system(f"start /B start cmd.exe @cmd /k python main.py")
            else:
                await ctx.reply(f":x: | ID {id} is not in the list!")

@bot.command(aliases=items_shortcut)
async def items(ctx):
    if await isowner(ctx.author.id):
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                items = config['items']

                embed = discord.Embed(
                    title="Item List",
                    color=0x1e5dff
                )

                for id in items:
                    details = await get_details(id)
                    name = details.get("name", "None")

                    embed.add_field(name="", value=f"``{id} - {name}``", inline=False)

                await ctx.reply(embed=embed)
        except Exception as e:
            await ctx.reply(f":x: An error occurred while trying to get the items. Try restarting BetterBot. Error: {e}")

@bot.command(aliases=cleanids_shortcut)
async def cleanids(ctx):
    if await isowner(ctx.author.id):
        try:
            with open('config.json', 'r+') as file:

                config = json.load(file)
                config['items'] = []
                file.seek(0)

                json.dump(config, file, indent=4)
                file.truncate()

                time.sleep(.5)

            await ctx.reply(":white_check_mark: All IDs have been removed successfully!")

            current_pid = os.getpid()
            processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
            programs_to_kill = ['python.exe', 'cmd.exe']

            for process in processes:
                for program in programs_to_kill:
                    if program in process:
                        pid = int(process.split()[1])
                        if pid != current_pid:
                            os.system(f'taskkill /PID {pid} /F')

            time.sleep(.5)
            os.system(f"start /B start cmd.exe @cmd /k python main.py")
        except Exception as e:
            await ctx.reply(f":x: An error occurred while trying to clean the IDs. Try restarting BetterBot. Error: {e}")

@bot.command(aliases=autosearch_shortcut)
async def autosearch(ctx, toggle=None):
    if await isowner(ctx.author.id):
        try:
            if toggle == None:
                await ctx.reply(f":x: Missing argument 'toggle'. Usage: {prefix}autosearch ``on/off``")
                return

            with open('config.json', 'r+') as file:

                config = json.load(file)

                if toggle.lower() == "on":
                    config['autosearch'] = True
                elif toggle.lower() == "off":
                    config['autosearch'] = False
                else:
                    await ctx.reply(f":x: Invalid argument 'toggle'. Usage: {prefix}autosearch ``on/off``")
                    return
                
                file.seek(0)
                json.dump(config, file, indent=4)
                file.truncate()

                time.sleep(.5)

            await ctx.reply(f":white_check_mark: Autosearch set to {toggle} succesfully!")

            current_pid = os.getpid()
            processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
            programs_to_kill = ['python.exe', 'cmd.exe']

            for process in processes:
                for program in programs_to_kill:
                    if program in process:
                        pid = int(process.split()[1])
                        if pid != current_pid:
                            os.system(f'taskkill /PID {pid} /F')

            time.sleep(.5)
            os.system(f"start /B start cmd.exe @cmd /k python main.py")
        except Exception as e:
            await ctx.reply(f":x: An error occurred while trying to change autosearch value. Try restarting BetterBot. Error: {e}")

@bot.command(aliases=details_shortcut)
async def details(ctx, id=None):
    if id is None:
        await ctx.reply(f':x: | You need to put an item id! Example: {prefix}details 12345')
        return
    
    details = await get_details(id)

    name = details.get("name")
    creator_name = details.get("creatorName")
    creator_id = details.get("creatorTargetId")
    price_status = details.get("priceStatus")
    description = details.get("description")
    #owned = details.get("owned")

    ingame = details.get("saleLocationType") == "ExperiencesDevApiOnly"

    price = details.get("price", "None")
    stock = details.get("totalQuantity")
    units_available = details.get("unitsAvailableForConsumption")
    lowest_resale_price = details.get("lowestResalePrice")
    quantity_limit_per_user = details.get("quantityLimitPerUser")

    thumbnail = get_thumbnail(id)

    details_embed = discord.Embed(
        title=f"Details | {id}",
        url=f"https://www.roblox.com/catalog/{id}/BetterBot",
        color=0x1e5dff
    )
    details_embed.set_thumbnail(url=thumbnail)
    details_embed.add_field(name="Name", value=name, inline=False)
    details_embed.add_field(name="Creator", value=f"{creator_name} | {creator_id}", inline=False)
    details_embed.add_field(name="Price", value=price, inline=False)
    details_embed.add_field(name="Price Status", value=price_status, inline=False)
    if units_available is not None and stock is not None:
        details_embed.add_field(name="Stock", value=f"{units_available}/{stock}", inline=False)
    details_embed.add_field(name="Description", value=f"```{description}```", inline=False)
    details_embed.add_field(name="In-game", value=ingame, inline=False)
    details_embed.add_field(name="Lowest Resale Price", value=lowest_resale_price, inline=False)
    details_embed.add_field(name="Max Buys Per User", value=quantity_limit_per_user, inline=False)

    await ctx.reply(embed=details_embed)

@bot.command(aliases=checkversion_shortcut)
async def checkversion(ctx):
    try:
        response = requests.get("https://raw.githubusercontent.com/PedrinBlox/BetterBot/main/version")
        if response.status_code != 200:
            pass
        if not response.text.rstrip() == version:
            await ctx.reply(f":x: | Your current BetterBot version is outdated! Current version: {version}, New version: {response.text.rstrip()}")
        elif response.text.rstrip() == version:
            await ctx.reply(f":white_check_mark: | Your current BetterBot version is up to date! Current version: {version}")
    except Exception as e:
        await ctx.reply(f':x: | An error occured: {e}')

auto_restart_task = None
auto_restart_status = "off"
auto_restart_interval = 15

async def auto_restart_bot():
    global auto_restart_status
    while True:
        await asyncio.sleep(auto_restart_interval * 60)
        if auto_restart_status == "on":
            current_pid = os.getpid()
            processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
            programs_to_kill = ['python.exe', 'cmd.exe']

            for process in processes:
                for program in programs_to_kill:
                    if program in process:
                        pid = int(process.split()[1])
                        if pid != current_pid:
                            os.system(f'taskkill /PID {pid} /F')

            time.sleep(.5)
            os.system(f"start /B start cmd.exe @cmd /k python main.py")
            
@bot.command(aliases=autorestart_shortcut)
async def autorestart(ctx, command=None, minutes=None):
    if await isowner(ctx.author.id):
        global auto_restart_task, auto_restart_status, auto_restart_interval

        if command is None:
            await ctx.reply(f":x: | Missing argument 'command'. Usage: {prefix}autorestart <on/off/info/interval> [minutes]")
            return
        
        if command == "on":
            auto_restart_status = "on"
            if auto_restart_task is not None:
                auto_restart_task.cancel()
            auto_restart_task = asyncio.create_task(auto_restart_bot())
            await ctx.reply(":white_check_mark: | Auto restart enabled!")

        elif command == "off":
            auto_restart_status = "off"
            if auto_restart_task is not None:
                auto_restart_task.cancel()
            await ctx.reply(":white_check_mark: | Auto restart disabled!")

        elif command == "info":
            await ctx.reply(f"Auto restart status: {auto_restart_status}\nInterval between restarts: {auto_restart_interval} minutes")

        elif command == "interval":
            if minutes is None:
                await ctx.reply(f":x: | Missing argument 'minutes'. Usage: {prefix}autorestart interval <minutes>")
                return
            try:
                auto_restart_interval = int(minutes)
                await ctx.reply(f":white_check_mark: | Auto restart interval set to {auto_restart_interval} minutes!")
            except ValueError:
                await ctx.reply(f":x: | The interval must be a number! Usage: {prefix}autorestart interval <minutes>")
                return

        else:
            await ctx.reply(f":x: | Invalid argument 'command'. Usage: {prefix}autorestart <on/off/info/interval> [minutes]")

@bot.command(aliases=addowner_shortcut)
async def addowner(ctx, new_id: str): # freaque.#0
    if await isowner(ctx.author.id):
        try:
            with open('BetterBot.py', 'r') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                if line.strip().startswith('owner_ids ='):
                    start = line.find('["')
                    end = line.find('"]')
                    current_ids = line[start+2:end].split('", "')
                    if new_id not in current_ids:
                        current_ids.append(new_id)
                    lines[i] = 'owner_ids = ["' + '", "'.join(current_ids) + '"] # The discord account ID for the owners (required for special commands)\n'
                    break

            with open('BetterBot.py', 'w') as f:
                f.writelines(lines)
                
            await ctx.reply(f':white_check_mark: | Successfully added owner ID {new_id} (restart betterbot to work)')
        except Exception as e:
            await ctx.reply(f":x: | An error occured: {e}")

bot.run(token=token)
