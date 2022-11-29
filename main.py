import pygame
import sys
from models.pokemon import Pokemon
from models.move import Move
from models.battle import Battle
from models.non_volatile_status import NonVolatileStatus
from components.battle_stats_box import BattleStatsBox
from components.battle_options_box import BattleOptionsBox

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


charmander_pokemon = Pokemon(hp=50, lvl=5,
                             type=["fire"], speed=100, name="charmander",
                             attack=50, defense=20,
                             moves=[Move(name="scratch", type="normal",
                                         pp=20, accuracy=80, power=15),
                                    Move(name="leer", type="normal",
                                         pp=30, accuracy=100, power=50),
                                    Move(name="ember", type="fire",
                                         pp=20, accuracy=85, power=25),
                                    Move(name="fly", type="fly",
                                         pp=15, accuracy=100, power=60)]
                             )
squirtle_pokemon = Pokemon(hp=50, type=["water"], lvl=5,
                           attack=50, defense=20,
                           speed=1, name="squirtle",
                           moves=[Move(name="scratch", type="normal",
                                       pp=20, accuracy=90, power=10),
                                  Move(name="leer", type="normal",
                                       pp=30, accuracy=100, power=35),
                                  Move(name="ember", type="fire",
                                       pp=20, accuracy=85, power=40),
                                  Move(name="fly", type="fly",
                                       pp=15, accuracy=100, power=50)]
                           )
squirtle_pokemon.apply_status("paralysis")
charmander_pokemon.apply_status("sleep")

principal_stats_box = BattleStatsBox(charmander_pokemon, False,
                                     smallfont, defaultfont)
enemy_stats_box = BattleStatsBox(squirtle_pokemon, True,
                                 smallfont, defaultfont)

battle_handler = Battle(charmander_pokemon, squirtle_pokemon)
battle_choice = BattleOptionsBox(charmander_pokemon, battle_handler, defaultfont,
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
