import pygame
import sys
import os
import random
import pygame_gui
import sqlite3


class MainMenu:  # Класс игрового меню
    def __init__(self, color):
        global SCREEN_SIZE
        self.bg = load_image('main_menu_bg.jpg', SCREEN_SIZE)
        self.font = pygame.font.Font('data/fonts/impact.ttf', 50)
        self.text = self.font.render('Main menu', True, pygame.Color(color))

    def render_menu(self):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.text, (230, 150))


class Shop:  # Класс игрового магазина
    def __init__(self):
        global SCREEN_SIZE
        self.bg = load_image('main_menu_bg.jpg', SCREEN_SIZE)
        self.font = pygame.font.Font('data/fonts/impact.ttf', 50)

        sql = '''SELECT money FROM DataCore WHERE id=1'''
        money_information = cursor.execute(sql).fetchall()[0][0]

        self.money_text = self.font.render(str(money_information) + '$', True, pygame.Color('white'))

        self.manager = pygame_gui.UIManager(SCREEN_SIZE)  # Переменная графического интерфейса

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


class Info:  # Класс меню с правилами игры
    def __init__(self):
        global SCREEN_SIZE
        self.bg = load_image('main_menu_bg.jpg', SCREEN_SIZE)
        self.font = pygame.font.Font('data/fonts/impact.ttf', 50)
        self.text1 = self.font.render('The game you must control', True, pygame.Color('white'))
        self.text2 = self.font.render('with Marks on keyboard', True, pygame.Color('white'))
        self.text3 = self.font.render('Cost money and', True, pygame.Color('white'))
        self.text4 = self.font.render('Buy new cars and roads in Shop', True, pygame.Color('white'))

        self.manager = pygame_gui.UIManager(SCREEN_SIZE)  # Переменная графического интерфейса

        self.main_menu_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((290, 450), (100, 50)),
            text='Back',
            manager=self.manager
        )

        screen.blit(self.bg, (0, 0))
        screen.blit(self.text1, (80, 150))
        screen.blit(self.text2, (120, 250))
        screen.blit(self.text3, (80, 300))
        screen.blit(self.text4, (40, 350))


class Game:  # Класс игрового процесса
    def __init__(self):
        global SCREEN_SIZE
        self.all_sprites = pygame.sprite.Group()

        sql = '''SELECT current_player FROM DataCore WHERE id=1'''
        sprite_name = cursor.execute(sql).fetchall()[0][0]

        if sprite_name.strip() == 'player5.jpg':
            car_size = [90, 130]
        elif sprite_name.strip() == 'car2.jpg':
            car_size = [90, 130]
        elif sprite_name.strip() == 'car3.jpg':
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

        sql = '''SELECT current_bg FROM DataCore WHERE id=1'''
        info_reader = cursor.execute(sql).fetchall()[0][0]

        self.bg = load_image(info_reader, SCREEN_SIZE)
        self.bg_rotate = pygame.transform.rotate(self.bg, 180)

        screen.blit(self.bg, (0, 0))

        self.render_counter = int()
        self.render_speed = 150
        self.speed_x = 3
        self.speed_y = 1
        self.speed_tech = 10

        if sprite_name == 'car2.png':
            self.speed_x = 4
        elif sprite_name == 'car3.jpg':
            self.speed_x = 5

        self.score = int()
        self.counter = True
        self.font = pygame.font.Font('data/fonts/impact.ttf', 28)

        self.manager = pygame_gui.UIManager(SCREEN_SIZE)  # Переменная графического интерфейса

        self.back_menu_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 50)),
            text='Back',
            manager=self.manager
        )

    def loop_event(self):  # Функция осуществляющая игровой процесс
        self.render_counter += 1

        if self.speed_tech < 100:
            self.speed_tech += 0.1

        sql = '''SELECT best_score FROM DataCore WHERE id=1'''
        best_record_text = cursor.execute(sql).fetchall()[0][0]

        self.text_score = self.font.render(
            f'Score: {str(self.score // 10)}',
            True,
            pygame.Color('white')
        )

        self.text_speed = self.font.render(
            f'Speed: {str(int(self.speed_tech))} km/h',
            True,
            pygame.Color('red')
        )

        self.best_score = self.font.render(
            f'Your best score: {best_record_text}',
            True,
            pygame.Color('orange')
        )

        if self.render_counter >= self.render_speed:
            enemy_sprite = random.choice(['enemy1.jpg', 'box1.jpg'])

            if random.randint(0, 10) > 6:
                if len(self.money_base) == 0:
                    self.money_base.append(pygame.sprite.Sprite())
                    self.money_base[0].image = load_image('money.jpg', [30, 30])
                else:
                    self.money_base[-1].image = load_image('money.jpg', [30, 30])

                self.money_base[-1].rect = self.money_base[-1].image.get_rect()
                self.money_base[-1].rect.x, self.money_base[-1].rect.y = random.randint(20, 590), \
                                                                         random.randint(0, 0)
                self.money_base[-1].mask = pygame.mask.from_surface(self.money_base[-1].image)
                self.all_sprites.add(self.money_base[-1])
            else:
                if len(self.box_base) == 0:
                    self.box_base.append(pygame.sprite.Sprite())
                    self.box_base[0].image = load_image(enemy_sprite, [140, 120])
                else:
                    self.box_base[-1].image = load_image(enemy_sprite, [140, 120])

                self.box_base[-1].rect = self.box_base[-1].image.get_rect()
                self.box_base[-1].rect.x, self.box_base[-1].rect.y = random.randint(20, 590), \
                                                                     random.randint(0, 0)
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
                sql = '''SELECT money FROM DataCore WHERE id=1'''
                reader_info = int(cursor.execute(sql).fetchall()[0][0])

                money = reader_info + 100

                sql = '''UPDATE DataCore SET money={} WHERE id=1'''.format(money)
                data_base.execute(sql)
                data_base.commit()

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

        if self.counter:
            screen.blit(self.bg, (0, 0))
            self.counter = False
        else:
            screen.blit(self.bg_rotate, (0, 0))
            self.counter = True

        self.all_sprites.draw(screen)

        screen.blit(self.text_score, (10, 550))
        screen.blit(self.text_speed, (500, 550))
        screen.blit(self.best_score, (200, 550))

        if flag:
            global controller
            global scene
            controller = 2
            scene = GameOver(self.score)


