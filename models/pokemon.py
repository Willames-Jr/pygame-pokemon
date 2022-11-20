from attrs import define, field, validators
from .move import Move
import random


@define
class AttackResult:
    effectiveness: str
    damage: int
    effects: list[str]


@define
class Pokemon:
    # id:  int
    # type:  list
    # name:  str
    # hp:  int
    # attack:  int
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
    conditions:  list = []
    modifiers:  dict = {"attack": 0, "defense": 0, "sp_attack": 0,
                        "sp_defense": 0, "speed": 0, "accuracy": 0,
                        "evasion": 0, "critical": 0}
    accuracy:  int = 100
    evasion:  int = 100

    def execute_move(self, move: Move, target):
        is_physical_attack = move.category == "physical"

        acc = (self.accuracy * ((self.modifiers["accuracy"] + 3) / 3)
               if self.modifiers["accuracy"] >= 0
               else self.accuracy * (3/(self.modifiers["accuracy"] + 3)))
        evs = (target.evasion * ((target.modifiers["evasion"] + 3) / 3)
               if target.modifiers["evasion"] >= 0
               else target.evasion * (3/(target.modifiers["evasion"] + 3)))

        power = move.power
        at_acc = move.accuracy * (acc / evs)
        if at_acc < int(random.uniform(1, 100)):
            print("errou")
            return AttackResult(damage=0,
                                effectiveness="miss",
                                effects=[])

        at, dt = (["attack", "defense"]
                  if is_physical_attack
                  else ["sp_attack", "sp_defense"])
        random_number = random.random()

        stab = 1.5 if move.type in self.type else 1
        a = self.attack if is_physical_attack else self.sp_attack
        d = target.defense if is_physical_attack else self.sp_defense
        burn = 0.5 if "burn" in self.conditions and is_physical_attack else 1
        screen = (0.5
                  if (is_physical_attack and "screen" in target.conditions)
                  or (not is_physical_attack
                      and "light_screen" in target.conditions)
                  else 1)
        # Alterar no caso de batalhas em duplas
        targets = 1
        weather = (1.5
                   if ("rain" in target.conditions and move.type == "water")
                   or ("harsh_sunlight" in target.conditions
                       and move.type == "fire")
                   else 1)
        weather = (0.5
                   if ("rain" in target.conditions and move.type == "fire")
                   or ("harsh_sunlight" in target.conditions
                       and move.type == "water")
                   else 1)
        # No caso de haver a habilidade flash fire
        ff = 1
        # Tem haver com o ataque spit up
        stock_piles = 1
        # Vira 2 se o pokemon usar certos ataques
        double_damage = 1
        charge = (2
                  if move.type == "eletric" and "charge" in self.conditions
                  else 1)
        hh = (1.5
              if "helping_hand" in self.conditions
              else 1)
        # Verificar se é super efetivo,  efetivo etc...
        effectiveness = 1
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
                d = d * (2/(target.modifiers[dt] + 2))
        else:
            critical = 1
            if self.modifiers[at] >= 0:
                a = a * ((self.modifiers[at] + 2)/2)
            else:
                a = a * (2/(self.modifiers[at] + 2))

            if target.modifiers[at] >= 0:
                d = d * ((target.modifiers[dt] + 2)/2)
            else:
                d = d * (2/(target.modifiers[dt] + 2))

        damage = int(((((((2*self.lvl)/5) + 2) * power * a/d)/50) * burn
                                                               * screen
                                                               * targets
                                                               * weather
                                                               * ff + 2)
                     * stock_piles * critical
                     * double_damage * charge
                     * hh * stab
                     * effectiveness * random_multiplier)
        #print("a", ((((2*self.lvl)/5) + 2) * power * a/d)/50)
        print(power)
        # print(stock_piles , critical
        #           , double_damage , charge
        #           , hh , stab
        #           , effectiveness , random_multiplier)
        target.hp -= damage
        print("ACERTOU", damage)
        return AttackResult(damage=damage,
                            effectiveness="normal",
                            effects=[])
