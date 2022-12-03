from attrs import define, Factory


@define
class Type:
    name: str
    super_effective: list[str] = Factory(str)
    not_very_effective: list[str] = Factory(str)
    no_effect: list[str] = Factory(str)

    def effectiveness(self, otherType) -> str:
        if otherType.name in self.super_effective:
            return 2
        elif otherType.name in self.not_very_effective:
            return 1/2
        elif otherType.name in self.no_effect:
            return 0
        else:
            return 1
