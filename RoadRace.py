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
        self.bg = load_image('main_menu_bg.jpg', SCREEN_SIZE)
        self.font = pygame.font.Font('data/fonts/impact.ttf', 50)

        money_base = open('money_count.txt', 'r', encoding='utf-8')
        money_information = money_base.readlines()[0].strip()
        money_base.close()

        self.money_text = self.font.render(money_information + '$', True, pygame.Color('white'))

        self.manager = pygame_gui.UIManager((700, 600))

        self.main_menu_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 50)),
            text='Back',
            manager=self.manager
        )

        self.car1_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 70), (190, 190)),
            text='Car1 (Standart)',
            manager=self.manager
        )

        self.car2_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 70), (190, 190)),
            text='Car2 (Cost: 1000$)',
            manager=self.manager
        )

        self.car3_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((450, 70), (190, 190)),
            text='Car3 (Cost: 10000$)',
            manager=self.manager
        )

        self.road1_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 280), (190, 190)),
            text='Road1 (Standart)',
            manager=self.manager
        )

        self.road2_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 280), (190, 190)),
            text='Road2 (Cost: 1000$)',
            manager=self.manager
        )

        self.road3_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((450, 280), (190, 190)),
            text='Road3 (Cost: 10000$)',
            manager=self.manager
        )

        screen.blit(self.bg, (0, 0))
        screen.blit(self.money_text, (350, 10))


class Info:
    def __init__(self):
        self.bg = load_image('main_menu_bg.jpg', SCREEN_SIZE)
        self.font = pygame.font.Font('data/fonts/impact.ttf', 50)
        self.text1 = self.font.render('The game you must control', True, pygame.Color('white'))
        self.text2 = self.font.render('with Marks on keyboard', True, pygame.Color('white'))

        self.manager = pygame_gui.UIManager((700, 600))

        self.main_menu_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((290, 400), (100, 50)),
            text='Back',
            manager=self.manager
        )

        screen.blit(self.bg, (0, 0))
        screen.blit(self.text1, (80, 150))
        screen.blit(self.text2, (120, 200))


class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()

        reader = open('player_sprite.txt', 'r', encoding='utf-8')
        sprite_name = reader.readlines()[0].strip()
        reader.close()

        if sprite_name == 'player5.jpg':
            car_size = [90, 130]
        elif sprite_name == 'car2.jpg':
            car_size = [90, 130]
        elif sprite_name == 'car3.jpg':
            car_size = [120, 150]

        self.player = pygame.sprite.Sprite()
        self.player.image = load_image(sprite_name, car_size)
        self.player.rect = self.player.image.get_rect()
        self.player.rect.x, self.player.rect.y = 300, 300
        self.player.mask = pygame.mask.from_surface(self.player.image)

        self.is_move = [False, False]

        self.box_base = list()
        self.money_base = list()

        self.all_sprites.add(self.player)

        reader = open('bg.txt', 'r', encoding='utf-8')
        info_reader = reader.readlines()[0].strip()
        reader.close()

        self.bg = load_image(info_reader, SCREEN_SIZE)

        screen.blit(self.bg, (0, 0))

        self.render_counter = int()
        self.render_speed = 150
        self.speed_x = 3
        self.speed_y = 1

        if sprite_name == 'car2.png':
            self.speed_x = 4
        elif sprite_name == 'car3.jpg':
            self.speed_x = 5

        self.score = int()

    def loop_event(self):
        self.render_counter += 1

        if self.render_counter >= self.render_speed:
            enemy_sprite = random.choice(['enemy1.jpg', 'box1.jpg'])

            if random.randint(0, 10) > 6:
                if len(self.money_base) == 0:
                    self.money_base.append(pygame.sprite.Sprite())
                    self.money_base[0].image = load_image('money.jpg', [30, 30])
                else:
                    self.money_base[-1].image = load_image('money.jpg', [30, 30])

                self.money_base[-1].rect = self.money_base[-1].image.get_rect()
                self.money_base[-1].rect.x, self.money_base[-1].rect.y = random.randint(20, 590), random.randint(0, 0)
                self.money_base[-1].mask = pygame.mask.from_surface(self.money_base[-1].image)
                self.all_sprites.add(self.money_base[-1])
            else:
                if len(self.box_base) == 0:
                    self.box_base.append(pygame.sprite.Sprite())
                    self.box_base[0].image = load_image(enemy_sprite, [140, 120])
                else:
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

        for i in range(len(self.money_base)):
            if pygame.sprite.collide_mask(self.player, self.money_base[i]):
                reader = open('money_count.txt', 'r', encoding='utf-8')
                reader_info = int(reader.readlines()[0].strip())
                reader.close()

                writer = open('money_count.txt', 'w', encoding='utf-8')
                writer.write(str(reader_info + 100))
                writer.close()

                self.money_base[i].rect.y += 10 ** 3

            self.money_base[i].rect.y += self.speed_y

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


def load_image(name, size=False):
    full_name = os.path.join('data', name)

    image = pygame.image.load(full_name)
    image.set_colorkey(image.get_at((0, 0)))

    if type(size) == list:
        image = pygame.transform.scale(image, size)

    return image


