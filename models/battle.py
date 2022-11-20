from models.pokemon import Pokemon
from models.move import Move
from attrs import define
from attrs import Factory
import random


@define
class BatleResults:
    principal_damage: int = 0
    enemy_damage: int = 0
    messages: list[str] = Factory(list)


class Battle:
    def __init__(self,  principal_pokemon:  Pokemon,  enemy_pokemon:  Pokemon):
        self._principal_pokemon = principal_pokemon
        self._enemy_pokemon = enemy_pokemon

    def battle(self, principal_pokemon_attack: Move):
        battle_result = BatleResults()
        enemy_pokemon_attack = self._enemy_pokemon.moves[
            int(random.uniform(0, 3))]
        if self._principal_pokemon.speed > self._enemy_pokemon.speed:
            p_attack_result = self._principal_pokemon.execute_move(principal_pokemon_attack,self._enemy_pokemon)
            battle_result.principal_damage = p_attack_result.damage
            battle_result.messages.append(f"{self._principal_pokemon.name} use {principal_pokemon_attack.name}")

            if self._principal_pokemon.hp <= 0 or self._enemy_pokemon.hp <= 0:
                battle_result.messages.append(f"{self._principal_pokemon.name} is fainted")
                return battle_result

            e_attack_result = self._enemy_pokemon.execute_move(enemy_pokemon_attack,self._principal_pokemon)
            battle_result.enemy_damage = e_attack_result.damage
            battle_result.messages.append(f"{self._enemy_pokemon.name} use {enemy_pokemon_attack.name}")
        else:
            e_attack_result = self._enemy_pokemon.execute_move(enemy_pokemon_attack,self._principal_pokemon)
            battle_result.enemy_damage = e_attack_result.damage
            battle_result.messages.append(f"{self._enemy_pokemon.name} use {enemy_pokemon_attack.name}")

            if self._principal_pokemon.hp <= 0 or self._enemy_pokemon.hp <= 0:
                battle_result.messages.append(f"{self._principal_pokemon.name} is fainted")
                return battle_result

            p_attack_result = self._principal_pokemon.execute_move(principal_pokemon_attack, self._enemy_pokemon)
            battle_result.principal_damage = p_attack_result.damage
            battle_result.messages.append(f"{self._principal_pokemon.name} use {principal_pokemon_attack.name}")

        if self._principal_pokemon.hp <= 0 or self._enemy_pokemon.hp <= 0:
            battle_result.messages.append(f"{self._principal_pokemon.name} is fainted")
            return battle_result

        return battle_result
