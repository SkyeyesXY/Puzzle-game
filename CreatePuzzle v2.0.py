__author__ = 'Skyeyes'

import pygame, sys, random
from pygame.locals import *

sys.setrecursionlimit(1000000)

def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))


# main program begins
pygame.init()
pygame.display.set_caption("Puzzle")

font1 = pygame.font.Font(None, 2)
white = 255, 255, 255
red = 220, 50, 50
yellow = 230, 230, 50
black = 0, 0, 0

# get the puzzle's size
size = int(input("the puzzle size is: "))
heigh = 660
width = 660
long = 600 // size
eage = (heigh - long * size) / 2

screen = pygame.display.set_mode((width, heigh))

enter_x = [0 for x in range(size * (size + 1))]
enter_y = [0 for x in range(size * (size + 1))]
tree = 0


def draw_road():
    point = size*size-1

    while tree.parent[point] != -1:
        pos_f_x = point % size
        pos_f_y = point // size
        point = tree.parent[point]
        pos_e_x = point % size
        pos_e_y = point // size
        pygame.draw.line(screen, red, (eage+pos_f_x*long+long//2, eage+pos_f_y*long+long//2),(eage+pos_e_x*long+long//2, eage+pos_e_y*long+long//2))


class Point:
    def __init__(self, size):
        self.__size = size
        self.__total = size*size
        self.parent = [-1 for i in range(size*size)]


    def Find(self, num1):
        pos_x = num1 % self.__size
        pos_y = num1 // self.__size

        num2 = num1 - self.__size
        if num2 >= 0:
            if enter_x[pos_y*self.__size+pos_x] == 1:
                self.parent[num2] = num1
                enter_x[pos_y*self.__size+pos_x] = 2
                if num2 != self.__total-1:
                    self.Find(num2)
        num2 = num1 - 1
        if num1 % size != 0:
            if enter_y[pos_x*self.__size+pos_y] == 1:
                self.parent[num2] = num1
                enter_y[pos_x*self.__size+pos_y] = 2
                if num2 != self.__total-1:
                    self.Find(num2)
        num2 = num1 + self.__size
        if num2 < self.__size * self.__size:
            if enter_x[(pos_y+1)*self.__size+pos_x] == 1:
                self.parent[num2] = num1
                enter_x[(pos_y+1)*self.__size+pos_x] = 2
                if num2 != self.__total-1:
                    self.Find(num2)
        num2 = num1 + 1
        if num2 % size != 0:
            if enter_y[(pos_x+1)*self.__size+pos_y] == 1:
                self.parent[num2] = num1
                enter_y[(pos_x+1)*self.__size+pos_y] = 2
                if num2 != self.__total-1:
                    self.Find(num2)


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
    ds = DisjointSet(size * size)
    while ds.Find(0) != ds.Find(size * size - 1):
        while True:
            num1 = random.randint(0, size * size - 1)
            pos_x = num1 % size
            pos_y = num1 // size
            num2 = num1 - size
            if num2 >= 0:
                if ds.Find(num1) != ds.Find(num2):
                    enter_x[pos_y*size+pos_x] = 1
                    break
            num2 = num1 - 1
            if num1 % size != 0:
                if ds.Find(num1) != ds.Find(num2):
                    enter_y[pos_x*size+pos_y] = 1
                    break
            num2 = num1 + size
            if num2 < size * size:
                if ds.Find(num1) != ds.Find(num2):
                    enter_x[(pos_y+1)*size+pos_x] = 1
                    break
            num2 = num1 + 1
            if num2 % size != 0:
                if ds.Find(num1) != ds.Find(num2):
                    enter_y[(pos_x+1)*size+pos_y] = 1
                    break
        ds.Union(ds.Find(num1), ds.Find(num2))
        enter_x[0] = enter_x[size * (size + 1)-1] = 1
        enter_y[0] = enter_y[size * (size + 1)-1] = 1

def draw_Puzzle():
    i = 0
    for x in enter_x:
        if x != 0:
            pos_x = i % size
            pos_y = i // size
            pygame.draw.line(screen, white, (eage+pos_x*long,eage+pos_y*long),(eage+(pos_x+1)*long,eage+pos_y*long))
        i += 1

    i = 0
    for y in enter_y:
        if y != 0:
            pos_y = i % size
            pos_x = i // size
            pygame.draw.line(screen, white, (eage+pos_x*long,eage+pos_y*long),(eage+pos_x*long,eage+(pos_y+1)*long))
        i += 1

createPuzzle(size)
num1 = 0
tree = Point(size)
tree.Find(num1)

pos_x = pos_y = 0
road = 0

while True:
    screen.fill(white)

    for x in range(1, size + 2):
        pygame.draw.line(screen, black, (eage, eage + (x - 1) * long), (eage + size * long, eage + (x - 1) * long))

    for y in range(1, size + 2):
        pygame.draw.line(screen, black, (eage + (y - 1) * long, eage), (eage + (y - 1) * long, heigh - eage))

    draw_Puzzle()
    if size <= 50:
        pygame.draw.circle(screen, yellow, (int(eage+pos_x*long+long//2),int(eage+pos_y*long+long//2)), long//4)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_w:
                    if pos_y != 0 and enter_x[pos_y*size+pos_x] != 0:
                        pos_y -= 1
                elif event.key == pygame.K_s:
                    if pos_y != size-1 and enter_x[(pos_y+1)*size+pos_x] != 0:
                        pos_y += 1
                elif event.key == pygame.K_d:
                    if pos_x != size-1 and enter_y[(pos_x+1)*size+pos_y] != 0:
                        pos_x += 1
                elif event.key == pygame.K_a:
                    if pos_x != 0 and enter_y[pos_x*size+pos_y] != 0:
                        pos_x -= 1
    keys = pygame.key.get_pressed()
    if keys[K_m]:
        if road == 0:
            road = 1
        else:
            road = 0
    if road == 1:
        draw_road()

    pygame.display.update()