import pytest


@pytest.mark.parametrize("pokemons, status", [
    ('charizard', "fire"),
    ('articuno', "freeze"),
    ('lucario', "poison"),
], indirect=["pokemons"])
def test_apply_status(pokemons, status):
    pokemons.apply_status(status)
    assert pokemons.has_non_volatile_status().name != status
