from enum import IntEnum
import json


class Mtype(IntEnum):
    GRASS = 1
    DESERT = 10
    MONTAIN1 = 11
    WALL1 = 31
    WALL2 = 32
    HERO = 255


class Node(object):#地图格子节点
    def __init__(self,type = Mtype.GRASS, u_w = 1, d_w = 1, l_w = 1, r_w = 1):
        self.type = type
        self.u_w = u_w#各方向权值
        self.d_w = d_w
        self.l_w = l_w
        self.r_w = r_w


class Map(object):
    def __init__(self,setting,map_name = 'map/world_map.json'):
        self.block_len = 30#每小块地图边长
        self.block_len_max = 70#每小块最大地图边长
        self.block_len_initial = 30#每小块地图初始边长
        self.block_len_change = 10#每次缩放改变的边长
        self.view_x = 0
        self.view_y = 0
        self.init_map(setting,map_name)#读入地图数据
        self.persons = []

    def set_node(self,posx,posy,type):
        self.node[posx][posy] = type

    def pos_transform_stw(self,screen_x,screen_y):#根据屏幕坐标转换为地图坐标，不在地图范围内返回(-1,-1)
        abs_x = (screen_x + self.view_x) // self.block_len
        abs_y = (screen_y + self.view_y) // self.block_len
        if abs_x >= 0 and abs_x < self.map_width and abs_y >= 0 and abs_y < self.map_height:
            return (abs_x,abs_y)
        else:
            return (-1,-1)

    def scale_update(self,method, mouse_pos):#缩放地图后更新地图上元素的浮点坐标
        if method == 1:#放大
            if self.block_len < self.block_len_max:
                self.view_x, self.view_y = self.pos_transform_stw(mouse_pos[0], mouse_pos[1])
                self.block_len += self.block_len_change
                self.view_x = self.view_x * self.block_len - mouse_pos[0] + self.block_len // 2
                self.view_y = self.view_y * self.block_len - mouse_pos[1] + self.block_len // 2
                for person in self.persons:
                    person.posx_float = person.posx_float / (self.block_len - self.block_len_change) * self.block_len
                    person.posy_float = person.posy_float / (self.block_len - self.block_len_change) * self.block_len
        elif method ==2:#缩小
            if self.block_len > self.block_len_change:
                self.view_x, self.view_y = self.pos_transform_stw(mouse_pos[0], mouse_pos[1])
                self.block_len -= self.block_len_change
                self.view_x = self.view_x * self.block_len - mouse_pos[0] + self.block_len // 2
                self.view_y = self.view_y * self.block_len - mouse_pos[1] + self.block_len // 2
                for person in self.persons:
                    person.posx_float = person.posx_float / (self.block_len + self.block_len_change) * self.block_len
                    person.posy_float = person.posy_float / (self.block_len + self.block_len_change) * self.block_len

    def add(self,obj):
        obj.posx_float = obj.posx * self.block_len
        obj.posy_float = obj.posy * self.block_len
        self.persons.append(obj)

    def init_map(self,setting,filename):
        with open(filename, "r", encoding='utf-8') as file:
            aa = json.loads(file.read())
            file.seek(0)
            cache = json.load(file)  # 与 json.loads(f.read())
        #print(cache)
        self.map_width = cache['map_width']
        self.map_height = cache['map_height']
        self.node = [[Node(cache['default_type']) for i in range(self.map_height)] for j in range(self.map_width)]  # 初始化为草原
        for unit in cache['nodes']:
            posx = unit['posx']
            posy = unit['posy']
            self.node[posx][posy].type = unit['type']
            self.node[posx][posy].u_w = unit['up_weight']
            self.node[posx][posy].d_w = unit['down_weight']
            self.node[posx][posy].l_w = unit['left_weight']
            self.node[posx][posy].r_w = unit['right_weight']


