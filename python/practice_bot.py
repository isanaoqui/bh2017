import battlecode
import time
import random

from pickup import *
from throw import *


#Start a game
game = battlecode.Game('testplayer')

start = time.clock()

for state in game.turns():
    # Your Code will run within this loop
    enemies = list(state.get_entities(team=state.other_team))

    for entity in state.get_entities(team=state.my_team): 
        if entity.is_thrower: 
            prep_stance(entity, 'attack', state.my_team)
            stance(entity, 'attack', state.map.tiles, state.my_team, enemies)

        for direction in battlecode.Direction.directions():
            if entity.can_move(direction):
                entity.queue_move(direction)

end = time.clock()
print('clock time: '+str(end - start))
print('per round: '+str((end - start) / 1000))