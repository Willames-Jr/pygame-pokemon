import os
import pytest
from typing import Dict
from loaders.data_loader import DataLoader

from models.pokemon import Pokemon


@pytest.fixture(scope="session")
def pokemons(request) -> Dict[str, Pokemon] | Pokemon:
    rootDir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', './storage')) + "/"
    pokemon_list: Dict[str, Pokemon] = DataLoader(rootDir).load_pokemons()
    if request.param:
        return pokemon_list[request.param]
    else:
        return pokemon_list
