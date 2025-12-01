import time
import uuid
from adventDays.helpers import execute, Point, Grid
import re
import sys
from operator import attrgetter
from collections import namedtuple

try:
    level = sys.argv[2]
    test = sys.argv[3] == 'test'
except:
    try:
        level = sys.argv[2]
        test = False
    except:
        level = 'one'
        test = False

day = re.search(r"\d+", __file__).group()

filename = f'adventInputs/day{day}.txt'
f = open(filename)
puzzle_input = f.read().splitlines()

test_input = ["""AAAA
BBCD
BECC
BBFC
GGGG
GHGI
GGGG""".splitlines(),
"""OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""".splitlines()
]

test_results = [140, 1930]

class Lot():
    def __init__(self, point:Point, crop: str, region: str, fence: int):
        self._point = point
        self._crop = crop
        self._region = region
        self._fence = fence

    def set_fence(self, fence: int):
        self._fence = fence

    @property
    def x(self):
        return self._point.x
    
    @property
    def y(self):
        return self._point.y

    @property
    def crop(self):
        return self._crop
    
    @property
    def region(self):
        return self._region
    
    @property
    def fence(self):
        return self._fence

Edge = namedtuple('Edge', ['direction', 'axis', 'start', 'end'])

class Farm(Grid):
    def __init__(self, grid_array: list):
        super().__init__(grid_array)
        region_grid = []
        for row in grid_array:
            region_grid.append([0]*len(row))
        self._region_grid = Grid(region_grid)
        
        self._regions: dict[str, (list[Lot], str)] = {}

    def map_lots(self):
        # print(self)
        # print(f'region grid:\n{self._region_grid}')
        for point in self.all_points():
            id = self._region_grid.value_at_point(point)
            if id == 0:
                id = uuid.uuid4()
                crop = self.value_at_point(point)
                self._region_grid.set_value_at_point(point, id)
                lot = Lot(point, crop, id, 0)
                self._regions[id] = ([lot],crop)
                self.map_region(lot)
    
    def map_region(self, lot: Lot):
        # print(f'checking lot: {lot.x}, {lot.y}, crop: {lot.crop}, region: {lot.region}')
        points_to_check = [Point(lot.x, lot.y-1), Point(lot.x+1, lot.y), Point(lot.x, lot.y+1), Point(lot.x-1, lot.y)]
        for point in points_to_check:
            point_in_region = False
            for lot in self._regions[lot.region][0]:
                if lot.x == point.x and lot.y == point.y:
                    point_in_region = True
                    break
            if point_in_region:
                # print(f'\tpoint {point.x}, {point.y} already in the same region')
                continue
            if self.valid_location(point) and lot.crop == self.value_at_point(point) and self._region_grid.value_at_point(point) == 0:
                # print(f'\tadding neighbor {point.x}, {point.y}, {self.value_at_point(point)} to region')
                # neighbor is in region
                self._region_grid.set_value_at_point(point, lot.region)
                _lot =Lot(point, lot.crop, lot.region, 0)
                self._regions[lot.region][0].append(_lot)
                self.map_region(_lot)
            else:
                # neighbor is not in region, don't crawl it
                # if(self.valid_location(point)): print(f'\tneighbor {point.x}, {point.y}, {self.value_at_point(point)} is not in region')
                # else: print(f'\t{point.x}, {point.y} is not a valid location')
                lot.set_fence(lot.fence + 1)

    def get_region_area(self, region: str):
        return len(self._regions[region][0])
    
    def get_region_perimeter(self, region: str):
        return sum([lot.fence for lot in self._regions[region][0]])
    
    def get_edges(self):
        log_region = 'E'
        directions = ['left', 'right', 'up', 'down']
        point_mods = {
            directions[0]:Point(-1, 0),
            directions[1]:Point(1, 0),
            directions[2]:Point(0, -1),
            directions[3]:Point(0, 1)
        }
        region_edges = {}
        for region in self._regions:
            region_edges[region] = {"total":0}
            for direction in directions: region_edges[region][direction] = 0

        def is_not_new_edge(point, direction, region, recursed = False):
            if recursed and self._regions[region][1]==log_region:
                print('\t\t checking recursed...')
            next_point = point + point_mods[direction]
            is_covered = self.valid_location(next_point) and self._region_grid.value_at_point(next_point) == region
            # if a first check is covered, it's not a new edge. If this is a pre-point, and it's covered, this is a new edge
            if is_covered: 
                if recursed:
                    return (False, '\tThe previous point is not on an edge on this side, so the initial point is on a new edge')
                return (True, '\tThe next point in that direction is in the same region, so this is not an edge')
            pre_point = point + point_mods['left' if direction in ['up', 'down'] else 'up']
            pre_point_is_valid = self.valid_location(pre_point) 
            pre_point_is_in_same_region = pre_point_is_valid and self._region_grid.value_at_point(pre_point) == region
            # the pre_point should only be checked if it's valid, and the same region, and not already recursed, otherwise, the current point is a new edge
            if pre_point_is_in_same_region:
                if recursed:
                    return (True, '\t\tThe previous point was in the same region, on the same edge, so this is not a new edge')
                (recursed_check, message) = is_not_new_edge(pre_point, direction, region, True)
                if(self._regions[region][1]==log_region and not recursed_check):
                    print(f'\trecursed check: {recursed_check} {message}')
                return(recursed_check, message)
            if recursed:
                return (True, '\t\tThis prepoint is a new edge, so the current point was not')
            return (False, None)

        for point in self.all_points():
            region = self._region_grid.value_at_point(point)
            if(self._regions[region][1] == log_region):
                print(point)
            for direction in directions:
                next_point = point + point_mods[direction]
                if(self._regions[region][1] == log_region):
                    print(f'  direction: {direction}\n\t next_point: {next_point}, point_mod: {point_mods[direction]}')
                (not_new_edge, message) = is_not_new_edge(point, direction, region)
                # skip if this is not a new edge
                if not_new_edge:
                    if(self._regions[region][1] == log_region):
                        print(message)
                    continue
                region_edges[region][direction] += 1
                if(self._regions[region][1] == log_region):
                        print(f'    EDGE TRACKED')

        for region in region_edges:
            edge_count = 0
            print(f'Region {self._regions[region][1]} edges:')
            for direction in directions:
                print(f'\t{direction}: {region_edges[region][direction]}')
                edge_count += region_edges[region][direction]      
            region_edges[region]['total'] += edge_count
            print(f'\t total: {edge_count}')
        print('total edges', region_edges[region]['total'])
        return region_edges


    
    def get_region_fence_cost(self, region: str):
        return self.get_region_area(region) * self.get_region_perimeter(region)
    
    def get_total_fence_cost(self, discount: bool = False):
        if not discount:
            return sum([(self.get_region_area(region) * self.get_region_perimeter(region)) for region in self._regions])
        else:
            region_edges = self.get_edges()
            cost = 0
            for region in region_edges:
                cost += self.get_region_area(region) * region_edges[region]['total']
                print(region_edges[region])
            return cost
                


def main():
    items = test_input[1] if test else puzzle_input
    if level == 'one':
        results = solver_one(items)
        if test:
            print('Tests passed!' if results == test_results[0] else 'Tests failed...')
        else:
            print(f'Results: {results}')
    elif level == 'two':
        results = solver_two(items)
        if test:
            print('Tests passed!' if results == test_results[0] else f'Tests failed..., results: {results}, test_results: {test_results[0]}')
        else:
            print(f'Results: {results}')

def solver_one(input):
    print(f'\nAdvent of Code Day: {day} - Solution One{' - Test' if test else ''}')
    input = [x for x in input]
    farm = Farm(input)
    farm.map_lots()
    print(f'Total fence cost for map: {farm.get_total_fence_cost()}')
    return farm.get_total_fence_cost()

def solver_two(input):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    input = [x for x in input]
    farm = Farm(input)
    farm.map_lots()

    return farm.get_total_fence_cost(discount=True)

if __name__ == "__main__":
    main()


import multiprocessing