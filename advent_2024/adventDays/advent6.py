from datetime import datetime
from colorama import Fore
from tqdm import tqdm

from helpers import Point, Grid 

f = open('adventInputs/daySix.txt', 'r')
bigmap = f.read()

minimap = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

class GuardMap(Grid):
    SPACE = '.'
    OBSTACLE = '#'

    DIRECTIONS = "^>v<"
    DIRECTIONS_MAP = {
        '^': Point(0, -1),
        '>': Point(1, 0),
        'v': Point(0, 1),
        '<': Point(-1, 0),
    }

    def __init__(self, grid_array: list):
        super().__init__(grid_array)
        self._all_obstacles = set()
        self._update_all_obstacles()
        
        self._guard_location = self._locate_guard()
        self._start_location = self._guard_location

        self._guard_direction = self.value_at_point(self._guard_location)
        self._directions_idx = GuardMap.DIRECTIONS.index(self._guard_direction)
        self._start_direction_idx = self._directions_idx

        self._visited_with_direction = set()
        self._visited_map = {}
        self._visited: list[tuple[Point, str]] = []
        self._in_loop = False

        self._update_visited()

        self._pre_obstacle_added = None

    def reset(self):
        self._guard_location = self._start_location
        self._guard_direction = self.value_at_point(self._guard_location)
        self._directions_idx = self._start_direction_idx

        self._visited_with_direction = set()
        self._visited_map: dict[Point, str] = {}
        self._visited = []
        self._in_loop = False

        self._update_visited()
        self._clear_obstacle()

    def add_obstacle(self, location: Point):
        self._pre_obstacle_added = (location, self.value_at_point(location))
        self.set_value_at_point(location, GuardMap.OBSTACLE)

    def _clear_obstacle(self):
        if self._pre_obstacle_added:
            self.set_value_at_point(self._pre_obstacle_added[0], self._pre_obstacle_added[1])
    
    @property
    def in_loop(self)-> bool:
        return self._in_loop
    
    @property
    def visited(self):
        return self._visited_map
    
    @property
    def distinct_visited_count(self) -> int:
        return len(self._visited_map)
    
    def _update_visited(self):
        location_config = (self._guard_location, self._guard_direction)

        self._visited_map[self._guard_location] = self._guard_direction
        self._visited.append(location_config)

        if location_config in self._visited_with_direction:
            self._in_loop = True
        else:
            self._visited_with_direction.add(location_config)

    def _update_all_obstacles(self):
        self._all_obstacles = set()

        for point in self._all_points:
            if self.value_at_point(point) == GuardMap.OBSTACLE:
                self._all_obstacles.add(point)

    def move(self) -> bool:
        while True:
            # print(f'guard location: {self._guard_location}, direction: {self._guard_direction}, mod: {GuardMap.DIRECTIONS_MAP[self._guard_direction]}')
            next_point = self._guard_location + GuardMap.DIRECTIONS_MAP[self._guard_direction]

            if not self.valid_location(next_point):
                # print('invalid location', next_point)
                return False
            
            next_value = self.value_at_point(next_point)
            if(next_value == GuardMap.OBSTACLE):
                # print('obstacle at', next_point, 'turning')
                self._directions_idx = (self._directions_idx + 1) % len(GuardMap.DIRECTIONS)
                self._guard_direction = GuardMap.DIRECTIONS[self._directions_idx]
                continue
            else:
                # print('moved to', next_point)
                self._guard_location = next_point
                self._update_visited()
                break
        return True
    
    def _locate_guard(self) -> Point:
        for point in self._all_points:
            if self.value_at_point(point) in GuardMap.DIRECTIONS:
                return point
            
    def __str__(self) -> str:
        row_strs = []
        for y, row in enumerate(self._array):
            row_list = []
            for x, char in enumerate(row):
                locn = Point(x, y)
                if locn in self._visited_map.keys():
                    row_list.extend([Fore.YELLOW, self._visited_map[locn], Fore.RESET])
                else:
                    row_list.append(char)

            row_strs.append("".join(row_list))

        return "\n".join(row_strs)
    
def solve_part1(data):
    guard_map = GuardMap(data)
    # print('start\n', guard_map)
    while guard_map.move():
        # print('\n', guard_map)
        pass

    print(f"\n{guard_map}")
    return guard_map.distinct_visited_count

# sample_inputs = []
# sample_inputs.append(minimap)
# sample_answers = [41]

# for curr_input, curr_ans in zip(sample_inputs, sample_answers):
#     if solve_part1(curr_input.splitlines()) == curr_ans:
#         print("Pass")

# soln = solve_part1(bigmap.splitlines())
# print(f"Part 1 soln={soln}")

def solve_part2(data):
    guard_map = GuardMap(data)
    while guard_map.move():
        pass

    route = [locn for locn in guard_map.visited.keys()][1:]

    loop_locations = 0

    for location in tqdm(route):
        guard_map.reset()
        guard_map.add_obstacle(location)
        while guard_map.move():
            if guard_map.in_loop:
                loop_locations += 1
                break
    
    return loop_locations

sample_inputs = []
sample_inputs.append(minimap)
sample_answers = [6]

for curr_input, curr_ans in zip(sample_inputs, sample_answers):
    if solve_part2(curr_input.splitlines()) == curr_ans:
        print("Pass")

soln = solve_part2(bigmap.splitlines())
print(f"Part 2 soln={soln}")