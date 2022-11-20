import pygame
from models.pokemon import Pokemon
from models.battle import Battle


class BattleOptionsBox(pygame.sprite.Sprite):
    def __init__(self, pokemon: Pokemon,
                 battle_handler: Battle,
                 font: pygame.font.Font,
                 small_font: pygame.font.Font):
        self._font_color = 66, 66, 66
        self._battle_handler = battle_handler
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
                #TODO: animação de dano
                battle_result = self._battle_handler.battle(self._pokemon.moves[self.actual_arrow_position])
                print(battle_result)

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