class GameOver:  # Класс заставки окончания игры
    def __init__(self, score):
        bg = load_image('game_over_bg.jpg', SCREEN_SIZE)
        self.score = score // 10

        sql = '''SELECT best_score FROM DataCore WHERE id=1'''
        self.best_score = cursor.execute(sql).fetchall()[0][0]

        if self.score > int(self.best_score):
            sql = '''UPDATE DataCore SET best_score={} WHERE id=1'''.format(self.score)
            data_base.execute(sql)
            data_base.commit()
            self.best_score = self.score

        font = pygame.font.Font('data/fonts/impact.ttf', 36)

        text1 = font.render(
            'Game Over! Enter "Space" to go to main menu!',
            True,
            pygame.Color('white')
        )

        text2 = font.render(f'Your score: {self.score}', True, pygame.Color('white'))
        text3 = font.render(f'Best score: {self.best_score}', True, pygame.Color('white'))

        screen.blit(bg, (0, 0))
        screen.blit(text1, (15, 250))
        screen.blit(text2, (280, 350))
        screen.blit(text3, (280, 380))


def load_image(name, size=False):  # Функция загрузки изображений
    full_name = os.path.join('data', name)

    image = pygame.image.load(full_name)
    image.set_colorkey(image.get_at((0, 0)))

    if type(size) == list:
        image = pygame.transform.scale(image, size)

    return image


def loader_img_car(sprite_name, cost):  # Функция загрузки автомобиля
    sql = '''SELECT money FROM DataCore WHERE id=1'''
    information = int(cursor.execute(sql).fetchall()[0][0])

    font = pygame.font.Font('data/fonts/impact.ttf', 22)

    flag = True

    sql = '''SELECT all_car FROM DataCore'''
    information_copy = list(cursor.execute(sql).fetchall())
    info_data_base = list()

    for i in information_copy:
        if i[0]:
            info_data_base.append(i[0])

    for i in info_data_base:
        if i.strip() == sprite_name:
            sql = '''UPDATE DataCore SET current_player="{}" WHERE id=1'''.format(sprite_name)
            data_base.execute(sql)
            data_base.commit()

            flag = False

    if flag:
        if information >= cost:
            sql = '''UPDATE DataCore SET current_player="{}" WHERE id=1'''.format(sprite_name)
            data_base.execute(sql)
            data_base.commit()

            sql = '''SELECT money FROM DataCore WHERE id=1'''
            info_reader = int(cursor.execute(sql).fetchall()[0][0])

            money = str(info_reader - cost)

            sql = '''UPDATE DataCore SET money={} WHERE id=1'''.format(money)
            data_base.execute(sql)
            data_base.commit()

            text = font.render("Bought have been success", True, pygame.Color('white'))

            sql = '''INSERT INTO DataCore(all_car) VALUES("{}")'''.format(sprite_name)
            data_base.execute(sql)
            data_base.commit()
        else:
            text = font.render("You can't bought the car", True, pygame.Color('white'))

        screen.blit(text, [20, 570])


