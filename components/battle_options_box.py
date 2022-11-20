import pygame
from models.pokemon import Pokemon
from models.battle import Battle
from models.battle import BattleResults
from components.battle_stats_box import BattleStatsBox


class BattleOptionsBox(pygame.sprite.Sprite):
    def __init__(self, pokemon: Pokemon,
                 battle_handler: Battle,
                 font: pygame.font.Font,
                 small_font: pygame.font.Font,
                 principal_bar: BattleStatsBox,
                 enemy_bar: BattleStatsBox):
        self._font_color = 66, 66, 66
        self._battle_handler = battle_handler
        self._need_reload = True
        self.box = pygame.image.load("assets/images/combat_choice.png").convert()
        self.box_position = (0, 416)
        self.move_pp = None
        self._is_in_battle = False
        self.move_type = None
        # Não implementado
        self._actual_screen = "main"
        self.choice_arrow = pygame.image.load("assets/images/choice_arrow.png").convert()
        self._pokemon_moves = pokemon.moves
        self._pokemon = pokemon
        self._default_font = font
        self._small_font = small_font
        self._log_time = 0
        # TODO: Retirar essas barras daqui
        self._principal_pokemon_status_bar = principal_bar
        self._enemy_pokemon_status_bar = enemy_bar
        self._actual_message = ""
        self._battle_results = BattleResults()
        self.actual_arrow_position = 0
        self.arrow_positions = [
            [480, 460], [690, 460],
            [480, 520], [690, 520]
        ]

        self._message1 = self._default_font.render("What will", True,
                                                   (255, 255, 255))
        self._message2 = self._default_font.render(f"{self._pokemon.name.upper()} do?", True, (255, 255, 255))
        self._move1 = self._default_font.render(f"{self._pokemon.moves[0].name.upper()}", True, self._font_color)
        self._move2 = self._default_font.render(f"{self._pokemon.moves[2].name.upper()}", True, self._font_color)
        self._move3 = self._default_font.render(f"{self._pokemon.moves[1].name.upper()}", True, self._font_color)
        self._move4 = self._default_font.render(f"{self._pokemon.moves[3].name.upper()}", True, self._font_color)
        self.pp = self._small_font.render(f"pp", True, (0, 0, 0))
        self.box.blit(self._message1, (40, 30))
        self.box.blit(self._message2, (40, 80))

    def comandHandler(self, comands):
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
            self.move_pp = pygame.font.Font("assets/fonts/poke_font.ttf", 55).render(f"{self._pokemon_moves[self.actual_arrow_position].pp}/{self._pokemon_moves[self.actual_arrow_position].pp}", True, (0, 0, 0))
            self.move_type = pygame.font.Font("assets/fonts/poke_font.ttf", 55).render(f"type/{self._pokemon_moves[self.actual_arrow_position].type.upper()}", True, self._font_color)

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

                    self.move_pp = pygame.font.Font("assets/fonts/poke_font.ttf", 55).render(f"{self._pokemon_moves[self.actual_arrow_position].pp}/{self._pokemon_moves[self.actual_arrow_position].pp}", True, (0, 0, 0))
                    self.move_type = pygame.font.Font("assets/fonts/poke_font.ttf", 55).render(f"type/{self._pokemon_moves[self.actual_arrow_position].type.upper()}", True, self._font_color)
            elif self._actual_screen == "battle":
                #TODO: EXIBIR MENSAGENS
                #TODO: Outra classe tem que tomar conta de todo o proceso de batalha
                self._battle_results = self._battle_handler.battle(self._pokemon.moves[self.actual_arrow_position])
                print(self._battle_results)

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

    def draw(self, surface):
        self._principal_pokemon_status_bar.draw(surface)
        self._enemy_pokemon_status_bar.draw(surface)
        #print(len(self._battle_results.actions), self._log_time)
        if len(self._battle_results.actions) > 0 and self._log_time == 0:
            action = self._battle_results.actions[0]
            if action.is_enemy:
                self._principal_pokemon_status_bar.health_modify(-action.enemy_damage)
            else:
                self._enemy_pokemon_status_bar.health_modify(-action.enemy_damage)
            self._battle_results.actions.remove(action)
            if len(self._battle_results.actions) == 0:
                self._actual_screen = "main"
                self._need_reload = True
            self.box = pygame.image.load("assets/images/battle_dialog.png").convert()
            print(action.message)
            self._actual_message = self._default_font.render(f"{action.message}", True, (255, 255, 255))
            self.box.blit(self._actual_message, (37, 25))
            surface.blit(self.box, self.box_position)
            self._log_time = 300
            return
        elif len(self._battle_results.actions) >= 0 and 0 < self._log_time <= 300:
            self._log_time -= 1
            self.box.blit(self._actual_message, (37,25))
            surface.blit(self.box, self.box_position)
            
            return

        if self._actual_screen == "main":
            self.box.fill((0, 0, 0))
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
            if self._need_reload:
                self.actual_arrow_position = 0
                self._need_reload = False
            surface.blit(self.box,  self.box_position)
            surface.blit(self.choice_arrow,
                         self
                         .arrow_positions[self.actual_arrow_position])
        elif self._actual_screen == "battle":
            surface.blit(self.box,  self.box_position)
            surface.blit(self._move1, (70, 444))
            surface.blit(self._move2, (70, 500))
            surface.blit(self._move3, (345, 444))
            surface.blit(self._move4, (345, 500))
            surface.blit(self.pp, (630, 440))
            surface.blit(self.move_pp, (745, 450))
            surface.blit(self.move_type, (630, 510))            
            surface.blit(self.choice_arrow,
                         self
                         .arrow_positions[self.actual_arrow_position])
