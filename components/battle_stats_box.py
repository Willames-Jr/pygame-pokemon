import pygame
from attrs import define
from models.pokemon import Pokemon
from typing import Tuple
from time import sleep


class BattleStatsBox(pygame.sprite.Sprite):
    # box_position:  Tuple[int, int]
    # _pokemon_total_life:  int
    # _pokemon_actual_life:  int
    # _pokemon_lvl:  int
    # _pokemon_name:  str
    # _pokemon_xp:  int
    # # Por enquanto não é usado
    # _pokemon_gender:  str
    # box:  pygame.image
    # _life_bar:  pygame.image
    # # Por enquanto não é usado
    # _xp_bar:  pygame.image
    # _font_color = 66, 66, 66
    # _small_font:  pygame.font.Font
    # _default_font:  pygame.font.Font
    # _is_enemy_pokemon:  bool = False
    # _animation_counter:  int = 0

    def __init__(self, pokemon: Pokemon, is_enemy_pokemon: bool,
                 small_font: pygame.font.Font,
                 default_font: pygame.font.Font, *groups) -> None:
        super(BattleStatsBox, self).__init__(*groups)
        self._life_bar = pygame.image.load("assets/images/green_life.png")
        self.box_position = None
        self._font_color = 66, 66, 66
        self._pokemon_total_life = pokemon.hp
        self._pokemon_actual_life = pokemon.hp
        self._pokemon_lvl = pokemon.lvl
        self._pokemon_name = pokemon.name
        self._pokemon_xp = pokemon.xp
        self._pokemon_gender = pokemon.gender
        self._default_font = default_font
        self._small_font = small_font
        self._is_enemy_pokemon = is_enemy_pokemon
        self.life_diff = None
        self._actual_life_diff = 0
        self._animation_counter = 0
        # Guarda o life antes e depois de tomar dano/heal
        self._life_interval = None
        self.image, self.rect = self.make_image()
        self._life_p_pixel = (self._life_bar.get_width() /
                              self._pokemon_total_life)
        self.redraw = True

    def position_animation(self):
        if self._is_enemy_pokemon:
            return
        if 80 > self._animation_counter > 0:
            self.box_position = [525, 285]
            self._animation_counter += 1
        else:
            if self._animation_counter > 0:
                self._animation_counter -= 180
            self.box_position = [525, 290]
            self._animation_counter += 1

    def make_image(self, life_change=False,changed_pixels=0):
        critical_life = self._pokemon_total_life * 0.25
        caution_life = self._pokemon_total_life * 0.50
        if critical_life < self._pokemon_actual_life <= caution_life:
            self._life_bar = pygame.image.load("assets/images/yellow_life.png")
        elif critical_life >= self._pokemon_actual_life:
            self._life_bar = pygame.image.load("assets/images/red_life.png")
        else:
            self._life_bar = pygame.image.load("assets/images/green_life.png")
        if self._is_enemy_pokemon:
            image = pygame.image.load("assets/images/enemy_stats.png")
            pokemon_name = self._small_font.render(self._pokemon_name.upper(),
                                                   True, self._font_color)
            pokemon_lvl = self._small_font.render(str(self._pokemon_lvl),
                                                  True, self._font_color)

            image.blit(pokemon_name, (20, 13))
            if life_change:
                new_life = self._life_bar.subsurface(pygame.Rect(0, 0,
                                                     self._life_bar.get_width() - changed_pixels, 
                                                     self._life_bar.get_height()))
                image.blit(new_life, (138, 63))
            else:
                image.blit(self._life_bar, (138, 63))
            image.blit(pokemon_lvl, (265, 13))
            box_position = (50, 60)
        else:
            image = pygame.image.load("assets/images/pokemon_stats.png")
            pokemon_name = self._small_font.render(self._pokemon_name.upper(),
                                                   True, self._font_color)
            pokemon_lvl = self._small_font.render(str(self._pokemon_lvl), True,
                                                  self._font_color)
            actual_life = self._small_font.render(str(self._pokemon_actual_life),
                                                  True, self._font_color)
            total_life = self._small_font.render(str(self._pokemon_total_life),
                                                 True, self._font_color)

            image.blit(pokemon_name, (50, 7))
            image.blit(actual_life, (210, 68))
            image.blit(total_life, (285, 68))
            image.blit(pokemon_lvl, (280, 7))
            if life_change:
                new_life = self._life_bar.subsurface(pygame.Rect(0, 0,
                                                     self._life_bar.get_width()  - changed_pixels, 
                                                     self._life_bar.get_height()))
                image.blit(new_life, (162, 58))
            else:
                image.blit(self._life_bar, (162, 58))
            #image.blit(self._life_bar, (162, 58))

            box_position = (525, 285)

        self.redraw = False
        return image, box_position

    def draw(self, surface):
        if self._is_enemy_pokemon:
            return
        if 80 > self._animation_counter > 0:
            self.rect = [525, 285]
            self._animation_counter += 1
        else:
            if self._animation_counter > 0:
                self._animation_counter -= 180
            self.rect = [525, 290]
            self._animation_counter += 1

        #for i in range(self._life_interval[0], self._life_interval[1]):

        if self.life_diff != self._actual_life_diff and self._pokemon_actual_life > 0:
            
            self._pokemon_actual_life -= 1
            self._actual_life_diff += 1
            pixel_changed = self._actual_life_diff * self._life_p_pixel
            self.image = self.make_image(life_change=True,changed_pixels=pixel_changed)[0]
        else:
            self.life_diff = self._actual_life_diff
        print(self.life_diff,self._actual_life_diff)
        print(self.life_diff == self._actual_life_diff)
        surface.blit(self.image, self.rect)

    def health_modify(self, value):
        print(value)
        #final_life = value + self._pokemon_actual_life
        #self.pixel_diff = self._life_bar.get_width() - ((self._life_bar.get_width()*final_life)/self._pokemon_total_life)
        self.life_diff = (self._pokemon_actual_life - (value + self._pokemon_actual_life))

    # Atualmente somente produz animações de dano
    # def make_image(self, damage=None):
    #     if damage != None:
    #         self.image.