import battlecode


def prep_stance(unit, setting, my_team):
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
        0 if holding someone => Can now throw
        1 if picked up someone => Can now throw
        -1 if done nothing => Can now move / build / etc. 
    """
    if not unit.is_holding: 
        if setting == 'expand': 
            return prep_expand(unit)
        elif setting == 'attack':
            return prep_attack(unit, my_team)
        elif setting == 'defend':
            return prep_defend(unit, my_team)
    return 0

def prep_expand(unit):
    raise NotImplementedError

def prep_attack(unit, my_team):
    """
    This function preps to attack enemies. 
    Return 1:
        Picks up enemy
        Picks up friend
    Return -1: 
        No one adjacent / did nothing
    """
    friend = None
    enemy = None

    for entity in unit.entities_within_adjacent_distance(1):
        if entity.team == my_team:
            friend = entity
        else: 
            enemy = entity

    if enemy != None and unit.can_pickup(enemy): 
        unit.queue_pickup(enemy)
        print('enemy pickup')
        return 1
    elif friend != None and unit.can_pickup(friend):
        unit.queue_pickup(friend)
        print('friend pickup')
        return 1
    return -1

def prep_defend(unit, my_team):
    """
    This function preps to defend a certain structure. 
    Pick up enemy and throw them as far away as possible from defendLoc.

    Returns:
        1 if picked up enemy 
        -1 if didn't pick up anyone
    """
    for entity in unit.entities_within_adjacent_distance(1):
        if unit.can_pickup(entity):
            if entity.team != my_team: 
                unit.queue_pickup(entity)
                return 1
    return -1
