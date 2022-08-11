# utf - 8
# 导入pygame外包

import pygame
import string
import sys
import operator
import time

# 全局变量
mx, my = 400, 400
answer_x1,answer_x2, answer_y = 0, 0, 0
bg_size = (800, 800)
bg_x, bg_y = bg_size
stop = True
draw_mod = False
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
pygame.display.set_caption('二次函数')


# 输入窗口类
class InputBOX:
    def __init__(self, in_x, in_y, w, h, font_size):
        self.rect = pygame.Rect(in_x, in_y, w, h)
        self.font = pygame.font.Font('./AaKaiSong（JianFan）-2.ttf', font_size)
        self.list = []
        self.count = 0
        self.delete = False
        self.active = False
        self.cursor = True

    def draw(self):
        pygame.draw.rect(win, black, self.rect, 2)
        text_pic = self.font.render(''.join(self.list), True, black)
        win.blit(text_pic, (self.rect.x + 1, self.rect.y + 2))
        self.count += 1
        if self.count == 9223372036854775806:
            self.count = 0
        if self.count % 100 == 0:
            self.cursor = not self.cursor
        if self.active and self.cursor:
            text_pic_rect = text_pic.get_rect()
            in_x = self.rect.x + 5 + text_pic_rect.width
            pygame.draw.line(win, black, (in_x, self.rect.y + 4), (in_x, self.rect.y + self.rect.height - 4))
        if self.delete and self.list and self.count % 10 == 0:
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
        self.font = pygame.font.Font('./AaKaiSong（JianFan）-2.ttf', font_size)
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


# 多次点击类
class Click:
    def __init__(self, interval_short, interval_long, count):
        self.inter_short = interval_short
        self.inter_lone = interval_long
        self.count = count
        self.time_list = []

    def return_click(self):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.time_list.append(time.time())
        if self.time_list:
            if time.time() - self.time_list[-1] > self.inter_lone:
                self.time_list.clear()
        if len(self.time_list) == self.count:
            if self.inter_short <= self.time_list[-1] - self.time_list[0] <= self.inter_lone:
                self.time_list.clear()
                return True
            else:
                self.time_list.clear()
                return False


# 绘制二次函数类
class Function:
    def __init__(self, lf_k=1, lf_b=0, qf_c=0):
        self.a = lf_k
        self.b = lf_b
        self.c = qf_c

    def draw(self):
        # 网格背景
        if draw_mod:
            pygame.draw.line(win, black, (mx, 0), (mx, 800), 2)
            pygame.draw.line(win, black, (0, my), (800, my), 2)
        else:
            for i in range(27):
                pygame.draw.line(win, gray, (mx + 30 * i, 0), (mx + 30 * i, 800))
                pygame.draw.line(win, gray, (mx - 30 * i, 0), (mx - 30 * i, 800))
                pygame.draw.line(win, gray, (0, my + 30 * i), (800, my + 30 * i))
                pygame.draw.line(win, gray, (0, my - 30 * i), (800, my - 30 * i))
            pygame.draw.line(win, black, (mx, 0), (mx, 800), 2)
            pygame.draw.line(win, black, (0, my), (800, my), 2)
        # 二次函数图像
        try:
            if self.a >= 0:
                for i in range(-800, 799):
                    x1 = i + mx
                    y1 = -1 * ((x1 + (15 * self.b / self.a) - mx) ** 2) / (30 * self.a ** 0.5) - 30 * self.c + (
                            15 * self.b ** 2) / (2 * self.a ** 2.5) + my
                    x2 = x1 + 1
                    y2 = -1 * ((x2 + (15 * self.b / self.a) - mx) ** 2) / (30 * self.a ** 0.5) - 30 * self.c + (
                            15 * self.b ** 2) / (2 * self.a ** 2.5) + my
                    x3 = ((-15 * self.b) / self.a) + mx
                    y3 = -1 * ((x3 + (15 * self.b / self.a) - mx) ** 2) / (30 * self.a ** 0.5) - 30 * self.c + (
                            15 * self.b ** 2) / (2 * self.a ** 2.5) + my
                    pygame.draw.line(win, red, (x1, y1), (x2, y2))
                    pygame.draw.line(win, blue, (x3, 0), (x3, 800))
                    pygame.draw.line(win, green, (0, y3), (800, y3))
            else:
                self.a = -1 * self.a
                for i in range(-800, 799):
                    x1 = i + mx
                    y1 = ((x1 - (15 * self.b / self.a) - mx) ** 2) / (30 * self.a ** 0.5) - 30 * self.c - (
                            15 * self.b ** 2) / (2 * self.a ** 2.5) + my
                    x2 = x1 + 1
                    y2 = ((x2 - (15 * self.b / self.a) - mx) ** 2) / (30 * self.a ** 0.5) - 30 * self.c - (
                            15 * self.b ** 2) / (2 * self.a ** 2.5) + my
                    x3 = ((15 * self.b) / self.a) + mx
                    y3 = ((x3 - (15 * self.b / self.a) - mx) ** 2) / (30 * self.a ** 0.5) - 30 * self.c - (
                            15 * self.b ** 2) / (2 * self.a ** 2.5) + my
                    pygame.draw.line(win, red, (x1, y1), (x2, y2))
                    pygame.draw.line(win, blue, (x3, 0), (x3, 800))
                    pygame.draw.line(win, green, (0, y3), (800, y3))
        except ZeroDivisionError:
            pass

    # 二次函数计算方法
    def Quadratic_function(self, tip=1, qf_x=0):
        if tip == 1:
            an_y = self.a * qf_x ** 2 + self.b * qf_x + self.c
            return an_y
        elif tip == 2:
            an_y = (-1 * self.b + (self.b ** 2 - 4 * self.a * (self.c - qf_x)) ** 0.5) / (2 * self.a)
            return an_y
        elif tip == 3:
            an_y = (-1 * self.b - (self.b ** 2 - 4 * self.a * (self.c - qf_x)) ** 0.5) / (2 * self.a)
            return an_y


