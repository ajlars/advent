from datetime import datetime
import time
from adventDays.helpers import Grid, execute
import re
import sys

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
puzzle_input = f.read().split(' ')

test_input = '125 17'.split(' ')

# test_results = ['253000 1 7', '253 0 2024 14168', '512072 1 20 24 28676032', '512 72 2024 2 0 2 4 2867 6032', '1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32', '2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2']
stone_map = {}

class Stones(list[int]):
    def __init__(self, stones: list[int]):
        super().__init__(stones)
        self._stone_map = {}
        for stone in stones:
            self._stone_map[stone] = 1
        print(f'initial stone_map: {self._stone_map}')
        for stone in self._stone_map:
            print(stone)
        self._blink_count = 0
        
    def get_count(self):
        count = 0
        for stone in self._stone_map:
            count += self._stone_map[stone]
        return count
    
    def get_stones(self):
        return self._stone_map

    def blink(self):
        stones = {}
        to_split = {}
        to_multiply = {}

        for stone in self._stone_map:
            if stone == 0:
                stones[1] = self._stone_map[stone]
            elif len(str(stone))%2 == 0:
                to_split[stone] = self._stone_map[stone]
            else:
                to_multiply[stone] = self._stone_map[stone]
        
        for stone in to_split:
            mid = len(str(stone))//2
            a = int(str(stone)[:mid])
            b = int(str(stone)[mid:])
            if a in stones: stones[a] += to_split[stone]
            else: stones[a] = self._stone_map[stone]
            if b in stones: stones[b] += to_split[stone]
            else: stones[b] = to_split[stone]
            
        for stone in to_multiply:
            _stone = stone * 2024
            if _stone in stones: stones[_stone] += to_multiply[stone]
            else: stones[_stone] = to_multiply[stone]
        self._stone_map = stones

def main():
    print(level)
    items = test_input if test else puzzle_input
    for i, item in enumerate(items):
        items[i] = int(item)
    if level == 'one':
        results = solver_one(items, 25)
        if test:
            print('Tests passed!' if results == 55312 else 'Tests failed...')
        else:
            print(f'Results: {results}')
    else:
        results = solver_two(items)
        if test:
            print('Tests passed!' if results == 0 else 'Tests failed...')
        else:
            print(f'Results: {results}')

def solver_one(input, blink_count):
    start = datetime.now()
    print(f'\nAdvent of Code Day: {day} - Solution One{' - Test' if test else ''}')
    stones = Stones(input)
    # results = []
    # stones.blink_to(blink_count)

    for i in range(blink_count):
        print(f'Calculating... blink {i+1}, {stones.get_count()} stones')
        stones.blink()
        # print(stones.get_stones())
    print(stones.get_count())
    # stones.handle_stack(25)
    print(f'Calculated in {datetime.now() - start}')

    return stones.get_count()

def solver_two(input):
    start = datetime.now()
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    stones = Stones(input)
    for i in range(75):
        # print(f'Calculating... blink {i+1}, {stones.get_count()} stones')
        stones.blink()
    print(stones.get_count())

    print(f'Calculated in {datetime.now() - start}')
    # return stones.get_count()

if __name__ == "__main__":
    main()