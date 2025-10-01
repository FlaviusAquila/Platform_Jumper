from tkinter import *
import time


class Game:
    """
    UA: Головний клас гри. Створює вікно, полотно (canvas), завантажує фон і запускає цикл гри.
    EN: Main game class. Creates the window, canvas, loads background, and runs the game loop.
    """

    def __init__(self):
        """
        UA: Ініціалізує вікно, створює canvas, встановлює фон і готує список об’єктів.
        EN: Initializes the window, creates canvas, sets background, and prepares the object list.
        """

        self.tk = Tk()
        self.tk.title('Running Mister StickMan')
        self.tk.resizable(False, False)
        self.tk.wm_attributes('-topmost', 1)
        self.canvas = Canvas(self.tk,
                             width=500,
                             height=500,
                             highlightthickness=2
                             )
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        # UA: Завантаження фонів
        # EN: Load backgrounds
        self.bg = PhotoImage(file='BackGroundGIF/background_1.gif')
        self.bg1 = PhotoImage(file='BackGroundGIF/background_0.gif') # колір
        self.bg2 = PhotoImage(file='BackGroundGIF/background_2.gif') # жовто-чорне
        self.bg3 = PhotoImage(file='BackGroundGIF/BackGround11.gif') # нічне моторошне місто 500х500
        w = self.bg.width()
        h = self.bg.height()
        # UA: Малюємо фон мозаїкою
        # EN: Draw background in a tiled pattern
        for row in range(0, 5): # 0, 5 for self.bg1 or self.bg2
            for column in range(0, 5): # 0, 5 for self.bg1 or self.bg2
                if (row + column) % 2 == 0:
                    self.canvas.create_image(column * w, row * h,
                                         image=self.bg,
                                         anchor='nw'
                                         )
                else:
                    self.canvas.create_image(column*w, row*h,
                                         image=self.bg,
                                         anchor='nw'
                                         )
        # UA: Список ігрових об’єктів
        # EN: List of game objects
        self.sprites = []
        self.running = True

    def mainloop(self):
        """
           UA: Основний цикл гри. Оновлює рух кожного об’єкта та перемальовує вікно.
           EN: Main game loop. Updates movement of each object and redraws the window.
        """

        while True:
            if self.running:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.015)


class Coords:
    """
        UA: Клас для зберігання координат об’єкта (x1, y1 — верхній лівий кут, x2, y2 — нижній правий кут).
        EN: Class for storing object coordinates (x1, y1 — top-left, x2, y2 — bottom-right).
    """

    def __init__(self,x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

# ===================== ФУНКЦІЇ КОЛІЗІЙ / COLLISION FUNCTIONS =====================

def within_x(co1, co2):
    """
        UA: Перевіряє накладання об’єктів по осі X.
        EN: Checks overlap of objects along X axis.
    """

    return (
            co2.x1 < co1.x1 < co2.x2
            or
            co2.x1 < co1.x2 < co2.x2
            or
            co1.x1 < co2.x1 < co1.x2
            or
            co1.x1 < co2.x2 < co1.x2
    )

def within_y(co1, co2):
    """
        UA: Перевіряє накладання об’єктів по осі Y.
        EN: Checks overlap of objects along Y axis.
    """

    return (
            co2.y1 < co1.y1 < co2.y2
            or
            co2.y1 < co1.y2 < co2.y2
            or
            co1.y1 < co2.y1 < co1.y2
            or
            co1.y1 < co2.y2 < co1.y2
    )



def collided_left(co1, co2):
    """
        UA: Перевіряє зіткнення зліва.
        EN: Checks collision from the left.
    """

    return within_y(co1, co2) and co2.x1 <= co1.x1 <= co2.x2

def collided_right(co1, co2):
    """
        UA: Перевіряє зіткнення справа.
        EN: Checks collision from the right.
    """

    return within_y(co1, co2) and co2.x2 >= co1.x2 >= co2.x1

def collided_top(co1, co2):
    """
        UA: Перевіряє зіткнення зверху.
        EN: Checks collision from the top.
    """

    return within_x(co1, co2) and co2.y2 >= co1.y1 >= co2.y1

def collided_bottom(y, co1, co2):
    """
        UA: Перевіряє зіткнення знизу.
        EN: Checks collision from the bottom.
    """

    return within_x(co1, co2) and co2.y1 <= co1.y2 + y <= co2.y2

# ===================== БАЗОВІ КЛАСИ СПРАЙТІВ / BASE CLASS FOR ALL GAME OBJECT =====================

class Sprite:
    """
        UA: Базовий клас для об’єктів гри. Усі спрайти наслідують його.
        EN: Base class for all game objects. All sprites inherit from it.
    """

    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        """
            UA: Рух об’єкта (перевизначається у спадкоємцях).
            EN: Moves the object (overridden in subclasses).
        """

        pass

    def coords(self):
        """
            UA: Повертає координати об’єкта.
            EN: Returns object coordinates.
        """

        return self.coordinates



class PlatformSprites(Sprite):
    """
        UA: Клас статичної платформи (нерухомий об’єкт).
        EN: Class for static platform (non-moving object).
    """

    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(
            x, y,
            image=self.photo_image,
            anchor='nw'
        )
        self.coordinates = Coords(x, y, x + width, y + height)



class StickFigureClass(Sprite):
    """
        UA: Клас головного персонажа (чоловічок). Вміє ходити, стрибати, анімуватися і взаємодіяти з об’єктами.
        EN: Main character class (stick man). Can walk, jump, animate, and interact with objects.
    """

    def __init__(self, game):
        Sprite.__init__(self, game)
        # UA: Анімації для руху
        # EN: Animations for movement
        self.images_left = [
            PhotoImage(file='StickManGif/figure-L1.gif'),
            PhotoImage(file='StickManGif/figure-L2.gif'),
            PhotoImage(file='StickManGif/figure-L3.gif')
        ]
        self.images_right = [
            PhotoImage(file='StickManGif/figure-R1.gif'),
            PhotoImage(file='StickManGif/figure-R2.gif'),
            PhotoImage(file='StickManGif/figure-R3.gif')
        ]
        self.image = game.canvas.create_image(200, 470,
                                              image=self.images_left[0],
                                              anchor='nw'
                                              )
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        # UA: Прив’язка клавіш керування
        # EN: Bind control keys
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2

    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2
            
    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0

    def animate(self):
        """
            UA: Відповідає за зміну кадрів анімації під час руху.
            EN: Handles animation frame switching while moving.
        """

        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image= self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, image= self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image= self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image= self.images_right[self.current_image])

    def coords(self):
        """
            UA: Оновлює і повертає координати персонажа.
            EN: Updates and returns character coordinates.
        """

        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates

    def move(self):
        """
            UA: Виконує рух, обробку зіткнень і анімацію персонажа.
            EN: Executes movement, collision handling, and animation of the character.
        """

        self.animate()
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4
        if self.y > 0:
            self.jump_count -= 1
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <=0:
            self.x = 0
            left = False
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0 :
                    self.y = 0
                bottom = False
                top = False
            if (bottom and
                    falling and
                    self.y == 0 and
                    co.y2 < self.game.canvas_height and
                    collided_bottom(1, co, sprite_co)):
                falling = False
            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                left = False
                if sprite.endgame:
                    self.game.running = False
                    self.game.canvas.create_text(260, 250, text=f'To be continued...\n',
                                                 fill='dark orange',
                                                 font=('Courier', 22, 'bold'),
                                                 )
            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0
                right = False
                if sprite.endgame:
                    self.game.running = False
                    self.game.canvas.create_text(260, 250, text=f'To be continued...\n',
                                                 fill='dark orange',
                                                 font=('Courier', 22, 'bold'),
                                                 )
        if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
            self.y = 4
        self.game.canvas.move(self.image, self.x, self.y)


