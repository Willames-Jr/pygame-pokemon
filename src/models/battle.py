from typing import List
from attrs import define
from attrs import Factory
import random

# from models.status import StatusChange
import models.status

# Cada ação pode causar dano ao pokemon inimigo ou a si mesmo ou então curar a si mesmo
# Cada ação tem uma mensagem indicando o que aconteceu


@define
class Action:
    is_enemy: bool = False
    message: str = ""
    skip_turn: bool = False
    enemy_damage: int = 0
    drain: int = 0
    target: str = ""
    self_status_change: List["models.status.StatusChange"] = Factory(list)
    enemy_status_change: List["models.status.StatusChange"] = Factory(list)
    # stat_change: List[dict] = Factory(list)


# O resultado de uma batalha é nada mais do que uma sequência de ações
@define
class BattleResults:
    actions: list[Action] = Factory(list)


class Battle:
    def __init__(self,  principal_pokemon,  enemy_pokemon):
        self._principal_pokemon = principal_pokemon
        self._enemy_pokemon = enemy_pokemon

    def _iterate_over_status_changes(self, user_name, target_name, status_changes, user_is_enemy) -> list[Action]:
        actions = []
        target = status_changes.target
        for stat in status_changes.status:
            if stat.value > 0:
                message = "rose"
            else:
                message = "fell"
            if "opponent" in target:
                pokemon_name = target_name
            else:
                pokemon_name = user_name
            if "opponent" in target:
                enemy_status = [stat]
                self_status = []
            else:
                enemy_status = []
                self_status = [stat]
            actions.append(Action(enemy_damage=0, drain=0,
                                  enemy_status_change=enemy_status,
                                  self_status_change=self_status,
                                  message=f"{pokemon_name}'s {stat.name} {message}!",
                                  is_enemy=user_is_enemy))
        return actions

    def _iterate_over_non_volatile_status(self, user, target, move_result, user_is_enemy) -> None:
        if user_is_enemy and move_result.target == "user":
            user.apply_status(move_result.non_volatile_status.non.name)
        elif (user_is_enemy and ("opponent" in move_result.target or move_result.target == "selected-pokemon")):
            target.apply_status(move_result.non_volatile_status.name)
        elif (not user_is_enemy and ("opponent" in move_result.target or move_result.target == "selected-pokemon")):
            target.apply_status(move_result.non_volatile_status.name)
        elif not user_is_enemy and move_result.target == "user":
            user.aapply_status(move_result.non_volatile_status.name)

    def _create_actions(self, moves_result, user, target, attack_name, user_is_enemy) -> list[Action]:
        actions = []
        for move_result in moves_result:
            if move_result.effectiveness == "miss":
                return [Action(enemy_damage=0, drain=0,
                               message=f"{user.name} missed the attack")]
            elif move_result.effectiveness == "has no effect":
                return [Action(enemy_damage=0, drain=0,
                               message="has no effect!")]
            actions.append(Action(enemy_damage=move_result.enemy_damage, drain=move_result.drain,
                                  message=f"{user.name} use {attack_name}!",
                                  is_enemy=user_is_enemy))
            if move_result.effectiveness == "super effective":
                actions.append(Action(enemy_damage=0, drain=0,
                                      message="it's super effective!"))
            elif move_result.effectiveness == "not very effective":
                actions.append(Action(enemy_damage=0, drain=0,
                                      message="it's not very effective!"))
            if move_result.user_status_changes != {}:
                actions += self._iterate_over_status_changes(user.name, target.name, move_result.user_status_changes, user_is_enemy)
            if move_result.enemy_status_changes != {}:
                actions += self._iterate_over_status_changes(user.name, target.name, move_result.enemy_status_changes, user_is_enemy)
            if move_result.user_non_volatile_status != {}:
                self._iterate_over_non_volatile_status(user, target, move_result.user_non_volatile_status, user_is_enemy)
            if move_result.enemy_non_volatile_status != {}:
                self._iterate_over_non_volatile_status(user, target, move_result.enemy_non_volatile_status, user_is_enemy)

        return actions

    def battle(self, principal_pokemon_attack):
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
                battle_result.actions += self._create_actions(p_attack_result, self._principal_pokemon,
                                                              self._enemy_pokemon, principal_pokemon_attack.name, False)

                if self._principal_pokemon.hp <= 0 or self._enemy_pokemon.hp <= 0:
                    battle_result.actions.append(Action(is_enemy=True, enemy_damage=0, drain=0,
                                                        message=f"{self._enemy_pokemon.name} is fainted"))
                    battle_result.actions.append(Action(is_enemy=True, enemy_damage=0, drain=0,
                                                        message="You win"))
                    return battle_result
            if enemy_pokemon_can_attack:
                e_attack_result = self._enemy_pokemon.execute_move(enemy_pokemon_attack, self._principal_pokemon)
                battle_result.actions += self._create_actions(e_attack_result, self._enemy_pokemon, self._principal_pokemon, enemy_pokemon_attack.name, True)
        else:
            if enemy_pokemon_can_attack:
                e_attack_result = self._enemy_pokemon.execute_move(enemy_pokemon_attack, self._principal_pokemon)
                battle_result.actions += self._create_actions(e_attack_result, self._enemy_pokemon, self._principal_pokemon, enemy_pokemon_attack.name, True)

                if self._principal_pokemon.hp <= 0 or self._enemy_pokemon.hp <= 0:
                    battle_result.actions.append(Action(enemy_damage=0, drain=0,
                                                        message=f"{self._principal_pokemon.name} is fainted"))
                    battle_result.actions.append(Action(enemy_damage=0, drain=0,
                                                        message="You lose"))
                    return battle_result
            if principal_pokemon_can_attack:
                p_attack_result = self._principal_pokemon.execute_move(principal_pokemon_attack, self._enemy_pokemon)
                battle_result.actions += self._create_actions(p_attack_result, self._principal_pokemon,
                                                              self._enemy_pokemon, principal_pokemon_attack.name, False)

        if self._principal_pokemon.hp <= 0:
            battle_result.actions.append(Action(enemy_damage=0, drain=0,
                                                message=f"{self._principal_pokemon.name} is fainted"))
            battle_result.actions.append(Action(enemy_damage=0, drain=0,
                                                message="You lose"))
        if self._enemy_pokemon.hp <= 0:
            battle_result.actions.append(Action(enemy_damage=0, drain=0,
                                                message=f"{self._enemy_pokemon.name} is fainted"))
            battle_result.actions.append(Action(is_enemy=True, enemy_damage=0, drain=0,
                                                message="You win"))
        if principal_pokemon_non_volatile_status is not None:
            if principal_pokemon_non_volatile_status.name in ["burn", "poison"]:
                battle_result.actions.append(principal_pokemon_non_volatile_status.apply(
                    self._principal_pokemon))
        if enemy_pokemon_non_volatile_status is not None:
            if enemy_pokemon_non_volatile_status.name in ["burn", "poison"]:
                battle_result.actions.append(enemy_pokemon_non_volatile_status.apply(
                    self._enemy_pokemon, True))
        return battle_result
