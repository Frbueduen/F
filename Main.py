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

@client.command()
async def start(ctx):
    await ctx.send("Start Command")

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
    pb = data["users"][str(ctx.author.id)]["Pokeballs"]
    gb = data["users"][str(ctx.author.id)]["Greatballs"]
    
    SHembed = discord.Embed (title=f"{name}",colour = colour)
    SHembed.add_field(name="Select a ball to use", value=f"Number of Pokeballs:{pb}\nNumber of Greatballs:{gb}")
    SHembed.set_footer(text=f"Pokedex Entry retrieval by {ctx.author}")
    SHembed.set_image(url=sprite_url)
    await ctx.send(embed=SHembed)

    while True:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content
        msg = await client.wait_for("message", check=check, timeout=60.0)

        if msg.content.lower() not in ["pokeball", "pb", "greatball" , "gb"]:
            await ctx.send("IDK what ball that is...")
            break 

        elif msg.content.lower() in ["pokeball", "pb"]:
            with open("inventory.json", "r") as file2:
                data2 = json.load(file2)
                pokeballs = data2["users"][str(ctx.author.id)]["Pokeballs"]
                greatballs = data2["users"][str(ctx.author.id)]["Greatballs"]
            data2["users"][str(ctx.author.id)] = {}
            data2["users"][str(ctx.author.id)]["Pokeballs"] = pokeballs - 1
            data2["users"][str(ctx.author.id)]["Greatballs"] = greatballs
            with open("inventory.json", "w") as file3:
                json.dump(data2, file3, indent = 1)

            with open("pokeballs.json","r") as balls:
                ball = json.load(balls)
            rate = ball["pokeballs_normal"]["Pokeball"]
            break

        elif msg.content.lower() in ["greatball", "gb"]:
            with open("inventory.json", "r") as file2:
                data2 = json.load(file2)
                pokeballs = data2["users"][str(ctx.author.id)]["Pokeballs"] 
                greatballs = data2["users"][str(ctx.author.id)]["Greatballs"]
            data2["users"][str(ctx.author.id)] = {}
            data2["users"][str(ctx.author.id)]["Pokeballs"] = pokeballs
            data2["users"][str(ctx.author.id)]["Greatballs"] = greatballs - 1
            with open("inventory.json", "w") as file3:
                json.dump(data2, file3, indent = 1)

            with open("pokeballs.json","r") as balls:
                ball = json.load(balls)
            rate = ball["pokeballs_normal"]["Greatball"]
            break
            
            
    catch = randint(0,100)
    if rate >= catch:
        await ctx.send(f"{name} was caught!\nCatch roll was {rate} and you needed only {catch} to catch")
            
            #Add a flee % to decide if user gets another try
    else:
        await ctx.send(f"{name} escaped... It rolled a {catch} but you only had {rate}")

@search.error
async def search(ctx,error):
  if isinstance(error, commands.CommandOnCooldown):
    retry_secs = error.retry_after
    await ctx.send (f"Please retry in {str(round(retry_secs))}seconds.")
  else:
    raise error
        


client.run(os.getenv('API_Key'))