day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
input_2 = f2.read().splitlines()
test_1 = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""".splitlines()
test_2 = """""".splitlines()

def solution_1(input):
    print("Solution 1 not yet implemented")

def solution_2(input):
    print("Solution 2 not yet implemented")

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)