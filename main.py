import pygame
import sys
import json
from models.pokemon import Pokemon
from models.move import Move
from models.battle import Battle
from models.type import Type
from models.non_volatile_status import NonVolatileStatus
from components.battle_stats_box import BattleStatsBox
from components.battle_options_box import BattleOptionsBox

types = {}

with open("./storage/types.json", "r") as types_file:
     types_json = json.load(types_file)
     for type_json in types_json.values():
          type = Type.from_json(type_json)
          types[type.name] = type

pygame.init()


width, height = 320, 240
white = 255, 255, 255
screen = pygame.display.set_mode((900, 596))
background = pygame.image.load("assets/images/grass_background.png").convert()
background_box = background.get_rect()

battle_choice = pygame.image.load("assets/images/combat_choice.png").convert()

charmander = pygame.image.load("assets/images/charmander.png")
squirtle = pygame.image.load("assets/images/squirtle.png")


defaultfont = pygame.font.Font("assets/fonts/poke_font.ttf", 65)
smallfont = pygame.font.Font("assets/fonts/poke_font.ttf", 45)

first_pokemon = [80, 270]
background_box.width = 900
background_box.height = 416


btDialog = 0

fire = types["fire"]

water = types["water"]

normal = types["normal"]

charmander_pokemon = Pokemon(hp=50, lvl=5,
                             type=[fire], speed=63, name="charmander",
                             attack=52, defense=43,
                             moves=[Move(name="scratch", type=normal,
                                         pp=20, accuracy=80, power=15),
                                    Move(name="leer", type=normal, category="status",
                                         pp=30, accuracy=100, power=0,
                                         enemy_debuffs=[{"defense": -1}]),
                                    Move(name="roar", type=normal, category="status",
                                       pp=30, accuracy=100, power=0,
                                       self_buffs=[{"attack": 2}]),
                                    Move(name="ember", type=fire,
                                         pp=15, accuracy=100, power=60)]
                             )
squirtle_pokemon = Pokemon(hp=50, type=[water], lvl=5,
                           attack=48, defense=65,
                           speed=43, name="squirtle",
                           moves=[Move(name="scratch", type=normal,
                                       pp=20, accuracy=90, power=10),
                                  Move(name="leer", type=normal, category="status",
                                       pp=30, accuracy=100, power=0,
                                       enemy_debuffs=[{"defense": -1}]),
                                  Move(name="water gun", type=water,
                                       pp=20, accuracy=85, power=40),
                                  Move(name="headbutt", type=normal,
                                       pp=15, accuracy=100, power=50)]
                           )
principal_stats_box = BattleStatsBox(charmander_pokemon, False,
                                     smallfont, defaultfont)
enemy_stats_box = BattleStatsBox(squirtle_pokemon, True,
                                 smallfont, defaultfont)

battle_handler = Battle(charmander_pokemon, squirtle_pokemon)
battle_choice = BattleOptionsBox(charmander_pokemon, squirtle_pokemon, battle_handler, defaultfont,
                                 pygame.font.Font("assets/fonts/poke_font.ttf",
                                                  55),
                                 principal_stats_box,
                                 enemy_stats_box,
                                 charmander,
                                 squirtle)
#principal_stats_box.health_modify(-25)
#enemy_stats_box.health_modify(-25)
all_sprites = pygame.sprite.Group(principal_stats_box, enemy_stats_box)
count = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            battle_choice.comandHandler(pygame.key.get_pressed())

    screen.fill((0, 0, 0))
    screen.blit(background,  background_box)
    battle_choice.draw(screen)
    pygame.display.flip()
