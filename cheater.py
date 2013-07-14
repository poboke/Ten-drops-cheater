# -*- coding : utf-8 -*-

from autopy import bitmap, color, mouse
from game import Game
from pprint import pprint
import time

class Cheater():
    #初始化
    def __init__(self):
        #获取游戏边框的位置
        self.get_border_position()
        #获取装水滴的格子的位置偏移值
        self.offset_x = self.border_x + 35
        self.offset_y = self.border_y + 20
        #装水滴的格子的边框长度
        self.grid_length = 60

    #通过游戏边框的颜色获取游戏边框的位置
    def get_border_position(self):
        #截取整个屏幕
        self.screen = bitmap.capture_screen()
        #注意：浏览器移到屏幕左上角，游戏垂直居中
        self.border_x = 0
        self.border_y = 0
        self.border_color = 0xCFDFEB
        for x in range(self.screen.width):
            color_value = self.screen.get_color(x, self.screen.height/2)
            if color_value == self.border_color:
                self.border_x = x
                break
        for y in range(self.screen.height):
            if self.screen.get_color(500, y) == self.border_color:
                self.border_y = y
                break

    #开始运行
    def run(self):
        while 1:
            self.play_game()
            if self.game_over():
                print "game over!"
                return

    #自动玩游戏
    def play_game(self):
        print "\nplay new game!"
        self.game = Game(self.get_water_list())
        pprint(self.waterlist)
        while not self.game.IsOver():
            point = self.game.GetBestPoint()
            self.game.Drop(point)
            self.click(point)
            print "click : (%d, %d)"%(point[0]+1, point[1]+1)
            #如果wait返回True或游戏结束，就返回
            if self.wait() or self.game_over():
                return

    #获取水滴数数组
    def get_water_list(self):
        self.screen = bitmap.capture_screen()
        self.waterlist = [[] for i in range(6)]
        for j in range(6):
            for i in range(6):
                drops = self.get_drops(i, j)
                self.waterlist[j].append(drops)
        return self.waterlist

    #获取某个格子上的水滴数
    def get_drops(self, i, j):
        #pos_list数组存放4、3、2、1滴水的位置相对坐标
        pos_list = [(35, 55), (30, 5), (48, 25), (30, 25)]
        #计算第j行第i列的格子原点(格子左上角的屏幕坐标)
        grid_x = self.offset_x + self.grid_length * i
        grid_y = self.offset_y + self.grid_length * j
        for index, (x, y) in enumerate(pos_list):
            #获取格子原点加上相对坐标后的点的颜色值
            color_value = self.screen.get_color(grid_x + x, grid_y + y)
            r, g, b = color.hex_to_rgb(color_value)
            #如果该点是水滴的颜色就返回水滴数
            if r < 0x70 and g > 0xA0:
                return 4 - index
        return 0

    #鼠标点击某个格子
    def click(self, point):
        grid_x = self.offset_x + self.grid_length * (point[1] + 0.5)
        grid_y = self.offset_y + self.grid_length * (point[0] + 0.5)
        mouse.move(int(grid_x), int(grid_y))
        mouse.click()

    #等待水滴动画停止
    def wait(self):
        times = 0
        while 1:
            times += 1
            time.sleep(3)
            #如果重新获取的水滴数组和游戏里算出来的数组一样，
            #说明动画已经停止了(可能有时间上的误差)。
            if self.get_water_list() == self.game.waterlist:
                return False
            #如果过关了，多等待几次以跳过过场画面。
            elif times > 3 and self.game.IsOver():
                return False
            #防止死循环，返回True，开始新游戏
            elif times > 5:
                return True
            #如果游戏结束，返回True，开始新游戏
            elif self.game_over():
                return True
            print "wait..."

    #如果找不到游戏边框，则游戏结束
    def game_over(self):
        if self.screen.get_color(500, self.border_y) != self.border_color:
            return True
        else:
            return False


if __name__ == "__main__":
    Cheater().run()


