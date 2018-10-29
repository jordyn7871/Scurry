import pygame
from pygame.locals import *
import os
import sys
import math
import random        



class sprite(object):
    move = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,16)]
    leap = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1,8)]
    drop = pygame.image.load(os.path.join('images', '0.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.jcount = 0
        self.rcount = 0

        self.falling = False

    def draw(self, win):
        if self.jumping:
            self.y -= self.jumpList[self.jcount] * 1.5
            win.blit(self.leap[self.jcount//18], (self.x,self.y))
            self.jcount += 1
            if self.jcount > 108:
                self.jcount = 0
                self.jumping = False
                self.rcount = 0
            self.hitbox = (self.x + 4,self.y,self.width - 24,self.height - 10)
            
        elif self.falling:
            win.blit(self.drop, (self.x, self.y + 30))

        
        else:
            if self.rcount > 42:
                self.rcount = 0
            win.blit(self.move[self.rcount//6], (self.x,self.y))
            self.rcount += 1
            self.hitbox = (self.x + 4,self.y,self.width - 24,self.height - 13)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

        

class shuriken(object):
    img = [pygame.image.load(os.path.join('images', 'shuriken0.png')), pygame.image.load(os.path.join('images', 'shuriken1.png')), pygame.image.load(os.path.join('images', 'shuriken2.png')), pygame.image.load(os.path.join('images', 'shuriken3.png'))]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x,y,width,height)
        self.count = 0
        
    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 10, self.width - 20, self.height)
        if self.count >=8:
            self.count = 0
        win.blit(pygame.transform.scale(self.img[self.count//2], (64,64)), (self.x,self.y))
        self.count += 1
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        
    def hit(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
            return False
        
def end():
    global stop, objects, speed, score
    stop = 0
    objects = []
    speed = 80
    
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        win.blit(background, (0,0))
        fontLarge = pygame.font.SysFont('comicsans',80)
        highScore = fontLarge.render('high Score: ' + str(updateScore()), 1, (255,0,0))
        win.blit(highScore, (W/2 - highScore.get_width()/2,200))
        newScore = fontLarge.render('score: ' + str(score), 1, (255,0,0))
        win.blit(newScore, (W/2 - newScore.get_width()/2,250))
        pygame.display.update()

    score = 0        
    

def sidescrolling():
    win.blit(background , (background1,0))
    win.blit(background , (background2,0))
    runner.draw(win)
    for t in objects:
        t.draw(win)

    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('score: ' +str(score),1,(255,0,0))
    win.blit(text, (290, 10))
    pygame.display.update()




def updateScore():
    f = open('scores.txt','r')
    file = f.readlines()
    bestscore = int(file[0])

    if bestscore < int(score):
        f.close()
        file = open('scores.txt','w')
        file.write(str(score))
        file.close()

        return score

    return bestscore


runner = sprite(200,250,64,64)  
pygame.time.set_timer(USEREVENT+1,500)
pygame.time.set_timer(USEREVENT+2, random.randrange(3000,5000))
speed = 80
run = True

stop = 0
fallvelocity = 0
objects = []

pygame.init()

W, H = 800, 305
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Scurry')

background = pygame.image.load(os.path.join('images','tokoyobg.png')).convert()
background1 = 0
background2 = background.get_width()

clock = pygame.time.Clock()

while run:
    score = speed//5 - 16
    if stop > 0:
        stop +=1
        if stop > fallvelocity * 2:
            end()

    for o in objects:
        if o.hit(runner.hitbox):
            runner.falling = True

            if stop == 0:
                fallvelocity = speed
                stop = 1
        
        o.x -= 1.4
        if o.x < o.width * -1:
            objects.pop(objects.index(o))
                      
    background1 -= 1.4
    background2 -= 1.4
    if background1 < background.get_width() * -1:
        background1 = background.get_width()
    if background2 < background.get_width() * -1:
        background2 = background.get_width()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == USEREVENT+1:
            speed += 1

        if event.type == USEREVENT+2:
            r = random.randrange(0,1)
            if r == 0:
                objects.append(shuriken(810,250,64,64))
            else:
                pass
            
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not(runner.jumping):
            runner.jumping = True
                
        

    clock.tick(speed)
    sidescrolling()    

