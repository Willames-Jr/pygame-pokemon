from attrs import define
from models.battle import Action
import random


@define
class NonVolatileStatus:
    name: str
    turns: int = 0
    sleep_counter: int = 0
    active: bool = False

    def apply(self, pokemon, is_enemy_pokemon=False):
        damage = 0
        message = ""
        skip_turn = False

        if self.name == "burn":
            damage = int(pokemon.hp/8)
            message = f"{pokemon.name} is hurt by burn!"

        if self.name == "poison":
            damage = int(pokemon.hp/8)
            message = f"{pokemon.name} is hurt by poison!"

        if self.name == "sleep":
            if self.turns == 0:
                self.sleep_counter = int(random.uniform(2, 5))
            if self.turns < self.sleep_counter:
                message = f"{pokemon.name} is fast asleep!"
                skip_turn = True
            else:
                message = f"{pokemon.name} woke up!"
                self.active = False

        if self.name == "freeze":
            unfreeze = int(random.uniform(1, 100))
            print(unfreeze, self.turns)
            if unfreeze < 20 and self.turns != 0:
                message = f"{pokemon.name} was defrosted!"
                self.active = False
            else:
                message = f"{pokemon.name} is frozen solid!"
                skip_turn = True

        if self.name == "paralysis":
            paralysed = int(random.uniform(1, 100))
            if paralysed <= 25:
                message = f"{pokemon.name} is paralyzed! It can't move"
                skip_turn = True
            else:
                return None

        self.turns += 1
        return Action(is_enemy=is_enemy_pokemon, enemy_damage=0,
                      self_heal=0, self_damage=damage,
                      message=message, skip_turn=skip_turn)
