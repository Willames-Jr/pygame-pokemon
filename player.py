import pygame


class Player:
    def __init__(self, moveKeys=[pygame.K_UP, pygame.K_DOWN,
                 pygame.K_LEFT, pygame.K_RIGHT]):
        self._upKey = moveKeys[0]
        self._downKey = moveKeys[1]
        self._leftKey = moveKeys[2]
        self._rightKey = moveKeys[3]
        self._upCount = 0
        self._downCount = 0
        self._leftCount = 0
        self._rightCount = 0
        self.char = pygame.image.load('assets/images/char_front.png').convert()
        self.char_box = self.char.get_rect()

    def move(self, moveDirection):

        x, y = self.char_box.x,  self.char_box.y
        if moveDirection == "down":
            print("pra baixo")
            self._downCount += 1
            if self._downCount == 1:
                self.char = pygame.image.load('assets/images/char_front_walk2.png').convert()
                self.char_box = self.char.get_rect()
            elif self._downCount == 2:
                self.char = pygame.image.load('assets/images/char_front_stand.png').convert()
                self.char_box = self.char.get_rect()
            elif self._downCount == 3:
                self.char = pygame.image.load('assets/images/char_front_walk.png').convert()
                self.char_box = self.char.get_rect()
            self.char_box.move_ip(x, y)
            self.char_box = self.char_box.move(0, 1)
            if self._downCount == 3:
                self._downCount = 0
            return
        else:
            if self._downCount != 2:
                self._downCount = 0
                self.char = pygame.image.load('assets/images/char_front_stand.png').convert()
                self.char_box = self.char.get_rect()
                self.char_box.move_ip(x, y)

        if moveDirection == "up":
            self._upCount += 1
            if self._upCount == 1:
                self.char = pygame.image.load('assets/images/char_back_walk2.png').convert()
                self.char_box = self.char.get_rect()
            elif self._upCount == 2:
                self.char = pygame.image.load('assets/images/char_back_stand.png').convert()
                self.char_box = self.char.get_rect()
            elif self._upCount == 3:
                self.char = pygame.image.load('assets/images/char_back_walk.png').convert()
                self.char_box = self.char.get_rect()
            self.char_box.move_ip(x, y)
            self.char_box = self.char_box.move(0, -1)
            if self._upCount == 3:
                self._upCount = 0
            return
        else:
            if self._upCount != 2:
                self._upCount = 0
                self.char = pygame.image.load('assets/images/char_back_stand.png').convert()
                self.char_box = self.char.get_rect()
                self.char_box.move_ip(x, y)

        if moveDirection == "left":
            self._leftCount += 1
            if self._leftCount == 1:
                self.char = pygame.image.load('assets/images/char_left_walk2.png').convert()
                self.char_box = self.char.get_rect()
            elif self._leftCount == 2:
                self.char = pygame.image.load('assets/images/char_left_stand.png').convert()
                self.char_box = self.char.get_rect()
            elif self._leftCount == 3:
                self.char = pygame.image.load('assets/images/char_left_walk.png').convert()
                self.char_box = self.char.get_rect()
            self.char_box.move_ip(x, y)
            self.char_box = self.char_box.move(-1, 0)
            if self._leftCount == 3:
                self._leftCount = 0
            return
        else:
            if self._leftCount != 2:
                self._leftCount = 0
                self.char = pygame.image.load('assets/images/char_left_stand.png').convert()
                self.char_box = self.char.get_rect()
                self.char_box.move_ip(x, y)

        if moveDirection == "right":
            self._rightCount += 1
            if self._rightCount == 1:
                self.char = pygame.image.load('assets/images/char_right_walk2.png').convert()
                self.char_box = self.char.get_rect()
            elif self._rightCount == 2:
                self.char = pygame.image.load('assets/images/char_right_stand.png').convert()
                self.char_box = self.char.get_rect()
            elif self._rightCount == 3:
                self.char = pygame.image.load('assets/images/char_right_walk.png').convert()
                self.char_box = self.char.get_rect()
            self.char_box.move_ip(x, y)
            self.char_box = self.char_box.move(1, 0)
            if self._rightCount == 3:
                self._rightCount = 0
            return
        else:
            if self._rightCount != 2:
                self._rightCount = 0
                self.char = pygame.image.load('assets/images/char_right_stand.png').convert()
                self.char_box = self.char.get_rect()
                self.char_box.move_ip(x, y)
