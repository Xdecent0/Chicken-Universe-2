import pygame
import random

class GameObject:
    def __init__(self, image_path, position, size=None):
        self.image = pygame.image.load(image_path)
        
        if size is not None:
            self.image = pygame.transform.scale(self.image, size)
            
        self.position = position
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Player(GameObject):
    def __init__(self, image_path, position, size=None, upper_limit=None, lower_limit=None, left_limit=None, right_limit=None):
        super().__init__(image_path, position, size)
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.selectedRaceIndex = 0
        self.selectedSkinIndex = 0
        self.lives = 1

        self.rect.width = 30 
        self.rect.height = 50

    def move(self, direction, speed, inversion=False):
        if inversion:
            if direction == "down" and (self.upper_limit is None or self.rect.y - speed >= self.upper_limit):
                self.rect.y -= speed
            elif direction == "up" and (self.lower_limit is None or self.rect.y + speed <= self.lower_limit):
                self.rect.y += speed
            elif direction == "right" and (self.left_limit is None or self.rect.x - speed >= self.left_limit):
                self.rect.x -= speed
            elif direction == "left" and (self.right_limit is None or self.rect.x + speed <= self.right_limit):
                self.rect.x += speed
        else:
            if direction == "up" and (self.upper_limit is None or self.rect.y - speed >= self.upper_limit):
                self.rect.y -= speed
            elif direction == "down" and (self.lower_limit is None or self.rect.y + speed <= self.lower_limit):
                self.rect.y += speed
            elif direction == "left" and (self.left_limit is None or self.rect.x - speed >= self.left_limit):
                self.rect.x -= speed
            elif direction == "right" and (self.right_limit is None or self.rect.x + speed <= self.right_limit):
                self.rect.x += speed


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image_path, position, size=(30, 30), speed=5, delete_x= 200):
        super().__init__()

        self.image = pygame.image.load(image_path)
        if size is not None:
            self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.delete_x = delete_x
        self.rect.height = int(self.rect.height * 0.9)

    def move(self):
        self.rect.x -= self.speed

        if self.delete_x is not None and self.rect.right < self.delete_x:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class SmallRocks(Obstacle):
    def __init__(self, image_path, size=(130, 50), speed=5, delete_x=250):
        y_choice = random.choice([1, 2])

        if y_choice == 1:
            position = (1100, 84)
        else:
            position = (1100, 536)

        super().__init__(image_path, position, size, speed, delete_x)

        if y_choice == 1:
            self.image = pygame.transform.rotate(self.image, 180)

        self.rect = pygame.Rect(self.rect.x, self.rect.y, 80, 30)

class Coin(pygame.sprite.Sprite):
    def __init__(self, image_path, position, size=(25, 30), speed=5, delete_x=200):
        super().__init__()
        self.speed = speed
        self.delete_x = delete_x
        self.image = pygame.image.load(image_path)
        if size is not None:
            self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect(center=position)

    def move(self):
        self.rect.x -= self.speed
        if self.delete_x is not None and self.rect.right < self.delete_x:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Egg(Coin):
    def __init__(self, image_path, position, size=(25, 30), speed=5, delete_x=200):
        super().__init__(image_path, position, size, speed, delete_x)











