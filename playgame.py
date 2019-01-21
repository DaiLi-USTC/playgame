#Todo:增加简单界面，交互操作
from time import sleep

import pygame
import sys
from common import Setting,State
from world import World
from role import Motion
from map import Map
from pyUI import PyUI

def new_start(setting,screen):
    ui = PyUI(setting)
    world = World(setting)
    while True:
        world.should_add_time = 0
        ui.wait_op(screen,world,setting)
        if world.me.motion != Motion.NOTHING:
            continue
        rs = False
        if world.me.directing: #若主角指令非空，主角尝试行动
            rs = world.me.excute_direct(world)
        else:
            continue
        if rs == True and world.should_add_time:#若主角指令执行成功，轮到AI行动
            for person in world.map.persons:
                if person == world.me:
                    continue
                else:
                    person.excute_AI(world.map)
                    person.excute_direct(world)
            #print('现在时间:%d年%d月%d日'%(world.state.get_year(),world.state.get_month(),world.state.get_day()))
            world.state.day_add()
    print('剧终')

def main():
    pygame.init()
    setting = Setting()
    screen = pygame.display.set_mode((setting.window_width, setting.window_height))
    pygame.display.set_caption("game")
    new_start(setting,screen)

main()