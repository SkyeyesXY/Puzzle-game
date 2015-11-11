__author__ = 'Skyeyes'

import pygame, sys, random
from pygame.locals import *


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
width = 1200
long = 600 // size
eage = (heigh - long * size) / 2
# num_size = long//3
# font2 = pygame.font.Font(None, num_size)

screen = pygame.display.set_mode((width, heigh))

enter_x = [0 for x in range(size * (size + 1))]
enter_y = [0 for x in range(size * (size + 1))]


def draw_line(color, start_x, start_y, end_x, end_y, pos=screen):
    if end_y == start_y:
        count = int((end_x-start_x) // long)
        count_x = int((start_x - eage) // long)
        count_y = int((start_y - eage) // long)
        for x in range(count):
            if color == white:
                enter_x[count_y * size + count_x] = 1
                count_x += 1
    if end_x == start_x:
        count = int((end_y-start_y) // long)
        count_x = int((start_x - eage) // long)
        count_y = int((start_y - eage) // long)
        for y in range(count):
            if color == white:
                enter_y[count_x * size + count_y] = 1
                count_y += 1
    pygame.draw.line(pos, color, (start_x, start_y), (end_x, end_y))

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
            # print(str(root1) + "parent is " + str(root2))
        else:
            self.parent[root1] += self.parent[root2]
            self.parent[root2] = root1
            # print(str(root2) + "parent is " + str(root1))


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
                    draw_line(white, eage + pos_x * long, eage + pos_y * long,
                                     eage + pos_x * long + long, eage + pos_y * long)
                    break
            num2 = num1 - 1
            if num1 % size != 0:
                if ds.Find(num1) != ds.Find(num2):
                    draw_line(white, eage + pos_x * long, eage + pos_y * long,
                                     eage + pos_x * long, eage + pos_y * long + long)
                    break
            num2 = num1 + size
            if num2 < size * size:
                if ds.Find(num1) != ds.Find(num2):
                    draw_line(white, eage + pos_x * long, eage + pos_y * long + long,
                                     eage + pos_x * long + long, eage + pos_y * long + long)
                    break
            num2 = num1 + 1
            if num2 % size != 0:
                if ds.Find(num1) != ds.Find(num2):
                    draw_line(white, eage + pos_x * long + long, eage + pos_y * long,
                                     eage + pos_x * long + long, eage + pos_y * long + long)
                    break
        ds.Union(ds.Find(num1), ds.Find(num2))
        # print("<" + str(num1) + "," + str(num2) + ">,")


screen.fill(white)
i = 1

# draw the blog number
# for y in range(1,size+1):
#     for x in range(1,size+1):
#         print_text(font2, eage+(x-1)*long+(long-num_size)/2, eage+(y-1)*long+(long-num_size)/2, str(i))
#         i += 1

# draw the eage line
for x in range(1, size + 2):
    draw_line(black, eage, eage + (x - 1) * long, eage + size * long, eage + (x - 1) * long)

for y in range(1, size + 2):
    draw_line(black, eage + (y - 1) * long, eage, eage + (y - 1) * long, heigh - eage)
draw_line(white, eage, eage, eage + long, eage)
draw_line(white, eage, eage, eage, eage + long)
draw_line(white, eage + size * long - long, heigh - eage,
                 eage + size * long, heigh - eage)
draw_line(white, eage + size * long, heigh - eage - long,
                 eage + size * long, heigh - eage)

createPuzzle(size)

# print(enter_x)
# print(enter_y)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()

    pygame.display.update()
