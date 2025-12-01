f = open('adventInputs/day7.txt', 'r')

mini = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".splitlines()

big = f.read().splitlines()

def main():
    total = 0
    for line in big:
        total += calculator(line)
    print(total)

def calculator(line):
    [_solution, problem] = line.split(':')
    solution = int(_solution)
    numbers = []
    for num in problem.split():
        numbers.append(int(num))
    print(f'solution: {solution}, numbers: {numbers}')
    solutions = [numbers[0]]
    for number in numbers[1:]:
        _solutions = []
        for _solution in solutions:
            _solutions.append(_solution + number)
            _solutions.append(_solution * number)
            _solutions.append(int(f'{_solution}{number}'))
        solutions = _solutions
    if solution in solutions:
        return solution
    return 0

if __name__ == "__main__":
    main()