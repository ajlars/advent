from datetime import datetime
import uuid
from adventDays.helpers import execute, Point, Grid
import re
import sys
from operator import attrgetter
from collections import namedtuple
import networkx as nx

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

test_input = """029A
980A
179A
456A
379A""".splitlines()

test_results = 126384

def main():
    items = test_input if test else puzzle_input
    if level == 'one':
        results = solver_one(items)
        if test:
            print('Tests passed!' if results == test_results else f'Tests failed... (Results: {results})')
        else:
            print(f'Results: {results}')
    elif level == 'two':
        results = solver_two(items)
        if test:
            print('Tests passed!' if results == test_results else f'Tests failed... (Results: {results})')
        else:
            print(f'Results: {results}')
    print(f'\nDuration: {datetime.now() - start}')

def solver_one(input):
    print(f'\nAdvent of Code Day: {day} - Solution One{' - Test' if test else ''}')
    codes = input
    keypad_pusher = ButtonPusher(codes)
    keypad_directions = keypad_pusher.get_presses()
    # for i in range(len(keypad_directions)):
    #     res = keypad_pusher.press_keys(keypad_directions[i], True)
    #     print(f'{codes[i]}: {res}, pass ? {codes[i] == res}')
    radiation_pusher = ButtonPusher(keypad_directions)
    radiation_directions = radiation_pusher.get_presses()
    # for i in range(len(radiation_directions)):
    #     res = radiation_pusher.press_keys(radiation_directions[i])
    #     print(f'{keypad_directions[i]}: {res}, pass ? {len(keypad_directions[i]) == len(res)}')
    freezing_pusher = ButtonPusher(radiation_directions)
    freezing_directions = freezing_pusher.get_presses()
    # for i in range(len(freezing_directions)):
    #     res = freezing_pusher.press_keys(freezing_directions[i])
    #     print(f'{radiation_directions[i]}: {res}, pass ? {len(radiation_directions[i]) == len(res)}')
    
    # for i in range(len(freezing_directions)):
    #     print(f'{codes[i]}: {freezing_directions[i]}, len: {len(freezing_directions[i])}')
    # for i in range(len(codes)):
    #     pushed = keypad_pusher.press_keys(radiation_pusher.press_keys(freezing_pusher.press_keys(freezing_directions[i])), True)
    #     print(f'Code expected: {codes[i]} - Code pushed: {pushed}, pass ? {codes[i] == pushed}')
    # print(keypad_pusher.press_keys(radiation_pusher.press_keys(freezing_pusher.press_keys(freezing_directions[0])), True))
    # complexity = 0
    # for i in range(len(codes)):
    #     print(f'{codes[i]}: {freezing_directions[i]}')
    #     _complexity = keypad_pusher.getComplexity(codes[i], freezing_directions[i])
    #     print(f'Complexity = {_complexity}')
    #     complexity += _complexity
    # return complexity

def solver_two(input):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    pass

