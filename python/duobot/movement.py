import battlecode
import time
import random


# def expansion(state, entity):
#     my_location = entity.location
#     sector_list = get_unclaimed_sector_list(state) #must be updated for every robot, so that each robot can go to different sectors
#     min_distance = 10000
#     closest_sector = None
#     for sector in sector_list:
#         sector_distance = sector.top_left.distance_to(my_location)
#         if sector_distance < min_distance:
#             min_distance = sector_distance
#             closest_sector = sector
#     if closest_sector == None:
#         return "idle"
#     sector_location = closest_sector.top_left

#     if sector_location == my_location and entity.can_build(battlecode.Direction.EAST):
#         entity.queue_build(battlecode.Direction.EAST)
#     else: 
#         move_to_location(state, entity, closest_sector.top_left)
#         return "moving"
#         #sprint("moving to location")
#     return "building"

def move_to_location(state, entity, location):
    my_location = entity.location
    if my_location == location: return
    
    target_direction = my_location.direction_to(location)
    if entity.can_move(target_direction):
        entity.queue_move(target_direction)


def get_fraction_sectors(state, team):
    num_sectors = 0
    total_sectors = 0
    map_height = state.map.height
    map_width = state.map.width
    for x in range(int(map_width/5)):
        for y in range(int(map_height/5)):
            sector = state.map.sector_at(battlecode.Location(5*x,5*y))
            total_sectors += 1
            if sector.team == team:
                num_sectors += 1
    return float(num_sectors) / float(total_sectors)

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

def space_out(state, entity, radius):
	my_location = entity.location
	direction_dict = {}

	cumulative_x = 0
	cumulative_y = 0
	nearby_entities = entity.entities_within_euclidean_distance(radius)
	for nearby_entity in nearby_entities:
		if nearby_entity.team == state.other_team: continue
		vector = compute_vector(entity,nearby_entity)
		cumulative_x += vector[0]
		cumulative_y += vector[1]

	if cumulative_x == 0 and cumulative_y == 0: return
	final_direction = battlecode.Direction.from_delta(cumulative_x,cumulative_y)

	if entity.can_move(final_direction):
		entity.queue_move(final_direction)
	else:
		for direction in battlecode.Direction.directions():
			if entity.can_move(direction):
				entity.queue_move(direction)



def compute_vector(entity, other):
	my_location = entity.location
	other_location = other.location
	dx = my_location.x - other_location.x
	dy = my_location.y - other_location.y
	return (dx,dy)





