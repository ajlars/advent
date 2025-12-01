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

test_input = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############""".splitlines()

test_results = 4

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
    race = Race(input)
    if test:
        print(f'Cheats:\n\t{"\n\t".join(race.get_cheat_counts())}')
        print(f'Cheat: {race.cheats[64]}')
    # print(f'A few cheats:{race.cheats}')
    return race.count_cheats_saving(25 if test else 100)

def solver_two(input):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    race = Race(input, 19)
    if test:
        print(f'Cheats:\n\t{"\n\t".join(race.get_cheat_counts())}')
    return race.count_cheats_saving(25 if test else 100)
    pass

Cheat = namedtuple('Cheat', ['launch', 'distance', 'land', 'savings'])

class Race(Grid):
    START = 'S'
    END = 'E'
    WALL = '#'
    PATH = ['.', 'S', 'E', 'C']
    CHEAT = 'C'
    def __init__(self, input, cheat_length = 1):
        super().__init__(input)
        self._added_edges = []
        self._changed_walls = []
        self._graph = nx.Graph()
        self.start_point =self.point_as_node(self.find_value(self.START))
        self.end_point =self.point_as_node(self.find_value(self.END))
        self.track = self.map_track()
        self.base_length = len(self.track)-1
        print(f'Base length: {self.base_length}, track width: {self.width}, track height: {self.height}, points: {len(self.all_points())}')
        self.cheats = self.get_cheats(cheat_length)

    def get_cheat_counts (self):
        return [f'{k}: {len(v)}' for k, v in self.cheats.items()]

    def count_cheats_saving(self, length):
        count = 0
        for savings in self.cheats:
            if savings >= length:
                # print(f'Cheats saving {savings}: {len(self.cheats[savings])}')
                count += len(self.cheats[savings])
        return count

    def reset(self):
        for edge in self._added_edges:
            self._graph.remove_edge(*edge)
        for wall in self._changed_walls:
            self.set_value_at_point(wall, self.WALL)
        self._added_edges = []

    def map_track(self):
        print('Mapping edges...')
        for point in self.all_points():
            if self.value_at_point(point) in self.PATH:
                for neighbor in self.get_neighbors(point):
                    if self.valid_location(neighbor) and self.value_at_point(neighbor) in self.PATH:
                        self._graph.add_edge(self.point_as_node(point), self.point_as_node(neighbor))
        track = nx.shortest_path(self._graph, self.start_point, self.end_point)
        length = len(track)
        print('Mapping distances...')
        distance_from_start = {}
        distance_from_end = {}
        for i, edge in enumerate(track):
            distance_from_start[edge] = i
            distance_from_end[edge] = length - i
        self._distance_from_start = distance_from_start
        self._distance_from_end = distance_from_end
        return track

    def get_run_length(self, start = None):
        if not start:
            start = self.start_point
        if(nx.has_path(self._graph, start, self.end_point)):
            return nx.shortest_path_length(self._graph, start, self.end_point)
        else:
            return 0

    def get_cheats(self, length = 1):
        cheats = {}
        track_length = len(self.track)
        for i in range(track_length):
            if i % 500 == 0 or i+1 == track_length:
                print(f'Checking point {i+1} of {track_length}, foo {length}')
            _launch = self.track[i]
            launch = Point(*map(int, _launch.split(',')))
            for _land in self.track[i+3:]:
                land = Point(*map(int, _land.split(',')))
                _gap = land - launch
                gap = abs(_gap.x) + abs(_gap.y) - 1
                if gap <= length:
                    distance = self._distance_from_start[_launch] + gap + self._distance_from_end[_land]
                    savings = self.base_length - distance
                    if savings > 0:
                        if savings in cheats:
                            cheats[savings].append(Cheat(launch, gap, land, savings))
                        else:
                            cheats[savings] = [Cheat(launch, gap, land, savings)]
            # current = Point(*map(int, self.track[i].split(',')))
            # previous = Point(*map(int, self.track[i-1].split(','))) if i-1 >= 0 else None
            # next = Point(*map(int, self.track[i+1].split(','))) if i+1 < len(self.track) else None
            # direction = current - previous if previous else next - current
            # for d in [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]:
            #     if d == Point(direction.x * -1 , direction.y*-1):
            #         continue
            #     first = current + d
            #     if self.valid_location(first) and self.value_at_point(first) == self.WALL:
            #         cheat = []
            #         cheat.append(first)
            #         while len(cheat) < length and self.valid_location(cheat[-1] + d):
            #             cheat.append(cheat[-1] + d)
            #         if self.value_at_point(cheat[-1]) in self.PATH:
            #             run = self._distance_from_start[self.point_as_node(current)] + len(cheat) + self._distance_from_end[self.point_as_node(cheat[-1])] - 1
            #             savings = self.base_length - run
            #             if savings > 0:
            #                 if savings in cheats:
            #                     cheats[savings].append(Cheat(current, len(cheat), cheat[-1], savings))
            #                 else:
            #                     cheats[savings] = [Cheat(current, len(cheat), cheat[-1], savings)]
        
                # print(f'Current: {current}, Direction: {d}, First: {first}')
                
        
        # print(cheats)
        # for i, track_point in enumerate(self.track):
        #     point = Point(*map(int, track_point.split(',')))
        #     next_point = Point(*map(int, self.track[i+1].split(','))) if i+1 < len(self.track) else None
        #     if(point.x == 7 and point.y in [6, 7]):
        #         print('point, next_point', point, next_point)
        #     for neighbor in self.get_neighbors(point):
        #         if self.value_at_point(neighbor) == self.WALL:
        #             next_neighbors = self.get_neighbors(neighbor)
        #             for next_neighbor in next_neighbors:
        #                 if self.value_at_point(next_neighbor) in self.PATH and self.point_is_further(point, next_neighbor):
        #                     cheats.add((point, neighbor, None))
        #                 elif self.value_at_point(next_neighbor) == self.WALL:
        #                     last_neighbors = self.get_neighbors(next_neighbor)
        #                     if(next_point and next_point in last_neighbors):
        #                         if(point.x == 7 and point.y in [6, 7]):
        #                             print('last neighbor check... point, next_point', point, next_point)
        #                         continue
        #                     for last_neighbor in self.get_neighbors(next_neighbor):
        #                         if self.value_at_point(last_neighbor) in self.PATH and self.point_is_further(point, last_neighbor):
        #                             cheats.add((point, neighbor, next_neighbor))
        # working = True
        # while working:
        #     working = False
        #     for cheat in cheats:
        #         matchIndex = next((i for i, t in enumerate(cheats) if t[2] == cheat[1]), None)
        #         if matchIndex:
        #             print('found longer match saving same time')
        #             working = True
        #             cheats.remove(list(cheats)[matchIndex])
        #         break
        return dict(sorted(cheats.items(), key=lambda x: x[0], reverse=True))
    
    def try_cheats(self):
        cheats: list[Cheat] = self.get_cheats()
        cheats_by_saved_time = {}
        cheat_count = len(cheats)
        print(f'Checking {cheat_count} cheats:')
        for i, cheat in enumerate(cheats):
            if i%250 == 0 or i+1 == cheat_count:
                print(f'Checking cheat {i+1} of {cheat_count}')
            self.reset()
            for point in cheat.cheated:
                # if point == None or self.point_as_node(point) in self.track:
                #     continue    
                if self.value_at_point(point) == self.WALL:
                    self.set_value_at_point(point, self.CHEAT)
                    self._changed_walls.append(point)
            for point in cheat.cheated:
                # if point == None:
                #     continue
                for neighbor in self.get_neighbors(point):
                    edge = (self.point_as_node(point), self.point_as_node(neighbor))
                    if self.valid_location(neighbor) and self.value_at_point(neighbor) in self.PATH and not self._graph.has_edge(*edge):
                        self._graph.add_edge(*edge)
                        self._added_edges.append(edge)
            run = self.get_run_length(self.point_as_node(cheat.pre))
            saved = self.base_length - cheat.passed - run
            # print(run, cheat.passed)
            if saved > 0:
                if saved in cheats_by_saved_time:
                    cheats_by_saved_time[saved].append(cheat)
                else:
                    cheats_by_saved_time[saved] = [cheat]
            # if saved in [18, 64]:
                # print(f'Cheats: {cheat}, saved: {saved}\n{self}')
        return dict(sorted(cheats_by_saved_time.items(), key=lambda x: x[0], reverse=True))

    def point_is_further(self, pointA, pointB):
        a = self.point_as_node(pointA)
        b = self.point_as_node(pointB)
        return b in self.track and self.track.index(b) > self.track.index(a)


if __name__ == "__main__":
    main()