def loader_img(sprite_name, cost):
    reader = open('money_count.txt', 'r', encoding='utf-8')

    information = int(reader.readlines()[0].strip())

    font = pygame.font.Font('data/fonts/impact.ttf', 22)

    flag = True

    data_base = open('car_base.txt', 'r', encoding='utf-8')
    info_data_base = data_base.readlines()

    for i in info_data_base:
        if i.strip() == sprite_name:
            writer = open('player_sprite.txt', 'w', encoding='utf-8')
            writer.write(sprite_name)
            flag = False

    data_base.close()

    if flag:
        if information >= cost:
            writer = open('player_sprite.txt', 'w', encoding='utf-8')
            writer.write(sprite_name)
            writer.close()

            reader = open('money_count.txt', 'r', encoding='utf-8')
            info_reader = int(reader.readlines()[0].strip())
            reader.close()

            writer_money = open('money_count.txt', 'w', encoding='utf-8')
            writer_money.write(str(info_reader - cost))
            writer_money.close()

            text = font.render("Bought have been success", True, pygame.Color('white'))

            appender_file = open('car_base.txt', 'r', encoding='utf-8')
            appender_file.write(sprite_name + '\n')
            appender_file.close()
        else:
            text = font.render("You can't bought the car", True, pygame.Color('white'))

        screen.blit(text, [20, 570])

    reader.close()


def loader_img_road(sprite_name, cost):
    reader = open('money_count.txt', 'r', encoding='utf-8')

    information = int(reader.readlines()[0].strip())

    font = pygame.font.Font('data/fonts/impact.ttf', 22)

    flag = True

    data_base = open('road_base.txt', 'r', encoding='utf-8')
    info_data_base = data_base.readlines()

    for i in info_data_base:
        if i.strip() == sprite_name:
            writer = open('bg.txt', 'w', encoding='utf-8')
            writer.write(sprite_name)
            flag = False

    data_base.close()

    if flag:
        if information >= cost:
            writer = open('bg.txt', 'w', encoding='utf-8')
            writer.write(sprite_name)
            writer.close()

            reader = open('money_count.txt', 'r', encoding='utf-8')
            info_reader = int(reader.readlines()[0].strip())
            reader.close()

            writer_money = open('money_count.txt', 'w', encoding='utf-8')
            writer_money.write(str(info_reader - cost))
            writer_money.close()

            text = font.render("Bought have been success", True, pygame.Color('white'))

            appender_file = open('road_base.txt', 'r', encoding='utf-8')
            appender_file.write(sprite_name + '\n')
            appender_file.close()
        else:
            text = font.render("You can't bought the road", True, pygame.Color('white'))

        screen.blit(text, [20, 570])

    reader.close()


if __name__ == '__main__':
    pygame.init()

    SCREEN_SIZE = [700, 600]

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('RoadRace')

    clock, FPS = pygame.time.Clock(), 30

    controller = int()

    reader = open('player_sprite.txt', 'r', encoding='utf-8')
    sprite_name = reader.readlines()[0].strip()
    reader.close()

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
            relative_rect=pygame.Rect((290, 400), (100, 50)),
            text='Exit',
            manager=manager
        )

        info_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((290, 350), (100, 50)),
            text='Info',
            manager=manager
        )

        shop_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((290, 300), (100, 50)),
            text='Shop',
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
                    if controller == 0:
                        if i.ui_element == start_game:
                            controller = 1
                            scene = Game()
                        if i.ui_element == exit_btn:
                            if controller == 0:
                                sys.exit(0)
                        if i.ui_element == info_btn:
                            controller = 3
                            scene = Info()
                        if i.ui_element == shop_btn:
                            controller = 4
                            scene = Shop()
                    if controller == 3:
                        if i.ui_element == scene.main_menu_btn:
                            controller = 0
                            scene = MainMenu()
                            scene.render_menu()
                    if controller == 4:
                        if i.ui_element == scene.main_menu_btn:
                            controller = 0
                            scene = MainMenu()
                            scene.render_menu()
                        elif i.ui_element == scene.car1_btn:
                            loader_img('player5.jpg', 0)
                        elif i.ui_element == scene.car2_btn:
                            loader_img('car2.jpg', 5000)
                        elif i.ui_element == scene.car3_btn:
                            loader_img('car3.jpg', 10000)
                        elif i.ui_element == scene.road1_btn:
                            loader_img('road4.jpg', 0)
                        elif i.ui_element == scene.road2_btn:
                            loader_img('road2.jpg', 5000)
                        elif i.ui_element == scene.road3_btn:
                            loader_img('road.jpg', 10000)
            if controller == 0:
                manager.process_events(i)
            elif controller in (3, 4):
                scene.manager.process_events(i)

        if controller == 1:
            scene.loop_event()

        pygame.display.flip()

        clock.tick(FPS)

        if controller == 0:
            manager.update(clock.tick(FPS) / 1000.0)
            manager.draw_ui(screen)
        elif controller in (3, 4):
            scene.manager.update(clock.tick(FPS) / 1000.0)
            scene.manager.draw_ui(screen)
