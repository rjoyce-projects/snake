#!/usr/bin/env python3
import random
import pygame
from pygame.locals import *
import sys
import os
font_dir = os.getcwd() #  Grabbing the name of the local pg install
path_t_font = os.path.join(font_dir, 'arial.ttf')

class Game(object):
    def __init__(self):
        pygame.init()
        self.W = 320
        self.H = 240
        self.FPS = 30
        self.win = pygame.display.set_mode((self.W,self.H))
        self.playing = False
        self.clock = pygame.time.Clock()
        self.alternate = 2
        self.score_initialise = 0
        self.score = self.score_initialise
        self.scorefont = pygame.font.Font(path_t_font, 20)
        self.score_label = self.scorefont.render("Score: " + str(self.score),  1, (255,255,0))

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
        self.snek.checkSelfCollision()
        self.check_snek_position()


    def redrawGameWindow(self):
        self.win.fill((0,0,0))
        self.snek.draw(self.win)
        self.score_label = self.scorefont.render("Score: " + str(self.score),  1, (255,255,0))
        g.win.blit(self.score_label,(g.W//100,g.H//100))
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
            self.redrawGameWindow()
            self.update()

    def check_noms(self):
        if not self.nom_exists:
            self.nom = Food(random.randint(10,self.W-self.snek.width), random.randint(10,self.H-self.snek.height))
            self.nom_exists = True

    def check_eaten(self):
        if self.snek.rect.colliderect(self.nom.rect):
            self.score += 1
            self.snek.add_body_part(SnekBody(self.snek.x,self.snek.y, self.snek.width,self.snek.height,self.snek.colour))
            self.nom_exists = False
        else:
            return False

    def check_snek_position(self):
        if self.snek.x > self.W - self.snek.width or self.snek.x < 0:

            endScreen(self.score, self.win)
        elif self.snek.y > self.H - self.snek.height or self.snek.y < 0:

            endScreen(self.score, self.win)

    def game_over(self):
        self.win.fill((255,0,0))
        self.font = pygame.font.Font(path_t_font, 20)
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
        self.counter = 0
        self.tailx = 0
        self.taily = 0

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for part in self.body_parts:
            part.draw(win)

    def add_body_part(self,body):
        ##  add to tail so need coordinates for this
        length = len(self.body_parts)
        if length > 1:
            tail_coords = self.body_parts[-1].rect
            self.body_parts.append(SnekBody(tail_coords[0],tail_coords[1],tail_coords[2],tail_coords[3], self.colour))
        else:
            self.body_parts.append(body)

    def checkSelfCollision(self):
        if self.rect in list(map(lambda z:z.rect,self.body_parts[1:])):
            endScreen(g.score, g.win)



    def body_movement(self):

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
            self.tailx = self.previous_body_x
            self.taily = self.previous_body_y
            part.rect = (self.tailx,self.taily,part.width,part.height)

    def check_events(self, e_list):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.last_yvel == 0:
            self.y -= self.vel
            self.last_xvel = 0
            self.last_yvel = self.vel * -1
        elif keys[pygame.K_DOWN] and self.last_yvel == 0:
            self.y += self.vel
            self.last_xvel = 0
            self.last_yvel = self.vel * 1
        elif keys[pygame.K_LEFT] and self.last_xvel == 0:
            self.x -= self.vel
            self.last_yvel = 0
            self.last_xvel = self.vel * -1
        elif keys[pygame.K_RIGHT] and self.last_xvel == 0:
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
        self.rect = (self.x, self.y, self.width, self.height)

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

def endScreen(score, bg):
    highest = updateHighscore(score)
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                g.new()
                g.score = 0
                while g.playing:
                    g.running()
        g.win.fill((0,0,0))
        myfont = pygame.font.Font(path_t_font, 20)
        elabel = myfont.render("you died. Press key, try again..", 1, (255,255,0))
        slabel = myfont.render(f"your score: {score}", 1, (255,255,0))
        hlabel = myfont.render(f"Highest ever score: {highest}", 1, (255,0,0))
        g.win.blit(elabel, (g.W//10,g.H//2))
        g.win.blit(slabel, (g.W//10, g.H//3))
        g.win.blit(hlabel, (g.W//10, g.H//4 - int(g.H//100)))
        pygame.display.update()
    return

def updateHighscore(score):
    f = open('score.txt','r')
    file = f.readlines()
    last = int(file[0])
    if last < int(score):
        f.close()
        file = open('score.txt', 'w')
        file.write(str(score))
        file.close()
        highest = score
    else:
        highest = last
    return highest


g = Game()
black=(0,0,0)
end_it=False
while (end_it==False):
    g.win.fill(black)
    myfont = pygame.font.Font(path_t_font, 20)
    nlabel = myfont.render("Welcome to Zan's first game", 1, (255, 255, 0))
    mlabel = myfont.render("Press any key to SNEK", 1, (255, 255, 0))
    for event in pygame.event.get():
        if event.type==KEYDOWN:
            end_it=True
    g.win.blit(nlabel,(g.W//10,g.H//10))
    g.win.blit(mlabel, (round(g.W//10), round(g.H//5)))
    pygame.display.flip()

g.new()
while g.playing:
    g.running()
#    while run:
#        endScreen(g.score, g.win)
