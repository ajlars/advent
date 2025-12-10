from helpers import Grid, Point
import networkx as nx
day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
# input_2 = f2.read().splitlines()
input_2 = input_1
test_1 = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".splitlines()
# test_2 = """""".splitlines()
test_2 = test_1

def solution_1(input):
    manifold_grid = manifold(input)
    manifold_grid.split_tachyons()
    print(manifold_grid)
    print(f'Solution 1: Tachyon Splits = {manifold_grid.split_count}')

def solution_2(input):
    manifold_grid = manifold(input)
    # manifold_grid.split_timelines()
    print(f'Solution 2: Timelines = {manifold_grid.count_timelines()}')

class manifold(Grid):
    def __init__(self, grid_lines: list[str]) -> None:
        super().__init__(grid_lines)
        self.start_point = self.find_value('S')
        self.split_points = self.find_all_values('^')
        self.split_count = 0
        self.timelines = []
    def split_tachyons(self):
        return self.split_timelines(False)
        self._reset()
        reached_end = False
        check_points = set([self.start_point + Point(0, 1)])
        current_row = self.start_point.y + 1
        while not reached_end:
            next_row = current_row + 1
            if next_row >= self._height or len(check_points) == 0:
                reached_end = True
                break
            next_check_points = set()
            for check_point in check_points:
                value = self.value_at_point(check_point)
                if value == '.':
                    next_check_points.add(check_point + Point(0, 1))
                    self.set_value_at_point(check_point, '|')
                    next_check_points.add(check_point + Point(0, 1))
                elif value == '^':
                    self.set_value_at_point(check_point + Point(1, 0), '|')
                    self.set_value_at_point(check_point - Point(1, 0), '|')
                    next_check_points.add(check_point + Point(-1, 1))
                    next_check_points.add(check_point + Point(1, 1))
                    self.split_count += 1
            check_points = next_check_points
            current_row += 1
        return
    def split_timelines(self, get_timelines = True):
        self._reset()
        reached_end = False
        check_point = self.start_point + Point(0, 1)
        check_points = set([self.start_point + Point(0, 1)])
        current_row = self.start_point.y + 1
        timelines: list[str] = [str(self.start_point)]
        while not reached_end:
            print(current_row)
            next_row = current_row + 1
            if next_row >= self._height or len(check_points) == 0:
                reached_end = True
                break
            next_check_points = []
            updated_timelines: list[str] = []
            for check_point in check_points:
                prev_point = check_point - Point(0, 1)
                value = self.value_at_point(check_point)
                if value == '.':
                    next_check_points.append(check_point + Point(0, 1))
                    # self.set_value_at_point(check_point, '|')
                    if get_timelines:
                        for timeline in timelines:
                            if(timeline.endswith(str(prev_point))):
                                timelines.remove(timeline)
                                new_timeline = timeline + str(check_point)
                                updated_timelines.append(new_timeline)
                    next_check_points.append(check_point + Point(0, 1))
                elif value == '^':
                    point_left = check_point + Point(-1, 0)
                    point_right = check_point + Point(1, 0)
                    # self.set_value_at_point(point_right, '|')
                    # self.set_value_at_point(point_left, '|')
                    next_check_points.append(check_point + Point(-1, 1))
                    next_check_points.append(check_point + Point(1, 1))
                    self.split_count += 1
                    if(get_timelines):
                        for timeline in timelines:
                            if(timeline.endswith(str(prev_point))):
                                timelines.remove(timeline)
                                new_timeline_left = timeline + str(point_left)
                                updated_timelines.append(new_timeline_left)
                                new_timeline_right = timeline + str(point_right)
                                updated_timelines.append(new_timeline_right)
            check_points = next_check_points
            timelines = updated_timelines
            current_row += 1
        self.timelines = list(timelines)
        return

    def node_graph(self):
        self._graph= nx.DiGraph()
        self._end_nodes = set()
        def next_split(point: Point):
            for y in range(point.y+1, self._height):
                current_point = Point(point.x, y)
                value = self.value_at_point(current_point)
                if value == '^':
                    return current_point
            # if no split found, add end point at the bottom of the grid
            end_point = Point(point.x, self._height-1)
            self._end_nodes.add(str(end_point))
            self._graph.add_node(str(end_point))
            return end_point

        self._graph.add_node(str(self.start_point))
        for point in self.split_points:
            self._graph.add_node(str(point))

        first_split = next_split(self.start_point)
        self._graph.add_edge(str(self.start_point), str(first_split))
        print(f'starting edge: {str(self.start_point), str(first_split)}')
        for i in range(len(self.split_points)):
            print(f'processing split {i+1} of {len(self.split_points)}')
            point = self.split_points[i]
            split_left = next_split(point - Point(1, 0))
            split_right = next_split(point + Point(1, 0))
            if split_left:
                self._graph.add_edge(str(point), str(split_left))
            if split_right:
                self._graph.add_edge(str(point), str(split_right))

    def count_timelines(self):
        self.node_graph()
        start_node = str(self.start_point)
        print('Counting timelines...')
        print(f'nodes: {len(self._graph.nodes)}, points: {len(self.split_points)}, ends: {len(self._end_nodes)}, width: {self._width}')
        
        # Check for cycles
        if not nx.is_directed_acyclic_graph(self._graph):
            print("WARNING: Graph has cycles!")
            cycles = list(nx.simple_cycles(self._graph))
            print(f"Found {len(cycles)} cycles")
            for cycle in cycles[:5]:  # Print first 5 cycles
                print(f"  Cycle: {cycle}")
        
        # Use dynamic programming to count paths
        from collections import defaultdict
        path_count = defaultdict(int)
        path_count[start_node] = 1
        
        # Process nodes in topological order
        for node in nx.topological_sort(self._graph):
            if node in path_count:
                for successor in self._graph.successors(node):
                    path_count[successor] += path_count[node]
        
        # Sum counts for all end nodes
        total = sum(path_count[node] for node in self._end_nodes)
        return total

    def get_timelines(self):
        return self.timelines

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)