class DoorSprite(Sprite):
    """
        UA: Клас дверей (кінцева ціль гри). Дотик до дверей завершує гру.
        EN: Door class (end goal of the game). Touching the door ends the game.
    """

    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + (width / 2), y + height)
        self.endgame = True

    def door_opened(self):
        """
            UA: Метод-заглушка для майбутніх дій при відкритті дверей.
            EN: Placeholder method for door interactions.
        """

        pass


class MovingPlatform(Sprite):
    """
        UA: Клас рухомої платформи, яка пересувається по осі X і змінює напрямок при досягненні меж.
        EN: Class for moving platform that travels along X axis and reverses direction at edges.
    """

    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(
            x, y,
            image=self.photo_image,
            anchor='nw'
        )
        self.width = width
        self.height = height
        self.x = 1
        self.coordinates = Coords(x, y, x + width, y + height)

    def move(self):
        # UA: Рух по осі X
        # EN: Movement along X axis
        self.game.canvas.move(self.image, self.x, 0)
        xy = self.game.canvas.coords(self.image)
        x = xy[0]
        y = xy[1]
        self.coordinates = Coords(x, y, x + self.width, y + self.height)
        # UA: Зміна напряму при зіткненні з межами вікна
        # EN: Reverse direction when reaching canvas edges
        if self.coordinates.x1 <= 0 or self.coordinates.x2 >= self.game.canvas_width:
            self.x = -self.x

# ===================== СТВОРЕННЯ ОБ’ЄКТІВ =====================

g = Game()
# UA: Створення платформ / EN: Creating platforms
platform1 = PlatformSprites(g, PhotoImage(file='PlatformGif/platform1.gif'), 10, 480, 92, 8)
platform2 = PlatformSprites(g, PhotoImage(file='PlatformGif/platform1.gif'), 150, 440, 92, 8)
platform3 = PlatformSprites(g, PhotoImage(file='PlatformGif/platform1.gif'), 300, 400, 92, 8)
platform4 = MovingPlatform(g, PhotoImage(file='PlatformGif/platform1.gif'), 280, 160, 92, 8)
platform5 = PlatformSprites(g, PhotoImage(file='PlatformGif/platform2.gif'), 175, 350, 58, 8)
platform6 = PlatformSprites(g, PhotoImage(file='PlatformGif/platform2.gif'), 50, 300, 58, 8)
platform7 = MovingPlatform(g, PhotoImage(file='PlatformGif/platform2.gif'), 170, 120, 58, 8)
platform8 = PlatformSprites(g, PhotoImage(file='PlatformGif/platform2.gif'), 45, 60, 58, 8)
platform9 = MovingPlatform(g, PhotoImage(file='PlatformGif/platform3.gif'), 170, 250, 25, 8)
platform10 = PlatformSprites(g, PhotoImage(file='PlatformGif/platform3.gif'), 230, 200, 25, 8)

# UA: Додаємо у список спрайтів
# EN: Append to sprites list
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)
door = DoorSprite(g, PhotoImage(file='doorsGIF/Door1.gif'), 45, 30, 28, 31)
g.sprites.append(door)

sf = StickFigureClass(g)
g.sprites.append(sf)

g.mainloop()