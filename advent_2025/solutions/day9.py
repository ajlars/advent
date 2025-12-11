from operator import ne
import networkx as nx
from helpers import Grid, Point
from itertools import combinations
from shapely.geometry import Polygon, box
from shapely.prepared import prep

day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
# input_2 = f2.read().splitlines()
input_2 = input_1
test_1 = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""".splitlines()
# test_2 = """""".splitlines()
test_2 = test_1

def solution_1(input):
    tiles = TileGrid(input)
    print("Solution 1: Largest rectangle area =", tiles.get_largest_rectangle()[2]['weight'])

def solution_2(input):
    tiles = TileGrid(input, part=2)
    largest_rectangle = tiles.get_largest_rectangle()
    print(largest_rectangle)
    # print("Solution 2: Largest rectangle area =", largest_rectangle[2]['weight'])

class TileGrid:
    def __init__(self, input, part=1):
        self.part = part
        self.red_tiles = [Point(x[0], x[1]) for x in [list(map(int, line.split(','))) for line in input]]
        self.green_tiles = []
        self.graph = nx.Graph()
        if part == 1:
            self.map_graph_1()
        else:
            self.build_outline_points()
            # Get bounding box
            self.min_x = min(p.x for p in self.red_tiles)
            self.max_x = max(p.x for p in self.red_tiles)
            self.min_y = min(p.y for p in self.red_tiles)
            self.max_y = max(p.y for p in self.red_tiles)
            print(f'Bounding box: ({self.min_x},{self.min_y}) to ({self.max_x},{self.max_y})')
            self.map_graph_2()

    def draw_map(self, fill_enclosed=True) -> Grid:
        max_x = max([tile.x for tile in self.red_tiles])
        max_y = max([tile.y for tile in self.red_tiles])
        rows = [ list('.' * (max_x+1)) for _ in range(max_y+1)]
        for i in range(len(self.red_tiles)):
            if(i%10==0):
                print(f'Drawing outline: processing red tile {i+1} of {len(self.red_tiles)}')
            current_tile = self.red_tiles[i]
            next_tile = self.red_tiles[(i + 1) % len(self.red_tiles)]
            diff = current_tile - next_tile
            direction = 'r' if diff.x < 0 else 'l' if diff.x > 0 else 'd' if diff.y < 0 else 'u'
            steps = abs(diff.x) if diff.x != 0 else abs(diff.y)
            for step in range(1, steps+1):
                change_tile = None
                if direction == 'r':
                    change_tile = Point(current_tile.x + step, current_tile.y)
                elif direction == 'l':
                    change_tile = Point(current_tile.x - step, current_tile.y)
                elif direction == 'd':
                    change_tile = Point(current_tile.x, current_tile.y + step)
                elif direction == 'u':
                    change_tile = Point(current_tile.x, current_tile.y - step)
                if change_tile:
                    self.green_tiles.append(change_tile)
                    rows[change_tile.y][change_tile.x] = 'X'

        for tile in self.red_tiles:
            rows[tile.y][tile.x] = '#'

        print(f'Grid outline has {len(self.red_tiles)} red tiles and {len(self.green_tiles)} green tiles')


        if(fill_enclosed):
            grid = Grid(rows)

            def is_enclosed(point: Point):
                left_point = Point(point.x - 1, point.y)
                up_point = Point(point.x, point.y - 1)
                if((grid.location_is_valid(left_point) and grid.value_at_point(left_point) in ['#', 'X']) and (grid.location_is_valid(up_point) and grid.value_at_point(up_point) in ['#', 'X'])):
                    return True

            for point in grid.all_points():
                if grid.value_at_point(point) == '.' and is_enclosed(point):
                    grid.set_value_at_point(point, 'X')
                    self.green_tiles.append(point)
        else:
            grid = Grid(rows)

        return grid

    def map_graph_1(self):
        for i in range(len(self.red_tiles)):
            for j in range(i + 1, len(self.red_tiles)):
                # x = 1
                # y = 1
                x = abs(self.red_tiles[i].x - self.red_tiles[j].x) + 1
                y = abs(self.red_tiles[i].y - self.red_tiles[j].y) + 1
                # print(f'Connecting {self.red_tiles[i]} to {self.red_tiles[j]} with area {x*y}')
                self.graph.add_edge(self.red_tiles[i], self.red_tiles[j], weight=x*y)
    
    def build_outline_points(self):
        """Build the outline points without creating a full grid"""
        print(f'Building outline from {len(self.red_tiles)} red tiles...')
        for i in range(len(self.red_tiles)):
            if i % 10 == 0:
                print(f'Processing edge {i+1}/{len(self.red_tiles)}')
            current_tile = self.red_tiles[i]
            next_tile = self.red_tiles[(i + 1) % len(self.red_tiles)]
            diff = current_tile - next_tile
            direction = 'r' if diff.x < 0 else 'l' if diff.x > 0 else 'd' if diff.y < 0 else 'u'
            steps = abs(diff.x) if diff.x != 0 else abs(diff.y)
            for step in range(1, steps):  # Don't include endpoints (they're already in red_tiles)
                if direction == 'r':
                    self.green_tiles.append(Point(current_tile.x + step, current_tile.y))
                elif direction == 'l':
                    self.green_tiles.append(Point(current_tile.x - step, current_tile.y))
                elif direction == 'd':
                    self.green_tiles.append(Point(current_tile.x, current_tile.y + step))
                elif direction == 'u':
                    self.green_tiles.append(Point(current_tile.x, current_tile.y - step))
        print(f'Outline complete: {len(self.red_tiles)} vertices + {len(self.green_tiles)} edge points = {len(self.red_tiles) + len(self.green_tiles)} total')
    
    def point_in_polygon(self, point: Point) -> bool:
        """Check if a point is inside the polygon using ray casting"""
        test_x, test_y = point.x, point.y
        num_vertices = len(self.red_tiles)
        inside = False
        
        edge_start_x, edge_start_y = self.red_tiles[0].x, self.red_tiles[0].y
        for i in range(1, num_vertices + 1):
            edge_end_x, edge_end_y = self.red_tiles[i % num_vertices].x, self.red_tiles[i % num_vertices].y
            if test_y > min(edge_start_y, edge_end_y):
                if test_y <= max(edge_start_y, edge_end_y):
                    if test_x <= max(edge_start_x, edge_end_x):
                        if edge_start_y != edge_end_y:
                            x_intersection = (test_y - edge_start_y) * (edge_end_x - edge_start_x) / (edge_end_y - edge_start_y) + edge_start_x
                        if edge_start_x == edge_end_x or test_x <= x_intersection:
                            inside = not inside
            edge_start_x, edge_start_y = edge_end_x, edge_end_y
        return inside
    
    
    def map_graph_2(self):
        # Create Shapely polygon from red_tiles for fast geometric operations
        polygon_coords = [(p.x, p.y) for p in self.red_tiles]
        polygon = Polygon(polygon_coords)
        # Prepared geometry for optimized repeated operations
        prepared_polygon = prep(polygon)
        
        print(f'Created Shapely polygon with {len(self.red_tiles)} vertices')
        print(f'Polygon area: {polygon.area}')
        
        # Now find rectangles - use Shapely's optimized containment checks
        print(f'Checking {len(self.red_tiles) * (len(self.red_tiles) - 1) // 2} rectangle combinations...')
        checked = 0
        
        for tile1, tile2 in combinations(self.red_tiles, 2):
            checked += 1
            if checked % 1000 == 0:
                print(f'Checked {checked} rectangles, found {self.graph.number_of_edges()} valid')
            
            left = min(tile1.x, tile2.x)
            right = max(tile1.x, tile2.x)
            top = min(tile1.y, tile2.y)
            bottom = max(tile1.y, tile2.y)
            
            # Create rectangle using Shapely
            rect = box(left, top, right, bottom)
            
            # Check if rectangle is completely within the polygon
            # This is MUCH faster than checking individual points
            if prepared_polygon.contains(rect):
                width = right - left + 1
                height = bottom - top + 1
                area = width * height
                self.graph.add_edge(tile1, tile2, weight=area)

    def get_largest_rectangle(self):
        edges = self.graph.edges(data=True)
        sorted_edges = sorted(edges, key=lambda x: x[2]['weight'], reverse=True)
        largest_rectangle = sorted_edges[0]
        return largest_rectangle

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)