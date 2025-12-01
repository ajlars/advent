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

test_input = """0
1
2
3
4""".splitlines()

test_results = 10

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
    input = [int(x) for x in input]
    return None

def solver_two(input):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    pass

if __name__ == "__main__":
    main()