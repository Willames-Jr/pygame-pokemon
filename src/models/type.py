from typing import List
from attrs import define, Factory


@define
class Type:
    name: str
    super_effective: List[str] = Factory(list)
    not_very_effective: List[str] = Factory(list)
    no_effect: List[str] = Factory(list)

    @classmethod
    def from_json(cls, model):
        return cls(model["name"], model["super_effective"],
                   model["not_very_effective"],
                   model["no_effect"])

    def effectiveness(self, otherType) -> float:
        if otherType.name in self.super_effective:
            return 2
        elif otherType.name in self.not_very_effective:
            return 1/2
        elif otherType.name in self.no_effect:
            return 0
        else:
            return 1
