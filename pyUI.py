#单独将UI相关操作提取出来以方便语言移植
import sys
from map import Mtype
import numpy

import pygame
from pygame import Rect
class PyUI(object):
    def __init__(self, setting):
        self.ground_image=['' for i in range(0,256)]
        self.ground_image[Mtype.GRASS] = pygame.image.load('resources/grass.png')#图像注册
        self.ground_image[Mtype.MONTAIN1] = pygame.image.load('resources/mountain1.png')
        self.ground_image[Mtype.DESERT] = pygame.image.load('resources/desert.png')
        self.ground_image[Mtype.WALL1] = pygame.image.load('resources/wall1.png')
        self.ground_image[Mtype.WALL2] = pygame.image.load('resources/wall2.png')
        self.view_moving = 0 #0：静止，1-4上下左右
        self.view_moving_rate = 10
        self.draging_x = 0
        self.draging_y = 0
        self.draging = False#鼠标中键拖动地图判断标志
        self.old_tick = pygame.time.get_ticks()
        self.old_action_tick = pygame.time.get_ticks()
        self.old_tip_tick = pygame.time.get_ticks()
        self.tip_font = pygame.font.SysFont('SimHei', 20)
        self.tip_board = self.tip_font.render("FPS:" , True, (0, 0, 255))

    def pos_transform_wts(self,mapx,mapy,map):#根据视点将绝对坐标转换为屏幕坐标
        len = map.block_len
        posx = -map.view_x+mapx*len
        posy = -map.view_y+mapy*len
        return Rect((posx,posy),(len,len))

    def view_check(self,map,setting):#检查视图有无超出边界并纠正
        if map.view_x < 0:
            map.view_x = 0
        elif map.view_x + setting.window_width > map.map_width * map.block_len:
            map.view_x = max(map.map_width * map.block_len - setting.window_width, 0)
        if map.view_y < 0:
            map.view_y = 0
        elif map.view_y + setting.window_height > map.map_height * map.block_len:
            map.view_y = max(map.map_height * map.block_len - setting.window_height, 0)

    def pos_transform_stw(self,screen_x,screen_y,map):#根据屏幕坐标转换为地图坐标，不在地图范围内返回(-1,-1)
        abs_x = (screen_x + map.view_x) // map.block_len
        abs_y = (screen_y + map.view_y) // map.block_len
        if abs_x >= 0 and abs_x < map.map_width and abs_y >= 0 and abs_y < map.map_height:
            return (abs_x,abs_y)
        else:
            return (-1,-1)

    def move_view(self,map,setting):#视角移动
        if self.view_moving == 0:#静止
            return
        elif self.view_moving == 1:#上
            map.view_y -= 1 * self.view_moving_rate
        elif self.view_moving == 2:#下
            map.view_y += 1 * self.view_moving_rate
        elif self.view_moving == 3:#左
            map.view_x -= 1 * self.view_moving_rate
        elif self.view_moving == 4:#右
            map.view_x += 1 * self.view_moving_rate

    def wait_op(self,screen,world,setting):
        command_str = ''
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:#按键处理
                if event.key == pygame.K_RIGHT:#方向键设置地图滚动状态
                    self.view_moving = 4
                if event.key == pygame.K_LEFT:
                    self.view_moving = 3
                if event.key == pygame.K_UP:
                    self.view_moving = 1
                if event.key == pygame.K_DOWN:
                    self.view_moving = 2
                if event.key == pygame.K_w:#先清空现有指令，再赋值新的移动指令
                    world.me.directing = []
                    world.me.directing.append("move 1")
                elif event.key == pygame.K_s:
                    world.me.directing = []
                    world.me.directing.append("move 2")
                elif event.key == pygame.K_a:
                    world.me.directing = []
                    world.me.directing.append("move 3")
                elif event.key == pygame.K_d:
                    world.me.directing = []
                    world.me.directing.append("move 4")
            elif event.type == pygame.KEYUP:#松开方向键时取消移动状态
                if (event.key == pygame.K_UP and self.view_moving == 1) or (event.key == pygame.K_DOWN and self.view_moving == 2) or (event.key == pygame.K_LEFT and self.view_moving == 3) or (event.key == pygame.K_RIGHT and self.view_moving == 4):
                    self.view_moving = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:#左键移动
                    abs_pos = self.pos_transform_stw(mouse_pos[0],mouse_pos[1],world.map)
                    if abs_pos[0] != -1: #若在地图范围内
                        world.me.directing.append("find_way %d %d"%(abs_pos[0],abs_pos[1]))
                if event.button == 4:#上滚轮
                    world.map.scale_update(1, mouse_pos)
                    #world.map.view_x,world.map.view_y = list(map(lambda x : x*world.map.block_len - , self.pos_transform_stw(mouse_pos[0],mouse_pos[1],world.map)))
                elif event.button == 5:#下滚轮
                    world.map.scale_update(2, mouse_pos)
                elif event.button == 2:#鼠标中键按下
                    self.draging = True
                    self.draging_x, self.draging_y = mouse_pos[0], mouse_pos[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:#鼠标中键松开
                    self.draging = False
        if self.draging:#鼠标中键拖动地图判断
            mouse_pos = pygame.mouse.get_pos()
            mouse_change_x, mouse_change_y = self.draging_x - mouse_pos[0], self.draging_y - mouse_pos[1]
            world.map.view_x += mouse_change_x
            world.map.view_y += mouse_change_y
            self.draging_x, self.draging_y = mouse_pos[0], mouse_pos[1]

        self.view_check(world.map, setting)
        self.move_view(world.map,setting)
        #self.update_screen(screen,world,setting)
        return command_str

    def float2Screen(self,posx_f,posy_f,map):#浮点坐标转屏幕坐标
        screen_x = posx_f // map.block_len * map.block_len - map.view_x + posx_f % map.block_len
        screen_y = posy_f // map.block_len * map.block_len - map.view_y + posy_f % map.block_len
        return (screen_x,screen_y)

    def update_screen(self,screen,world,setting):
        tick = pygame.time.get_ticks()
        if tick - self.old_tick > setting.refresh_gap:#限制帧率
            screen.fill((0,0,0))
            bl = world.map.block_len
            x_num = setting.window_width // world.map.block_len + 2
            y_num = setting.window_height // world.map.block_len + 2
            for i in range(world.map.view_x//bl,min(world.map.view_x//bl+x_num,world.map.map_width)):
                for j in range(world.map.view_y//bl,min(world.map.view_y//bl+y_num,world.map.map_height)):
                    if i>= 0 and j>= 0:
                        screen.blit(pygame.transform.scale(self.ground_image[world.map.node[i][j].type],(bl,bl)),self.pos_transform_wts(i,j,world.map))#绘制地图
            for person in world.map.persons:
                screen.blit(pygame.transform.scale(person.img,(bl,bl)), Rect(self.float2Screen(person.posx_float,person.posy_float,world.map),(bl,bl)))#绘制人物
            if tick - self.old_tip_tick > 500:#更新帧率显示
                self.tip_board = self.tip_font.render("FPS:%.2f"%(1000/(tick - self.old_tick)), True, (0, 0, 255))
                self.old_tip_tick = tick
            screen.blit(self.tip_board, (setting.window_width-200,0,100,100))
            pygame.display.flip()
            self.old_tick = tick
        else:
            pygame.time.wait(20)#让出CPU给其它进程

