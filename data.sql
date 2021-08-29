USE sql_intro; 

CREATE  TABLE owner(
    name VARCHAR (20),
    town VARCHAR (20),
PRIMARY KEY(name, town)
);


CREATE TABLE pokemon(
    id INT ,
    name  VARCHAR(20),
    height INT,
    weight INT,
    PRIMARY KEY(id)
);


CREATE  TABLE ownerPokemon(
    pokemon_id INT ,
    owne_name VARCHAR (20),
    owne_town VARCHAR (20),
    PRIMARY KEY(pokemon_id, owne_name, owne_town),
    FOREIGN KEY(owne_name, owne_town) REFERENCES owner (name, town),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon (id)
);


CREATE TABLE TypesPokemon  (
    pokemon_id INT,
    pokemon_type VARCHAR(20),
    PRIMARY KEY(pokemon_id, pokemon_type),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon (id)
);


CREATE TABLE favorite_pokemon(
	pokemon_id INT,
	rating INT,
	PRIMARY KEY(pokemon_id),
	FOREIGN KEY(pokemon_id) REFERENCES pokemon (id)
); 

