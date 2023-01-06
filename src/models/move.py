from typing import List
from models.status import NonVolatileStatus
from attrs import define
from attrs import Factory
from models.status import MoveStatus, StatusChange
from models.type import Type
import random


@define
class Move:
    type:  Type
    category:  str = "physical"
    name:  str = ""
    power:  int = 0
    accuracy:  int = 0
    pp:  int = 0
    non_volatile_status: str = ""
    non_volatile_status_chance: int = 0
    effect_chance: int = 0
    min_hits: int = 0
    max_hits: int = 0
    # Prioridade do movimento
    priority: int = 0
    # Porcentagem de vida que o atacante ganha ou perde
    drain_percent: int = 0
    # Aumento do critico em buff
    critical_rate: int = 0
    # Probabilidade do pokemon inimigo pular o turno
    flinch_chance: int = 0
    healing_percent: int = 0
    target:  List[str] = Factory(lambda: ["enemy"])
    status_change:  List[StatusChange] = Factory(list)

    @classmethod
    def from_json(cls, model):
        return cls(
                   type=model["type"],
                   category=model["category"],
                   name=model["name"],
                   power=model["power"],
                   accuracy=model["accuracy"],
                   pp=model["pp"],
                   non_volatile_status=model["non_volatile_status"],
                   non_volatile_status_chance=model["non_volatile_status_chance"],
                   effect_chance=model["effect_chance"],
                   min_hits=model["min_hits"],
                   max_hits=model["max_hits"],
                   priority=model["priority"],
                   drain_percent=model["drain"],
                   critical_rate=model["crit_rate"],
                   flinch_chance=model["flinch_chance"],
                   healing_percent=model["healing"],
                   target=model["target"],
                   status_change=[StatusChange.from_json(x) for x in model["stat_changes"]])

    def effectiveness(self, pokemon):
        effectiveness: float = 1
        effectiveness_message = ""
        for type in pokemon.type:
            effectiveness *= self.type.effectiveness(type)

        if effectiveness in [2, 4]:
            effectiveness_message = "super effective"
        elif effectiveness in [1/2, 1/4]:
            effectiveness_message = "not very effective"
        elif effectiveness == 0:
            effectiveness_message = "has no effect"
        else:
            effectiveness_message = "normal"
        return effectiveness, effectiveness_message

    def hits_number(self) -> int:
        if self.min_hits == 0 or self.min_hits is None:
            return 1
        elif self.min_hits != self.max_hits:
            probability = random.uniform(1, 100)
            if probability <= 37.5:
                return 2
            elif 37.5 < probability <= 75:
                return 3
            elif 75 < probability <= 87.5:
                return 4
            elif 87.5 < probability <= 100:
                return 5
        # else:
        #    return self.min_hits

        return 0

    def applyHealing(self, user):
        return user.hp * (self.healing_percent/100)

    def applyDrain(self, user, enemy, damage):
        if self.drain_percent < 0:
            return user.hp * (self.drain_percent/100)
        else:
            return damage * (self.drain_percent/100)

    def applyStatus(self, user, enemy):
        if self.effect_chance == 0:
            return None
        else:
            # TODO: O target pode não ser igual ao target do movimento
            # como no caso do ancient power em que o target é o
            # target = self.target if "selected-pokemon" not in self.target else "enemy"
            move_result = MoveStatus(target=self.target, status=self.status_change)
            probability = int(random.uniform(1, 100))
            if probability <= self.effect_chance:
                return move_result

    def applyNonVolatileStatus(self, user, enemy):
        if self.non_volatile_status_chance == 0:
            return None
        else:
            # TODO: O target pode não ser igual ao target do movimento
            # como no caso do ancient power em que o target é o
            # target = self.target if "selected-pokemon" not in self.target else "enemy"
            move_result = MoveStatus(target=self.target, non_volatile_status=NonVolatileStatus(self.non_volatile_status))
            probability = int(random.uniform(1, 100))
            if probability <= self.non_volatile_status_chance:
                return move_result
