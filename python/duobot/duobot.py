import battlecode
import time
import random

import movement
from pickup import *
from throw import *

#Start a game
game = battlecode.Game('testplayer')

start = time.clock()

self_turn = 0
increase_explorer = False
explorer_id_list = []

for state in game.turns():
    Your Code will run within this loop
    self_turn += 1
    if self_turn % 20 == 0: #increase number of explorers
        increase_explorer = True

    enemies = list(state.get_entities(team=state.other_team))

    for entity in state.get_entities(team=state.my_team): 
        # This line gets all the bots on your team
        my_location = entity.location
        if entity.type != "thrower":
            continue

        # code if this entity is an explorer
        if increase_explorer and entity.id not in explorer_id_list:
            increase_explorer = False
            explorer_id_list.append(entity.id)
            # print("increased number of explorers to: ",len(explorer_id_list))


        #DESIGNATE ROLES
        if entity.id in explorer_id_list:
            role = "explore"
        else: role = "idle" #default

        # CARRY OUT ROLES
        if role == "explore":
            current_action = movement.expansion(state,entity)
            if current_action == "idle":
                role = "idle"
            else: continue

        # if role == "idle":# If thrower, tries to attack
        if state.map.sector_at(my_location).team.name != state.my_team.name:
            # print("hello?")
            for direction in battlecode.Direction.directions():
                if entity.can_build(direction):
                    entity.queue_build(direction)
                    break

        carrying = prep_stance(entity, 'attack', state)
        if carrying >= 0: 
            attacked = stance(entity, 'attack', state, enemies)
            if attacked == 0:
                stance(entity, 'hedge', state)

        movement.away_from_glass(entity, state)

        if role == "defend":
            pass        



end = time.clock()
print('clock time: '+str(end - start))
print('per round: '+str((end - start) / 1000))
