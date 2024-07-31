import json

def load_moves_into_dict():
    with open('all_move_data.json', 'r') as file:
        move_data = json.load(file)
    
    move_dict = {move['name']: move for move in move_data}
    return move_dict

def search_move_by_name(move):
    dict = load_moves_into_dict()
    results = dict.get(move, None)
    return results