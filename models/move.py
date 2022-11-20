from attrs import define, field, validators


@define
class Move:
    category:  str = field(default="physical")
    target:  list[str] = field(default="enemy")
    name:  str = ""
    type:  str = ""
    power:  int = 0
    accuracy:  int = 0
    pp:  int = 0
    condition:  bool = False
    effects:  list[dict] = []

    @target.validator
    def _check_target(self, attr, value):
        if value not in ["enemy", "self"]:
            raise ValueError("The target must be 'enemy' or 'self'")

    @category.validator
    def _check_category(self, attr, value):
        if value not in ["physical", "special", "status"]:
            raise ValueError("The category must be 'physical',  'especial' or 'status'")
