import scipy.optimize as scipi
from typing import NamedTuple
day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
# input_2 = f2.read().splitlines()
input_2 = input_1
test_1 = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".splitlines()
# test_2 = """""".splitlines()
test_2 = test_1



def solution_1(input):
    presser = ButtonPresser(input)
    solutions = presser.solve_lights()
    print(f'Solution 1: Total button presses needed = {sum(solutions)}')

def solution_2(input):
    presser = ButtonPresser(input)
    solutions = presser.solve_joltages()
    
    # Detailed debugging
    print(f'\nDEBUG: Solutions details:')
    print(f'  Total machines: {len(solutions)}')
    print(f'  Min solution: {min(solutions) if solutions else "N/A"}')
    print(f'  Max solution: {max(solutions) if solutions else "N/A"}')
    print(f'  First 10: {solutions[:10]}')
    print(f'  Last 10: {solutions[-10:]}')
    
    total = sum(solutions)
    print(f'\nSolution 2: Total button presses needed = {total}')
    # print("Solution 2 not yet implemented")

class Doc(NamedTuple):
    target: int
    buttons: list[list[int]]
    joltage: list[int]

    def __str__(self) -> str:
        return f'Target: {self.target}, Buttons: {self.buttons}, Joltage: {self.joltage}'

class ButtonPresser():
    def __init__(self, docs: list[str]) -> None:
        self.docs = self.parse_docs(docs)

    def parse_docs(self, docs: list[str]) -> list[Doc]:
        parsed_docs = []
        for line in docs:
            split = line.split(' ')
            _target = split[0][1:-1]
            target = 0
            for i, light in enumerate(_target):
                if light == '#':
                    target |= (1 << i)
            buttons = [[int(x) for x in b[1:-1].split(',')] for b in split[1:-1]]
            joltages = [int(x) for x in split[-1][1:-1].split(',')]
            parsed_docs.append(Doc(target, buttons, joltages))
        return parsed_docs
    
    def solve_lights(self):
        results = []
        for doc in self.docs:
            result = self.solve_lights_for_doc(doc.target, doc.buttons)
            results.append(result)
        self.light_results = results
        return results
    
    def solve_joltages(self):
        results = []
        for i in range(len(self.docs)):
            print(f'Solving joltage doc {i+1} of {len(self.docs)}')
            doc = self.docs[i]
            # result = self.solve_joltages_for_doc(doc.buttons, doc.joltage)
            result = self.opt_solution_2(doc.joltage, doc.buttons)
            results.append(result)
        self.joltage_results = results
        return results
    

    def solve_lights_for_doc(self, target:int, buttons: list[list[int]]) -> int:
        initial_state = 0

        if initial_state == target:
            return 0  # No presses needed
        
        # queue the states to explore
        queue = [(initial_state, 0)]
        # track visited states
        visited = {initial_state}

        # process the queue until we've found the target state or seen all possible states
        while queue:
            current_state, presses = queue.pop(0)

            for button in buttons:
                new_state = current_state
                for light_index in button:
                    new_state ^= (1 << light_index)

                if new_state == target:
                    return presses + 1

                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, presses + 1))

        return -1  # If not found
    
    def solve_joltages_for_doc(self, buttons: list[list[int]], joltage: list[int]) -> int:
        initial_state = []
        for i in range(len(joltage)):
            initial_state.append(0)

        if initial_state == joltage:
            return 0
        
        queue = [(initial_state, 0)]
        visited = {tuple(initial_state)}

        while queue:
            current_state, presses = queue.pop(0)

            for button in buttons:
                new_state = current_state.copy()
                for index in button:
                    new_state[index] += 1

                if new_state == joltage:
                    return presses + 1
                
                cleaned = tuple(new_state)
                if cleaned not in visited:
                    visited.add(cleaned)
                    queue.append((new_state, presses + 1))

        return -1
    
    def opt_solution_2(self, joltages: list[int], buttons_positions_list: list[list[int]]):
        constraint_matrix = []
        for target_index in range(len(joltages)):
            row = []
            for button_positions in buttons_positions_list:
                row.append(1 if target_index in button_positions else 0)
            constraint_matrix.append(row)

        optimization_result = scipi.linprog(
            [1] * len(buttons_positions_list),
            A_eq=constraint_matrix, 
            b_eq=joltages,
            bounds=(0, None),
            method='highs',
            integrality = 1            )

        if optimization_result.success:
            result = optimization_result.fun
            # Check for rounding issues - int() truncates, causing errors!
            int_val = int(result)
            round_val = round(result)
            if int_val != round_val:
                print(f"ROUNDING DIFF: {result} -> int={int_val}, round={round_val}")
            return round_val
        else:
            print(f"ERROR: Optimization failed!")
            print(f"  Status: {optimization_result.status}")
            print(f"  Message: {optimization_result.message}")
            print(f"  Joltages: {joltages}")
            print(f"  Buttons: {buttons_positions_list}")
            return 0  # Return 0 for failed cases
        

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)
