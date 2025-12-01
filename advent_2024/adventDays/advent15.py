from datetime import datetime
import uuid
from adventDays.helpers import execute, Point, Grid
import re
import sys
from operator import attrgetter
from collections import namedtuple

start = datetime.now()

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

test_input = ["""#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^""".splitlines(),
"""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""".splitlines()]

test_results = [2028, 10092]

def main():
    items = test_input[1] if test else puzzle_input
    if level == 'one':
        results = solver_one(items)
        if test:
            print('Tests passed!' if results == test_results[1] else f'Tests failed...{results}')
        else:
            print(f'Results: {results}')
    elif level == 'two':
        results = solver_two(items)
        if test:
            print('Tests passed!' if results == test_results[1] else f'Tests failed...{results}')
        else:
            print(f'Results: {results}')
    print(f'\nDuration: {datetime.now() - start}')

def solver_one(input):
    print(f'\nAdvent of Code Day: {day} - Solution One{' - Test' if test else ''}')
    empty_line = input.index('')
    map = Warehouse(input[:empty_line])
    moves = list(filter(lambda x: x in ['<', '^', '>', 'v'], ''.join(input[(empty_line +1) :])))

    for move in moves:
        map.move_robot(move)

    print(map)    

    return map.get_coords_sum()

def solver_two(input):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    empty_line = input.index('')
    new_map = []
    for line in input[:empty_line]:
        new_row = []
        for char in line:
            if char == Warehouse.BOX:
                new_row.append(Warehouse.BOX_LEFT)
                new_row.append(Warehouse.BOX_RIGHT)
            elif char == Warehouse.ROBOT:
                new_row.append(Warehouse.ROBOT)
                new_row.append(Warehouse.EMPTY)
            else:
                new_row.append(char)
                new_row.append(char)
        new_map.append(new_row)
    map = Warehouse(new_map, True)
    moves = list(filter(lambda x: x in ['<', '^', '>', 'v'], ''.join(input[(empty_line +1) :])))
    print(map)    
    
    for move in moves:
        map.move_robot(move)

    print(map) 

    # return None
    return map.get_coords_sum()

class Warehouse(Grid):
    DIRECTION_MAP = {
        '<': Point(-1, 0),
        '>': Point(1, 0),
        '^': Point(0, -1),
        'v': Point(0, 1)
    }
    BOX = 'O'
    ROBOT = '@'
    WALL = '#'
    EMPTY = '.'
    BOX_LEFT = "["
    BOX_RIGHT = "]"

    def __init__(self, grid_array:list, doubled=False):
        super().__init__(grid_array)
        self._robot_location = self._locate_robot()
        self._doubled = doubled

    def _locate_robot(self):
        return self.find_value(Warehouse.ROBOT)
        
    def move_robot(self, move:str):
        print(self)
        if not self._doubled:
            # print(f'move: {move}')
            move_mod = self.DIRECTION_MAP[move]
            # print(f'move_mod: {move_mod}')
            # print(f'self._robot_location: {self._robot_location}, self.move_mod: {move_mod}')
            check_point = self._robot_location + move_mod
            # print(f'check_point: {check_point}, self._robot_location: {self._robot_location}')
            queued_moves = []
            while(self.value_at_point(check_point) in [Warehouse.BOX]):
                if(self.value_at_point(check_point) == Warehouse.BOX):
                    queued_moves.append(check_point)
                check_point += move_mod
                if(self.value_at_point(check_point) == Warehouse.WALL):
                    queued_moves = []
            if(self.value_at_point(check_point) == Warehouse.EMPTY):
                queued_moves.append(check_point)
            
            for point in reversed(queued_moves):
                source = point - move_mod
                # print(f'\tpoint: {point},\n\tself.value_at_point(point): {self.value_at_point(point)},\n\tself.value_at_point(source): {self.value_at_point(source)}')
                self.set_value_at_point(point, self.value_at_point(source))
                self.set_value_at_point(source, Warehouse.EMPTY)

            if(len(queued_moves) > 0):
                self._robot_location = queued_moves[0]
                # print(f'after move {move}:\n{self}\n')
        else:
            move_mod = self.DIRECTION_MAP[move]
            points_to_move = [[self._robot_location]]
            check_points = set([self._robot_location + move_mod])
            print(f'robot_location: {self._robot_location}, move: {move},   move_mod: {move_mod}')
            all_empty = False
            hit_wall = False
            while(not all_empty and not hit_wall):
                all_empty = True
                new_check_points = set()
                new_points_to_move = set()
                print(f'all_empty: {all_empty}, hit_wall: {hit_wall}, check_points: {check_points}')
                for point in check_points:
                    if not self.valid_location(point) or self.value_at_point(point) == Warehouse.WALL:
                        all_empty = False
                        hit_wall = True
                        break
                    if(self.value_at_point(point) in [Warehouse.BOX_LEFT, Warehouse.BOX_RIGHT]):
                        all_empty = False
                        new_points_to_move.add(point)
                        new_check_points.add(point + move_mod)
                        if move in ['^', 'v']:
                            if self.value_at_point(point) == Warehouse.BOX_LEFT:
                                new_points_to_move.add(point + Point(1, 0))
                                new_check_points.add(point + Point(1, 0) + move_mod)
                            elif self.value_at_point(point) == Warehouse.BOX_RIGHT:
                                new_points_to_move.add(point + Point(-1, 0))
                                new_check_points.add(point + Point(-1, 0) + move_mod)
                escape = False
                for point in new_check_points:
                    if point in check_points:
                        print('some weird loop')
                        escape = True
                        break
                if escape: break
                check_points = new_check_points
                points_to_move.append(list(new_points_to_move))
            print(f'points_to_move: {points_to_move}, all_empty: {all_empty}, hit_wall: {hit_wall}')

            if all_empty:
                # to_move = sorted(list(points_to_move), key=lambda p: (p.y, p.x))
                for row in reversed(points_to_move):
                    for point in reversed(row):
                # for point in to_move:
                        destination = point + move_mod
                        self.set_value_at_point(destination, self.value_at_point(point))
                        self.set_value_at_point(point, Warehouse.EMPTY)
                self._robot_location = self._locate_robot()
            # print(f'points_to_move: {points_to_move}, all_empty: {all_empty}, hit_wall: {hit_wall}')
                
            

    def get_box_coordinates(self):
        coords = []
        for point in self.all_points():
            # print(f'point: {point}, self.valid_location(point): {self.valid_location(point)}\ncoords: {coords}')
            # print(f'self.width: {self.width}, self.height: {self.height}')
            if(self.valid_location(point)):
                if(self.value_at_point(point) in [Warehouse.BOX, Warehouse.BOX_LEFT]):
                    coords.append(point.x + 100 * point.y)
            # else:
                # print(f'point: {point} is apparently not valid?')
        return coords

    def get_coords_sum(self):
        return sum(self.get_box_coordinates())

if __name__ == "__main__":
    main()