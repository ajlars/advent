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

test_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""".splitlines()

test_results = 22

def main():
    items = [item.split(',') for item in (test_input if test else puzzle_input)]
    if level == 'one':
        results = solver_one(items)
        if test:
            print('Tests passed!' if results == test_results else f'Tests failed... (Results: {results})')
        else:
            print(f'Results: {results}')
    elif level == 'two':
        results = solver_two(items)
        if test:
            print('Tests passed!' if results == '(6, 1)' else f'Tests failed... (Results: {results})')
        else:
            print(f'Results: {results}')
    print(f'\nDuration: {datetime.now() - start}')

def solver_one(input):
    print(f'\nAdvent of Code Day: {day} - Solution One{' - Test' if test else ''}')
    memory = MemorySector(make_grid(input), input)
    memory.byte_fall(1024)
    print(memory)
    return memory.find_path()

def solver_two(input):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    memory = MemorySector(make_grid(input), input)
    return memory.find_impassible()

def make_grid(input):
    width = max(int(line[0]) for line in input)+1
    height = max(int(line[1]) for line in input)+1
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append('.')
        grid.append(row)
    return grid

class MemorySector(Grid):
    def __init__(self, grid_array:list, items: list[Point]):
        super().__init__(grid_array)
        self._bytes = [Point(int(x[0]), int(x[1])) for x in items]
        self.sectors = {}
        self.sector_id = 0

    def reset_grid(self):
        for point in self.all_points():
            self.set_value_at_point(point, '.')

    def byte_fall(self, count):
        self._graph = nx.Graph()
        for byte in self._bytes[:count+1]:
            self.set_value_at_point(byte, '#')
        for point in self.all_points():
            if self.value_at_point(point) == '.':
                for neighbor in [Point(point.x, point.y-1), Point(point.x, point.y+1), Point(point.x-1, point.y), Point(point.x+1, point.y)]:
                    if self.valid_location(neighbor) and self.value_at_point(neighbor) == '.':
                        self._graph.add_edge(f'{point.x,point.y}', f'{neighbor.x,neighbor.y}')
                        # print(f'Adding edge between {point.x,point.y} and {neighbor.x,neighbor.y}')
    
    def find_path(self):
        start = '(0, 0)'
        end = f'{self.width-1,self.height-1}'
        return nx.shortest_path_length(self._graph, start, end)
    
    def find_impassible(self):
        i = 1024
        for i in range(len(self._bytes)):
            self.reset_grid()
            self.byte_fall(i)
            has_path = nx.has_path(self._graph, '(0, 0)', f'{self.width-1,self.height-1}')
            print(i, self._bytes[i], has_path)
            if not has_path:
                return self._bytes[i]
            # else: print(self)
            
if __name__ == "__main__":
    main()