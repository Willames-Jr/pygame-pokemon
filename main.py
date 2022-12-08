import pygame
import sys
import json
import random
from models.pokemon import Pokemon
from models.move import Move
from models.battle import Battle
from models.type import Type
from models.non_volatile_status import NonVolatileStatus
from components.battle_stats_box import BattleStatsBox
from components.battle_options_box import BattleOptionsBox
from loaders.data_loader import DataLoader

data_loader = DataLoader()

types = data_loader.load_types("./storage/types.json")
moves = data_loader.load_moves("./storage/moves.json")
pokemons = data_loader.load_pokemons("./storage/pokemons.json")

pygame.init()

screen = pygame.display.set_mode((900, 596))
background = pygame.image.load("assets/images/grass_background.png").convert()
background_box = background.get_rect()
background_box.height = 416
background_box.width = 900

default_font = pygame.font.Font("assets/fonts/poke_font.ttf", 50)
log_font = pygame.font.Font("assets/fonts/poke_font.ttf", 65)
medium_font = pygame.font.Font("assets/fonts/poke_font.ttf", 55)
small_font = pygame.font.Font("assets/fonts/poke_font.ttf", 45)

enemy_pokemon_number = int(random.uniform(1, 10))
principal_pokemon_number = enemy_pokemon_number
while principal_pokemon_number == enemy_pokemon_number:
    principal_pokemon_number = int(random.uniform(1, 10))


principal_pokemon = list(pokemons.values())[principal_pokemon_number]
enemy_pokemon = list(pokemons.values())[enemy_pokemon_number]


principal_stats_box = BattleStatsBox(principal_pokemon, False,
                                     small_font, default_font)
enemy_stats_box = BattleStatsBox(enemy_pokemon, True,
                                 small_font, default_font)

battle_handler = Battle(principal_pokemon, enemy_pokemon)
battle_choice = BattleOptionsBox(principal_pokemon, enemy_pokemon, battle_handler, default_font, log_font,
                                 medium_font,
                                 principal_stats_box,
                                 enemy_stats_box,
                                 pygame.image.load(principal_pokemon.back_image),
                                 pygame.image.load(enemy_pokemon.front_image))

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
