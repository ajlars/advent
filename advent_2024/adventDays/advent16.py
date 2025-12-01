from datetime import datetime
import uuid
from adventDays.helpers import execute, Point, Grid
import re
import sys
from operator import attrgetter
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt

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

test_input = ["""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""".splitlines(),
"""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""".splitlines()]

test_results = [7036, 11048]

def main():
    test_index = 1
    items = test_input[test_index] if test else puzzle_input
    if level == 'one':
        results = solver_one(items)
        if test:
            print('Tests passed!' if results == test_results[test_index] else 'Tests failed...')
        else:
            print(f'Results: {results}')
    elif level == 'two':
        results = solver_two(items)
        if test:
            print('Tests passed!' if results == test_results[test_index] else 'Tests failed...')
        else:
            print(f'Results: {results}')
    print(f'\nDuration: {datetime.now() - start}')

def solver_one(input):
    print(f'\nAdvent of Code Day: {day} - Solution One{' - Test' if test else ''}')
    maze = Maze(input)
    # print(maze)
    # for i in range(45):
    i = 0
    # while maze.has_incomplete_paths():
    #     maze.move()
    #     print(f'Iteration {i} : time: {datetime.now() - start}, current low:\t{maze.lowest_score}, cut:\t{maze._cut}, blocked:\t{maze._blocked_paths}, current:\t{len(maze._paths)}')
    #     i+=1
        # print('has incompletes', maze.has_incomplete_paths())
    # score = maze.traverse_corners()
    # score = maze.weighted_graph()
    
    # print(maze)
    # print('complete', len(maze.get_complete_paths()))
    # print('incomplete', len(maze.get_incomplete_paths()))
    # print('lowest', maze.get_paths()[0].score)
    return maze.networkx_graph()[0]

def solver_two(input):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    maze = Maze(input)
    return maze.networkx_graph()[1]

Path = namedtuple("Path", ["run", "score", "complete"])

