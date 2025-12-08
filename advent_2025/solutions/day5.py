import numpy as np

day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
# input_2 = f2.read().splitlines()
input_2 = input_1
test_1 = """3-5
10-14
16-20
12-18

1
5
8
11
17
32""".splitlines()
# test_2 = """""".splitlines()
test_2 = test_1

def solution_1(input):
    ingredients = Ingredients(input)
    print(f'{ingredients.check_ingredients()} fresh ingredients by id')

def solution_2(input):
    ingredients = Ingredients(input)
    print(f'{ingredients.get_fresh_id_count()} total fresh ingredient ids possible')

class Ingredients():
    def __init__(self, lists: list[str]) -> None:
        self.id_ranges = []
        self.ingredient_ids = []
        self.fresh_ingredients = set()
        self.rotten_ingredients = set()
        self.fresh_ids = set()
        parsing_ranges = True
        for line in lists:
            if line == "":
                parsing_ranges = False
                continue
            if parsing_ranges:
                parts = line.split("-")
                self.id_ranges.append((int(parts[0]), int(parts[1])))
            else:
                self.ingredient_ids.append(int(line))

    def check_fresh(self, value: int) -> bool:
        for r in self.id_ranges:
            if r[0] <= value <= r[1]:
                return True
        return False

    def check_ingredients(self) -> int:
        self.fresh_ingredients = set()
        self.rotten_ids = set()
        for v in self.ingredient_ids:
            if self.check_fresh(v):
                self.fresh_ingredients.add(v)
            else:
                self.rotten_ids.add(v)
        return len(self.fresh_ingredients)

    def get_fresh_id_count(self) -> set:
        sorted_ranges = sorted(self.id_ranges, key=lambda x: x[0])
        print(len(sorted_ranges))
        merged_ranges = [sorted_ranges[0]]
        for current in sorted_ranges[1:]:
            last = merged_ranges[-1]
            if current[0] <= last[1] + 1:
                merged_ranges[-1] = (last[0], max(last[1], current[1]))
            else:
                merged_ranges.append(current)
        print(len(merged_ranges))
        count = sum(end-start+1 for start, end in merged_ranges)
        print(f'count: {count}')
        return count

    def __str__(self) -> str:
        return f'Ranges: \n\t{'\n\t'.join([f'{r[0]}-{r[1]}' for r in self.id_ranges])}\nValues: \n\t{', '.join([str(v) for v in self.ingredient_ids])}'

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)