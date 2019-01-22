from common import Setting,State
from map import Map
from role import Role,NPC
from AI import AI_type

class World(object):
    def __init__(self,setting):#世界的生成，主角初始化
        self.map = Map(setting)
        self.state = State(setting)
        self.me =  Role(1,1,'猪脚')
        self.me.set_attr(1,1000)
        self.me.speed = 1.2
        self.me.set_img('resources/person/hero.png')
        self.me.check()
        self.map.add(self.me)
        self.should_add_time = 0
        self.npc1 = NPC(15,14,'士兵1')
        self.npc1.set_attr(1,500)
        self.npc1.set_img('resources/person/soldier.png')
        self.npc1.set_AI(AI_type.PATROL,(8,9),(8,19))
        self.map.add(self.npc1)
        self.npc2 = NPC(15, 14, '士兵2')
        self.npc2.set_attr(1, 500)
        self.npc2.set_img('resources/person/soldier.png')
        self.npc2.set_AI(AI_type.PATROL, (9, 8), (19, 8))
        self.map.add(self.npc2)
        self.npc3 = NPC(15, 14, '士兵3')
        self.npc3.set_attr(1, 500)
        self.npc3.set_img('resources/person/soldier.png')
        self.npc3.set_AI(AI_type.PATROL, (9, 20), (19, 20))
        self.map.add(self.npc3)
        self.npc4 = NPC(15, 14, '士兵4')
        self.npc4.set_attr(1, 500)
        self.npc4.set_img('resources/person/soldier.png')
        self.npc4.set_AI(AI_type.PATROL, (21, 9), (21, 19))
        self.map.add(self.npc4)

