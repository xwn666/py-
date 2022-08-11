# utf - 8
# 导入pygame外包

import pygame
import string
import sys
import operator

# 全局变量
mx, my = 200, 200
answer_x, answer_y = 0, 0
bg_size = (400, 500)
bg_x, bg_y = bg_size
stop = False
draw_mod = False
draw_win = pygame.Rect(0, 0, 400, 400)
# 常用颜色
red = (255, 0, 0)
pink = (255, 192, 203)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue_green = (0, 255, 255)
blue = (0, 0, 255)
purple = (128, 0, 128)
gray = (192, 192, 192)
white = (255, 255, 255)
black = (0, 0, 0)

# 初始化窗口
pygame.init()
win = pygame.display.set_mode(bg_size)
pygame.display.set_caption('一次函数')


# 输入窗口类
class InputBOX:
    def __init__(self, in_x, in_y, w, h, font_size):
        self.rect = pygame.Rect(in_x, in_y, w, h)
        self.font = pygame.font.Font('E:\字体\AaKaiSong（JianFan）-2.ttf', font_size)
        self.list = []
        self.count = 0
        self.delete = False
        self.active = False
        self.cursor = True

    def draw(self):
        pygame.draw.rect(win, black, self.rect, 1)
        text_pic = self.font.render(''.join(self.list), True, black)
        win.blit(text_pic, (self.rect.x + 1, self.rect.y + 2))
        self.count += 1
        if self.count == 9223372036854775806:
            self.count = 0
        if self.count % 250 == 0:
            self.cursor = not self.cursor
        if self.active and self.cursor:
            text_pic_rect = text_pic.get_rect()
            in_x = self.rect.x + 5 + text_pic_rect.width
            pygame.draw.line(win, black, (in_x, self.rect.y + 4), (in_x, self.rect.y + self.rect.height - 4))
        if self.delete and self.list and self.count % 83 == 0:
            self.list.pop()

    def get_text(self, events, len_list=255):
        if events.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(events.pos):
                self.active = True
            else:
                self.active = False
        elif self.active:
            if events == pygame.KEYDOWN:
                if events.key == pygame.K_BACKSPACE:
                    self.delete = True
                if len(self.list) <= len_list:
                    if events.unicode in string.ascii_letters or events.unicode in "1234567890_":
                        self.list.append(events.unicode)
            elif events.type == pygame.KEYUP:
                if events.key == pygame.K_BACKSPACE:
                    self.delete = False

    def get_num(self, events, len_list=255):
        if events.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(events.pos):
                self.active = True
            else:
                self.active = False
        elif self.active:
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_BACKSPACE:
                    self.delete = True
                if len(self.list) <= len_list - 1:
                    if len(self.list) == 0 and events.unicode in "1234567890-":
                        self.list.append(events.unicode)
                    elif len(self.list) == 1 and self.list[0] == "0" \
                            or len(self.list) == 2 and operator.eq(self.list[0:2], ["-", "0"]):
                        if events.unicode in ".":
                            self.list.append(events.unicode)
                    elif len(self.list) == 1 and self.list[0] == "-" \
                            or len(self.list) >= 1 and "." in self.list:
                        if event.unicode in "1234567890":
                            self.list.append(event.unicode)
                    elif event.unicode in "1234567890.":
                        self.list.append(event.unicode)
                if len(self.list) == len_list:
                    for i in range(len_list):
                        # print(self.list,self.list[-1])
                        if self.list[-1] == "0":
                            self.list.pop()
                        else:
                            break
            elif events.type == pygame.KEYUP:
                if events.key == pygame.K_BACKSPACE:
                    self.delete = False

    @property
    def back_text(self):
        return "".join(self.list)

    @property
    def back_num(self):
        number = 0
        count = 0
        num = 0
        copy_list = self.list.copy()
        if self.list:
            # 读取数字并合法化
            if "." in self.list:
                point_index = copy_list.index(".")
                little_num = copy_list[point_index:]
                del copy_list[point_index:]
                big_num = copy_list
                for i in big_num:
                    if i in "1234567890":
                        i = int(i)
                    else:
                        i = 0
                    count += 1
                    number += i * 10 ** (len(big_num) - count)
                count = 0
                for i in little_num:
                    if i in "1234567890":
                        i = int(i)
                    else:
                        i = 0
                    num += i * 0.1 ** count
                    count += 1
                number += num
            else:
                for i in self.list:
                    if i in "1234567890":
                        i = int(i)
                    else:
                        i = 0
                    count += 1
                    number += i * 10 ** (len(self.list) - count)
            # 返回数字
            if self.list[0] == "-":
                # print(-1 * number,self.list)
                return -1 * number
            else:
                # print(number,big_num,len(big_num),little_num,len(little_num),self.list,len(self.list))
                return number
        else:
            return 0


