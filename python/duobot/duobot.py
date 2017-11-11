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
    #Your Code will run within this loop
    '''
    self_turn += 1
    if self_turn % 20 == 0: #increase number of explorers
        increase_explorer = True
    '''
    enemies = list(state.get_entities(team=state.other_team))

    frac_my_sectors = movement.get_fraction_sectors(state, state.my_team)
    frac_enemy_sectors = movement.get_fraction_sectors(state, state.other_team)

    print('my sectors: ', frac_my_sectors)
    print('enemy sectors: ', frac_enemy_sectors)
    mode = 'regular'
    
    ## Defensive mode
    if frac_enemy_sectors > 0.7: 
        mode = 'defense'
    ## Run it down mid mode
    elif frac_my_sectors > 0.7: 
        mode = 'offense'

    for entity in state.get_entities(team=state.my_team): 
        # This line gets all the bots on your team
        my_location = entity.location
        if entity.type != "thrower":
            continue

        #DESIGNATE ROLES

        nearby_entities = entity.entities_within_euclidean_distance(6)
        nearby_enemies = list(filter(lambda x: x.team == state.other_team, nearby_entities))
        build_state = True

        for ent in entity.entities_within_euclidean_distance(4):
            if state.map.sector_at(my_location).team == state.my_team or ent.type == "statue":
                build_state = False
                break

        if len(nearby_enemies) > 0:
            role = "attack"
        elif build_state: 
            role = "explore"
        elif mode == "defense":
            role = "defend"
        else: role = "idle" #default

        # CARRY OUT ROLES

        if role == "defend":
            carrying = prep_stance(entity, 'defend', state)
            if carrying >= 0: 
                defended = stance(entity, 'defend', state, enemies)  

            role = "idle"

        if role == "explore":# If thrower, tries to attack
            for direction in battlecode.Direction.directions():
                if entity.can_build(direction):
                    entity.queue_build(direction)
                    break
            role = "idle"

        if role == "attack":
            carrying = prep_stance(entity, 'attack', state)
            if carrying >= 0: 
                attacked = stance(entity, 'attack', state, enemies)
                if attacked == 0:
                    stance(entity, 'hedge', state)
            role = "idle"

        if role == "idle":
            movement.space_out(state, entity, 3)

        

end = time.clock()
print('clock time: '+str(end - start))
print('per round: '+str((end - start) / 1000))
