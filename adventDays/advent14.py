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

test_input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""".splitlines()

test_results = 12

class Robot:
    def __init__(self, starting_stats: str, room_width:int, room_height:int):
        self._room_width = room_width
        self._room_height = room_height
        _starting_stats = [x[1].split(',') for x in [x.split('=') for x in starting_stats.split(' ')]]
        # print(_starting_stats)
        self._location = Point(int(_starting_stats[0][0]), int(_starting_stats[0][1]))
        self._velocity = Point(int(_starting_stats[1][0]), int(_starting_stats[1][1]))

    def move(self):
        self._location += self._velocity
        x_adjust = self._room_width if self._location.x < 0 else -1 * self._room_width if self._location.x >= self._room_width else 0
        y_adjust = self._room_height if self._location.y < 0 else -1 * self._room_height if self._location.y >= self._room_height else 0
        # if x_adjust or y_adjust:
            # print(f'\tAdjusting: {x_adjust}, {y_adjust} for {self._location}')
        self._location += Point(x_adjust, y_adjust)
        # print(self)

    def get_quadrant(self):
        mid_x = int(self._room_width/2)
        mid_y = int(self._room_height/2)
        # print(f'Mid: {mid_x}, {mid_y}')
        if self.location.x == mid_x or self.location.y == mid_y:
            return -1
        elif self.location.x < mid_x:
             if self.location.y < mid_y:
                 return 0
             else:
                return 2
        else:
            if self.location.y < mid_y:
                return 1
            else:
                return 3

    @property
    def location(self):
        return self._location
    
    @property
    def velocity(self):
        return self._velocity
    
    def __str__(self):
        return f'Location: {self._location} Velocity: {self._velocity}'
    
class RobotList:
    def __init__(self, inputs: list, width:int, height:int):
        robots = []
        self._room_width = width
        self._room_height = height
        for input in inputs:
            robots.append(Robot(input, width, height))
        self._robots = robots
    
    def move(self):
        for robot in self._robots:
            robot.move()
    
    def get_quadrants(self):
        quadrants = [0, 0, 0, 0]
        for robot in self._robots:
            quadrant = robot.get_quadrant()
            # print(f'Robot: {robot} Quadrant: {quadrant}')
            if quadrant > -1:
                quadrants[quadrant] += 1
        print('Per Quadrant:\n', quadrants)
        return quadrants

    def get_safety_factor(self):
        quadrants = self.get_quadrants()
        return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
    
    def check_for_easter_egg(self):
        locations = set()
        for robot in self._robots:
            if robot.location in locations:
                return False
            locations.add(robot.location)
        return True
        # robot_at_center_top = False
        # robot_at_center_bottom = False
        # for robot in self._robots:
        #     if robot.location == Point(int(self._room_width/2),0):
        #         robot_at_center_top = True
        #     elif robot.location == Point(int(self._room_width/2),self._room_height-1):
        #         robot_at_center_bottom = True
        # return robot_at_center_top and robot_at_center_bottom

    def __str__(self):
        grid = []
        for y in range(self._room_height):
            row = []
            for x in range(self._room_width):
                robots = 0
                for robot in self._robots:
                    if robot.location == Point(x, y):
                        robots += 1
                row.append('.' if robots == 0 else robots)
            grid.append(''.join([str(x) for x in row]))
        return f'{len(self._robots)} Robots:\n{'\n'.join(grid)}'

def main():
    inputs = test_input if test else puzzle_input
    if test:
        robots = RobotList(inputs, 11, 7)
    else:
        robots = RobotList(inputs, 101, 103)

    if level == 'one':
        results = solver_one(robots)
        if test:
            print('Tests passed!' if results == test_results else f'Tests failed...{results}')
        else:
            print(f'Results: {results}')
    elif level == 'two':
        results = solver_two(robots)
        if test:
            print('Tests passed!' if results == test_results else f'Tests failed...{results}')
        else:
            print(f'Results: {results}')
    print(f'\nDuration: {datetime.now() - start}')

def solver_one(robots):
    print(f'\nAdvent of Code Day: {day} - Solution One{' - Test' if test else ''}')
    for i in range(100):
        robots.move()

    print(robots)
    return robots.get_safety_factor()

def solver_two(robots):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    for i in range(10000):
        robots.move()
        if(robots.check_for_easter_egg()):
            print(f'i: {i}\n{robots}\n\n')
            return i
        # print(f'\n\n{i}\n{robots}')
    return None

if __name__ == "__main__":
    main()