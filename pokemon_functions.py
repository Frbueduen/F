import json
import random

def initialize_wild_pool():
    with open('all_pokemon_data.json', 'r') as file:
        pokemon_data = json.load(file)
    
    normal_ID_list = [pokemon["id"] for pokemon in pokemon_data if pokemon['rarity'] == "Normal"]
    mythical_ID_list =  [pokemon["id"] for pokemon in pokemon_data if pokemon['rarity'] == "Mythical"]
    legendary_ID_list = [pokemon["id"] for pokemon in pokemon_data if pokemon['rarity'] == "Legendary"]

    return normal_ID_list, mythical_ID_list, legendary_ID_list

def load_pokemon_into_dict():
    with open('all_pokemon_data.json', 'r') as file:
        pokemon_data = json.load(file)

    pokemon_dict = {pokemon["name"]: pokemon for pokemon in pokemon_data}
    return pokemon_dict

def load_pokemon_into_dict_id():
    with open('all_pokemon_data.json', 'r') as file:
        pokemon_data = json.load(file)

    pokemon_dict = {pokemon["id"]: pokemon for pokemon in pokemon_data}
    return pokemon_dict

def search_pokemon_by_name(pokemon):
    dict = load_pokemon_into_dict()
    results = dict.get(pokemon, None)
    return results

def search_pokemon_by_id(pokemon):
    dict = load_pokemon_into_dict_id()
    results = dict.get(pokemon, None)
    return results

def get_next_evolution(evolution_line, current_pokemon):
    if not evolution_line:
        return "-"
    
    try:
        current_index = evolution_line.index(current_pokemon)
        # If it's the last evolution, return "-"
        if current_index == len(evolution_line) - 1:
            return "-"
        # Return the next evolution
        return evolution_line[current_index + 1]
    except ValueError:
        # If the current Pokémon is not found in the evolution line, return "-"
        return "-"
    
def get_type_colour(type):

    if type[0] == "Grass":
        colour = 0x7AC74C
    elif type[0] =="Fire":
        colour = 0xEE8130
    elif type[0] =="Water":
        colour = 0x6390F0
    elif type[0] =="Electric":
        colour = 0xF7D02C
    elif type[0] =="Flying":
        colour = 0xA98FF3
    elif type[0] =="Bug":
        colour = 0xA6B91A
    elif type[0] =="Steel":
        colour = 0xB7B7CE
    elif type[0] =="Fairy":
        colour = 0xD685AD
    elif type[0] =="Poison":
        colour = 0xA33EA1
    elif type[0] =="Steel":
        colour = 0xB7B7CE
    elif type[0] =="Dragon":
        colour = 0x6F35FC
    elif type[0] =="Psychic":
        colour = 0xF95587
    elif type[0] =="Dark":
        colour = 0x705746
    elif type[0] =="Ghost":
        colour = 0x735797
    elif type[0] =="Rock":
        colour = 0xB6A136
    elif type[0] =="Ground":
        colour = 0xE2BF65
    elif type[0] =="Fighting":
        colour = 0xC22E28
    elif type[0] =="Ice":
        colour = 0x96D9D6
    elif type[0] == "Normal":
        colour = 0xA8A77A

    return colour

def choose_random_wild(normal_ID_list, mythical_ID_list, legendary_ID_list):
    rarity_choice = random.choices(
        ["normal", "mythical", "legendary"],
        #weights=[0.9895,0.01,0.0005],
        weights=[80, 15, 5],
        k=1
    )[0]

    shiny = random.choices(
        [True, False],
        weights=[10,90],
        k=1
    )[0]

    if rarity_choice == "normal":
        chosen_id = random.choice(normal_ID_list)
    elif rarity_choice == "mythical":
        chosen_id = random.choice(mythical_ID_list)
    else:
        chosen_id = random.choice(legendary_ID_list)

    pokemon = search_pokemon_by_id(chosen_id)

    return pokemon, shiny