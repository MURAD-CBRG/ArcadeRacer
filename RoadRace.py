import pygame
import sys
import os
import random
import pygame_gui


class MainMenu:
    def __init__(self):
        self.bg = load_image('main_menu_bg.jpg', SCREEN_SIZE)
        self.font = pygame.font.Font('data/fonts/impact.ttf', 50)
        self.text = self.font.render('Main menu', True, pygame.Color('white'))

    def render_menu(self):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.text, (230, 150))


class Shop:
    def __init__(self):
        pass


class Info:
    def __init__(self):
        pass


class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()

        self.player = pygame.sprite.Sprite()
        self.player.image = load_image('player5.jpg', [90, 130])
        self.player.rect = self.player.image.get_rect()
        self.player.rect.x, self.player.rect.y = 300, 300
        self.player.mask = pygame.mask.from_surface(self.player.image)  ##

        self.is_move = [False, False]

        self.box_base = list()

        self.all_sprites.add(self.player)

        self.bg = load_image('road.jpg', SCREEN_SIZE)

        screen.blit(self.bg, (0, 0))

        self.render_counter, self.render_speed, self.speed_x, self.speed_y = int(), 150, 3, 1
        self.score = int()

    def loop_event(self):
        self.render_counter += 1

        if self.render_counter >= self.render_speed:
            self.box_base.append(pygame.sprite.Sprite())
            enemy_sprite = random.choice(['enemy1.jpg', 'box1.jpg'])
            self.box_base[-1].image = load_image(enemy_sprite, [140, 120])
            self.box_base[-1].rect = self.box_base[-1].image.get_rect()
            self.box_base[-1].rect.x, self.box_base[-1].rect.y = random.randint(20, 590), random.randint(0, 0)
            self.box_base[-1].mask = pygame.mask.from_surface(self.box_base[-1].image)
            self.all_sprites.add(self.box_base[-1])
            self.render_counter = int()

            if self.render_speed > 60:
                self.render_speed -= 10
            if self.speed_y < 12:
                self.speed_y += 1

        flag = False

        self.score += 1

        for i in range(len(self.box_base)):
            if pygame.sprite.collide_mask(self.player, self.box_base[i]):
                flag = True
            self.box_base[i].rect.y += self.speed_y

        if self.is_move[0] and self.player.rect.x > 20:
            self.player.rect.x -= self.speed_x
        elif self.is_move[1] and self.player.rect.x < 590:
            self.player.rect.x += self.speed_x

        screen.blit(self.bg, (0, 0))

        self.all_sprites.draw(screen)

        if flag:
            global controller
            global scene
            controller = 2
            scene = GameOver(self.score)


class GameOver:
    def __init__(self, score):
        bg = load_image('game_over_bg.jpg', SCREEN_SIZE)
        self.score = score // 10
        saver = open('base_score.txt', 'r', encoding='utf-8')
        self.best_score = saver.readlines()[0].strip()
        saver.close()

        if self.score > int(self.best_score):
            saver = open('base_score.txt', 'w', encoding='utf-8')
            saver.write(str(self.score))
            saver.close()
            self.best_score = self.score

        font = pygame.font.Font('data/fonts/impact.ttf', 36)
        text1 = font.render('Game Over! Enter "Space" to go to main menu!', True, pygame.Color('white'))
        text2 = font.render(f'Your score: {self.score}', True, pygame.Color('white'))
        text3 = font.render(f'Best score: {self.best_score}', True, pygame.Color('white'))

        screen.blit(bg, (0, 0))
        screen.blit(text1, (15, 250))
        screen.blit(text2, (280, 350))
        screen.blit(text3, (280, 380))


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

    controller = int()
    if controller == 0:
        scene = MainMenu()
        scene.render_menu()

        manager = pygame_gui.UIManager((700, 600))

        start_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((290, 250), (100, 50)),
            text='Start Game',
            manager=manager
        )

        exit_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((290, 300), (100, 50)),
            text='Exit',
            manager=manager
        )
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
                    if controller == 2:
                        controller = 0
                        scene = MainMenu()
                        scene.render_menu()
            if i.type == pygame.KEYUP:
                if controller == 1:
                    if i.key == pygame.K_LEFT:
                        scene.is_move[0] = not scene.is_move[0]
                    if i.key == pygame.K_RIGHT:
                        scene.is_move[1] = not scene.is_move[1]
            if i.type == pygame.USEREVENT:
                if i.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if i.ui_element == start_game:
                        if controller == 0:
                            controller = 1
                            scene = Game()
                    if i.ui_element == exit_btn:
                        if controller == 0:
                            sys.exit(0)

            manager.process_events(i)

        if controller == 1:
            scene.loop_event()

        pygame.display.flip()

        clock.tick(FPS)

        if controller == 0:
            manager.update(clock.tick(FPS) / 1000.0)
            manager.draw_ui(screen)
