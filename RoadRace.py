import pygame
import sys
import os
import random


class MainMenu:
    def __init__(self):
        bg = load_image('main_menu_bg.jpg', SCREEN_SIZE)
        font = pygame.font.Font('data/fonts/impact.ttf', 50)
        text = font.render('Enter "Space" to start game!', True, pygame.Color('white'))
        screen.blit(bg, (0, 0))
        screen.blit(text, (70, 250))


class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()

        self.player = pygame.sprite.Sprite()
        self.player.image = load_image('player5.jpg', [90, 130])
        self.player.rect = self.player.image.get_rect()
        self.player.rect.x, self.player.rect.y = 300, 300

        self.is_move = [False, False]

        self.box_base = list()

        self.all_sprites.add(self.player)

        self.bg = load_image('road.jpg', SCREEN_SIZE)

        screen.blit(self.bg, (0, 0))

        self.render_counter, self.render_speed, self.speed_x, self.speed_y = int(), 150, 3, 1

    def loop_event(self):
        self.render_counter += 1

        if self.render_counter >= self.render_speed:
            self.box_base.append(pygame.sprite.Sprite())
            self.box_base[-1].image = load_image('box1.jpg', [55, 55])
            self.box_base[-1].rect = self.box_base[-1].image.get_rect()
            self.box_base[-1].rect.x, self.box_base[-1].rect.y = random.randint(0, 700), random.randint(0, 0)
            self.all_sprites.add(self.box_base[-1])
            self.render_counter = int()
            if self.render_speed > 60:
                self.render_speed -= 10
            if self.speed_y < 12:
                self.speed_y += 1

        for i in range(len(self.box_base)):
            self.box_base[i].rect.y += self.speed_y

        if self.is_move[0]:
            self.player.rect.x -= self.speed_x
        elif self.is_move[1]:
            self.player.rect.x += self.speed_x

        screen.blit(self.bg, (0, 0))

        self.all_sprites.draw(screen)


class GameOver:
    def __init__(self):
        bg = load_image('game_over_bg.jpg', SCREEN_SIZE)

        screen.blit(bg, (0, 0))


def load_image(name, size=False, rotate=False):
    full_name = os.path.join('data', name)

    image = pygame.image.load(full_name)
    image.set_colorkey(image.get_at((0, 0)))

    if type(size) == list:
        image = pygame.transform.scale(image, size)

    return image


if __name__ == '__main__':
    pygame.init()

    SCREEN_SIZE = [700, 600]

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('RoadRace')

    clock, FPS = pygame.time.Clock(), 30

    controller = 0
    if controller == 0:
        scene = MainMenu()
    elif controller == 1:
        scene = Game()
    elif controller == 2:
        scene = GameOver()

    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit(0)
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_LEFT:
                    if controller == 1:
                        scene.is_move[0] = not scene.is_move[0]
                if i.key == pygame.K_RIGHT:
                    if controller == 1:
                        scene.is_move[1] = not scene.is_move[1]
                if i.key == pygame.K_SPACE:
                    if controller == 0:
                        controller = 1
                        scene = Game()
            if i.type == pygame.KEYUP:
                if controller == 1:
                    if i.key == pygame.K_LEFT:
                        scene.is_move[0] = not scene.is_move[0]
                    if i.key == pygame.K_RIGHT:
                        scene.is_move[1] = not scene.is_move[1]

        if controller == 1:
            scene.loop_event()

        pygame.display.flip()

        clock.tick(FPS)