Corner = namedtuple("Corner", ["point", "up", "down", "left", "right"])
MappedCorner = namedtuple("MappedCorner", ["corner", "up", "down", "left", "right"])
MappedPoint = namedtuple("MappedPoint", ["corner", "distance", "traversed"])
class Maze(Grid):
    WALL = '#'
    EMPTY = '.'
    START = 'S'
    END = 'E'
    MOVES = {
        '^': Point(0, -1),
        'v': Point(0, 1),
        '<': Point(-1, 0),
        '>': Point(1, 0)
    }
    def __init__(self, grid_array: list) -> None:
        super().__init__(grid_array)
        self._start = self.find_value(self.START)
        self._end = self.find_value(self.END)
        self._paths: list[Path] = [Path([(self._start, '>')], 0, False)]
        self._lowest_complete = False
        self._blocked_paths = 0
        self._cut = 0

    def _can_travel(self, run: list[tuple[Point, str]]) -> list[tuple[str, bool]]:
        location, direction = run[-1]
        moves: list[tuple[str, bool]] = []
        for _direction in self.MOVES.keys():
            if(self.MOVES[direction]+self.MOVES[_direction] != Point(0, 0)):
                next_location = location + self.MOVES[_direction]
                already_traversed = location in [x[0] for x in run[:-1]]
                if self.value_at_point(next_location) != self.WALL and not already_traversed:
                    moves.append((_direction, _direction != direction))
                elif direction == _direction: self._blocked_paths += 1
        return moves
    
    def move(self):
        paths = []
        for path in self._paths:
            if(path.complete):
                paths.append(path)
                continue
            # print(path)
            moves = self._can_travel(path.run)
            # print(moves)
            # if len(moves) == 0:
                # print(f'Run blocked: {path}')
            for move in moves:
                new_run = path.run.copy()
                new_score = path.score
                new_complete = False
                if move[1] :
                    new_run[-1] = (new_run[-1][0], move[0])
                    new_score += 1000
               
                new_run.append((new_run[-1][0] + self.MOVES[move[0]], move[0]))
                new_score += 1
                if(new_run[-1][0] == self._end):
                    if not self._lowest_complete or new_score < self._lowest_complete :
                        self._lowest_complete = new_score
                    new_complete = True
                if self._lowest_complete != False and new_score > self._lowest_complete :
                    self._cut +=1
                else:
                    paths.append(Path(new_run, new_score, new_complete))
        self._paths = paths
            # for move in moves:
            #     runs.append((run + (run[-1][0] + self.MOVES[move[0]], move[1])), run[-1][1] + 1001 if move[1] else 1 )

    @property
    def lowest_score(self):
        return self._lowest_complete

    def get_paths(self):
        return sorted(self._paths, key=attrgetter('score'))
    
    def has_incomplete_paths(self):
        return any(not path.complete for path in self._paths)
    
    def get_complete_paths(self):
        paths = [path for path in self._paths if path.complete]
        # val = ''
        # print(f'Complete Paths: {len(paths)}')
        # for i, path in enumerate(paths):
        #     val += f'\nRun {i}\n\tScore:\t\t{path.score}\n\tComplete:\t{path.complete}\n\t{'\n\t'.join(f'{x[0], x[1]}' for x in path.run)}'
        # print(f'Complete Paths: {len(paths)}')
        return paths
    
    def get_incomplete_paths(self):
        paths = [path for path in self._paths if not path.complete]
        # val = ''
        # print(f'Complete Paths: {len(paths)}')
        # for i, path in enumerate(paths):
        #     val += f'\nRun {i}\n\tScore:\t\t{path.score}\n\tComplete:\t{path.complete}\n\t{'\n\t'.join(f'{x[0], x[1]}' for x in path.run)}'
        # print(f'Complete Paths: {len(paths)}')
        return paths
    
    def _map_corners(self):
        corners:list[Corner] = []
        points = self.all_points()
        len_points = len(points)
        for i, point in enumerate(points):
            if i%100 == 0:
                print(f'Point {i+1}/{len_points}')
            if self.value_at_point(point) != self.WALL:
                paths = 0
                up = self.valid_location(point + Point(0, -1)) and self.value_at_point(point + Point(0, -1)) != self.WALL
                down = self.valid_location(point + Point(0, 1)) and self.value_at_point(point + Point(0, 1)) != self.WALL
                left = self.valid_location(point + Point(-1, 0)) and self.value_at_point(point + Point(-1, 0)) != self.WALL
                right = self.valid_location(point + Point(1, 0)) and self.value_at_point(point + Point(1, 0)) != self.WALL
                for place in [up, down, left, right]:
                    if place:
                        paths +=1
                # print(f'Point: {point}, value: {self.value_at_point(point)}, up: {up}, down: {down}, left: {left}, right: {right}, paths: {paths}')
                if point == self._start or paths > 2 or (paths > 1 and ((up and right) or (up and left) or (down and right) or (down and left))):
                    corners.append(Corner(point, up, down, left, right))
        len_corners = len(corners)
        print(f'Found {len_corners} corners')
        mappedCorners:list[MappedCorner] = []
        for i, corner in enumerate(corners):
            if i%25==0 :
                print(f'Mapping corner {i+1}/{len_corners}')
            mapped_up = False
            mapped_down = False
            mapped_left = False
            mapped_right = False
            if corner.up :
                for y in range(1, corner.point.y):
                    if self.value_at_point(Point(corner.point.x, corner.point.y-y)) == self.WALL:
                        break
                    _up = next((c for c in corners if c.point.x == corner.point.x and c.point.y == corner.point.y-y), None)
                    if _up!=None:
                        mapped_up = MappedPoint(_up.point, abs(y), False)
                        break
            if corner.down :
                for y in range(1, self.height - corner.point.y):
                    if self.value_at_point(Point(corner.point.x, corner.point.y+y)) == self.WALL:
                        break
                    _down = next((c for c in corners if c.point.x == corner.point.x and c.point.y == corner.point.y+y), None)
                    if _down!=None:
                        mapped_down = MappedPoint(_down.point, abs(y), False)
                        break
            if corner.left :
                for x in range(1, corner.point.x):
                    if self.value_at_point(Point(corner.point.x-x, corner.point.y)) == self.WALL:
                        break
                    _left = next((c for c in corners if c.point.x == corner.point.x-x and c.point.y == corner.point.y), None)
                    if _left != None:
                        mapped_left = MappedPoint(_left.point, abs(x), False)
                        break
            if corner.right :
                for x in range(1, self.width - corner.point.x):
                    if self.value_at_point(Point(corner.point.x+x, corner.point.y)) == self.WALL:
                        break
                    _right = next((c for c in corners if c.point.x == corner.point.x+x and c.point.y == corner.point.y), None)
                    if _right != None:
                        mapped_right = MappedPoint(_right.point, abs(x), False)
                        break
            # print(f'\t{corner.point}, up: {mapped_up}, down: {mapped_down}, left: {mapped_left}, right: {mapped_right}')
            mappedCorners.append(MappedCorner(corner.point, mapped_up, mapped_down, mapped_left, mapped_right))
        self._mappedCorners = mappedCorners
        return mappedCorners
    
    def networkx_graph(self):
        n = nx.DiGraph()
        for point in self.all_points():
            if self.value_at_point(point) != self.WALL:
                for d in range(4):
                    dx, dy = [(1, 0),(0, 1), (-1, 0), (0, -1)][d]
                    n.add_edge( (point.x, point.y, d), (point.x+dx, point.y+dy, d), weight=1)
                    n.add_edge( (point.x, point.y, d), (point.x, point.y, (d-1)%4), weight=1000)
                    n.add_edge( (point.x, point.y, d), (point.x, point.y, (d+1)%4), weight=1000)

        m = [nx.shortest_path_length(n, source=(self._start.x, self._start.y, 0), target=(self._end.x, self._end.y, d), weight='weight') for d in range(4)]
        min_score = min (m)
        spaces = len(set(tuple(p) for d in range(4) if m[d]==min(m) for t in nx.all_shortest_paths(n, source=(self._start.x, self._start.y, 0), target=(self._end.x, self._end.y, d), weight='weight') for *p, h in t))
        return min_score, spaces

    def weighted_graph(self):
        corner_graph = nx.Graph()
        corners = self._map_corners()
        edges = set()
        edge_count = 0
        for i, corner in enumerate(corners):
            for direction in ['up', 'down', 'left', 'right']:
                if getattr(corner, direction) != False:
                    edge_count += 1
                    next_corner:MappedPoint = getattr(corner, direction)
                    if(next_corner.corner.x < corner.corner.x):
                        edges.add((f'{next_corner.corner.x, next_corner.corner.y}', f'{corner.corner.x, corner.corner.y}', next_corner.distance))
                    else:
                    # print(f'Adding edge {corner.corner.x, corner.corner.y} -> {next_corner.corner.x, next_corner.corner.y}')
                        edges.add((f'{corner.corner.x, corner.corner.y}', f'{next_corner.corner.x, next_corner.corner.y}', next_corner.distance))
        print(f'Added {edge_count} edges, set length {len(edges)}')
        for edge in edges:
            corner_graph.add_edge(edge[0], edge[1], weight=edge[2])
                    # corner_graph.add_edge(f'{corner.corner.x, corner.corner.y}', f'{next_corner.corner.x, next_corner.corner.y}')
        # path_gen = nx.all_simple_paths(corner_graph, source=f'{self._start.x, self._start.y}', target=f'{self._end.x, self._end.y}')
        scores = []
        # shortest = nx.shortest_path(corner_graph, source=f'{self._start.x, self._start.y}', target=f'{self._end.x, self._end.y}', weight="weight")
        shortest = nx.shortest_path_length(corner_graph, source=f'{self._start.x, self._start.y}', target=f'{self._end.x, self._end.y}', weight="weight")

        for path in nx.all_shortest_paths(corner_graph, source=f'{self._start.x, self._start.y}', target=f'{self._end.x, self._end.y}', weight="weight"):
            _prev_node = path[0][1:-1].split(',')
            prev_node = Point(int(_prev_node[0]), int(_prev_node[1]))
            change_axis = 'x'
            points = 0
            for node in path[1:]:
                _node = node[1:-1].split(',')
                next_node = Point(int(_node[0]), int(_node[1]))
                if(prev_node.x != next_node.x):
                    if change_axis == 'y':
                        points += 1000
                    change_axis = 'x'
                    points += abs(prev_node.x - next_node.x)
                else:
                    if change_axis == 'x':
                        points += 1000
                    change_axis = 'y'
                    points += abs(prev_node.y - next_node.y)
                prev_node = next_node
            scores.append(points)
            print(f'Scores {len(scores)}')
        scores.sort()
        print(scores)

        print(shortest)
            
        # shortest = nx.shortest_path(corner_graph, source=f'{self._start.x, self._start.y}', target=f'{self._end.x, self._end.y}')
        # _prev_node = shortest[0][1:-1].split(',')
        # prev_node = Point(int(_prev_node[0]), int(_prev_node[1]))
        # change_axis = 'y'
        # points = 0
        # for node in shortest[1:]:
        #     _node = node[1:-1].split(',')
        #     next_node = Point(int(_node[0]), int(_node[1]))
        #     if(prev_node.x != next_node.x):
        #         if change_axis == 'y':
        #             points += 1000
        #         change_axis = 'x'
        #         points += abs(prev_node.x - next_node.x)
        #     else:
        #         if change_axis == 'x':
        #             points += 1000
        #         change_axis = 'y'
        #         points += abs(prev_node.y - next_node.y)
        #     prev_node = next_node
            
        # print(shortest)
        # print(points)
        return scores[0]
    
