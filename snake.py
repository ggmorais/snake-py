import random

import pygame as pg


class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)


class Snake:
    def __init__(self, game, pos, size, speed, color=Colors.green):
        self.game = game
        self.pos = list(pos)
        self.size= size
        self.color = color
        self.speed = speed
        self.dir = None
        self.parts = []
        self.historic = []
        self.dead = False
        
        self.grow(4)
        self.parts.reverse()
        
        self.set_historic()
        self.update(self.dir)

    def grow(self, quant=1):
        for n in range(quant):
            part = pg.Rect((self.pos[0] * n, self.pos[1]), self.size)
            self.parts.append(part)

    def set_historic(self):
        self.historic = [(part.x, part.y) for part in self.parts]

    def update(self, direction):
        nx, ny = self.parts[0].x, self.parts[0].y

        if direction == 'right':
            nx += self.speed
        elif direction == 'left':
            nx -= self.speed
        elif direction == 'up':
            ny -= self.speed
        elif direction == 'down':
            ny += self.speed

        food = self.parts[0].collidelist(self.game.foods)
        tail = self.parts[0].collidelist(self.parts[1:])

        if food > -1:
            del self.game.foods[food]
            self.grow(1)
        
        if tail > -1:
            self.dead = True

        for n in range(len(self.parts)):                
            if n == 0:
                self.parts[n].x = nx
                self.parts[n].y = ny

                if self.parts[0].x > self.game.window_size[0] or self.parts[0].x < 0:
                    self.dead = True
                if self.parts[0].y > self.game.window_size[1] or self.parts[0].y < 0:
                    self.dead = True
            else:
                if direction:
                    self.parts[n].x = self.historic[n - 1][0]
                    self.parts[n].y = self.historic[n - 1][1]

            pg.draw.rect(self.game.display, self.color, self.parts[n])

        self.set_historic()


class Game:
    def __init__(self, w, h):
        pg.init()
        
        self.running = True
        self.window_size = (w, h)
        self.display = pg.display.set_mode(self.window_size)
        self.clock = pg.time.Clock()
        
        pg.display.set_caption('Snake game')

        self.fps = 20

        self.food_color = Colors.red
        self.foods = []
        self.food_timeout = 10

        self.dir = None

        self.player = Snake(self, (8, 8), (8, 8), 8)

        self.loop()
    
    def on_keydown(self, key):

        if key == pg.K_RIGHT and self.dir != 'left':
            self.dir = 'right'
        if key == pg.K_LEFT and self.dir != 'right':
            self.dir = 'left'
        if key == pg.K_UP and self.dir != 'down':
            self.dir = 'up'
        if key == pg.K_DOWN and self.dir != 'up':
            self.dir = 'down'
    
    def on_keyup(self, key):
        pass

    def drop_food(self):
        if len(self.foods) == 0:
            posx = random.randint(2, (self.window_size[0] - 16) / 8)
            posy = random.randint(2, (self.window_size[1] - 16) / 8)

            food = pg.Rect((posx * 8, posy * 8), (8, 8))
            self.foods.append(food)

        for food in self.foods:
            pg.draw.rect(self.display, self.food_color, food)

    def loop(self):
        while self.running and not self.player.dead:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.running = False
                if e.type == pg.KEYDOWN:
                    self.on_keydown(e.key)
                if e.type == pg.KEYUP:
                    self.on_keyup(e.key)

            self.display.fill(Colors.black)
            self.player.update(self.dir)
            self.drop_food()

            pg.display.update()

            self.clock.tick(self.fps)

Game(320, 240)
