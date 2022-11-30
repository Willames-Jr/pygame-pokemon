from attrs import define, field, validators
from attrs import Factory

@define
class Move:
    category:  str = "physical"
    target:  list[str] = Factory(lambda: ["enemy"])
    name:  str = ""
    type:  str = ""
    power:  int = 0
    accuracy:  int = 0
    pp:  int = 0
    condition:  bool = False
    enemy_debuffs:  list[dict] = Factory(list)
    self_buffs:  list[dict] = Factory(list)
