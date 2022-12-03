from attrs import define, field, validators
from attrs import Factory
from models.type import Type


@define
class Move:
    type:  Type
    category:  str = "physical"
    name:  str = ""
    power:  int = 0
    accuracy:  int = 0
    pp:  int = 0
    condition:  bool = False
    target:  list[str] = Factory(lambda: ["enemy"])
    enemy_debuffs:  list[dict] = Factory(list)
    self_buffs:  list[dict] = Factory(list)

    @classmethod
    def from_json(cls, model):
        return cls(model["type"], model["category"], model["name"],
                   model["power"], model["accuracy"], model["pp"],
                   model["condition"], model["target"], model["enemy_debuffs"],
                   model["self_buffs"])

    def effectiveness(self, pokemon):
        effectiveness = 1
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


