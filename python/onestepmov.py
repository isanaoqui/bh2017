import battlecode 

def away_from_glass(unit, state):
    """
    This function instructs unit to move away from closest statue.

    Returns: 
        1 if moved away
        -1 if moved "randomly"
        0 if didn't move
    """
    statues = list(state.get_entities(entity_type='statue',team=state.my_team))
    statues = sorted(statues, key=lambda x: unit.location.distance_to(x.location))

    for statue in statues: 
        direction = statue.location.direction_to(unit.location)
        if unit.can_move(direction):
            unit.queue_move(direction)
            return 1

    for direction in battlecode.Direction.directions():
        if unit.can_move(direction):
            unit.queue_move(direction)
            return -1
            
    return 0