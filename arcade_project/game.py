import arcade
import random
from pyglet.graphics import Batch

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TITLE = 'Новогодний Ловец'


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ALMOND)

        self.item_list = arcade.SpriteList()
        self.falling_list = arcade.SpriteList()

        self.basket = None
        self.basket_change_x = 0

        self.spawn_timer = 0
        self.score = 0

        self.virus_sound = arcade.load_sound('sounds/virus_sound.mp3')
        self.coin_sound = arcade.load_sound('sounds/coin_sound.mp3')
        self.sound = arcade.load_sound('sounds/sound.mp3')

        self.setup()
    def setup(self):
        """Настройка игры"""
        basket = arcade.Sprite('images/basket.png', scale=0.3)

        self.basket = basket

        basket.center_x = 400
        basket.center_y = 60
        self.item_list.append(basket)

        items_data = [
            ('images/mandarin.png', 0.4, 10),
            ('images/bell.png', 0.4, 10),
            ('images/cone.png', 0.4, 10),
            ('images/snowflake.png', 0.4, 10),
            ('images/coin.png', 0.4, 30),
            ('images/virus.png', 0.4, -20)
        ]

    def on_draw(self):
        self.clear()
        self.item_list.draw()

        self.text1 = arcade.Text(f'Счет: {self.score}', 10, SCREEN_HEIGHT - 30,
                                 arcade.color.WHITE, 24)

        self.text1.draw()


    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш для управления корзиной"""
        if key == arcade.key.LEFT:
            self.basket_change_x -= 5
        if key == arcade.key.RIGHT:
            self.basket_change_x += 5

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.basket_change_x = 0

    def on_update(self, delta_time: float):
        """Обновление состояния игры"""
        self.basket.center_x += self.basket_change_x

        self.spawn_timer += delta_time
        if self.spawn_timer > 0.6:
            self.spawn_timer = 0
            self.spawn_new_item()

        if self.basket.center_x < 0:
            self.basket.center_x = 0
        elif self.basket.center_x > SCREEN_WIDTH:
            self.basket.center_x = SCREEN_WIDTH

        for item in self.falling_list:
            item.center_y -= 5

        hit_list = arcade.check_for_collision_with_list(self.basket, self.falling_list)

        for item in hit_list:
            self.score += item.points
            if item.file == 'images/virus.png':
                self.virus_sound.play()
            if item.file == 'images/coin.png':
                self.coin_sound.play()
            if item.file != 'images/virus.png' and item.file != 'images/coin.png':
                self.sound.play()

            item.remove_from_sprite_lists()

        for item in list(self.falling_list):
            if item.center_y < 0:
                item.remove_from_sprite_lists()

    def spawn_new_item(self):
        items = [
            ('images/mandarin.png', 0.4, 10),
            ('images/bell.png', 0.4, 10),
            ('images/cone.png', 0.4, 10),
            ('images/snowflake.png', 0.4, 10),
            ('images/coin.png', 0.4, 30),
            ('images/virus.png', 0.4, -20)
        ]

        file, scale, points = random.choice(items)
        item = arcade.Sprite(file, scale)
        item.center_x = random.randint(50, SCREEN_WIDTH - 50)
        item.center_y = SCREEN_HEIGHT
        item.points = points
        item.file = file

        self.item_list.append(item)
        self.falling_list.append(item)


class StartView(arcade.View):
    def on_show(self):
        """Настройка начального экрана"""
        arcade.set_background_color(arcade.color.FELDSPAR)

    def on_draw(self):
        """Отрисовка начального экрана"""
        self.clear(arcade.color.DARK_SLATE_BLUE)
        self.batch = Batch()
        start_text = arcade.Text('Новогодний Ловец',
                                 self.window.width / 2, self.window.height - 150,
                                 arcade.color.WHITE,
                                 font_size=50,
                                 font_name='Comic Sans MS',
                                 anchor_x="center",
                                 batch=self.batch)
        any_key_text = arcade.Text('Нажмите любую клавишу, чтобы начать',
                                   self.window.width / 2, self.window.height / 2 + 50,
                                   arcade.color.GRAY,
                                   font_size=22,
                                   italic=True,
                                   anchor_x="center",
                                   batch=self.batch)
        rules = arcade.Text('Правила:\n'
                            '• Мандарины, колокольчики, шишки, снежинки: +10 очков\n'
                            '• Монеты: +30 очков\n'
                            '• Вирусы: -20 очков',
                            self.window.width / 2 + 250, self.window.height / 2 - 50,
                            arcade.color.ASH_GREY,
                            font_size=20,
                            anchor_x="center",
                            batch=self.batch,
                            multiline=True,
                            width=400)
        controls = arcade.Text('Управление: ← →',
                               self.window.width / 2,
                               self.window.height / 2 - 250,
                               arcade.color.LIGHT_GRAY,
                               font_size=18,
                               font_name='Arial',
                               anchor_x="center",
                               batch=self.batch)

        self.batch.draw()

    def on_key_press(self, key, modifiers):
        """Начало игры при нажатии клавиши"""
        game_view = MyGame()
        self.window.show_view(game_view)

def main():
    """Главная функция"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