# 创建默认类
double_click = Click(0.13, 0.23, 2)
Function_Text1 = Text("y=ax²+bx+c", 0, 0, 23, white)
Function_Text2 = Text("x=±√[(y+b²/4a-c)/a]-b/2a", 0, 25, 23, white)
a = Text("a", 0, 605, 50, white)
b = Text("b", 0, 648, 50, white)
c = Text("c", 0, 680, 50, white)
x = Text("x", 0, 715, 50, white)
y = Text("y", 0, 745, 50, white)
x_1 = Text("x1:", 130, 728, 35, white)
x_2 = Text("x2:", 130, 763, 35, white)
a_box = InputBOX(25, 618, 100, 34, 32)
b_box = InputBOX(25, 655, 100, 34, 32)
c_box = InputBOX(25, 692, 100, 34, 32)
x_box = InputBOX(25, 728, 100, 34, 32)
y_box = InputBOX(25, 763, 100, 34, 32)
# 循环播放
while True:
    # 背景
    win.fill(white)
    # OK开始写代码了！！！
    new_x = x_box.back_num
    new_y = y_box.back_num
    new_a = a_box.back_num
    new_b = b_box.back_num
    new_c = c_box.back_num
    # print(new_x,new_y,new_k,new_b)
    Quadratic_function = Function(new_a, new_b, new_c)
    if not y_box.list:
        answer_y = Quadratic_function.Quadratic_function(1, new_x)

    elif not x_box.list and new_a != 0:
        answer_x1 = Quadratic_function.Quadratic_function(2, new_y)
        answer_x2 = Quadratic_function.Quadratic_function(3, new_y)

    if answer_x1 == 0.0:
        answer_x1 = int(answer_x1)
    if answer_x2 == 0.0:
        answer_x2 = int(answer_x2)
    if answer_y == 0.0:
        answer_y = int(answer_y)
    dr_answer_y = Text(str(answer_y), 27, 765, 30, white)
    dr_answer_x1 = Text(str(answer_x1), 180, 730, 30, white)
    dr_answer_x2 = Text(str(answer_x2), 180, 765, 30, white)
    # print(answer_x,answer_y)
    # 画面
    Function_Text1.draw()
    Function_Text2.draw()

    y.draw()
    x.draw()
    c.draw()
    b.draw()
    a.draw()

    a_box.draw()
    b_box.draw()
    c_box.draw()
    x_box.draw()
    y_box.draw()
    if a_box.list and x_box.list:
        dr_answer_y.draw()
    elif a_box.list and y_box.list:
        dr_answer_x1.draw()
        dr_answer_x2.draw()
        x_1.draw()
        x_2.draw()
    Quadratic_function.draw()
    # 数据跟踪指针
    if new_x != 0:
        pygame.draw.line(win, orange, (new_x * 30 + mx, 0), (new_x * 30 + mx, 800))
    elif new_y != 0:
        pygame.draw.line(win, orange, (0, my - new_y * 30), (800, my - new_y * 30))
    # 最高图层
    if y_box.list and b_box.list and a_box.list and new_a == 0:
        error()
    # 刷新屏幕
    pygame.display.update()
    # print(x_box.list,y_box.list)
    # 事件监听
    for event in pygame.event.get():
        a_box.get_num(event, 10)
        b_box.get_num(event, 10)
        c_box.get_num(event, 10)
        if not x_box.list:
            y_box.get_num(event, 10)
        if not y_box.list:
            x_box.get_num(event, 10)
        if double_click.return_click():
            stop = not stop
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            if not stop:
                mx, my = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass
            elif event.button == 3:
                draw_mod = not draw_mod
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 or event.button == 3:
                pass
                # stop = not stop
