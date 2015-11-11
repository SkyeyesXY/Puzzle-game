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
font3 = pygame.font.Font(None, 60)

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


def block(color, pos_x, pos_y, width, height, font, text):
        pygame.draw.rect(screen, color, (pos_x, pos_y, width, height))
        if font == font1:
            print_text(font, pos_x + 10, pos_y + 20, text, black)
        else:
            print_text(font, pos_x + 15, pos_y + 15, text, black)

def Draw_block1():
    block(yellow, 785, 125, 50, 50, font2, "U")
    block(yellow, 785, 200, 50, 50, font2, "D")
    block(yellow, 710, 200, 50, 50, font2, "L")
    block(yellow, 860, 200, 50, 50, font2, "R")
    block(yellow, 760, 350, 100, 50, font1, "DRAW MAP")
    block(yellow, 760, 450, 100, 50, font1, "RESTART")
    block(yellow, 760, 550, 100, 50, font1, "NEW PUZZLE")


def Draw_block2():
    block(yellow, 280, 150, 400, 100, font3, "EASY(10*10)")
    block(yellow, 280, 270, 400, 100, font3, "NOMAL(20*20)")
    block(yellow, 280, 390, 400, 100, font3, "HARD(30*30)")
    block(yellow, 280, 510, 400, 100, font3, "CRAZY(50*50)")


