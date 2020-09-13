import random
import pygame
from pygame.locals import *
import sys


#todo: die on body contact, end game and restart screens, rnadomise re-entry
#if go off screen

class Game(object):
    def __init__(self):
        pygame.init()
        self.W = 640
        self.H = 480
        self.FPS = 30
        self.win = pygame.display.set_mode((self.W,self.H))
        self.playing = False
        self.clock = pygame.time.Clock()
        

    def new(self):
        self.playing = True
        self.snek = Snek(50,50,(0,255,0))
        self.nom = Food(random.randint(10,self.W), random.randint(10,self.H))
        self.nom_exists = True

    def events(self):
        e_list = pygame.event.get()
        for event in e_list:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        self.snek.check_events(e_list)
        self.check_eaten()
        self.check_noms()
        self.snek.body_movement()

    def redrawGameWindow(self):
        self.win.fill((0,0,0))
        self.snek.draw(self.win)
        if self.nom_exists:
            self.nom.draw(self.win)
            

    def update(self):
        self.clock.tick(self.FPS)
        pygame.display.flip()
        pygame.display.update()
        pass

    def running(self):
        while self.playing:
            self.events()
            self.check_snek_position()
            self.redrawGameWindow()
            self.update()

    def check_noms(self):
        if not self.nom_exists:
            self.nom = Food(random.randint(10,self.W), random.randint(10,self.H))
            self.nom_exists = True

    def check_eaten(self):
        if self.snek.rect.colliderect(self.nom.rect):
            print("collision")
            self.snek.add_body_part(SnekBody(self.snek.x,self.snek.y, self.snek.width,self.snek.height,self.snek.colour))
            self.nom_exists = False
        else:
            return False

    def check_snek_position(self):
        #need to do this separately for every snek segment so we dont teleport whole snake
        if self.snek.x > self.W:
            self.dead()


    def dead(self):
        self.playing = False
        print(self.playing)
        pygame.quit()
        sys.exit()

    def game_over(self):
        self.win.fill((255,0,0))
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render('You ded', True, (0,0,0), (255,0,0))
        
        


class Snek(object):
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.colour = colour
        self.vel = 5
        self.last_xvel = 0
        self.last_yvel = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.body_parts = []

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for part in self.body_parts:
            part.draw(win)
        

    def add_body_part(self,body):
        self.body_parts.append(body)

    def body_movement(self):

        #snake must be bendy and stuff how do i do that?
        self.counter = 1
        self.previous_body_x = self.x - self.last_xvel
        self.previous_body_y = self.y - self.last_yvel
        self.current_body_x = 0
        self.current_body_y = 0
        for part in self.body_parts:
            self.current_body_x = part.x
            self.current_body_y = part.y
            part.x = self.previous_body_x
            part.y = self.previous_body_y
            self.counter += 1
            self.previous_body_x = self.current_body_x
            self.previous_body_y = self.current_body_y

    def check_events(self, e_list):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= self.vel
            self.last_xvel = 0
            self.last_yvel = self.vel * -1
        elif keys[pygame.K_DOWN]:
            self.y += self.vel
            self.last_xvel = 0
            self.last_yvel = self.vel * 1
        elif keys[pygame.K_LEFT]:
            self.x -= self.vel
            self.last_yvel = 0
            self.last_xvel = self.vel * -1
        elif keys[pygame.K_RIGHT]:
            self.x += self.vel
            self.last_yvel = 0
            self.last_xvel = self.vel * 1
        else:
            self.y += self.last_yvel
            self.x += self.last_xvel

class SnekBody(Snek):
    def __init__(self, x, y, width, height, colour):
        #super().__init__(x,y,width, height, colour)
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.colour = colour       

    def draw(self,win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))


class Food(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.colour = (255,255,255)
        self.exists = True
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        

g = Game()
g.new()
while g.playing:
    g.running()
