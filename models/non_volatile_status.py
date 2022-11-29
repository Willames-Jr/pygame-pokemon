from attrs import define
from models.battle import Action


@define
class NonVolatileStatus:
    name: str
    turns: int = 0
    sleep_counter: int = 0
    active: bool = False

    def apply(self, pokemon, is_enemy_pokemon=False):
        damage = 0
        message = ""

        if self.name == "burn":
            damage = int(pokemon.hp/16)
            message = f"{pokemon.name} is hurt by burn!"


        if self.name == "sleep":
            message = f"{pokemon.name} is sleeping!"

        return Action(is_enemy=is_enemy_pokemon,enemy_damage=0,
                      self_heal=0, self_damage=damage,
                      message=message)
