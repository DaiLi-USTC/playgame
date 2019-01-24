import pygame
from enum import IntEnum


class Ptype(IntEnum):
    Town = 1

class Position():
    def __init__(self,posx,posy,id,scale,type,name):
        self.id = id
        self.posx = posx  #地图格子坐标
        self.posy = posy
        self.name = name
        self.scale = scale
        self.type = type
        #self.posx_float = 0  #地图绝对浮点坐标
        #self.posy_float = 0
        self.roles = []
        self.img = None

    def update_img(self):
        if self.type == 1:#城镇类型
            if self.scale == 1:
                self.img = pygame.image.load('resources/position/village.png')
            elif self.scale == 2:
                self.img = pygame.image.load('resources/position/town.png')
            else:
                self.img = pygame.image.load('resources/position/none.png')
        else:#默认类型
            self.img = pygame.image.load('resources/position/none.png')

class City(Position):
    def __init__(self,posx,posy,id,scale,type,name):
        Position.__init__(self,posx,posy,id,scale,type,name)
        self.scale = 1
        self.population = 1000  #人口
        self.army = [] #军队
        self.bussiness = 0  #商业繁荣度
        self.agriculture = 0  #农业繁荣度
        self.industry = 200  #工业繁荣度
        self.culture = 0  #文化繁荣度
        self.money = 0  #仓库公有金币
        self.food = 0  #仓库公有粮草
        self.owner = None  #拥有者