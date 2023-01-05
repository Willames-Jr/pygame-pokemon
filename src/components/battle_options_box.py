from typing import List, Tuple
import pygame
from pygame.font import Font
from pygame.surface import Surface
from models.move import Move
from models.pokemon import Pokemon
from models.battle import Battle
from models.battle import BattleResults
from components.battle_stats_box import BattleStatsBox


class BattleOptionsBox(pygame.sprite.Sprite):
    def __init__(self, pokemon: Pokemon, enemy_pokemon: Pokemon,
                 battle_handler: Battle,
                 font: pygame.font.Font,
                 log_font: pygame.font.Font,
                 small_font: pygame.font.Font,
                 principal_bar: BattleStatsBox,
                 enemy_bar: BattleStatsBox,
                 principal_pokemon_sprite: pygame.surface.Surface,
                 enemy_pokemon_sprite: pygame.surface.Surface):
        self._font_color: Tuple[int, int, int] = (66, 66, 66)
        self._battle_handler: Battle = battle_handler
        self._need_reload: bool = True
        self.box: Surface = pygame.image.load("assets/images/combat_choice.png").convert()
        self.box_position: Tuple[int, int] = (0, 416)
        self._is_in_battle: bool = False
        # Não implementado
        self._actual_screen: str = "main"
        self.choice_arrow: Surface = pygame.image.load("assets/images/choice_arrow.png").convert()
        self._pokemon_moves: List[Move] = pokemon.moves
        self._pokemon: Pokemon = pokemon
        self._enemy_pokemon: Pokemon = enemy_pokemon
        self._default_font: Font = font
        self._small_font: Font = small_font
        self._log_font: Font = log_font
        self._log_time: int = 0
        # TODO: Retirar essas barras daqui
        self._principal_pokemon_status_bar: BattleStatsBox = principal_bar
        self._enemy_pokemon_status_bar: BattleStatsBox = enemy_bar
        self.move_pp: Surface
        self.move_type: Surface
        self._actual_message: Surface
        self._battle_results: BattleResults = BattleResults()
        self.actual_arrow_position: int = 0
        self.arrow_positions: List[List[int]] = [
            [480, 460], [690, 460],
            [480, 520], [690, 520]
        ]
        self._principal_pokemon_sprite: Surface = principal_pokemon_sprite
        self._enemy_pokemon_sprite: Surface = enemy_pokemon_sprite
        self._pokemon_move: int = 0
        self._pokemon_actual_faint_time: int = 0
        self._total_faint_time: int = 500
        self._fainted: str = ""
        self._principal_pokemon_sprite_position: List[int] = [80, 270]
        self._enemy_pokemon_sprite_position: Tuple[int, int] = (530, 20)

        self._message1: Surface = self._default_font.render("What will", True,
                                                            (255, 255, 255))
        self._message2: Surface = self._default_font.render(f"{self._pokemon.name.upper()} do?", True, (255, 255, 255))
        self._move1: Surface = self._default_font.render(f"{self._pokemon.moves[0].name.upper()}", True, self._font_color)
        self._move2: Surface = self._default_font.render(f"{self._pokemon.moves[2].name.upper()}", True, self._font_color)
        self._move3: Surface = self._default_font.render(f"{self._pokemon.moves[1].name.upper()}", True, self._font_color)
        self._move4: Surface = self._default_font.render(f"{self._pokemon.moves[3].name.upper()}", True, self._font_color)
        self.pp: Surface = self._small_font.render("pp", True, (0, 0, 0))
        self.box.blit(self._message1, (40, 30))
        self.box.blit(self._message2, (40, 80))

    def comandHandler(self, comands):
        if self._block_interaction:
            return
        if (comands[pygame.K_DOWN] or comands[pygame.K_UP]
                or comands[pygame.K_LEFT] or comands[pygame.K_DOWN]
                or comands[pygame.K_RIGHT]):
            self._moveArrow(comands)
        if comands[pygame.K_z] or comands[pygame.K_x]:
            self._make_choice(comands)

    def _moveArrow(self, comands):

        if comands[pygame.K_DOWN] and self.actual_arrow_position in [0, 1]:
            self.actual_arrow_position += 2

        if comands[pygame.K_UP] and self.actual_arrow_position in [2, 3]:
            self.actual_arrow_position -= 2

        if comands[pygame.K_LEFT] and self.actual_arrow_position in [1, 3]:
            self.actual_arrow_position -= 1

        if comands[pygame.K_RIGHT] and self.actual_arrow_position in [0, 2]:
            self.actual_arrow_position += 1
        if self._actual_screen == "battle":
            self.move_pp = pygame.font.Font("assets/fonts/poke_font.ttf", 55)\
                                      .render(f"{self._pokemon_moves[self.actual_arrow_position].pp}/{self._pokemon_moves[self.actual_arrow_position].pp}",
                                              True, (0, 0, 0))
            self.move_type = pygame.font.Font("assets/fonts/poke_font.ttf", 55)\
                                        .render(f"type/{self._pokemon_moves[self.actual_arrow_position].type.name.upper()}", True, self._font_color)

    def _make_choice(self, comands):
        if comands[pygame.K_z]:
            if self._actual_screen == "main":
                if self.actual_arrow_position == 0:
                    self._actual_screen = "battle"
                    self.box = pygame.image.load("assets/images/chose_attack.png").convert()
                    self.arrow_positions = [
                        [40, 460], [315, 460],
                        [40, 514], [315, 514]
                    ]

                    self.move_pp = pygame.font.Font("assets/fonts/poke_font.ttf", 55)\
                                              .render(
                                                f"{self._pokemon_moves[self.actual_arrow_position].pp}/{self._pokemon_moves[self.actual_arrow_position].pp}",
                                                True, (0, 0, 0))
                    self.move_type = pygame.font.Font("assets/fonts/poke_font.ttf", 55)\
                                                .render(f"type/{self._pokemon_moves[self.actual_arrow_position].type.name.upper()}", True, self._font_color)
            elif self._actual_screen == "battle":
                # TODO: Outra classe tem que tomar conta de todo o proceso de batalha
                self._battle_results = self._battle_handler.battle(self._pokemon.moves[self.actual_arrow_position])

        elif comands[pygame.K_x]:
            if self._actual_screen == "battle":
                self._actual_screen = "main"
                self.box = pygame.image.load("assets/images/combat_choice.png").convert()
                self._message1 = self._default_font.render("What will", True,
                                                           (255, 255, 255))
                self._message2 = self._default_font.render(f"{self._pokemon.name.upper()} do?", True,
                                                           (255, 255, 255))
                self.box.blit(self._message1, (40, 30))
                self.box.blit(self._message2, (40, 80))
                self.arrow_positions = [
                    [480, 460], [690, 460],
                    [480, 520], [690, 520]
                ]
                self.actual_arrow_position = 0

    def drawPokemons(self, surface):
        if self._pokemon_move < 100 and self._pokemon_move > 0:
            self._principal_pokemon_sprite_position[1] = 193
            self._pokemon_move += 1
        else:
            if self._pokemon_move > 0:
                self._pokemon_move = -100
            self._principal_pokemon_sprite_position[1] = 187
            self._pokemon_move += 1
        if self._fainted != "principal":
            surface.blit(self._principal_pokemon_sprite, self._principal_pokemon_sprite_position)
        if self._fainted != "enemy":
            surface.blit(self._enemy_pokemon_sprite, self._enemy_pokemon_sprite_position)

    def draw(self, surface):

        # TODO: FAZER ANIMAÇÃO DE FAINT
        self.drawPokemons(surface)

        self._principal_pokemon_status_bar.draw(surface)
        self._enemy_pokemon_status_bar.draw(surface)
        if len(self._battle_results.actions) > 0 and self._log_time == 0:
            action = self._battle_results.actions[0]
            if action.is_enemy:
                self._principal_pokemon_status_bar.health_modify(-action.enemy_damage)
                self._enemy_pokemon_status_bar.health_modify(action.drain)
                if action.enemy_status_change != [] or action.self_status_change != []:
                    for status in action.enemy_status_change:
                        self._pokemon.change_modifiers(status.name, status.value)

                    for status in action.self_status_change:
                        self._enemy_pokemon.change_modifiers(status.name, status.value)
            else:
                self._enemy_pokemon_status_bar.health_modify(-action.enemy_damage)
                self._principal_pokemon_status_bar.health_modify(action.drain)
                # print(action)
                if action.enemy_status_change != [] or action.self_status_change != []:
                    for status in action.enemy_status_change:
                        self._enemy_pokemon.change_modifiers(status.name, status.value)
                    for status in action.self_status_change:
                        self._pokemon.change_modifiers(status.name, status.value)
            # print(self._pokemon.modifiers)
            # print(self._enemy_pokemon.modifiers)
            self._battle_results.actions.remove(action)
            if len(self._battle_results.actions) == 0:
                self._actual_screen = "main"
                self._need_reload = True
            if self._principal_pokemon_status_bar.pokemon_actual_life <= 0:
                self._principal_fainted = True
            if self._enemy_pokemon_status_bar.pokemon_actual_life <= 0:
                self._enemy_fainted = True
            self.box = pygame.image.load("assets/images/battle_dialog.png").convert()
            self._actual_message = self._log_font.render(f"{action.message}", True, (255, 255, 255))
            self.box.blit(self._actual_message, (37, 25))
            surface.blit(self.box, self.box_position)
            # alterar quando sair dos testes
            self._log_time = 300
            self._block_interaction = True
            return
        elif ((len(self._battle_results.actions) >= 0 and 0 < self._log_time <= 300)
              or (self._principal_pokemon_status_bar.pokemon_actual_life <= 0
                  or self._enemy_pokemon_status_bar.pokemon_actual_life <= 0)
              ):
            self._log_time -= 1
            self.box.blit(self._actual_message, (37, 25))
            surface.blit(self.box, self.box_position)
            self._block_interaction = True
            if self._principal_pokemon_status_bar.pokemon_actual_life <= 0:
                self._fainted = "principal"
            elif self._enemy_pokemon_status_bar.pokemon_actual_life <= 0:
                self._fainted = "enemy"
            return

        if self._actual_screen == "main":
            self._block_interaction = False
            self.box.fill((0, 0, 0))
            self.box = pygame.image.load("assets/images/combat_choice.png").convert()
            self._message1 = self._log_font.render("What will", True,
                                                   (255, 255, 255))
            self._message2 = self._log_font.render(f"{self._pokemon.name.upper()} do?", True,
                                                   (255, 255, 255))
            self.box.blit(self._message1, (40, 30))
            self.box.blit(self._message2, (40, 80))
            self.arrow_positions = [
                [480, 460], [690, 460],
                [480, 520], [690, 520]
            ]
            if self._need_reload:
                self.actual_arrow_position = 0
                self._need_reload = False
            surface.blit(self.box,  self.box_position)
            surface.blit(self.choice_arrow,
                         self
                         .arrow_positions[self.actual_arrow_position])
        elif self._actual_screen == "battle":
            self._block_interaction = False
            surface.blit(self.box,  self.box_position)
            surface.blit(self._move1, (70, 452))
            surface.blit(self._move2, (70, 508))
            surface.blit(self._move3, (345, 452))
            surface.blit(self._move4, (345, 508))
            surface.blit(self.pp, (630, 440))
            surface.blit(self.move_pp, (745, 450))
            surface.blit(self.move_type, (630, 510))
            surface.blit(self.choice_arrow,
                         self
                         .arrow_positions[self.actual_arrow_position])
