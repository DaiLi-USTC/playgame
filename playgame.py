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
        if world.me.motion != Motion.NOTHING:#若主角行动中
            world.me.update_action(world.map,setting)#更新主角状态
            for person in world.map.persons:
                if person == world.me:
                    continue
                else:
                    person.update_action(world.map,setting)#更新NPC角色状态
                    person.excute_AI(world.map)#若AI系统下达了新的指令
                    if person.motion == Motion.NOTHING:
                        person.excute_direct(world)
            if world.state.day_add():
                print('现在时间:%d年%d月%d日' % (world.state.get_year(), world.state.get_month(), world.state.get_day()))
        else:#若主角无动作，等待玩家下命令
            ui.wait_op(screen, world, setting)
            world.me.excute_direct(world)
        ui.update_screen(screen, world, setting)
    print('剧终')

def main():
    pygame.init()
    setting = Setting()
    screen = pygame.display.set_mode((setting.window_width, setting.window_height))
    pygame.display.set_caption("game")
    new_start(setting,screen)

main()