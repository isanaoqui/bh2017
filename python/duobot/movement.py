import battlecode
import time
import random


def expansion(state, entity):
	my_location = entity.location
	sector_list = get_unclaimed_sector_list(state) #must be updated for every robot, so that each robot can go to different sectors
	min_distance = 10000
	closest_sector = None
	for sector in sector_list:
		sector_distance = sector.top_left.distance_to(my_location)
		if sector_distance < min_distance:
			min_distance = sector_distance
			closest_sector = sector
	if closest_sector == None:
		return "idle"
	sector_location = closest_sector.top_left

	if sector_location == my_location and entity.can_build(battlecode.Direction.EAST):
		entity.queue_build(battlecode.Direction.EAST)
	else: 
		move_to_location(state, entity, closest_sector.top_left)
		return "moving"
		#sprint("moving to location")
	return "building"

def move_to_location(state, entity, location):
	my_location = entity.location
	if my_location == location: return
	
	target_direction = my_location.direction_to(location)
	if entity.can_move(target_direction):
		entity.queue_move(target_direction)


def get_unclaimed_sector_list(state):
	sector_list = []
	total_sector_list = []
	map_height = state.map.height
	map_width = state.map.width
	for x in range(int(map_width/5)):
		for y in range(int(map_height/5)):
			sector = state.map.sector_at(battlecode.Location(5*x,5*y))
			total_sector_list.append(sector)
			if sector.team.name != state.my_team.name:
				sector_list.append(sector)
	return sector_list

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




