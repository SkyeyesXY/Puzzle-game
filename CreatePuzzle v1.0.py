__author__ = 'Skyeyes'

import pygame, sys, random
from pygame.locals import *

def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

#main program begins
pygame.init()
pygame.display.set_caption("Puzzle")

font1 = pygame.font.Font(None, 2)
white = 255,255,255
red = 220,50,50
yellow = 230,230,50
black = 0,0,0

#get the puzzle's size
size = int(input("the puzzle size is: "))
long = 30
eage = long
num_size = 10
font2 = pygame.font.Font(None, num_size)
total_size = size*long+2*long
screen = pygame.display.set_mode((total_size,total_size))

class DisjointSet:
    def __init__(self, size):
        self.__size = size
        self.parent = [-1 for i in range(size)]

    def Find(self, x):
        if self.parent[x] < 0:
            return x
        self.parent[x] = self.Find(self.parent[x])
        return self.parent[x]

    def Union(self, root1, root2):
        if root1 == root2:
            return
        if self.parent[root1] > self.parent[root2]:
            self.parent[root2] += self.parent[root1]
            self.parent[root1] = root2
        else:
            self.parent[root1] += self.parent[root2]
            self.parent[root2] = root1


def createPuzzle(size):
    ds = DisjointSet(size*size)
    while ds.Find(0) != ds.Find(size*size-1):
        while True:
            num1 = random.randint(0, size*size-1)
            pos_x = num1 % size
            pos_y = num1 // size
            num2 = num1-size
            if num2 >= 0:
                if ds.Find(num1) != ds.Find(num2):
                    pygame.draw.line(screen, white, (eage+pos_x*long+1,eage+pos_y*long), (eage+pos_x*long+long-1,eage+pos_y*long))
                    break
            num2 = num1 - 1
            if num1 % size != 0:
                if ds.Find(num1) != ds.Find(num2):
                    pygame.draw.line(screen, white, (eage+pos_x*long,eage+pos_y*long+1), (eage+pos_x*long,eage+pos_y*long+long-1))
                    break
            num2 = num1 + size
            if num2 < size*size:
                if ds.Find(num1) != ds.Find(num2):
                    pygame.draw.line(screen, white, (eage+pos_x*long+1,eage+pos_y*long+long), (eage+pos_x*long+long-1,eage+pos_y*long+long))
                    break
            num2 = num1 + 1
            if num2 % size != 0:
                if ds.Find(num1) != ds.Find(num2):
                    pygame.draw.line(screen, white, (eage+pos_x*long+long,eage+pos_y*long+1), (eage+pos_x*long+long,eage+pos_y*long+long-1))
                    break
        ds.Union(ds.Find(num1), ds.Find(num2))
        print("<" + str(num1) + "," + str(num2) + ">,")

screen.fill(white)
i = 1

#draw the blog number
# for y in range(1,size+1):
#     for x in range(1,size+1):
#         print_text(font2, eage+(x-1)*long+(long-num_size)/2, eage+(y-1)*long+(long-num_size)/2, str(i))
#         i += 1

#draw the eage line
for x in range(1,size+2):
    pygame.draw.line(screen, black, (eage,eage+(x-1)*long), (total_size-eage,eage+(x-1)*long))
for y in range(1,size+2):
    pygame.draw.line(screen, black, (eage+(y-1)*long,eage), (eage+(y-1)*long,total_size-eage))
pygame.draw.line(screen, white, (eage,eage), (eage+long-1,eage))
pygame.draw.line(screen, white, (eage,eage), (eage,eage+long-1))
pygame.draw.line(screen, white, (total_size-eage,total_size-eage), (total_size-eage-long+1,total_size-eage))
pygame.draw.line(screen, white, (total_size-eage,total_size-eage), (total_size-eage,total_size-eage-long+1))

createPuzzle(size)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()

    pygame.display.update()
