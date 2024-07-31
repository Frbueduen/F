import discord
import os
import json
from random import randint
from dotenv import load_dotenv
from discord.ext import commands
from move_functions import *
from pokemon_functions import *

load_dotenv()

Admins = [786083062172745770]

client = commands.Bot(command_prefix=('%'),
                      case_insensitive=True,
                      intents=discord.Intents.all())

normal_ID_list, mythical_ID_list, legendary_ID_list = initialize_wild_pool()

@client.event
async def on_ready():
    print('Flapple is online, Wild pokemon pool initialized.')

@client.command()
async def ping(ctx):
    await ctx.send(f'The current ping is {round(client.latency * 1000)}ms!')

@client.command(aliases= ["pd", "dex"])
async def pokedex(ctx,*, pokemon):
    
    if pokemon.isdigit():
        pokemon = int(pokemon)
        results = search_pokemon_by_id(pokemon)
        if not results:     
            await ctx.send(f"Pokemon #'{pokemon}' not found.")
            return

        id = results["id"]
        name = results["name"].capitalize().replace('-', ' ')
        type = ", ".join([t.capitalize() for t in results["types"]])
    
    else:
        pokemon = pokemon.lower().replace(' ', '-')
        results = search_pokemon_by_name(pokemon)
        if not results:     
            await ctx.send(f"Pokemon '{pokemon}' not found.")
            return

        id = results["id"]
        name = results["name"].capitalize().replace('-', ' ')
        type = ", ".join([t.capitalize() for t in results["types"]])
    
    sprite_url = results["sprites"]["front_default"]
    evolution_line = results["evolution_line"]
    next_evolution = get_next_evolution(evolution_line,results["name"]).capitalize()

    description = results["description"].replace("\n", " ").replace("POK\u00e9MON", "PokÃ©mon")

    colour = get_type_colour(type.split(","))


    PDembed = discord.Embed (title=f"{name} - Pokedex No. {id}",colour = colour)

    PDembed.set_thumbnail(url=sprite_url)
    PDembed.add_field(name = "Type", value = type, inline=False)
    PDembed.add_field(name = "Evolves into", value = f"{next_evolution}",inline=False)
    PDembed.add_field(name = "Description", value = description, inline=False)
    PDembed.set_footer(text=f"Pokedex Entry retrieval by {ctx.author}")
    await ctx.send(embed=PDembed)
        

@client.command(aliases= ["mv"])
async def move(ctx, *,move_name):
    move = move_name.lower().replace(' ', '-')
    results = search_move_by_name(move)
    if not results:     
        await ctx.send(f"Move '{move}' not found.")
        return

    id = results["id"]
    name = results["name"].capitalize().replace('-', ' ')
    type = results["type"].capitalize()
    pp = results["pp"]
    power = results["power"]
    accuracy = results["accuracy"]
    effect = results["effect"]
    short_effect = results["short_effect"]

    MVembed = discord.Embed (title=f"{name} - Move ID {id}",colour = 0xffffff)
    MVembed.add_field(name = "Type", value = type, inline=True)
    MVembed.add_field(name = "Power", value = power, inline=True)
    MVembed.add_field(name = "PP", value = pp, inline=True)
    MVembed.add_field(name = "Accuracy", value = accuracy, inline=True)
    MVembed.add_field(name = "Effect", value = effect, inline=False)
    MVembed.add_field(name = "Short Effect", value = short_effect, inline=False)
    MVembed.set_footer(text=f"Move Entry retrieval by {ctx.author}")
    await ctx.send(embed=MVembed)


@client.command(aliases = ["s"])
@commands.cooldown (1,7, commands.BucketType.user)
async def search(ctx):
    results, shiny = choose_random_wild(normal_ID_list, mythical_ID_list, legendary_ID_list)

    type = ", ".join([t.capitalize() for t in results["types"]])
    colour = get_type_colour(type.split(','))
    name = results["name"].capitalize().replace('-', ' ')
    if not shiny:
        sprite_url = results["sprites"]["front_default"]
    else:
        sprite_url = results["sprites"]["front_shiny"]
        name = f"Shiny {name}"
        colour = 0x000000
    
    with open("Inventory.json", "r") as file:
        data = json.load(file)
        if str(ctx.author.id) not in data["users"]:
            await ctx.send("You have not begun your adventure! Start by using the `%start` command.")
            return
    pb = data["users"][str(ctx.author.id)]["Pokeballs"]
    gb = data["users"][str(ctx.author.id)]["Greatballs"]
    ub = data["users"][str(ctx.author.id)]["Ultraballs"]
    mb = data["users"][str(ctx.author.id)]["Masterballs"]
    
    SHembed = discord.Embed (title=f"{ctx.author.name} found {name}!",colour = colour)
    SHembed.add_field(name="Select a ball to use", value=f"Number of Pokeballs:{pb}\nNumber of Greatballs:{gb}\nNumber of Ultraballs:{ub}\nNumber of Masterballs:{mb}")
    SHembed.set_footer(text=f"Enter 'pb' or 'gb' to use a ball")
    SHembed.set_image(url=sprite_url)
    await ctx.send(embed=SHembed)
    
    code, catch_result, catch, rate = await search_cmd_handler(client, ctx, name) #can consider removing catch and rate, only there for testing purposes
            
    if code == 0:
        print("timed out")
    elif catch_result:
        await ctx.send(f"{name} was caught!\nCatch roll was {rate} and you needed only {catch} to catch")
    else:
        await ctx.send(f"{name} escaped... It rolled a {catch} but you only had {rate}")

@client.command()
async def start(ctx):
    with open('Inventory.json', 'r+') as file:
        data = json.load(file)
        if str(ctx.author.id) not in data["users"]:
            data["users"][str(ctx.author.id)] = {}
            data["users"][str(ctx.author.id)]["Pokeballs"] = 20
            data["users"][str(ctx.author.id)]["Greatballs"] = 0
            data["users"][str(ctx.author.id)]["Ultraballs"] = 0
            data["users"][str(ctx.author.id)]["Masterballs"] = 0
            file.seek(0)
            json.dump(data, file, indent = 1)
            await ctx.send(f"Your adventure has just begun. Trainer {ctx.author.name} has received 20 Pokeballs. Try `%s` to find a wild pokemon!")
        else:
            await ctx.send("You have already begun your adventure! Start searching for wild pokemon using `%s`")
        


@search.error
async def search(ctx,error):
  if isinstance(error, commands.CommandOnCooldown):
    retry_secs = error.retry_after
    await ctx.send (f"Please retry in {str(round(retry_secs))} seconds.")
  else:
    raise error
        

client.run(os.getenv('API_Key'))