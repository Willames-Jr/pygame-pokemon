from models.move import Move
from models.non_volatile_status import NonVolatileStatus
from models.type import Type
from models.pokemon import Pokemon
from attrs import define
import json


@define
class DataLoader:
    types: dict = {}
    moves: dict = {}
    pokemons: dict = {}
    types_loaded = False

    def load_types(self, json_path):
        with open(json_path, "r") as types_file:
            types_json = json.load(types_file)
        for type_json in types_json.values():
            type = Type.from_json(type_json)
            self.types[type.name] = type
        return self.types

    def load_moves(self, json_path):
        formated_moves = {}

        with open(json_path, "r") as json_file:
            moves = json.load(json_file)

        for move in moves:
            move = Move.from_json(moves[move])
            move.type = self.types[move.type]
            formated_moves[move.name] = move
        self.moves = formated_moves
        return formated_moves

    def load_pokemons(self, json_path):
        formated_pokemons = {}
        with open(json_path, "r") as pokemon_file:
            pokemons_json = json.load(pokemon_file)

        for pokemon in pokemons_json.values():
            moves = [self.moves[x] for x in pokemon["moves"]]
            types = [self.types[x] for x in pokemon["type"]]
            pokemon["moves"] = moves
            pokemon["type"] = types
            formated_pokemons[pokemon["name"]] = Pokemon.from_json(pokemon)
        self.pokemons = formated_pokemons
        return formated_pokemons
