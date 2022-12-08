from attrs import define, field, validators
from attrs import Factory
from attrs import Attribute
from .move import Move
import random
from models.non_volatile_status import NonVolatileStatus


@define
class MoveResult:
    effectiveness: str
    enemy_damage: int
    # Esse atributo representa um valor a ser adicionado a vida do pokemon que realizou o movimento
    # Ou seja, pode ser tanto um recoil, tanto um heal
    drain: int = 0
    target: str = ""
    user_status_changes: list[str] = Factory(dict)
    enemy_status_changes: list[str] = Factory(dict)
    user_non_volatile_status: list[str] = Factory(dict)
    enemy_non_volatile_status: list[str] = Factory(dict)


@define
class Pokemon:
    id:  int = None
    type:  list = None
    name:  str = None
    hp:  int = None
    attack:  int = None
    defense:  int = None
    sp_attack:  int = None
    sp_defense:  int = None
    speed:  int = None
    back_image:  str = None
    front_image:  str = None
    moves:  list[Move] = None
    # Propriedades que não estão sendo usadas
    # Usar conditions na hora de melhorar o sistema de batalha e adicionar poison, burn,  confusion etc.
    # Usar ev, iv,  nature,  xp e lvl quando fizer a implementação de xp
    # Usar gender por último,  por enquanto só afeta a interface
    nature:  str = None
    gender:  str = None
    ev:  int = None
    iv:  int = None
    lvl:  int = None
    xp:  int = None
    volatile_status: list[str] = Factory(list)
    non_volatile_status: list[str] = Factory(lambda: [
                                      NonVolatileStatus(name="poison"),
                                      NonVolatileStatus(name="paralysis"),
                                      NonVolatileStatus(name="freeze"),
                                      NonVolatileStatus(name="burn"),
                                      NonVolatileStatus(name="sleep")
                                      ])
    modifiers:  dict = Factory(lambda: {
                            "attack": 0, "defense": 0,
                            "sp_attack": 0, "sp_defense": 0,
                            "speed": 0, "accuracy": 0,
                            "evasion": 0, "critical": 0
                            })
    accuracy:  int = 100
    evasion:  int = 100

    @classmethod
    def from_json(cls, model):
        return cls(
            type=model["type"],
            name=model["name"],
            hp=model["hp"],
            attack=model["attack"],
            defense=model["defense"],
            sp_attack=model["sp_attack"],
            sp_defense=model["sp_defense"],
            speed=model["speed"],
            back_image=model["back_image"],
            front_image=model["front_image"],
            moves=model["moves"],
            lvl=model["lvl"]
            )

    def get_non_volatile_status(self, status_name) -> NonVolatileStatus:
        for status in self.non_volatile_status:
            if status.name == status_name:
                return status

    def has_non_volatile_status(self) -> NonVolatileStatus:
        for status in self.non_volatile_status:
            if status.active:
                return status
        return None

    def get_speed(self) -> int:
        is_paralysed = self.get_non_volatile_status("paralysis")
        if is_paralysed:
            return self.speed * 0.25
        else:
            return self.speed

    def has_type(self, type_name: str) -> bool:
        for type in self.type:
            if type.name == type_name:
                return True
        return False

    def apply_status(self, status_name: str) -> None:
        if status_name == "burn" and self.has_type("fire"):
            return
        if status_name == "poison" and self.has_type("steel"):
            return
        if status_name == "freeze" and self.has_type("ice"):
            return
        for status in self.non_volatile_status:
            if status.name == status_name:
                status.active = True
                return

    def change_modifiers(self, name, value):
        if -6 <= self.modifiers[name] + value <= 6:
            self.modifiers[name] += value
        return

    def remove_status(self, status_name: str) -> None:
        for status in self.non_volatile_status:
            if status.name == status_name:
                status.active = False
                status.turns = 0

    def execute_move(self, move: Move, user, target, total_hits: int = None, actual_hit: int = 0, previous_results: list[MoveResult] = None) -> MoveResult:
        is_physical_attack = move.category == "physical"
        
        # Somente usado caso o ataque acerte mais de uma vez, como fury attack
        number_of_hits = move.hits_number()
        if number_of_hits != 1 and total_hits is None:
            total_hits = number_of_hits
        actual_hit += 1
        # Define quem é o alvo do ataque, por enquanto não é usado
        if move.target == "user":
            move_target = "user"
        elif "opponent" in move.target:
            move_target = "opponent"

        # Verificando se o movimento aplica algum efeito nos status ou aplica
        # status não volatil, como poison, freeze etc.
        status_change = move.applyStatus(user, target)
        non_volatile_status = move.applyNonVolatileStatus(user, target)

        
        acc = (self.accuracy * ((self.modifiers["accuracy"] + 3) / 3)
               if self.modifiers["accuracy"] >= 0
               else self.accuracy * (3/(-1*self.modifiers["accuracy"] + 3)))
        evs = (target.evasion * ((target.modifiers["evasion"] + 3) / 3)
               if target.modifiers["evasion"] >= 0
               else target.evasion * (3/(-1*target.modifiers["evasion"] + 3)))

        if move.category == "status":
            healing = move.applyHealing(user)
            drain = move.applyDrain(user, target, 0)
            if drain == 0:
                drain = healing

            move_result = MoveResult(enemy_damage=0,
                                 drain=drain,
                                 effectiveness="normal")
            if status_change is not None:
                if status_change.target == "enemy":
                    move_result.enemy_status_changes = status_change
                else:
                    move_result.user_status_changes = status_change
            if non_volatile_status is not None:
                if non_volatile_status.target == "enemy":
                    move_result.enemy_non_volatile_status = non_volatile_status
                else:
                    move_result.user_non_volatile_status = non_volatile_status
            return [move_result]

        power = move.power
        at_acc = move.accuracy * (acc / evs)
        if at_acc < int(random.uniform(1, 100)):
            return MoveResult(enemy_damage=0,
                                effectiveness="miss")

        at, dt = (["attack", "defense"]
                  if is_physical_attack
                  else ["sp_attack", "sp_defense"])
        random_number = random.random()

        stab = 1.5 if self.has_type(move.type.name) else 1
        a = self.attack if is_physical_attack else self.sp_attack
        d = target.defense if is_physical_attack else target.sp_defense
        burn = 0.5 if "burn" in self.non_volatile_status and is_physical_attack else 1
        screen = (0.5
                  if (is_physical_attack and "screen" in target.volatile_status)
                  or (not is_physical_attack
                      and "light_screen" in target.volatile_status)
                  else 1)
        # Alterar no caso de batalhas em duplas
        targets = 1
        weather = (1.5
                   if ("rain" in target.volatile_status and move.type.name == "water")
                   or ("harsh_sunlight" in target.volatile_status
                       and move.type.name == "fire")
                   else 1)
        weather = (0.5
                   if ("rain" in target.volatile_status and move.type.name == "fire")
                   or ("harsh_sunlight" in target.volatile_status
                       and move.type.name == "water")
                   else 1)
        # No caso de haver a habilidade flash fire
        ff = 1
        # Tem haver com o ataque spit up
        stock_piles = 1
        # Vira 2 se o pokemon usar certos ataques
        double_damage = 1
        charge = (2
                  if move.type.name == "electric" and "charge" in self.volatile_status
                  else 1)
        hh = (1.5
              if "helping_hand" in self.volatile_status
              else 1)
        effectiveness, effectiveness_message = move.effectiveness(target)

        random_multiplier = float(random.uniform(0.85, 1))

        if ((self.modifiers["critical"] == 0 and random_number <= 1/16)
                or (self.modifiers["critical"] == 1 and random_number <= 1/8)
                or (self.modifiers["critical"] == 2 and random_number <= 1/4)
                or (self.modifiers["critical"] == 3 and random_number <= 1/3)
                or (self.modifiers["critical"] >= 4 and random_number <= 1/2)):
            critical = 2

            if self.modifiers[at] > 0:
                a = a * ((self.modifiers[at] + 2)/2)

            if target.modifiers[dt] < 0:
                d = d * (2/(-1*target.modifiers[dt] + 2))
        else:
            critical = 1
            if self.modifiers[at] >= 0:
                a = a * ((self.modifiers[at] + 2)/2)
            else:
                a = a * (2/(-1*self.modifiers[at] + 2))

            if target.modifiers[dt] >= 0:
                d = d * ((target.modifiers[dt] + 2)/2)
            else:
                d = d * (2/(-1*target.modifiers[dt] + 2))

        damage = int(((((((2*self.lvl)/5) + 2) * power * a/d)/50) * burn
                                                               * screen
                                                               * targets
                                                               * weather
                                                               * ff + 2)
                     * stock_piles * critical
                     * double_damage * charge
                     * hh * stab
                     * effectiveness * random_multiplier)
        # print("a", ((((2*self.lvl)/5) + 2) * power * a/d)/50)
        target.hp -= damage
        # print(self.name, damage)
        # print(stock_piles , critical
        #           , double_damage , charge
        #           , hh , stab
        #           , effectiveness , random_multiplier)
        

        # Valor a ser adicionado ou subtraido da vida do pokemon atacante
        drain = move.applyDrain(user, target, damage)

        move_result = MoveResult(enemy_damage=damage,
                                 drain=drain,
                                 effectiveness=effectiveness_message)
        if status_change is not None:
            if "opponent" in status_change.target:
                move_result.enemy_status_changes = status_change
            else:
                move_result.user_status_changes = status_change
        
        if non_volatile_status is not None:
            if "opponent" in non_volatile_status.target:
                move_result.enemy_non_volatile_status = non_volatile_status
            else:
                move_result.user_non_volatile_status = non_volatile_status

        battle_result = [move_result]
        if number_of_hits != 1:
            self.execute_move(move, target, total_hits, actual_hit, battle_result + previous_results)
        elif number_of_hits == total_hits:
            return battle_result + previous_results
        else:
            return battle_result
