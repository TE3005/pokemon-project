from flask import Flask ,Response, request
import requests
import json
from pymysql import IntegrityError
import sql 
import pokemon_api

app = Flask(__name__, static_url_path = '', static_folder = 'dist')

@app.route('/<path:file_path>')
def serve_static_file(file_path):
    return app.send_static_file(file_path)


@app.route('/type/<pokemon_name>', methods = ["put"])
def update_types (pokemon_name):
    try:
        if not sql.correct_name(pokemon_name):
            return json.dumps({"error": "The pokemon's name " + pokemon_name + " does not exist"}), 404
        data = pokemon_api.pokemon(pokemon_name) 
        sql.update(data,pokemon_name)
        return json.dumps({"status":"update  pokemon"}), 201
    except Exception as e:
        return({"error db": str(e)}), 500


@app.route('/trainers/<pokemon_name>')
def find_Owners(pokemon_name):
    try:
        if not sql.correct_name(pokemon_name):
            return json.dumps({"error": "The pokemon's name " + pokemon_name + " does not exist"}), 404
        owners = sql.find_trainers(pokemon_name)
        return json.dumps({"names": owners}), 200
    except Exception as e:
        return({"error db": str(e)}), 500    


@app.route('/pokemons/<trainer_name>')
def find_Roster(trainer_name):
    try:
        if not sql.correct_trainer:
            return json.dumps({"error": "The trainer's name " + trainer_name + " does not exist"}), 404
        pokemons =sql.find_pokemons(trainer_name)
        return json.dumps({"names": pokemons}), 200
    except Exception as e:
        return({"error db": str(e)}), 500 


@app.route('/pokemon', methods =  ["post"])
def add_new_pokemon():
    new_pokemon = request.get_json()
    try:
        create_pokemon = pokemon_api.add_pokemon(new_pokemon) 
        if  create_pokemon != " ":
            if create_pokemon == "name":
                return json.dumps({"error": "Pokemon's name does not exist "} ), 404
            return json.dumps({"error":"The " + create_pokemon +"  does not suitable to the pokemon's name  " + new_pokemon["name"]}), 404
        return json.dumps({"status": "Success. Added pokemon"}), 201
    except IntegrityError as e:
            code, message = e.args
            return ({"Error": "The Pokemon " + new_pokemon["name"] + " already exist "}), 404
    except Exception as e:
        return({"error db": str(e)}), 500 


@app.route('/pokemons')
def find():
    try:
        ptype = request.args.get("type")

        if not sql.correct_type:
            return json.dumps({"error": "The pokemon's type " + ptype + " does not exist"}), 404    
        types = sql.find_by_type(ptype)
        return json.dumps({"names": types}), 200
    except Exception as e:
        return({"error db": str(e)}), 500 


@app.route('/pokemon/<name>,<trainer>', methods = ["delete"])
def delete (name, trainer):
    try:
        if not sql.correct_name(name):
            return json.dumps({"error": "The pokemon's name " + name + " does not exist"}), 404
        if trainer not in sql.find_trainers(name):
            return json.dumps({"error": "The pokemon's name " + name + " did not belong to the  " + trainer}), 404 
        sql.delete_by_trainer(name, trainer)
        return json.dumps({"status": "Success. Delete pokemon"}), 200
    except Exception as e:
        return({"error db": str(e)}), 500    


@app.route('/evolve/<name>,<trainer>', methods = ["put"])
def evolve (name, trainer):
    try:
        if not sql.correct_name(name):
            return json.dumps({"error": "The pokemon's name " + name + " does not exist"}), 404
        if trainer not in sql.find_trainers(name):
            return json.dumps({"error": "The pokemon's name " + name + " did not belong to the  " + trainer}), 404 
        pevolve = pokemon_api.pokemon_evolve(name, trainer)
        if pevolve == []:
            return json.dumps({"error":"The pokemon "+ name + " can not evolve"}), 404
        if pevolve == 0 :
            return json.dumps({"error":"The pokemon "+ name + " evolve to the pokemon that exist in the trainer " + trainer}), 404
        return json.dumps({"evolve":"The pokemon " + name + " of trainer " + trainer + " elvove to " + pevolve }), 201
    except Exception as e:
        return({"error db": str(e)}), 500        


@app.route('/rate/<name>',methods = ["put"])
def rate(name):
    try:
        if  not sql.correct_name(name):
            return json.dumps({"error": "The pokemon's name " + name + " does not exist"}), 404
        sql.rate_pokemon(name)
        return json.dumps({"status": "Success.Rated pokemon"}), 200
    except Exception as e:
        return({"error db": str(e)}), 500    


@app.route('/max_rating')
def max_rating():
    try:
        max_ = sql.max_rating()
        return json.dumps(max_), 200
    except Exception as e:
        return({"error db": str(e)}), 500


@app.route('/rating/<pokemon>')
def rating(pokemon):
    try:
        if  not sql.correct_name(pokemon):
            return json.dumps({"error": "The pokemon's name " + pokemon + " does not exist"}), 404
        rat = sql.get_rating(pokemon)
        return json.dumps({"name": pokemon, "rating": rat}), 200
    except Exception as e:
        return({"error db": str(e)}), 500   


@app.route('/avg_move')
def avg_move():
    try:
        moves = request.get_json()
        max_avg = pokemon_api.move_average(moves["names"])
        if max_avg == "error":
            return json.dumps({"error": "The names of the moves are incorrect"}), 404
        return  json.dumps(max_avg), 200
    except Exception as e:
        return({"error db": str(e)}), 500     



if __name__ == '__main__':
    app.run(port = 3001)    