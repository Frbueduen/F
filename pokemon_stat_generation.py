import json
import random
import uuid

def generate_iv():
    return random.randint(0, 31)

def calculate_stat(base, iv, level, ev=0, nature=1):
    return int((((2 * base + iv + (ev // 4)) * level) // 100 + 5) * nature) #got this calculation from chatgpt dont ask me what this is

def store_caught_pokemon(pokemon_data, user_id, shiny, level):
    ivs = {
        "hp": generate_iv(),
        "attack": generate_iv(),
        "defense": generate_iv(),
        "special-attack": generate_iv(),
        "special-defense": generate_iv(),
        "speed": generate_iv()
    }
    unique_id = str(uuid.uuid4())

    caught_pokemon = {
        "unique_id" : unique_id,
        "pokedex_id": pokemon_data["id"],
        "name": pokemon_data["name"],
        "shiny" : shiny,
        "level": level,
        "ivs": ivs,
        "base_stats": pokemon_data["stats"],
        "final_stats": {
            "hp": calculate_stat(pokemon_data["stats"]["hp"], ivs["hp"], level),
            "attack": calculate_stat(pokemon_data["stats"]["attack"], ivs["attack"], level),
            "defense": calculate_stat(pokemon_data["stats"]["defense"], ivs["defense"], level),
            "special-attack": calculate_stat(pokemon_data["stats"]["special-attack"], ivs["special-attack"], level),
            "special-defense": calculate_stat(pokemon_data["stats"]["special-defense"], ivs["special-defense"], level),
            "speed": calculate_stat(pokemon_data["stats"]["speed"], ivs["speed"], level)
        }
    }        

    with open("caught_pokemon_data.json", "r+") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}  # If file is empty or invalid, start with an empty dictionary
        data[unique_id] = caught_pokemon
        file.seek(0)
        json.dump(data, file, indent=1)
        file.truncate()

    with open("Inventory.json", "r+") as file:
        data = json.load(file)
        if "caught_pokemon" not in data["users"][str(user_id)]:
            data["users"][str(user_id)] = {"caught_pokemon": []}
        data["users"][str(user_id)]["caught_pokemon"].append(unique_id)
        file.seek(0)
        json.dump(data, file, indent=1)
        file.truncate()