def loader_img_road(sprite_name, cost):  # Функция загрузки дороги
    sql = '''SELECT money FROM DataCore WHERE id=1'''
    information = int(cursor.execute(sql).fetchall()[0][0])

    font = pygame.font.Font('data/fonts/impact.ttf', 22)

    flag = True

    sql = '''SELECT all_road FROM DataCore'''
    information_copy = list(cursor.execute(sql).fetchall())
    info_data_base = list()

    for i in information_copy:
        if i[0]:
            info_data_base.append(i[0])

    for i in info_data_base:
        if i.strip() == sprite_name:
            sql = '''UPDATE DataCore SET current_bg="{}" WHERE id=1'''.format(sprite_name)
            data_base.execute(sql)
            data_base.commit()

            flag = False

    if flag:
        if information >= cost:
            sql = '''UPDATE DataCore SET current_bg="{}" WHERE id=1'''.format(sprite_name)
            data_base.execute(sql)
            data_base.commit()

            sql = '''SELECT money FROM DataCore WHERE id=1'''
            info_reader = int(cursor.execute(sql).fetchall()[0][0])

            money = str(info_reader - cost)

            sql = '''UPDATE DataCore SET money={} WHERE id=1'''.format(money)
            data_base.execute(sql)
            data_base.commit()

            text = font.render("Bought have been success", True, pygame.Color('white'))

            sql = '''INSERT INTO DataCore(all_road) VALUES("{}")'''.format(sprite_name)
            data_base.execute(sql)
            data_base.commit()
        else:
            text = font.render("You can't bought the road", True, pygame.Color('white'))

        screen.blit(text, [20, 570])


if __name__ == '__main__':
    pygame.init()

    SCREEN_SIZE = [700, 600]  # Константа с размерами экрана

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('RoadRace')

    clock = pygame.time.Clock()
    FPS = 30  # Константа с FPS игры

    pygame.mixer.music.load('data/main_theme.mp3')  # Загрузка музыкы
    pygame.mixer.music.play(-1)  # Проигрывание музыки без конца

    colors = (
        'yellow',
        'red',
        'blue',
        'pink',
        'white',
        'gray',
        'orange',
        'green'
    )

    controller = int()  # Переменная содержащая номер текущей сцены

    data_base = sqlite3.connect('data_base.db')  # Подключение к базе данных
    cursor = data_base.cursor()

    sql = '''SELECT money FROM DataCore WHERE id=1'''
    sprite_name = cursor.execute(sql).fetchall()[0][0]

    scene = MainMenu(random.choice(colors))
    scene.render_menu()

    manager = pygame_gui.UIManager((700, 600))  # Переменная графического интерфейса

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

    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                data_base.close()
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
                        scene = MainMenu(random.choice(colors))
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
                            scene = MainMenu(random.choice(colors))
                            scene.render_menu()
                    if controller == 4:
                        if i.ui_element == scene.main_menu_btn:
                            controller = 0
                            random_color_menu = random.choice(colors)
                            scene = MainMenu(random_color_menu)
                            scene.render_menu()
                        elif i.ui_element == scene.car1_btn:
                            loader_img_car('player5.jpg', 0)
                        elif i.ui_element == scene.car2_btn:
                            loader_img_car('car2.jpg', 5000)
                        elif i.ui_element == scene.car3_btn:
                            loader_img_car('car3.jpg', 10000)
                        elif i.ui_element == scene.road1_btn:
                            loader_img_road('road4.jpg', 0)
                        elif i.ui_element == scene.road2_btn:
                            loader_img_road('road2.jpg', 5000)
                        elif i.ui_element == scene.road3_btn:
                            loader_img_road('road.jpg', 10000)
                    if controller == 1:
                        if i.ui_element == scene.back_menu_btn:
                            controller = 0
                            random_color_menu = random.choice(colors)
                            scene = MainMenu(random_color_menu)
                            scene.render_menu()
            if controller == 0:
                manager.process_events(i)
            elif controller in (3, 4, 1):
                scene.manager.process_events(i)

        if controller == 1:
            scene.loop_event()
            if controller == 1:
                scene.manager.update(clock.tick(FPS) / 1000.0)
                scene.manager.draw_ui(screen)

        pygame.display.flip()

        clock.tick(FPS)

        if controller == 0:
            manager.update(clock.tick(FPS) / 1000.0)
            manager.draw_ui(screen)
        elif controller in (3, 4, 1):
            scene.manager.update(clock.tick(FPS) / 1000.0)
            scene.manager.draw_ui(screen)
