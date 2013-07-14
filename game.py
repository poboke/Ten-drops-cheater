# -*- coding : utf-8 -*-

import copy
import time
from pprint import pprint



class Game():
    def __init__(self, _waterlist):
        self.waterlist = copy.deepcopy(_waterlist)
        self.length = len(self.waterlist)
        self.burstlist = []
        self.direction = [[-1,0], [0,1], [0,-1], [1,0]]

    def Drop(self, t_point):
        self.CheckBurst(t_point)
        while(self.IsBursting()):
            for i,t_list in enumerate(self.burstlist[:]):
                for j,t_point in enumerate(t_list[:]):
                    if not self.IsOutOfRange(t_point):
                        t_point = [t_list[j][k] + self.direction[j][k] for k in range(2)]
                        self.burstlist[i][j] = t_point
                        if not self.IsOutOfRange(t_point):
                            if self.CheckBurst(t_point):
                                self.burstlist[i][j] = [-1,-1]

    def CheckBurst(self, t_point):
        t_drop = self.waterlist[t_point[0]][t_point[1]]
        if t_drop:
            if t_drop >= 4:
                self.waterlist[t_point[0]][t_point[1]] = 0
                self.burstlist.append([t_point]*4)
            else:
                self.waterlist[t_point[0]][t_point[1]] +=  1
            return True
        else:
            return False

    def IsBursting(self):
        for t_list in self.burstlist[:]:
            for t_point in t_list:
                if not self.IsOutOfRange(t_point):
                    return True
            self.burstlist.remove(t_list)
        return False

    def IsOutOfRange(self, t_point):
        for x in t_point:
            if x < 0 or x >= self.length:
                return True
        return False

    def GetDrops(self):
        return sum([sum(x) for x in self.waterlist])

    def IsOver(self):
        return self.GetDrops() == 0

    def GetAllPoints(self):
        return [[i, j] for i in range(self.length) 
                for j in range(self.length) if self.waterlist[i][j]]

    def GetPointsNumber(self):
        return len(self.GetAllPoints())

    def GetSinglePointsNumber(self):
        t_number = 0
        t_points = self.GetAllPoints()
        for t_point in t_points:
            t_countX = len([x for x in self.waterlist[t_point[0]] if x])
            if t_countX == 1:
                t_countY = len([x for x in self.waterlist if x[t_point[1]]])
                if t_countY == 1:
                    t_number += 1
        return t_number

    def GetScore(self):
        t_number = self.GetPointsNumber()
        t_drops = self.GetDrops()
        t_singlenumber = self.GetSinglePointsNumber()
        return -5 * t_number + t_drops - t_singlenumber

    def GetBestResult(self):
        t_sortlist = []
        t_points = self.GetAllPoints()
        if not t_points:
            return self.waterlist
        for t_point in t_points:
            t_newgame = Game(copy.deepcopy(self.waterlist))
            t_newgame.Drop(t_point)
            t_sortlist.append([t_point, t_newgame.waterlist])
        t_sortlist.sort(key = lambda x:(Game(x[1]).GetScore(), 
                        self.waterlist[x[0][0]][x[0][1]]), reverse = True)
        return t_sortlist[0][1]

    def GetBestPoint(self):
        t_sortlist = []
        t_points = self.GetAllPoints()
        for t_point in t_points:
            t_newgame = Game(copy.deepcopy(self.waterlist))
            t_newgame.Drop(t_point)
            t_sortlist.append([t_point, t_newgame.waterlist])
        for i in range(11):
            if not len([x for x in t_sortlist if Game(x[1]).IsOver()]):
                for i,x in enumerate(t_sortlist):
                    t_newgame = Game(copy.deepcopy(x[1]))
                    t_sortlist[i][1] = t_newgame.GetBestResult()
        t_sortlist.sort(key = lambda x:(Game(x[1]).GetScore(), 
                        self.waterlist[x[0][0]][x[0][1]]), reverse = True)
        return t_sortlist[0][0]



if __name__ == "__main__":

    t_list = [
        #"210322",
        #"210220",
        #"021110",
        #"202002",
        #"212301",
        #"014031",
        "240322",
        "240220",
        "021410",
        "202002",
        "242304",
        "044034",
    ]
    t_list = [[int(y) for y in x] for x in t_list]
    #pprint(t_list)

    t_index = 0
    t_game = Game(t_list)
    t_time1 = time.time()
    while(not t_game.IsOver()):
        t_index += 1
        t_point = t_game.GetBestPoint()
        print "%2d : (%d, %d)"%(t_index, t_point[0]+1, t_point[1]+1)
        t_game.Drop(t_point)
        #pprint(t_game.waterlist)
    t_time2 = time.time()
    print "time :", t_time2 - t_time1


