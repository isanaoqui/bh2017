import battlecode

def stance(unit, setting, state, enemies=None, defendLoc=None):
    """
    This function evaluates what setting is on (expand, attack, defend). 
    Expand: 
        try to pick up a friend and throw them as far away as possible
    Attack: 
        try to pick up an enemy and throw them down onto enemies
        try to pick up a friend and throw them onto enemy (make sure land on grass)
    Defend: 
        try to pick up an enemy and throw them as far away as possible 

    Returns:
        0 if still holding someone 
        -1 if didn't do anything / not holding someone
        1 if threw someone 
    """
    tiles = state.map.tiles
    my_team = state.my_team

    if unit.is_holding: 
        if setting == 'expand': 
            return expand(unit, my_team)
        elif setting == 'attack':
            return attack(unit, tiles, my_team, enemies)
        elif setting == 'defend' and defendLoc != None:
            return defend(unit, defendLoc, my_team, enemies)
        elif setting == 'hedge': 
            return hedge(unit, state)
    return -1

def expand(unit, my_team):
    raise NotImplementedError

def attack(unit, tiles, my_team, enemies):
    """
    Priority:
        pick up enemy and throw them onto enemy (for 10 turns)
            glass statues
            throwers
            hedges
        pick up enemy and throw them away (from statue?)
            hedges
            dirt 
            grass
        pick up ally and throw them onto enemy, land on grass
        pick up ally and throw them onto enemy, land on dirt

    Returns:
        True if threw someone
        False if still holding someone
    """
    # if unit.holding.team != my_team: 
    #     return attack_with_enemy(unit, tiles, enemies)
    # else:
    #     return attack_with_ally(unit, enemies)
    return attack_with_enemy(unit, tiles, enemies)

def attack_with_enemy(unit, tiles, enemies):
    """
    1. Scan for enemies 
    2. Scan for dirt spaces

    Returns:
        True if threw someone
        False if still holding someone
    """
    ## Enemies
    if len(enemies) > 0:
        glass_statues = filter(lambda x: x.is_statue == True, enemies)
        glass_statues = sorted(filter(lambda x: unit.location.distance_to(x.location) < 8, glass_statues))

        if len(glass_statues) > 0:
            for glass_statue in glass_statues: 
                direction = unit.location.direction_to(glass_statue.location)
                if unit.can_throw(direction):
                    unit.queue_throw(direction)
                    return 1

        enemies.sort(key=lambda x: unit.location.distance_to(x.location))
        for enemy in enemies: 
            if enemy.location != unit.location:
                direction = unit.location.direction_to(enemy.location)
                # if Throw.coast_clear(unit, enemy.location, direction) and unit.can_throw(direction): 
                if unit.can_throw(direction):
                    unit.queue_throw(direction)
                    # print('enemy throw')
                    return 1

    ## Dirt spaces
    # dirt_tiles = get_dirt_tiles(unit.location, tiles) # List of dirt tile locations
    # if len(dirt_tiles) > 0:
    #     for tile in dirt_tiles: 
    #         if unit.location != tile: 
    #             direction = unit.location.direction_to(tile)
    #             # if Throw.coast_clear(unit, tile, direction) and unit.can_throw(direction): 
    #             if unit.can_throw(direction):
    #                 unit.queue_throw(direction)
    #                 # print('DIRTTT')
    #                 return 1

    return 0

# def attack_with_ally(unit, enemies):
#     """
#     1. Scan for enemies

#     Returns:
#         True if threw someone
#         False if still holding someone
#     """
#     if len(enemies) > 0:
#         glass_statues = filter(lambda x: x.is_statue == True, enemies)
#         glass_statues = sorted(filter(lambda x: unit.location.distance_to(x.location) < 8, glass_statues))

#         if len(glass_statues) > 0:
#             for glass_statue in glass_statues: 
#                 direction = unit.location.direction_to(glass_statue.location)
#                 if unit.can_throw(direction):
#                     unit.queue_throw(direction)
#                     return 1

#         enemies.sort(key=lambda x: x.location)
#         for enemy in enemies: 
#             if enemy.location != unit.location:
#                 direction = unit.location.direction_to(enemy.location)
#                 # if Throw.coast_clear(unit, enemy.location, direction) and unit.can_throw(direction): 
#                 if unit.can_throw(direction):
#                     unit.queue_throw(direction)
#                     # print('friend throw')
#                     return 1
#     return 0

def defend(unit, defendLoc, my_team, enemies):
    """
    1. Scan for far away dirt patches
    2. Scan for nearer dirt patches
    3. Throw at enemies
    """
    ## Dirt spaces
    dirt_tiles = get_dirt_tiles(unit.location, tiles) # List of dirt tile locations
    if len(dirt_tiles) > 0:
        for tile in dirt_tiles: 
            if unit.location != tile: 
                direction = unit.location.direction_to(tile)
                # if Throw.coast_clear(unit, tile, direction) and unit.can_throw(direction): 
                if unit.can_throw(direction):
                    unit.queue_throw(direction)
                    # print('DIRTTT')
                    return 1

    ## Enemies
    if len(enemies) > 0:
        enemies.sort(key=lambda x: unit.location.distance_to(x.location))
        for enemy in enemies: 
            if enemy != unit.holding:
                direction = unit.location.direction_to(enemy.location)
                # if Throw.coast_clear(unit, enemy.location, direction) and unit.can_throw(direction): 
                if unit.can_throw(direction):
                    unit.queue_throw(direction)
                    # print('enemy throw')
                    return 1
    return 0

def hedge(unit, state):
    """
    Tries to get rid of hedges. IMPROVE!
    
    Returns: 
    1 Threw someone
    0 Didn't throw someone
    """
    for entity in unit.entities_within_adjacent_distance(1):
        if entity.team.id == 0: 
            direction = unit.location.direction_to(entity.location)
            if unit.can_throw(direction): 
                unit.queue_throw(direction)
                # print('HEDGEE')
                return 1
    return 0

# def coast_clear(unit, targetLoc, direction):
#     """
#     This function checks if the unit I want to hit is the first one
#     in the given direction. 
#     """
#     raise NotImplementedError

def get_dirt_tiles(startLoc, tiles):
    """
    Returns a list of sorted Location objects in terms of startLoc.
    Far away first, closer last (so reverse order).
    """
    dirt_tiles = []
    for j in range(len(tiles)):
        row = tiles[j]
        for i in range(len(tiles[0])):
            elem = row[i]
            if elem == 'D':
                dirt_tiles.append(battlecode.Location(i,j))

    dirt_tiles = sorted(dirt_tiles, key=lambda x: startLoc.distance_to(x), reverse=True)
    return dirt_tiles

# @staticmethod
# def throw(thrower, targetLoc):
#     """
#     This function performs the art of throwing an ally to a target
#     location targetLoc. 
#     """
#     thrower_loc = thrower.location
#     throw_dir = thrower_loc.direction_to(targetLoc)

#     ## Has unit on its back, no cooldowns to throw
#     if thrower.can_throw(throw_dir):
#         queue_throw(throw_dir)
#         return True
#     else: 
#         return False