import enum
from AI import AI_type
import pygame

class Motion(enum.Enum):
    NOTHING = 0
    MOVING = 30
    DIREC_UP = 1
    DIREC_DOWN = 2
    DIREC_LEFT = 3
    DIREC_RIGHT = 4

class Role(object):
    def __init__(self,posx,posy,name):
        self.posx = posx  #地图格子坐标
        self.posy = posy
        self.posx_float = 0  #地图绝对浮点坐标
        self.posy_float = 0
        self.name = name
        self.motion = Motion.NOTHING
        self.motion_param = Motion.NOTHING
        self.directing_num = 0  #角色指令序列数目
        self.directing = []
        self.img = None

    def set_img(self,filename):
        self.img = pygame.image.load(filename)

    def set_attr(self,rank,money):#设置等级和金钱
        self.rank = rank
        self.money = money

    def update_action(self,map,setting):#每帧更新动作状态
        if self.motion == Motion.MOVING:
            if self.motion_param == Motion.DIREC_UP:
                self.posy_float -= map.block_len / setting.action_frame_num * setting.action_rate
                if self.posy_float <= self.posy * map.block_len:
                    self.posy_float = self.posy * map.block_len
                    self.motion = Motion.NOTHING
            elif self.motion_param == Motion.DIREC_DOWN:
                self.posy_float += map.block_len / setting.action_frame_num * setting.action_rate
                if self.posy_float >= self.posy * map.block_len:
                    self.posy_float = self.posy * map.block_len
                    self.motion = Motion.NOTHING
            elif self.motion_param == Motion.DIREC_LEFT:
                self.posx_float -= map.block_len / setting.action_frame_num * setting.action_rate
                if self.posx_float <= self.posx * map.block_len:
                    self.posx_float = self.posx * map.block_len
                    self.motion = Motion.NOTHING
            elif self.motion_param == Motion.DIREC_RIGHT:
                self.posx_float += map.block_len / setting.action_frame_num * setting.action_rate
                if self.posx_float >= self.posx * map.block_len:
                    self.posx_float = self.posx * map.block_len
                    self.motion = Motion.NOTHING

    def excute_direct(self,world):
        rs = False
        if self.directing:
            command_str = self.directing.pop()
            command = command_str.split()
            #print(self,':%s'%command)
            if command[0]=='move_to':
                tar_x = int(command[1])
                tar_y = int(command[2])
                rs = self.move_to(tar_x,tar_y,world.map)
            elif command[0] == 'find_way':
                tar = (int(command[1]),int(command[2]))
                rs = self.find_way((self.posx,self.posy),tar,world.map)
            elif command[0] == 'move':
                direction = int(command[1])
                rs = self.move(direction,world)
        return rs

    def find_way_rec(self,now,src,map,cost,path):#从已知距离点回溯到原出发点，走最快下降梯度方向
        if src == now:
            return
        min_dis = 100000
        if now[1] - 1 >= 0 and map.node[now[0]][now[1]].u_w != -1 and map.node[now[0]][now[1]-1].d_w != -1 and cost[now[0]][now[1] - 1] < min_dis:#若向上的格子存在且走得通
            direction = 1
            min_dis = cost[now[0]][now[1] - 1]
        if now[1] + 1 < map.map_height and map.node[now[0]][now[1]].d_w != -1 and map.node[now[0]][now[1]+1].u_w != -1 and cost[now[0]][now[1] + 1] < min_dis:
            direction = 2
            min_dis = cost[now[0]][now[1] + 1]
        if now[0] - 1 >= 0 and map.node[now[0]][now[1]].l_w != -1 and map.node[now[0]-1][now[1]].r_w != -1 and cost[now[0] - 1][now[1]] < min_dis:
            direction = 3
            min_dis = cost[now[0] - 1][now[1]]
        if now[0] + 1 < map.map_width and map.node[now[0]][now[1]].r_w != -1 and map.node[now[0]+1][now[1]].l_w != -1 and cost[now[0] + 1][now[1]] < min_dis:
            direction = 4
        if direction == 1:
            path.append('move 2')
            self.find_way_rec((now[0],now[1] - 1),src,map,cost,path)
        elif direction == 2:
            path.append('move 1')
            self.find_way_rec((now[0], now[1] + 1), src,map, cost, path)
        elif direction == 3:
            path.append('move 4')
            self.find_way_rec((now[0] - 1, now[1]), src,map, cost, path)
        else:
            path.append('move 3')
            self.find_way_rec((now[0] + 1, now[1]), src,map, cost, path)

    def find_way(self,src,tar,map):
        path = []
        known = [src]
        cost = [[-1 for i in range(map.map_height)] for j in range(map.map_width)]#各点最短距离
        cost[src[0]][src[1]] = 0
        flag = True #
        while flag:
            flag = False
            for pos in known:
                #if cost[pos[0]][pos[1]]>100:#性能优化：过远的距离不能自动寻路
                    #continue
                if pos[1] - 1 >= 0 and map.node[pos[0]][pos[1]].u_w >= 0 and map.node[pos[0]][pos[1] - 1].d_w >= 0:#上方向存在，本方格可向上走且上方格可向下走
                    if cost[pos[0]][pos[1] - 1] == -1:#若未被探索过，加入已探索过的结点集合
                        known.append((pos[0],pos[1] - 1))
                    tmp_dis = map.node[pos[0]][pos[1]].u_w + map.node[pos[0]][pos[1] - 1].d_w
                    if cost[pos[0]][pos[1] - 1] == -1 or (cost[pos[0]][pos[1] - 1] >= 0 and cost[pos[0]][pos[1] - 1] > cost[pos[0]][pos[1]] + tmp_dis):#若上方向未被探索过或者已知路径长于新路径
                        cost[pos[0]][pos[1] - 1] = cost[pos[0]][pos[1]] + tmp_dis
                        flag = True
                if pos[1] + 1 < map.map_height and map.node[pos[0]][pos[1]].d_w >=0 and map.node[pos[0]][pos[1] + 1].u_w >= 0:
                    if cost[pos[0]][pos[1] + 1] == -1:
                        known.append((pos[0],pos[1] + 1))
                    tmp_dis = map.node[pos[0]][pos[1]].d_w + map.node[pos[0]][pos[1] + 1].u_w
                    if cost[pos[0]][pos[1] + 1] == -1 or (cost[pos[0]][pos[1] + 1] >= 0 and cost[pos[0]][pos[1] + 1] > cost[pos[0]][pos[1]] + tmp_dis):
                        cost[pos[0]][pos[1] + 1] = cost[pos[0]][pos[1]] + tmp_dis
                        flag = True
                if pos[0] - 1 >= 0 and map.node[pos[0]][pos[1]].l_w >= 0 and map.node[pos[0] - 1][pos[1]].r_w >= 0:#左方向存在，本方格可向左走且左方格可向右走
                    if cost[pos[0] - 1][pos[1]] == -1:
                        known.append((pos[0] - 1,pos[1]))
                    tmp_dis = map.node[pos[0]][pos[1]].l_w + map.node[pos[0] - 1][pos[1]].r_w
                    if cost[pos[0] - 1][pos[1]] == -1 or (cost[pos[0] - 1][pos[1]] >= 0 and cost[pos[0] - 1][pos[1]] > cost[pos[0]][pos[1]] + tmp_dis):
                        cost[pos[0] - 1][pos[1]] = cost[pos[0]][pos[1]] + tmp_dis
                        flag = True
                if pos[0] + 1 < map.map_width and map.node[pos[0]][pos[1]].r_w >=0 and map.node[pos[0] + 1][pos[1]].l_w >= 0:
                    if cost[pos[0] + 1][pos[1]] == -1:
                        known.append((pos[0] + 1,pos[1]))
                    tmp_dis = map.node[pos[0]][pos[1]].r_w + map.node[pos[0] + 1][pos[1]].l_w
                    if cost[pos[0] + 1][pos[1]] == -1 or (cost[pos[0] + 1][pos[1]] >= 0 and cost[pos[0] + 1][pos[1]] > cost[pos[0]][pos[1]] + tmp_dis):
                        cost[pos[0] + 1][pos[1]] = cost[pos[0]][pos[1]] + tmp_dis
                        flag = True
        # print('目标地点：%d,%d的最短距离为：%f'%(tar[0],tar[1],cost[tar[0]][tar[1]]))
        if cost[tar[0]][tar[1]] >= 0:
            self.find_way_rec(tar, src, map, cost, path)
            self.directing = path
            # print(self.directing)
            return True
        else:
            return False

    def move(self,direction,world):#上下左右移动
        if self.motion != Motion.NOTHING:
            return False
        self.motion = Motion.MOVING
        if direction == 1 and self.posy-1>=0 and world.map.node[self.posx][self.posy].u_w > 0 and world.map.node[self.posx][self.posy-1].d_w > 0:#上
            self.posy -= 1
            self.motion_param = Motion.DIREC_UP
        elif direction == 2 and self.posy+1<world.map.map_height and world.map.node[self.posx][self.posy].d_w > 0 and world.map.node[self.posx][self.posy+1].u_w > 0:#下
            self.posy += 1
            self.motion_param = Motion.DIREC_DOWN
        elif direction == 3 and self.posx-1>=0 and world.map.node[self.posx][self.posy].l_w > 0 and world.map.node[self.posx-1][self.posy].r_w > 0:#左
            self.posx -= 1
            self.motion_param = Motion.DIREC_LEFT
        elif direction == 4 and self.posx+1<world.map.map_width and world.map.node[self.posx][self.posy].r_w > 0 and world.map.node[self.posx+1][self.posy].l_w > 0:#右
            self.posx += 1
            self.motion_param = Motion.DIREC_RIGHT
        else:
            return False
        world.should_add_time = 1
        return True

    def move_to(self,posx,posy,map):#瞬移，一般作弊模式或调试模式用，某些技能下也可用
        if posx>=0 and posx< map.map_width and posy>=0 and posy < map.map_height:
            self.posx = posx
            self.posy = posy
            self.posx_float = posx * map.block_len
            self.posy_float = posy * map.block_len
            #print('移动到%d,%d'%(posx,posy))
            return True
        else:
            #print("移动超出范围！")
            return False

    def check(self):
        print('我叫%s，我在位置(%d,%d)，我%d级了,我有%d金币' % (self.name, self.posx, self.posy, self.rank, self.money))

class NPC(Role):
    def __init__(self,posx,posy,name):
        Role.__init__(self,posx,posy,name)
        self.target = None
        self.AI = AI_type.NOTHING
        self.AI_param1 = None
        self.AI_param2 = None
        self.AI_state = None

    def set_AI(self,AI,param1 = None,param2 = None):
        self.AI = AI
        self.AI_param1 = param1
        self.AI_param2 = param2

    def set_target(self,target):
        self.target = target

    def excute_AI(self,map):
        if self.AI == AI_type.PATROL:#巡逻参数
            if self.posx == self.AI_param1[0] and self.posy == self.AI_param1[1]:#若到达巡逻A点，走向巡逻B点
                self.find_way((self.posx,self.posy),(self.AI_param2[0],self.AI_param2[1]),map)
            elif self.posx == self.AI_param2[0] and self.posy == self.AI_param2[1]:#若到达巡逻B点，走向巡逻A点
                self.find_way((self.posx,self.posy),(self.AI_param1[0],self.AI_param1[1]),map)
            elif not self.directing:
                self.find_way((self.posx, self.posy), (self.AI_param1[0], self.AI_param1[1]), map)