class ButtonPusher():
    CODEPAD = [['7','8','9'],['4','5','6'],['1','2','3'],[None, '0', 'A']]
    DIRPAD = [[None, '^', 'A'], ['<', 'v', '>']]
    DIRMAP = {
        '^': Point(0, -1),
        'v': Point(0, 1),
        '<': Point(-1, 0),
        '>': Point(1, 0)
    }
    CHANGEMAP = {
        Point(0, -1): '^',
        Point(0, 1): 'v',
        Point(-1, 0): '<',
        Point(1, 0): '>'
    }
    SORT_PRIORITY = ['^', '>','v','<']

    def __init__(self, codes, log = False) -> None:
        self.grid = Grid(self.DIRPAD) if 'v' in ''.join(codes) else Grid(self.CODEPAD)
        self.pointer_location = self.grid.find_value('A')
        self.graph = self.map_grid()
        self.codes = codes
        self._log = log
        self.mem = {}
        print(self.grid)
        if 'v'in ''.join(codes):
            print(nx.shortest_path(self.graph, self.grid.point_as_node(self.grid.find_value('^')), self.grid.point_as_node(self.grid.find_value('<'))))
            print(nx.shortest_path(self.graph, self.grid.point_as_node(self.grid.find_value('<')), self.grid.point_as_node(self.grid.find_value('A'))))

    def get_presses(self):
        presses = []
        for code in self.codes:
            if self.grid.height == 2:
                _codes = code.split('A')
                for _code in _codes:
                    self.sort_keys(_code, self.grid.find_value('A'))
                code = "A".join(_codes)
            code_presses = ''
            for key in code:
                code_presses += self.get_dirpress(key)
            self.log(f'{code}: {code_presses}')
            presses.append(code_presses)
        return presses
    
    def getComplexity(self, code, keys):
        print(f'code: {int(code.replace("A", ""))} * keys: {len(keys)}')
        return int(code.replace('A', '')) * len(keys)

    def map_grid(self):
        graph = nx.Graph()
        for point in self.grid.all_points():
            if self.grid.value_at_point(point) is not None:
                neighbors = self.grid.get_neighbors(point)
                for neighbor in neighbors:
                    if self.grid.value_at_point(neighbor) is not None:
                        graph.add_edge(self.grid.point_as_node(point), self.grid.point_as_node(neighbor))
        return graph
    
    def log(self, message):
        if self._log:
            print(message)
    
    def get_dirpress(self, key):
        self.log(f'Getting dirpress for {key}')
        current = self.grid.point_as_node(self.pointer_location)
        end_pointer = self.grid.find_value(key)
        target = self.grid.point_as_node(end_pointer)
        path = nx.shortest_path(self.graph, current, target)
        _current = self.pointer_location
        dirpress = ''
        self.log(f'\tCurrent: {current} - Target: {target} - Path: {path}')
        for _point in path:
            self.log(f'\t\tPoint: {_point}')
            if _point == current:
                if _point == target:
                    dirpress += 'A'
                    continue
                self.log(f'\t\tSkipping current')
                continue
            point = Point(*map(int, _point.split(',')))
            change = point - _current
            self.log(f'\t\tChange: {change}')
            dirpress += self.CHANGEMAP[change]
            _current = point
            if _point == target:
                dirpress =''.join(sorted(dirpress))
                dirpress += 'A'
        self.pointer_location = end_pointer
        self.log(dirpress)
        return dirpress
    
    def sort_keys(self, keys, starting_point):
        _keys = []
        _sorted = ''
        _current = (self.grid.value_at_point(starting_point), starting_point)
        for key in keys:
            _keys.append((key, self.grid.find_value(key)))
        while len(_keys) > 0:
            unique_values = list(set([(key, point) for key, point in _keys]))
            distances = []
            for value in unique_values:
                if((starting_point[0], value[0]) in self.mem):
                    distance = self.mem[(starting_point[0], value[0])]
                else:
                    distance = abs(_current[1].x - value[1].x) + abs(_current[1].y - value[1].y)
                    self.mem[(starting_point[0], value[0])] = distance
                distances.append((value[0], distance))
            distances = sorted(distances, key=lambda x: x[1])
            _closest = distances[0][0]
            count = keys.count(_closest)
            # print('closest', _closest, count)
            _sorted += _closest * count
            _current = _closest
            _keys = [key for key in _keys if key[0] != _closest[0]]
            # print('unique_values', unique_values)
        # print(f'Sorted: {keys} -> {_sorted}')
        return _sorted
    
    def press_keys(self, keys, codepad = False):
        grid = Grid(self.CODEPAD if codepad else self.DIRPAD)
        current = grid.find_value('A')
        pressed = ''
        for key in keys:
            if key == 'A':
                pressed+=grid.value_at_point(current)
                continue
            current += self.DIRMAP[key]
        return pressed

            
        

if __name__ == "__main__":
    main()


# 029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A


# 980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
# 980A: <<vA>>^AAAvA^A<<vAA>A>^AvAA<^A>A<<vA>A>^AAAvA<^A>A<vA>^A<A>A


# 179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# 179A: <<vAA>A>^AAvA<^A>AvA^A<<vA>>^AAvA^A<vA>^AA<A>A<<vA>A>^AAAvA<^A>A


# 456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A


# 379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A