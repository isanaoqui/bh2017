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
    # Your Code will run within this loop
    self_turn += 1
    if self_turn % 20 == 0: #increase number of explorers
        increase_explorer = True

    enemies = list(state.get_entities(team=state.other_team))

    for entity in state.get_entities(team=state.my_team): 
        # This line gets all the bots on your team

        # code if this entity is an explorer
        if increase_explorer and entity.id not in explorer_id_list and entity.type == "thrower":
            increase_explorer = False
            explorer_id_list.append(entity.id)
            print("increased number of explorers to: ",len(explorer_id_list))

        if entity.id in explorer_id_list:
            movement.expansion(state,entity)
            continue

        # If thrower, tries to attack
        if entity.is_thrower: 
            carrying = prep_stance(entity, 'attack', state)
            if carrying >= 0: 
                stance(entity, 'attack', state, enemies)

            movement.away_from_glass(entity, state)


end = time.clock()
print('clock time: '+str(end - start))
print('per round: '+str((end - start) / 1000))
