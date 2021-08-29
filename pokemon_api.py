import requests
import json
import sql

def pokemon(name):
    pokemon_url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(name)
    res = requests.get(url = pokemon_url, verify=False)
    pokemon_data = res.json ()
    return pokemon_data


def add_pokemon(new_pokemon):
    try:
        pokemon_data = pokemon(new_pokemon["name"])
        if (new_pokemon["id"]) != pokemon_data ["id"]:
            return "id "
        if (new_pokemon["height"]) != pokemon_data ["height"]:
            return "height "    
        if (new_pokemon["weight"]) != pokemon_data ["weight"]:
            return "weight "
        types_list = [x["type"]["name"] for x in pokemon_data["types"]]    
        for item in new_pokemon["types"]:
            if item not in types_list:
                return "type " + item
        if len(types_list) != len(new_pokemon["types"]):
            return "type's pokemon less "

        sql.create_pokemon(pokemon_data,new_pokemon)
        return " "
    except json.decoder.JSONDecodeError:
        return "name" 


def add (pokemon):
    pokemon_url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(pokemon)
    res = requests.get(url = pokemon_url, verify=False)
    pokemon_data = res.json ()
    sql.create_pokemon(pokemon_data,pokemon_data)
    

def pokemon_evolve(pokemon,trainer):
    url_evolve = 'https://pokeapi.co/api/v2/pokemon-species/{}'.format(pokemon)
    res = requests.get(url = url_evolve , verify=False)
    evolve_data = res.json()
    url_chain = str(evolve_data["evolution_chain"]["url"])
    res = requests.get(url = url_chain , verify=False)
    evolve_chain = res.json()
    find = False 
    list_ = evolve_chain["chain"]["evolves_to"]    
    if evolve_chain["chain"]["species"]["name"]!= pokemon:
        while not find: 
            for item in list_:
                if  item ["species"]["name"]  == pokemon:
                    find = True
                    list_ = item ["evolves_to"]
                    break
            else:
                list_ = list_[0]["evolves_to"]
    if list_== []:
        return []       
    for item in list_:
        if item ["species"]["name"] not in sql.find_pokemons(trainer):
            new_pokemon = item ["species"]["name"] 
            break
    else:
        return 0
    if not (sql.correct_name(new_pokemon)):
        add(new_pokemon)
    sql.evolve_by_trainer(new_pokemon,trainer)
    return new_pokemon


def move_average(list_moves):
    try:
        max_move = {"max_avg":0, "moves":[]}
        keys = ["accuracy", "pp", "power" ]
        for move in list_moves:
            url_moves = 'https://pokeapi.co/api/v2/move/{}'.format(move)
            res = requests.get(url = url_moves , verify=False)
            move_data = res.json()
            list_values = [move_data[key]for key in keys if move_data[key]]
            avg = sum(list_values)/3 
            if avg == max_move["max_avg"]:
                max_move["moves"].append(move) 
            elif avg > max_move["max_avg"]:
                max_move["max_avg"] = avg
                max_move["moves"] = [move]
        return max_move   
    except json.decoder.JSONDecodeError:
        return("error")







     
