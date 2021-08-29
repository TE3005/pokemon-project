import pymysql
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="sql_intro",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def pokemon_id(name):
    with connection.cursor() as cursor:
        query = "SELECT id from  pokemon   WHERE name = '{}'".format(name)
        cursor.execute(query)
        result = cursor.fetchall()
        result = result[0]["id"]
        return result


def update (pokemon_data, name):
    id_ =  pokemon_id(name)
    with connection.cursor() as cursor:
        for item in pokemon_data["types"]:
            query = """INSERT into TypesPokemon (pokemon_id, pokemon_type) SELECT %s,%s 
            WHERE NOT EXISTS (SELECT %s, %s FROM TypesPokemon  WHERE %s = pokemon_id and %s = pokemon_type)"""
            value = (id_, item["type"]["name"],id_, item["type"]["name"],id_, item["type"]["name"])
            cursor.execute(query, value)
            connection.commit()


def correct_name(pokemon_name):
    with connection.cursor() as cursor:
        query = "SELECT name FROM pokemon WHERE name = '{}'".format(pokemon_name)
        cursor.execute(query)
        if(cursor.fetchall() == ()):
            return False
        return True 


def correct_trainer(trainer_name):
    with connection.cursor() as cursor:
        query = "SELECT name FROM owner WHERE name = '{}'".format(trainer_name)
        cursor.execute(query)
        if(cursor.fetchall() == ()):
            return False       
        return True


def correct_type(type_):
    with connection.cursor() as cursor:
        query = "SELECT pokemon_type FROM TypesPokemon WHERE pokemon_type = '{}'".format(type_)
        cursor.execute(query)
        if(cursor.fetchall() == ()):
            return False
        return True            


def find_trainers(pokemon_name):
    with connection.cursor() as cursor:
        query = """SELECT owne_name  FROM pokemon JOIN ownerPokemon on
        id = pokemon_id WHERE name = '{}' """.format(pokemon_name)
        cursor.execute(query)
        result = cursor.fetchall()
        return [x ["owne_name"]for x in result]  


def find_pokemons(trainer_name):
    with connection.cursor() as cursor:
        query = """SELECT name  FROM pokemon JOIN ownerPokemon on 
        id = pokemon_id WHERE owne_name = '{}' """.format(trainer_name)
        cursor.execute(query)
        result = cursor.fetchall()
        return [x["name"] for x in result] 


def find_by_type(type_):
    with connection.cursor() as cursor:
        query = """SELECT name   FROM pokemon join TypesPokemon on id = pokemon_id 
        WHERE pokemon_type ='{}' """.format(type_)
        cursor.execute(query)
        result = cursor.fetchall()
        return  [x["name"]for x in result]        


def create_pokemon(pokemon_api,new_pokemon):
    with connection.cursor() as cursor:
        query = 'INSERT into pokemon (id, name , height, weight) values (%s, %s, %s, %s)'
        val = (new_pokemon["id"], new_pokemon["name"], new_pokemon["height"], new_pokemon["weight"])
        cursor.execute(query, val)
        connection.commit()
        update(pokemon_api, new_pokemon["name"])


def delete_by_trainer(pokemon, trainer):
    with connection.cursor() as cursor:
        id_ = pokemon_id(pokemon)
        query = "DELETE FROM ownerPokemon WHERE  owne_name = '{}' and pokemon_id = '{}'".format(trainer, id_)    
        cursor.execute(query)   
        connection.commit()


def evolve_by_trainer(name, trainer):
    with connection.cursor() as cursor:
        query = "SELECT  town   FROM owner  WHERE name  = '{}'".format(trainer)    
        cursor.execute(query)
        town_result = cursor.fetchall()[0]["town"]
        id_evolve =  pokemon_id (name)
        query = """INSERT into ownerPokemon(pokemon_id,owne_name, owne_town) SELECT %s,%s,%s
          WHERE NOT EXISTS(SELECT %s, %s, %s from ownerPokemon WHERE %s = pokemon_id AND %s = owne_name AND %s = owne_town)""" 
        val = (id_evolve, trainer,town_result, id_evolve, trainer,town_result, id_evolve, trainer,town_result)
        cursor.execute(query, val)
        connection.commit()


def get_rating(pokemon):
    with connection.cursor() as cursor:
        id_ =  pokemon_id(pokemon)
        query = "SELECT rating  FROM favorite_pokemon WHERE pokemon_id = {}".format(id_)
        cursor.execute(query)
        result = cursor.fetchall()
        if result == ():
            return 0
        return result[0]["rating"]    


def max_rating():
    with connection.cursor() as cursor:
        query = "SELECT  MAX(rating) as max FROM favorite_pokemon"
        cursor.execute(query)
        result = cursor.fetchall()
        max_ = result[0]["max"]

        query = "SELECT   pokemon_id FROM favorite_pokemon WHERE rating = {}".format(max_)
        cursor.execute(query)
        result = cursor.fetchall()
        fav_pokemons = []
        for item in result:
            query = "SELECT  name FROM pokemon  WHERE id  = {}".format(item["pokemon_id"])
            cursor.execute(query)
            result = cursor.fetchall()
            fav_pokemons.append(result[0]["name"])
        return {"max_rating":max_ , "names": fav_pokemons}    

      
def rate_pokemon(name):
    with connection.cursor() as cursor:
        id_ =  pokemon_id(name)
        pokemon_rat = get_rating(name) 
        if pokemon_rat == 0:
            query = "INSERT into favorite_pokemon (pokemon_id, rating)  values(%s, %s)"
            val = (id_, 1)
            cursor.execute(query, val)
            connection.commit()
        else:
            query = "UPDATE favorite_pokemon SET  rating = {} WHERE pokemon_id  = {}".format(pokemon_rat + 1 , id_)
            cursor.execute(query)
            connection.commit()    
        