# [102388, 102388, 102388, 104388, 104388, 104388]

    def traverse_corners(self):
        corners = self._map_corners()
        to_crawl: list[tuple[list[Point, int, str]]] = [[(self._start, 0, 'right')]]
        crawled: list[tuple[list[Point, int, str], int]]= []
        blocked = 0
        last_time = datetime.now()
        i = 0
        while(len(to_crawl) > 0):
            print(f'Iteration {i+1}\n\tto_crawl: {len(to_crawl)}\n\tblocked: {blocked}\n\tcrawled: {len(crawled)}\n\tprevious iteration time: {datetime.now() - last_time}')
            last_time = datetime.now()
            # if i < 5:
                # print(f'Iteration {i+1}, to_crawl:\n\t{'\n\t'.join([f'{x}' for x in to_crawl])}')
            _to_crawl: list[tuple[list[Point, int, str]]] = []
            for crawling in to_crawl:
                # if i < 5:
                    # print(f'\tcrawling: {crawling}, last_point = {crawling[-1]}')
                _corner = next((c for c in corners if c.corner == crawling[-1][0]), None)
                if _corner != None:
                    # if i < 5:
                        # print(f'\tcorner: {_corner}')
                    for direction in ['up', 'down', 'left', 'right']:
                        if getattr(_corner, direction) != False:
                            # if i < 5:
                                # print(f'\tDirection: {direction}, next_corner: {getattr(_corner, direction)}')
                            next_corner:MappedPoint = getattr(_corner, direction)
                            if any(next_corner.corner == x[0] for x in crawling):
                                # if i < 5:
                                    # print('\t\tblocked')
                                blocked += 1
                                continue
                            next_crawl = crawling.copy()
                            next_crawl.append((next_corner.corner, next_corner.distance, direction))
                            # if i == 0:
                            #     print(f'\tNext Crawl: {next_crawl}')
                            if next_corner.corner == self._end :
                                # print(f'Found path: {next_crawl}')
                                crawled.append((next_crawl, 0))
                            else:
                                _to_crawl.append(next_crawl)
            
            to_crawl = _to_crawl
            i+=1
        # print('\n'.join(f'{x}' for x in corners))
        print(f'Found {len(crawled)} paths')
        # print(crawled[0])
        for i, path, in enumerate(crawled):
            if i % 100 == 0:
                print(f'Path {i+1}/{len(crawled)}')
            # if i == 0:
                # print(f'\n\nPath: {path}')
            points = 0
            for j, corner in enumerate(path[0]):
                # if i == 0:
                    # print(f'\t{points} points += {corner[1]}')
                points += corner[1]
                if j > 0 and corner[2] != path[0][j-1][2]:
                    # print(corner[2], path[0][j-1][2])
                    # if i == 0:
                        # print(f'\t{points} points += 1000 ({corner[2]} != {path[0][j-1][2]})')
                    points += 1000
            crawled[i] = (path[0], points)
            # if i == 0:
                # print(f'\t{points} points')
                # print(f'\n\nupdated: {'\n\t'.join(f'{x}' for x in crawled[i][0])}\n\t{crawled[i][1]}')
        sorted_by_points = sorted(crawled, key=lambda x: x[1])
        print(f'Lowest score: \n\t{'\n\t'.join(f'{x}' for x in sorted_by_points[0][0])}\n\tPoints: {sorted_by_points[0][1]}')
        return(sorted_by_points[0][1])

    def __str__(self) -> str:
        val = ''
        for i, path in enumerate(self._paths):
            val += f'\nRun {i}\n\tScore:\t\t{path.score}\n\tComplete:\t{path.complete}\n\t{'\n\t'.join(f'{x[0], x[1]}' for x in path.run)}'
        return val
    
if __name__ == "__main__":
    main()