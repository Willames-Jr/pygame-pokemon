from os.path import basename
from typing import List
import random
import components
import pytest

from models.pokemon import MoveResult, Pokemon


@pytest.mark.parametrize("pokemons, status", [
    ('charizard', "fire"),
    ('articuno', "freeze"),
    ('lucario', "poison"),
], indirect=["pokemons"])
def test_apply_status(pokemons, status):
    pokemons.apply_status(status)
    assert pokemons.has_non_volatile_status().name != status


def test_physical_damage(pokemons, moves):
    charizard: Pokemon = pokemons["charizard"]
    blastoise: Pokemon = pokemons["blastoise"]
    charizard.moves[0] = moves["slash"]

    while True:
        result: List[MoveResult] = charizard.execute_move(charizard.moves[0], blastoise)
        if result[0].effectiveness != "miss": break

    baseDamage = int(((((((2*charizard.lvl)/5) + 2) * charizard.moves[0].power * charizard.attack/blastoise.defense)/50)+ 2))

    minDamage = baseDamage * 0.85
    maxDamage = baseDamage * 2

    assert minDamage <= result[0].enemy_damage <= maxDamage
