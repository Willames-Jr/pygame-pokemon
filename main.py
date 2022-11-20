import pygame
import sys
from models.pokemon import Pokemon
from models.move import Move
from models.battle import Battle
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
pkMove1 = 0


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
                                         pp=15, accuracy=100, power=60)])
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
                                       pp=15, accuracy=100, power=50)])
principal_stats_box = BattleStatsBox(charmander_pokemon, False,
                                     smallfont, defaultfont)
enemy_stats_box = BattleStatsBox(squirtle_pokemon, True,
                                 smallfont, defaultfont)

battle_handler = Battle(charmander_pokemon, squirtle_pokemon)
battle_choice = BattleOptionsBox(charmander_pokemon, battle_handler, defaultfont,
                                 pygame.font.Font("assets/fonts/poke_font.ttf",
                                                  55),
                                 principal_stats_box,
                                 enemy_stats_box)
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

    if pkMove1 < 100 and pkMove1 > 0:
        first_pokemon[1] = 193
        pkMove1 += 1
    else:
        if pkMove1 > 0:
            pkMove1 = -100
        first_pokemon[1] = 187
        pkMove1 += 1

    #principal_stats_box.position_animation()
    # if count == 0 and principal_stats_box.life_diff == 0:
    #     principal_stats_box.health_modify(5)
    #     enemy_stats_box.health_modify(-20)
    #     count += 1
    # principal_stats_box.draw(screen)
    # enemy_stats_box.draw(screen)
    screen.fill((0, 0, 0))
    screen.blit(background,  background_box)
    #screen.blit(enemy_stats_box.box, enemy_stats_box.box_position)
    screen.blit(charmander,  first_pokemon)
    screen.blit(squirtle,  (530, 50))
    battle_choice.draw(screen)
    #screen.blit(principal_stats_box.box, principal_stats_box.box_position)
    #screen.blit(battle_choice.box,  battle_choice.box_position)
    #screen.blit(battle_choice.choice_arrow,
    #             battle_choice
    #             .arrow_positions[battle_choice.actual_arrow_position])
    
    # if battle_choice._actual_screen == "battle":
    #     screen.blit(battle_choice._move1, (70, 444))
    #     screen.blit(battle_choice._move2, (70, 500))
    #     screen.blit(battle_choice._move3, (345, 444))
    #     screen.blit(battle_choice._move4, (345, 500))

    #     screen.blit(battle_choice.pp, (630, 440))
    #     screen.blit(battle_choice.move_pp, (745, 450))
    #     screen.blit(battle_choice.move_type, (630, 510))
    #screen.blit(player.char, player.char_box)
    #all_sprites.draw(screen)
    pygame.display.flip()