def draw_road():
    point = size * size - 1

    while tree.parent[point] != -1:
        pos_f_x = point % size
        pos_f_y = point // size
        point = tree.parent[point]
        pos_e_x = point % size
        pos_e_y = point // size
        pygame.draw.line(screen, red, (eage + pos_f_x * long + long // 2, eage + pos_f_y * long + long // 2),
                         (eage + pos_e_x * long + long // 2, eage + pos_e_y * long + long // 2))


class Point:
    def __init__(self, size):
        self.__size = size
        self.__total = size * size
        self.parent = [-1 for i in range(size * size)]

    def Find(self, num1):
        pos_x = num1 % self.__size
        pos_y = num1 // self.__size

        num2 = num1 - self.__size
        if num2 >= 0:
            if enter_x[pos_y * self.__size + pos_x] == 1:
                self.parent[num2] = num1
                enter_x[pos_y * self.__size + pos_x] = 2
                if num2 != self.__total - 1:
                    self.Find(num2)
        num2 = num1 - 1
        if num1 % size != 0:
            if enter_y[pos_x * self.__size + pos_y] == 1:
                self.parent[num2] = num1
                enter_y[pos_x * self.__size + pos_y] = 2
                if num2 != self.__total - 1:
                    self.Find(num2)
        num2 = num1 + self.__size
        if num2 < self.__size * self.__size:
            if enter_x[(pos_y + 1) * self.__size + pos_x] == 1:
                self.parent[num2] = num1
                enter_x[(pos_y + 1) * self.__size + pos_x] = 2
                if num2 != self.__total - 1:
                    self.Find(num2)
        num2 = num1 + 1
        if num2 % size != 0:
            if enter_y[(pos_x + 1) * self.__size + pos_y] == 1:
                self.parent[num2] = num1
                enter_y[(pos_x + 1) * self.__size + pos_y] = 2
                if num2 != self.__total - 1:
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
                    enter_x[pos_y * size + pos_x] = 1
                    break
            num2 = num1 - 1
            if num1 % size != 0:
                if ds.Find(num1) != ds.Find(num2):
                    enter_y[pos_x * size + pos_y] = 1
                    break
            num2 = num1 + size
            if num2 < size * size:
                if ds.Find(num1) != ds.Find(num2):
                    enter_x[(pos_y + 1) * size + pos_x] = 1
                    break
            num2 = num1 + 1
            if num2 % size != 0:
                if ds.Find(num1) != ds.Find(num2):
                    enter_y[(pos_x + 1) * size + pos_y] = 1
                    break
        ds.Union(ds.Find(num1), ds.Find(num2))
        enter_x[0] = enter_x[size * (size + 1) - 1] = 1
        enter_y[0] = enter_y[size * (size + 1) - 1] = 1


def draw_Puzzle():
    i = 0
    for x in enter_x:
        if x != 0:
            pos_x = i % size
            pos_y = i // size
            pygame.draw.line(screen, white, (eage + pos_x * long, eage + pos_y * long),
                             (eage + (pos_x + 1) * long, eage + pos_y * long))
        i += 1

    i = 0
    for y in enter_y:
        if y != 0:
            pos_y = i % size
            pos_x = i // size
            pygame.draw.line(screen, white, (eage + pos_x * long, eage + pos_y * long),
                             (eage + pos_x * long, eage + (pos_y + 1) * long))
        i += 1


createPuzzle(size)
num1 = 0
tree = Point(size)
tree.Find(num1)

pos_x = pos_y = 0
road = 0
code = 0
help = 3
restart = 5
new = 3
choose = 0
out_flag = 0


while True:
    screen.fill(white)
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    print_text(font3, 380, 50, "Choose level", black)
    Draw_block2()
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.type == MOUSEBUTTONUP:
            mouse_up_x, mouse_up_y = event.pos
            if 280 <= mouse_up_x <= 680 and 150 <= mouse_up_y <= 250:
                size = 10
                out_flag = 1
            elif 280 <= mouse_up_x <= 680 and 270 <= mouse_up_y <= 370:
                size = 20
                out_flag = 1
            elif 280 <= mouse_up_x <= 680 and 390 <= mouse_up_y <= 490:
                size = 30
                out_flag = 1
            elif 280 <= mouse_up_x <= 680 and 510 <= mouse_up_y <= 610:
                size = 50
                out_flag = 1
    if out_flag == 1:
        break



    pygame.display.update()

while True:
    screen.fill(white)
    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    for x in range(1, size + 2):
        pygame.draw.line(screen, black, (eage, eage + (x - 1) * long), (eage + size * long, eage + (x - 1) * long))

    for y in range(1, size + 2):
        pygame.draw.line(screen, black, (eage + (y - 1) * long, eage), (eage + (y - 1) * long, heigh - eage))

    draw_Puzzle()
    Draw_block1()

    print_text(font1, 650, 20, "Code:" + str(code), black)
    print_text(font1, 710, 20, "Help:" + str(help), black)
    print_text(font1, 760, 20, "Restart:" + str(restart), black)
    print_text(font1, 830, 20, "New:" + str(new), black)
    print_text(font1, 880, 20, "Size:" + str(size), black)


    if size <= 50:
        pygame.draw.circle(screen, yellow, (int(eage + pos_x * long + long // 2), int(eage + pos_y * long + long // 2)),
                           long // 4)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if pos_y != 0 and enter_x[pos_y * size + pos_x] != 0:
                    pos_y -= 1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if pos_y != size - 1 and enter_x[(pos_y + 1) * size + pos_x] != 0:
                    pos_y += 1
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if pos_x != size - 1 and enter_y[(pos_x + 1) * size + pos_y] != 0:
                    pos_x += 1
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if pos_x != 0 and enter_y[pos_x * size + pos_y] != 0:
                    pos_x -= 1

        elif event.type == MOUSEBUTTONUP:
            mouse_up_x, mouse_up_y = event.pos
            if 785 <= mouse_up_x <= 835 and 125 <= mouse_up_y <= 175:
                if pos_y != 0 and enter_x[pos_y * size + pos_x] != 0:
                    pos_y -= 1
            elif 785 <= mouse_up_x <= 835 and 200 <= mouse_up_y <= 250:
                if pos_y != size - 1 and enter_x[(pos_y + 1) * size + pos_x] != 0:
                    pos_y += 1
            elif 710 <= mouse_up_x <= 760 and 200 <= mouse_up_y <= 250:
                if pos_x != 0 and enter_y[pos_x * size + pos_y] != 0:
                    pos_x -= 1
            elif 860 <= mouse_up_x <= 910 and 200 <= mouse_up_y <= 250:
                if pos_x != size - 1 and enter_y[(pos_x + 1) * size + pos_y] != 0:
                    pos_x += 1
            elif 760 <= mouse_up_x <= 860 and 350 <= mouse_up_y <= 400:
                if road == 0:
                    road = 1
                    help -= 1
                else:
                    road = 0
            elif 760 <= mouse_up_x <= 860 and 450 <= mouse_up_y <= 500:
                if restart > 0:
                    pos_x = pos_y = 0
                restart -= 1
            elif 760 <= mouse_up_x <= 860 and 550 <= mouse_up_y <= 600:
                if new > 0:
                    enter_x = [0 for x in range(size * (size + 1))]
                    enter_y = [0 for x in range(size * (size + 1))]
                    createPuzzle(size)
                    num1 = 0
                    tree = Point(size)
                    tree.Find(num1)

                    pos_x = pos_y = 0
                    road = 0

                new -= 1

    if pos_x == pos_y == size - 1:
        enter_x = [0 for x in range(size * (size + 1))]
        enter_y = [0 for x in range(size * (size + 1))]
        createPuzzle(size)
        num1 = 0
        tree = Point(size)
        tree.Find(num1)

        pos_x = pos_y = 0
        road = 0

        code += 10

    if help <= 0:
        help = 0
        print_text(font1, 700, 50, "You can't get help", black)

    if restart <= 0:
        restart = 0
        print_text(font1, 700, 70, "You can't restart the game", black)

    if new <= 0:
        new = 0
        print_text(font1, 700, 90, "You can't get a new puzzle", black)


    if road == 1 and help > 0:
        draw_road()

    pygame.display.update()
