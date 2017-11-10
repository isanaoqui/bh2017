import battlecode

def stance(unit, setting, tiles, my_team, enemies, defendLoc=None):
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
    if unit.is_holding: 
        if setting == 'expand': 
            return expand(unit, my_team)
        elif setting == 'attack':
            return attack(unit, tiles, my_team, enemies)
        elif setting == 'defend' and defendLoc != None:
            return defend(unit, defendLoc, my_team, enemies)
    return -1

def expand(unit, my_team):
    raise NotImplementedError

def attack(unit, tiles, my_team, enemies):
    """
    Priority:
        pick up enemy and throw them onto enemy (for 10 turns)
        pick up enemy and throw them away (from statue?)
        pick up ally and throw them onto enemy, land on grass
        pick up ally and throw them onto enemy, land on dirt

    Returns:
        True if threw someone
        False if still holding someone
    """
    if unit.holding.team != my_team: 
        return attack_with_enemy(unit, tiles, enemies)
    else:
        return attack_with_ally(unit, enemies)

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
        enemies.sort(key=lambda x: unit.location.distance_to(x.location))
        for enemy in enemies: 
            if enemy != unit.holding:
                direction = unit.location.direction_to(enemy.location)
                # if Throw.coast_clear(unit, enemy.location, direction) and unit.can_throw(direction): 
                if unit.can_throw(direction):
                    unit.queue_throw(direction)
                    return 1

    # ## Dirt spaces
    # else: 
    #     dirt_tiles = Throw.get_dirt_tiles(unit.location, tiles) # List of dirt tile locations
    #     if len(dirt_tiles) > 0:
    #         for tile in dirt_tiles: 
    #             direction = unit.location.direction_to(tile)
    #             # if Throw.coast_clear(unit, tile, direction) and unit.can_throw(direction): 
    #             if unit.can_throw(direction):
    #                 unit.queue_throw(direction)
    #                 return True

    return 0

def attack_with_ally(unit, enemies):
    """
    1. Scan for enemies

    Returns:
        True if threw someone
        False if still holding someone
    """
    if len(enemies) > 0:
        enemies.sort(key=lambda x: x.location)
        for enemy in enemies: 
            direction = unit.location.direction_to(enemy.location)
            # if Throw.coast_clear(unit, enemy.location, direction) and unit.can_throw(direction): 
            if unit.can_throw(direction):
                unit.queue_throw(direction)
                return 1
    return 0

def coast_clear(unit, targetLoc, direction):
    """
    This function checks if the unit I want to hit is the first one
    in the given direction. 
    """
    raise NotImplementedError

def get_dirt_tiles(startLoc, tiles):
    """
    Returns a list of sorted Location objects in terms of startLoc.
    Far away first, closer last (so reverse order).
    """
    raise NotImplementedError

def defend(unit, defendLoc, my_team, enemy_team):
    """
    1. Scan for far away dirt patches
    2. Scan for nearer dirt patches
    3. Throw at enemies
    """
    raise NotImplementedError

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