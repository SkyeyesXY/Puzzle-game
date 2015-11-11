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

font1 = pygame.font.Font(None, 20)
font2 = pygame.font.Font(None, 40)
white = 255, 255, 255
red = 220, 50, 50
yellow = 230, 230, 50
black = 0, 0, 0

# get the puzzle's size
size = int(input("the puzzle size is: "))
heigh = 660
width = 960
long = 600 // size
eage = (heigh - long * size) / 2

screen = pygame.display.set_mode((width, heigh))

enter_x = [0 for x in range(size * (size + 1))]
enter_y = [0 for x in range(size * (size + 1))]
tree = 0


def Draw_block():
    def block(color, pos_x, pos_y, width, height, font, text):
        pygame.draw.rect(screen, color, (pos_x, pos_y, width, height))
        if font == font1:
            print_text(font, pos_x+10, pos_y+20, text, black)
        else:
            print_text(font, pos_x+15, pos_y+15, text, black)

    block(yellow, 785, 125, 50, 50, font2, "U")
    # pos_rect_up_h = 785, 125
    # pos_rect_up_b = 835, 175
    # pygame.draw.rect(screen, black, pos_rect_up_h, pos_rect_up_b)
    # print_text(font1, 800, 145, 'UP', white)

    block(yellow, 785, 200, 50, 50, font2, "D")
    # pos_rect_down_h = 785, 200, 835, 250
    # pygame.draw.rect(screen, black, pos_rect_down)
    # print_text(font1, 800, 220, 'DOWN', white)

    block(yellow, 710, 200, 50, 50, font2, "L")
    # pos_rect_left_h = 710, 200
    # pos_rect_left_b = 760, 250
    # pygame.draw.rect(screen, black, pos_rect_left_h, pos_rect_left_b)
    # print_text(font1, 725, 220, 'LEFT', white)

    block(yellow, 860, 200, 50, 50, font2, "R")
    # pos_rect_right_h = 860, 200
    # pos_rect_right_b = 910, 250
    # pygame.draw.rect(screen, black, pos_rect_right_h, pos_rect_right_b)
    # print_text(fint1, 875, 220, 'RIGHT', white)

    block(yellow, 760, 350, 100, 50, font1, "DRAW MAP")
    # pos_rect_map = 760, 350, 860, 400
    # pygame.draw.rect(screen, black, pos_rect_map)
    # print_text(font1, 770, 370, 'DRAW MAP', white)

    block(yellow, 760, 450, 100, 50, font1, "RESTART")
    # pos_rect_restart = 760, 450, 860, 500
    # pygame.draw.rect(screen, black, pos_rect_restart)
    # print_text(font1, 775, 470, 'RESTART', white)

    block(yellow, 760, 550, 100, 50, font1, "NEW PUZZLE")
    # pos_rect_new = 760, 550, 860, 600
    # pygame.draw.rect(screen, black, pos_rect_new)
    # print_text(font1, 765, 570, 'NEW PUZZLE', white)


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
    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    for x in range(1, size + 2):
        pygame.draw.line(screen, black, (eage, eage + (x - 1) * long), (eage + size * long, eage + (x - 1) * long))

    for y in range(1, size + 2):
        pygame.draw.line(screen, black, (eage + (y - 1) * long, eage), (eage + (y - 1) * long, heigh - eage))

    draw_Puzzle()
    Draw_block()

    if size <= 50:
        pygame.draw.circle(screen, yellow, (int(eage+pos_x*long+long//2),int(eage+pos_y*long+long//2)), long//4)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if pos_y != 0 and enter_x[pos_y*size+pos_x] != 0:
                    pos_y -= 1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if pos_y != size-1 and enter_x[(pos_y+1)*size+pos_x] != 0:
                    pos_y += 1
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if pos_x != size-1 and enter_y[(pos_x+1)*size+pos_y] != 0:
                    pos_x += 1
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if pos_x != 0 and enter_y[pos_x*size+pos_y] != 0:
                    pos_x -= 1

        elif event.type == MOUSEBUTTONUP:
            mouse_up_x, mouse_up_y = event.pos
            if 785 <= mouse_up_x <= 835 and 125 <= mouse_up_y <= 175:
                if pos_y != 0 and enter_x[pos_y*size+pos_x] != 0:
                        pos_y -= 1
            elif 785 <= mouse_up_x <= 835 and 200 <= mouse_up_y <= 250:
                if pos_y != size-1 and enter_x[(pos_y+1)*size+pos_x] != 0:
                        pos_y += 1
            elif 710 <= mouse_up_x <= 760 and 200 <= mouse_up_y <= 250:
                if pos_x != 0 and enter_y[pos_x*size+pos_y] != 0:
                    pos_x -= 1
            elif 860 <= mouse_up_x <= 910 and 200 <= mouse_up_y <= 250:
                if pos_x != size-1 and enter_y[(pos_x+1)*size+pos_y] != 0:
                    pos_x += 1
            elif 760 <= mouse_up_x <= 860 and 350 <= mouse_up_y <= 400:
                if road == 0:
                    road = 1
                else:
                    road = 0
            elif 760 <= mouse_up_x <= 860 and 450 <= mouse_up_y <= 500:
                pos_x = pos_y = 0
            elif 760 <= mouse_up_x <= 860 and 550 <= mouse_up_y <= 600:
                enter_x = [0 for x in range(size * (size + 1))]
                enter_y = [0 for x in range(size * (size + 1))]
                createPuzzle(size)
                num1 = 0
                tree = Point(size)
                tree.Find(num1)

                pos_x = pos_y = 0
                road = 0


    keys = pygame.key.get_pressed()
    if keys[K_m]:
        if road == 0:
            road = 1
        else:
            road = 0
    if road == 1:
        draw_road()

    pygame.display.update()


