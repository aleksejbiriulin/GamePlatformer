import sys
import pygame


class lums(pygame.sprite.Sprite):
    def __init__(self, x, y, a, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((a, a))
        self.image.fill(self.color)
        #img_dir = path.join(path.dirname(__file__), 'img')
        #self.image = pygame.image.load(path.join(img_dir, 'ray.jpg')).convert()
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
    def corx(self):
        return self.x
    def cory(self):
        return self.y

class colums(pygame.sprite.Sprite):
    def __init__(self, x, y, a, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((1, a))
        self.image.fill(self.color)
        #img_dir = path.join(path.dirname(__file__), 'img')
        #self.image = pygame.image.load(path.join(img_dir, 'ray.jpg')).convert()
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
    def corx(self):
        return self.x
    def cory(self):
        return self.y


def RGB(r, g, b):
    return '#' + r + g + b

def color_massiv():
    color = []
    for i in range(0, 256, 1):
        color.append(RGB(dec_to_hex(i, 2), '00', 'FF'))
    for i in range(0, 244, 1):
        color.append(RGB('FF', '00', dec_to_hex(255 - i, 2)))
    for i in range(0, 244, 1):
        color.append(RGB('FF', dec_to_hex(255 - i, 2), '00'))
    return color

def color_root(canv):
    XMAX = 256 * 2
    YMAX = 400
    for i in range(0, 256, 1):
        color = RGB('FF', dec_to_hex(i, 2), '00')
        canv.create_line(i, 0, i, YMAX + 1, fill=color)

    for i in range(0, 256, 1):
        color = RGB(dec_to_hex(255 - i, 2), 'FF', '00')
        canv.create_line(i + 256, 0, i + 256, YMAX + 1, fill=color)

def dec_to_hex(x, rasr):
    digits = '0123456789ABCDEF'
    hex_str = ''
    i = 0
    while i < rasr:
        hex_str = digits[x % 16] + hex_str
        x = x // 16
        i = i + 1
    return (hex_str)


def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(True, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def file_read(name):
    # file_out = open(name, 'a')
    # file_out.close()
    file_out = open(name, 'r')
    s = file_out.readline()
    file_list = []
    while s != '':
        s = s.rstrip()
        file_list.append(s)
        s = file_out.readline()
    file_out.close()
    return file_list

def rest(i, j, color1, color2, n):
    global lum, color
    color[i][j] = color2
    lum[i * n + j].image.fill(color2)
    if j < len(color[0]) - 1:
        if color[i][j+1] == color1:
            rest(i, j + 1, color1, color2, n)
    if j > 0:
        if color[i][j-1] == color1:
            rest(i, j - 1, color1, color2, n)
    if i < len(color) - 1:
        if color[i + 1][j] == color1:
            rest(i + 1, j, color1, color2, n)
    if i > 0 and j > 0:
        if color[i - 1][j - 1] == color1:
            rest(i - 1, j - 1, color1, color2, n)
    if j < len(color[0]) - 1 and i < len(color) - 1:
        if color[i + 1][j+1] == color1:
            rest(i + 1, j + 1, color1, color2, n)
    if j > 0 and i < len(color) - 1:
        if color[i + 1][j-1] == color1:
            rest(i + 1, j - 1, color1, color2, n)
    if i > 0 and j < len(color) - 1:
        if color[i - 1][j + 1] == color1:
            rest(i - 1, j + 1, color1, color2, n)



def main():
    sys.setrecursionlimit(10000)
    global lum, color
    n= 20
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    open_name = input()
    file_name = input()
    if open_name=='new':
        file_out = open(file_name, 'w')
        color = []
        for i in range(0, n, 1):
            k = []
            s = ''
            for j in range(0, n, 1):
                k.append(WHITE)
                s += str(WHITE[0]) + ' '  + str(WHITE[1]) + ' ' + str(WHITE[2]) + ' '
            print(s, file = file_out)
            color.append(k)
        file_out.close()
    elif open_name == 'open':
        color = []
        file_list = file_read(file_name)
        n = len(file_list)
        for i in range(0, n, 1):
            k = file_list[i].split()
            x = [0]*n
            for j in range(0, n, 1):
                x[j] = (int(k[3*j]), int(k[3*j+1]), int(k[3*j + 2]))
            color.append(x)





    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    running_main = True

    FPS = 30

    # Задаем цвета


    hieght = 800
    widht = 800


    # Создаем игру и окно
    pygame.init()
    pygame.mixer.init()
    #pygame.FULLSCREEN
    screen = pygame.display.set_mode((widht + 750, hieght + 120))
    pygame.display.set_caption("Pixels Draw " + file_name)
    clock = pygame.time.Clock()
    # Рендеринг
    screen.fill(BLACK)
    pygame.display.flip()
    widht, hieght = pygame.display.get_surface().get_size()

    all_sprites = pygame.sprite.Group()
    all_sprites.update()
    all_sprites.draw(screen)
    w, h = pygame.display.get_surface().get_size()
    w1,h1 = w, h
    #draw_text(surf, text, size, x, y, RED)
    w-= 750
    h -= 125
    x = (w  - h) // 2 + 50
    y = 110
    lum = []
    a = h//n
    for i in range(0, n, 1):
        for j in range(0, n, 1):
            lum_x = x+w//n*j + j
            lum_y = y + h//n* i  + i
            lum.append(lums(lum_x, lum_y, h//n, color[i][j]))
            all_sprites.add(lum[-1])
            all_sprites.update()
    color_main = RED
    running_main = True
    c  = 0
    all_sprites.update()
    lum_color = lums(w + 100, h //2, h // n,  RED)
    all_sprites.add(lum_color)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()
    color_sp = [WHITE] * 5
    colum = []
    coly= 5
    colx = 10
    colum.append(colums(colx, coly, 100, color_sp[-1]))
    colx+=1
    all_sprites.add(colum[-1])
    colum.append(colums(colx, coly, 100, color_sp[-1]))
    colx += 1
    all_sprites.add(colum[-1])
    colum.append(colums(colx, coly, 100, color_sp[-1]))
    colx += 1
    all_sprites.add(colum[-1])
    colum.append(colums(colx, coly, 100, color_sp[-1]))
    colx += 1
    all_sprites.add(colum[-1])
    colum.append(colums(colx, coly, 100, color_sp[-1]))
    colx += 1
    all_sprites.add(colum[-1])
    all_sprites.update()
    for i in range(0, 256, 1):
        color_sp.append((255,i,0))
        colum.append(colums(colx, coly, 100, color_sp[-1]))
        colx += 1
        all_sprites.add(colum[-1])
        all_sprites.update()

    for i in range(0, 256, 1):
        color_sp.append((255-i,255,0))
        colum.append(colums(colx, coly, 100, color_sp[-1]))
        colx += 1
        all_sprites.add(colum[-1])
        all_sprites.update()
    for i in range(0, 256, 1):
        color_sp.append((0,255,i))
        colum.append(colums(colx, coly, 100, color_sp[-1]))
        colx += 1
        all_sprites.add(colum[-1])
        all_sprites.update()
    for i in range(0, 256, 1):
        color_sp.append((0, 255-i, 255))
        colum.append(colums(colx, coly, 100, color_sp[-1]))
        colx += 1
        all_sprites.add(colum[-1])
        all_sprites.update()

    for i in range(0, 256, 1):
        color_sp.append((i,0,255))
        colum.append(colums(colx, coly, 100, color_sp[-1]))
        colx += 1
        all_sprites.add(colum[-1])
        all_sprites.update()
    for i in range(0, 256, 1):
        color_sp.append((255, 0, 255-i))
        colum.append(colums(colx, coly, 100, color_sp[-1]))
        colx += 1
        all_sprites.add(colum[-1])
        all_sprites.update()
    d = True
    restbool = False
    while running_main:
        a = h // n
        all_sprites.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                running_main = False
                gamer = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    x = input()
                    if x == 'save':
                        file_out = open(file_name, 'w')
                        for i in range(0, n, 1):
                            s = ''
                            for j in range(0, n, 1):
                                s += str( color[i][j][0]) + ' ' + str(color[i][j][1]) + ' ' + str(color[i][j][2]) + ' '
                            print(s, file=file_out)
                    else:
                        x = int(x)
                        y = int(input())
                        z = int(input())
                        color_main = (x, y, z)
                        lum_color.image.fill(color_main)
                if event.key == pygame.K_s:
                    file_out = open(file_name, 'w')
                    for i in range(0, n, 1):
                        s = ''
                        for j in range(0, n, 1):
                            s += str(color[i][j][0]) + ' ' + str(color[i][j][1]) + ' ' + str(color[i][j][2]) + ' '
                        print(s, file=file_out)
                elif event.key == pygame.K_r:
                    d = False
                    restbool = not restbool
                elif event.key == pygame.K_l:
                    d = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = pos[0], pos[1]
                c = True
                i = 0
                if 5 < mouse_y < 105 and 5 <=  mouse_x <= 5 + 256 * 6:
                    color_main = color_sp[mouse_x - 5]
                    lum_color.image.fill(color_main)
                    c = False
                while i < len(lum) and c:
                    cx = lum[i].corx() + a/2
                    cy = lum[i].cory() + a/2
                    if abs(cx-mouse_x) < a/2 and abs(cy-mouse_y) < a/2:
                        #lum[i] = lums(cx, cy, w/n, color_main)
                        color1 = color[i//n][i%n]
                        c = False
                        color[i//n][i%n] = color_main
                        if  color1 != color_main and restbool:
                            rest(i%n, i//n,color1 , color_main, n)
                            d = True
                            lum[i].image.fill(color_main)
                        else:
                            lum[i].image.fill(color_main)
                    i += 1
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()

    pygame.quit()
main()