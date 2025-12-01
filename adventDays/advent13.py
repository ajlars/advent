from datetime import datetime
import uuid
from adventDays.helpers import execute, Point, Grid
import re
import sys
from operator import attrgetter
from collections import namedtuple
from sympy import symbols, solve, Eq

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

test_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""".splitlines()

test_results = 480

def main():
    items = test_input if test else puzzle_input
    machines = []
    i= 0
    while(len(items) > 0):
        machines.append(claw_machine(items[:3]))
        items = items[4:]

    if level == 'one':
        results = solver_one(machines)
        if test:
            print('Tests passed!' if results == test_results else f'Tests failed... results: {results}, test_results: {test_results}')
        else:
            print(f'Results: {results}')
    elif level == 'two':
        results = solver_two(machines)
        if test:
            print('Tests passed!' if results == test_results else f'Tests failed... results: {results}, test_results: {test_results}')
        else:
            print(f'Results: {results}')
    print(f'\nDuration: {datetime.now() - start}')

def solver_one(input):
    print(f'\nAdvent of Code Day: {day} - Solution One{' - Test' if test else ''}')
    total_cost = 0
    for machine in input:
        machine.calculate_presses()
        total_cost += machine.cost

    return total_cost

def solver_two(input):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    pass

class claw_machine:
    BUTTON_A_COST = 3
    BUTTON_B_COST = 1
    def __init__(self, input: list[str]):
        self.input = input
        a_x = int(re.search(r"(?<=X\+)\d+", input[0]).group())
        a_y = int(re.search(r"(?<=Y\+)\d+", input[0]).group())
        b_x = int(re.search(r"(?<=X\+)\d+", input[1]).group())
        b_y = int(re.search(r"(?<=Y\+)\d+", input[1]).group())
        prize_x = 10000000000000 + int(re.search(r"(?<=X\=)\d+", input[2]).group())
        prize_y = 10000000000000 + int(re.search(r"(?<=Y\=)\d+", input[2]).group())

        self._a_presses = 0
        self._b_presses = 0
        self._cost = 0

        self.button_a_distance = Point(a_x, a_y)

        self.button_b_distance = Point(b_x, b_y)

        self.prize_location = Point(prize_x, prize_y)

        # print(f'Configured machine\n\tButton A: {self.button_a_distance}\n\tButton B: {self.button_b_distance}\n\tPrize: {self.prize_location}')    

    def calculate_presses(self):
        a, b = symbols('a b')
        # print(f'Calculating presses for {self.button_a_distance} and {self.button_b_distance}, prize at {self.prize_location}')
        # eq1 = Eq(a*self.button_a_distance.x + b*self.button_a_distance.x, self.prize_location.x)
        # eq2 = Eq(a*self.button_a_distance.y + b*self.button_a_distance.y, self.prize_location.y)
        # print(isinstance(self.button_a_distance.x, int))

        eq1 = Eq(a*self.button_a_distance.x + b*self.button_b_distance.x, self.prize_location.x)
        eq2 = Eq(a*self.button_a_distance.y + b*self.button_b_distance.y, self.prize_location.y)

        solution = solve((eq1, eq2), (a, b), cubics=False)
        # print(solution)
        # print(int(solution[a]))
        a_is_int = not '/' in f'{solution[a]}'
        b_is_int = not '/' in f'{solution[b]}'

        if(len(solution) == 0 or not (a_is_int and b_is_int)):
            return
        self._a_presses = int(solution[a])
        self._b_presses = int(solution[b])
        self._cost = int(solution[a]) * self.BUTTON_A_COST + int(solution[b]) * self.BUTTON_B_COST
    
    @property
    def cost(self):
        return self._cost

    def get_costs(self):
        return self.calculate_presses()
            
    
if __name__ == "__main__":
    main()