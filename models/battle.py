from models.move import Move
from attrs import define
from attrs import Factory
import random


# Cada ação pode causar dano ao pokemon inimigo ou a si mesmo ou então curar a si mesmo
# Cada ação tem uma mensagem indicando o que aconteceu
@define
class Action:
    is_enemy: bool = False
    skip_turn: bool = False
    enemy_damage: int = 0
    self_heal: int = 0
    self_damage: int = 0
    message: str = ""


# O resultado de uma batlaha é nada mais do que uma sequência de ações
@define
class BattleResults:
    actions: list[Action] = Factory(list)


class Battle:
    def __init__(self,  principal_pokemon,  enemy_pokemon):
        self._principal_pokemon = principal_pokemon
        self._enemy_pokemon = enemy_pokemon

    def battle(self, principal_pokemon_attack: Move):
        battle_result = BattleResults()
        principal_pokemon_non_volatile_status = self._principal_pokemon.has_non_volatile_status()
        enemy_pokemon_non_volatile_status = self._enemy_pokemon.has_non_volatile_status()
        principal_pokemon_can_attack = True
        enemy_pokemon_can_attack = True
        enemy_pokemon_attack = self._enemy_pokemon.moves[
            int(random.uniform(0, 3))]

        # Aplicando efeitos de freeze e sleep
        if principal_pokemon_non_volatile_status is not None:
            if principal_pokemon_non_volatile_status.name in ["freeze", "sleep", "paralysis"]:
                result = principal_pokemon_non_volatile_status.apply(self._principal_pokemon)
                if result is not None:
                    battle_result.actions.append(result)
                    if battle_result.actions[-1].skip_turn:
                        principal_pokemon_can_attack = False
        if enemy_pokemon_non_volatile_status is not None:
            if enemy_pokemon_non_volatile_status.name in ["freeze", "sleep", "paralysis"]:
                result = enemy_pokemon_non_volatile_status.apply(self._enemy_pokemon, True)
                if result is not None:
                    battle_result.actions.append(result)
                    if battle_result.actions[-1].skip_turn:
                        enemy_pokemon_can_attack = False

        # Atacando o outro pokemon
        if self._principal_pokemon.get_speed() > self._enemy_pokemon.get_speed():
            if principal_pokemon_can_attack:
                p_attack_result = self._principal_pokemon.execute_move(principal_pokemon_attack, self._enemy_pokemon)
                battle_result.actions.append(Action(enemy_damage=p_attack_result.damage, self_heal=0, self_damage=0,
                    message=f"{self._principal_pokemon.name} use {principal_pokemon_attack.name}!"))
                if p_attack_result.effectiveness == "miss":
                    battle_result.actions.append(Action(enemy_damage=0, self_heal=0, self_damage=0,
                    message=f"{self._principal_pokemon.name} missed the attack"))

                if self._principal_pokemon.hp <= 0 or self._enemy_pokemon.hp <= 0:
                    battle_result.actions.append(Action(is_enemy=True, enemy_damage=0, self_heal=0, self_damage=0,
                    message=f"{self._enemy_pokemon.name} is fainted"))
                    return battle_result
            if enemy_pokemon_can_attack:
                e_attack_result = self._enemy_pokemon.execute_move(enemy_pokemon_attack,self._principal_pokemon)
                battle_result.actions.append(Action(is_enemy=True, enemy_damage=e_attack_result.damage, self_heal=0, self_damage=0,
                    message=f"{self._enemy_pokemon.name} use {enemy_pokemon_attack.name}!"))
                if e_attack_result.effectiveness == "miss":
                    battle_result.actions.append(Action(is_enemy=True, enemy_damage=0, self_heal=0, self_damage=0,
                    message=f"{self._enemy_pokemon.name} missed the attack"))
        else:
            if enemy_pokemon_can_attack:
                e_attack_result = self._enemy_pokemon.execute_move(enemy_pokemon_attack,self._principal_pokemon)
                battle_result.actions.append(Action(is_enemy=True, enemy_damage=e_attack_result.damage, self_heal=0, self_damage=0,
                    message=f"{self._enemy_pokemon.name} use {enemy_pokemon_attack.name}!"))
                if e_attack_result.effectiveness == "miss":
                    battle_result.actions.append(Action(is_enemy=True, enemy_damage=0, self_heal=0, self_damage=0,
                    message=f"{self._enemy_pokemon.name} missed the attack"))

                if self._principal_pokemon.hp <= 0 or self._enemy_pokemon.hp <= 0:
                    battle_result.actions.append(Action(enemy_damage=0, self_heal=0, self_damage=0,
                    message=f"{self._principal_pokemon.name} is fainted"))
                    return battle_result
            if principal_pokemon_can_attack:
                p_attack_result = self._principal_pokemon.execute_move(principal_pokemon_attack, self._enemy_pokemon)
                battle_result.actions.append(Action(enemy_damage=p_attack_result.damage, self_heal=0, self_damage=0,
                    message=f"{self._principal_pokemon.name} use {principal_pokemon_attack.name}"))
                if p_attack_result.effectiveness == "miss":
                    battle_result.actions.append(Action(enemy_damage=0, self_heal=0, self_damage=0,
                    message=f"{self._principal_pokemon.name} missed the attack"))

        if self._principal_pokemon.hp <= 0:
            battle_result.actions.append(Action(enemy_damage=0, self_heal=0, self_damage=0,
                message=f"{self._principal_pokemon.name} is fainted"))
        if self._enemy_pokemon.hp <= 0:
            battle_result.actions.append(Action(enemy_damage=0, self_heal=0, self_damage=0,
                message=f"{self._enemy_pokemon.name} is fainted"))
        
        if principal_pokemon_non_volatile_status != None:
            if principal_pokemon_non_volatile_status.name in ["burn","poison"]:
                battle_result.actions.append(principal_pokemon_non_volatile_status.apply(
                    self._principal_pokemon))
        if enemy_pokemon_non_volatile_status != None:
            if enemy_pokemon_non_volatile_status.name in ["burn","poison"]:
                battle_result.actions.append(enemy_pokemon_non_volatile_status.apply(
                    self._enemy_pokemon,True))
        return battle_result
