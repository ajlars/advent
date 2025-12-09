day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
# input_2 = f2.read().splitlines()
input_2 = input_1
test_1 = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """.splitlines()
# test_2 = """""".splitlines()
test_2 = test_1

def solution_1(input):
    homework = math_homework(input)
    homework.solve_problems()
    print(f'Solution 1: Problem Solutions = {homework.sum_solutions()}')

def solution_2(input):
    homework = math_homework(input, rev=True)
    homework.solve_problems()
    print(f'Solution 2: Problem Solutions = {homework.sum_solutions()}')

class math_homework():
    def __init__(self, problems: list[str], rev = False) -> None:
        if rev:
            self.problems = self.parse_cephalopod_math(problems)
            print(self.problems)
        else:
            self.problems = self.parse_problems(problems)
        self.solutions = []

    def parse_cephalopod_math(self, _problems: list[str]) -> list:
        problems = []
        values = []
        num_string = ''
        operator = ''
        for i in range(len(_problems[0])):
            col = []
            for line in _problems:
                col.append(line[::-1][i])
            num_string = ''.join(filter(lambda x: x.isdigit(), col))
            if col[-1] in ['+', '*']:
                operator = col[-1]
            if len(num_string) > 0:
                values.append(int(num_string))
            if len(num_string) == 0 or i == len(_problems[0]) -1:
                problems.append((values, operator))
                values = []
                operator = ''
            print(f'{i}: {"".join(col)}')
        return problems

    def parse_problems(self, _problems: list[str]) -> list:
        problems = []
        for line in [prob.strip() for prob in _problems]:
            chunks = line.split(" ")
            to_add = []
            for chunk in chunks:
                if chunk != "":
                    to_add.append(int(chunk) if chunk.isdigit() else chunk)
            for i in range(len(to_add)):
                if i >= len(problems):
                    problems.append([[], ''])
                if isinstance(to_add[i], int):
                    problems[i][0].append(to_add[i])
                else:
                    problems[i][1] = to_add[i]
        return problems

    def solve_problems(self) -> list:
        solutions = []
        for problem in self.problems:
            if problem[1] == '+':
                solutions.append(sum(problem[0]))
            elif problem[1] == '*':
                result = 1
                for num in problem[0]:
                    result *= num
                solutions.append(result)
        self.solutions = solutions
        return solutions

    def sum_solutions(self) -> int:
        if(self.solutions == []):
            self.solve_problems()
        return sum(self.solutions)

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)