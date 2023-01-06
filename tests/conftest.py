import os
from _pytest.fixtures import SubRequest
import pytest
from typing import Dict
from loaders.data_loader import DataLoader
from models.move import Move

from models.pokemon import Pokemon


@pytest.fixture(scope="session")
def pokemons(request) -> Dict[str, Pokemon] | Pokemon:
    rootDir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', './storage')) + "/"
    pokemon_list: Dict[str, Pokemon] = DataLoader(rootDir).load_pokemons()

    if 'param' in request.__dict__.keys():
        return pokemon_list[request.param]
    else:
        return pokemon_list

@pytest.fixture(scope="session")
def moves(request) -> Dict[str, Move] | Move:
    rootDir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', './storage')) + "/"
    moves: Dict[str, Move] = DataLoader(rootDir).load_moves()
    if 'param' in request.__dict__.keys():
        return moves[request.param]
    else:
        return moves