# 文字显示类
class Text:
    def __init__(self, msg, m_x, m_y, font_size, bg_color):
        self.font = pygame.font.Font('E:\字体\AaKaiSong（JianFan）-2.ttf', font_size)
        self.x = m_x
        self.y = m_y
        self.msg = msg
        self.text = self.font.render(msg, True, black, bg_color)
        self.text_size = self.text.get_size()

    def draw(self):
        win.blit(self.text, (self.x, self.y))

    def back(self):
        return self.msg, self.text_size


# 报错方法
def error():
    error_text = Text("你输入的表达式违法了！！！", 0, 0, 32, red)
    error_text.draw()


# 绘制一次函数类
class Linear_function:
    def __init__(self, lf_k, lf_b):
        self.x = mx
        self.y = my
        self.k = lf_k
        self.b = lf_b

    def draw(self):
        if draw_mod:
            pygame.draw.line(win, black, (mx, 0), (mx, 400))
            pygame.draw.line(win, black, (0, my), (400, my))
        else:
            for i in range(17):
                if i == 0:
                    color = black
                else:
                    color = gray
                pygame.draw.line(win, color, (mx + 30 * i, 0), (mx + 30 * i, 400))
                pygame.draw.line(win, color, (mx - 30 * i, 0), (mx - 30 * i, 400))
                pygame.draw.line(win, color, (0, my + 30 * i), (400, my + 30 * i))
                pygame.draw.line(win, color, (0, my - 30 * i), (400, my - 30 * i))
        if self.k != 0 or self.b != 0:
            # y = -k(x-mx) + b + my
            y1 = self.x * self.k - self.b * 30 + self.y
            y2 = -1 * self.k * (400 - self.x) - self.b * 30 + self.y
            pygame.draw.line(win, red, (0, y1), (400, y2))

        # 一次函数计算方法

    def Linear_function(self, tip=1, lf_x=0, lf_y=0):
        if tip == 1:
            an_y = lf_x * self.k + self.b
            return an_y
        elif tip == 2:
            an_x = (lf_y - self.b) / self.k
            return an_x
        # pygame.draw.line(win,black,(mx,0),(mx,400),1)
        # pygame.draw.line(win, black, (200, 0), (200, 400), 1)


# 创建默认类
Function_Text1 = Text("y=kx+b", 0, 0, 23, white)
Function_Text2 = Text("x=(y-b)/k", 0, 25, 23, white)
k = Text("k", 0, 400, 50, (218, 201, 166))
b = Text("b", 0, 450, 50, (218, 201, 166))
x = Text("x", 200, 400, 50, (218, 201, 166))
y = Text("y", 200, 440, 50, (218, 201, 166))
k_box = InputBOX(25, 405, 170, 40, 35)
b_box = InputBOX(25, 455, 170, 40, 35)
x_box = InputBOX(225, 405, 170, 40, 35)
y_box = InputBOX(225, 455, 170, 40, 35)
# 循环播放
while True:
    # 背景
    win.fill(white)
    # OK开始写代码了！！！
    new_x = x_box.back_num
    new_y = y_box.back_num
    new_k = k_box.back_num
    new_b = b_box.back_num
    # print(new_x,new_y,new_k,new_b)
    Linear_Function = Linear_function(new_k, new_b)
    if not y_box.list:
        answer_y = Linear_Function.Linear_function(1, new_x, new_y)

    elif not x_box.list and new_k != 0:
        answer_x = Linear_Function.Linear_function(2, new_x, new_y)

    if answer_x == 0.0:
        answer_x = int(answer_x)
    if answer_y == 0.0:
        answer_y = int(answer_y)
    dr_answer_y = Text(str(answer_y), 226, 457, 35, white)
    dr_answer_x = Text(str(answer_x), 226, 407, 35, white)
    # print(answer_x,answer_y)
    # 画面
    Function_Text1.draw()
    Function_Text2.draw()
    Linear_Function.draw()

    # 文本
    pygame.draw.rect(win, (218, 201, 166), (0, 400, 400, 500))
    k.draw()
    b.draw()
    x.draw()
    y.draw()
    k_box.draw()
    b_box.draw()
    x_box.draw()
    y_box.draw()
    if k_box.list and b_box.list and x_box.list:
        dr_answer_y.draw()
    elif k_box.list and b_box.list and y_box.list:
        dr_answer_x.draw()

    # 最高图层
    if y_box.list and b_box.list and k_box.list and new_k == 0:
        error()
    # 刷新屏幕
    pygame.display.update()
    # print(x_box.list,y_box.list)
    # 事件监听
    for event in pygame.event.get():
        k_box.get_num(event, 10)
        b_box.get_num(event, 10)
        if not x_box.list:
            y_box.get_num(event, 10)
        if not y_box.list:
            x_box.get_num(event, 10)
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            if not stop:
                mx, my = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if draw_win.collidepoint(event.pos):
                    stop = not stop
            elif event.button == 3:
                draw_mod = not draw_mod
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 or event.button == 3:
                pass
                # stop = not stop
