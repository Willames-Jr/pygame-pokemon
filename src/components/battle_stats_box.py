from typing import Dict, List, Tuple
import pygame
from pygame.font import Font
from pygame.surface import Surface
from models.pokemon import Pokemon


class BattleStatsBox(pygame.sprite.Sprite):

    def __init__(self, pokemon: Pokemon, is_enemy_pokemon: bool,
                 small_font: pygame.font.Font,
                 default_font: pygame.font.Font, *groups) -> None:
        super(BattleStatsBox, self).__init__(*groups)
        self._life_bar: Surface = pygame.image.load("assets/images/green_life.png")
        self.box_position: List[int] = [0, 0]
        self._font_color: Tuple[int, int, int] = (66, 66, 66)
        self._pokemon: Pokemon = pokemon
        self._pokemon_total_life: int = pokemon.hp
        self.pokemon_actual_life: int = pokemon.hp
        self._pokemon_lvl: int = pokemon.lvl
        self._pokemon_name: str = pokemon.name
        self._pokemon_xp: int = pokemon.xp
        self._pokemon_gender: str = pokemon.gender
        self._default_font: Font = default_font
        self._small_font: Font = small_font
        self._is_enemy_pokemon: bool = is_enemy_pokemon
        self.life_diff: int = 0
        self._actual_life_diff: int = 0
        self._animation_counter: int = 0
        self._status_images: Dict[str, str] = {
            "burn": "assets/images/burned.png",
            "poison": "assets/images/poisoned.png",
            "paralysis": "assets/images/paralysis.png",
            "freeze": "assets/images/frozen.png",
            "sleep": "assets/images/sleep.png"
        }

        # Medidadas para o pokemon principal e inimigo
        self._enemy_life_position: Tuple[int, int] = (138, 63)
        self._principal_pokemon_life_position: Tuple[int, int] = (162, 58)
        self._enemy_pokemon_status_position: Tuple[int, int] = (20, 55)
        self._principal_pokemon_status_position: Tuple[int, int] = (45, 73)

        # Guarda o life antes e depois de tomar dano/heal
        # self._life_interval: int = 0
        self.image, self.rect_size = self.make_image()
        self._life_bar_pixels: int = self._life_bar.get_width()
        self._life_p_pixel: float = (self._life_bar.get_width() /
                                     self._pokemon_total_life)
        self.redraw: bool = True

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

    def make_image(self, life_change=False, changed_pixels=0):
        critical_life = self._pokemon_total_life * 0.25
        caution_life = self._pokemon_total_life * 0.50
        pokemon_non_volatile_status = self._pokemon.has_non_volatile_status()
        pokemon_name = self._small_font.render(self._pokemon_name.upper(),
                                               True, self._font_color)
        pokemon_lvl = self._small_font.render(str(self._pokemon_lvl),
                                              True, self._font_color)

        if critical_life < self.pokemon_actual_life <= caution_life:
            self._life_bar = pygame.image.load("assets/images/yellow_life.png")
        elif critical_life >= self.pokemon_actual_life:
            self._life_bar = pygame.image.load("assets/images/red_life.png")
        else:
            self._life_bar = pygame.image.load("assets/images/green_life.png")
        if self._is_enemy_pokemon:
            image = pygame.image.load("assets/images/enemy_stats.png")
            image.blit(pokemon_name, (20, 13))
            image.blit(pokemon_lvl, (265, 13))
            life_position = self._enemy_life_position
            non_volatile_status_position = self._enemy_pokemon_status_position
            box_position = (50, 60)
        else:
            image = pygame.image.load("assets/images/pokemon_stats.png")
            actual_life = self._small_font.render(str(self.pokemon_actual_life),
                                                  True, self._font_color)
            total_life = self._small_font.render(str(self._pokemon_total_life),
                                                 True, self._font_color)

            image.blit(pokemon_name, (50, 7))
            image.blit(actual_life, (205, 68))
            image.blit(total_life, (280, 68))
            image.blit(pokemon_lvl, (280, 7))
            life_position = self._principal_pokemon_life_position
            non_volatile_status_position = self._principal_pokemon_status_position

            box_position = (525, 285)

        if life_change:
            new_life = self._life_bar.subsurface(pygame.Rect(0, 0,
                                                 self._life_bar.get_width()
                                                 - changed_pixels,
                                                 self._life_bar.get_height()))
            image.blit(new_life, life_position)
        else:
            image.blit(self._life_bar, life_position)

        if pokemon_non_volatile_status is not None:
            status_image = pygame.image.load(self._status_images[
                pokemon_non_volatile_status.name])
            image.blit(status_image, non_volatile_status_position)

        self.redraw = False
        return image, box_position

    def draw(self, surface):
        if not self._is_enemy_pokemon:
            if 80 > self._animation_counter > 0:
                self.rect_size = [525, 285]
                self._animation_counter += 1
            else:
                if self._animation_counter > 0:
                    self._animation_counter -= 180
                self.rect_size = [525, 290]
                self._animation_counter += 1

        # Altera a barra de vida enquanto a diferenca de vida for diferente de 0
        if self.life_diff > 0 and self.pokemon_actual_life > 0:
            self.pokemon_actual_life -= 1
            self.life_diff -= 1
            pixel_changed = self._life_bar_pixels - (self.pokemon_actual_life * self._life_p_pixel)
            self.image = self.make_image(life_change=True, changed_pixels=int(pixel_changed))[0]

        if self.pokemon_actual_life != 0:
            surface.blit(self.image, self.rect)

    def health_modify(self, value):
        # calcula a diferenca entre a vida atual e a vida que o pokemon ter?? ao receber o dano/cura
        self.life_diff = (self.pokemon_actual_life - (value + self.pokemon_actual_life))
