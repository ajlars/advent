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
test_results = 0


def main():
    print('Running Tests...')
    passed = True
    computer = ChronoComputer(*(Register(0, 0, 9), [int(x) for x in "2,6".split(',')]))
    computer.run()
    if computer.register.B != 1:
        print('A: If register C contains 9, the program 2,6 would set register B to 1.')
        print(f'\tPass: {computer.register.B == 1} (Register: {computer.register})\n')
        passed=False
    computer = ChronoComputer(*(Register(10, 0, 0), [int(x) for x in "5,0,5,1,5,4".split(',')]))
    computer.run()
    if computer.output!="0,1,2":
        print('B: If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.')
        print(f'\tPass: {computer.output == "0,1,2"} (output: ${computer.output})\n')
        passed=False
    computer = ChronoComputer(*(Register(2024, 0, 0), [int(x) for x in "0,1,5,4,3,0".split(',')]))
    computer.run()
    if computer.output != "4,2,5,6,7,7,7,7,3,1,0":
        print('C: If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.')
        print(f'\tPass: {computer.output == "4,2,5,6,7,7,7,7,3,1,0"} (output: ${computer.output})\n')
        passed=False
    computer = ChronoComputer(*(Register(0, 29, 0), [int(x) for x in "1,7".split(',')]))
    computer.run()
    if computer.register.B != 26:
        print('D: If register B contains 29, the program 1,7 would set register B to 26')
        print(f'\tPass: {computer.register.B == 26} (Register: {computer.register})\n')
        passed=False
    computer = ChronoComputer(*(Register(0, 2024, 43690), [int(x) for x in "4,0".split(',')]))
    computer.run()
    if computer.register.B != 44354:
        print('E: If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.')
        print(f'\tPass: {computer.register.B == 44354} (Register: {computer.register})\n')
        passed=False
    computer = ChronoComputer(*(Register(117440, 0, 0), [int(x) for x in "0,3,5,4,3,0".split(',')]))
    computer.run()
    if computer.output != "0,3,5,4,3,0":
        print('Part 2: With Register A: 117440, B: 0, C: 0, program: "0,3,5,4,3,0", this program should output an exact match of the original program.')
        print(f'\tPass: {computer.output == "0,3,5,4,3,0"} (output: {computer.output})\n')
        print('\n'.join(computer._logs))
        passed=False

    if passed:
        print('All tests passed!\n')
    else:
        return
    
    register, instructions = (Register(23999685, 0, 0), [int(x) for x in "2,4,1,1,7,5,1,5,0,3,4,4,5,5,3,0".split(',')])
    if level == 'one':
        results = solver_one(register, instructions)
        if test:
            print('Tests passed!' if results == test_results else f'Tests failed... (Results: {results})')
        else:
            print(f'Results: {results}')
    elif level == 'two':
        results = solver_two(register, instructions)
        if test:
            print('Tests passed!' if results == test_results else f'Tests failed... (Results: {results})')
        else:
            print(f'Results: {results}')
    print(f'\nDuration: {datetime.now() - start}')

def solver_one(register, instructions):
    print(f'\nAdvent of Code Day: {day} - Solution One{' - Test' if test else ''}')
    computer = ChronoComputer(register, instructions)
    computer.run()
    return computer.output

def solver_two(register, instructions):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    potentials = [0]
    calculated = []
    for val in reversed(instructions):
        print(f'potentials: {potentials}')
        next_vals = []
        # print('val', val)
        calculated.insert(0, val)
        for potential in potentials:
            for i in range(8):
                shifted = potential << 3
                a = shifted + i
                computer = ChronoComputer(Register(a, register.B, register.C), instructions)
                computer.run()
                # print(f'\ti: {i}, out: {computer.output}, expected: {",".join(f"{x}" for x in calculated)}')
                if computer.output == ','.join(f'{x}' for x in calculated):
                    next_vals.append(a)
                    # print('match')
        
        potentials = next_vals

    
    potentials.sort()
    for i, potential in enumerate(potentials):
        computer = ChronoComputer(Register(potential, register.B, register.C), instructions)
        computer.run()
        print(f'potential {i+1},\ta: {potential}, output: {computer.output}')

    # i = 1
    # length = 1
    # 4,5,6,7,1,4,0,4,5,6,7,3,0,4,5,7,5,3,4,0,4
    # while results != expected and len(results) <= len(expected) and i < 100:
    #     computer = ChronoComputer(Register(a, register.B, register.C), instructions)
    #     computer.run()
    #     results = computer.output
    #     # print(f'Iteration: {i}\n\tRegister: {computer.register}\n\tOutput:\t\t{results}\n\tExpected:\t\t{expected}\n')
    #     # print(f'input:{a}, results:{results}')
    #     # if i % 100000 == 0:
    #     #     print(f'Iterated... {a}\t{results}')
    #     print(f'Iterated... {a}\t{results}')
    #     # if len(results) > length:
    #     #     length = len(results)
    #     #     print(f'Iteration: {i} - Added an output\n\tRegister: {computer.register}\n\tOutput:\t\t{results}\n\tExpected:\t{expected}\n')
    #     a += 1
    #     i += 1
    # return a, results
    # power = 12
    # a = 8**15
    # i = 1
    # entries = [a, a+8, a + 8**2, a + 8**3, a + 8**4, a + 8**5, a + 8**6, a + 8**7, a + 8**8, a + 8**9, a + 8**10, a + 8**11, a + 8**12, a + 8**13, a + 8**14, a + 8**15, 8**16]
    # for a in entries:
    #     computer = ChronoComputer(Register(int(a), register.B, register.C), instructions)
    #     computer.run()
    #     results = computer.output
    #     print(a, results)
    # print(places, expected[places:], len(results), len(expected))
    # while results != expected and i < 10:
        # computer = ChronoComputer(Register(int(a), register.B, register.C), instructions)
        # computer.run()
        # results = computer.output
    #     print(f'Iteration {i} - length: {len(results)},  a: {a}, results: {results}')
    #     m = 1
    #     while a & m:
    #         a ^= m
    #         m <<= 1
    #     a ^= m
    #     i += 1
    # return a, results

Register = namedtuple('Register', ['A', 'B', 'C'])

class ChronoComputer:
    def __init__(self, register:Register, instructions:list[int]):
        self._register = register
        self._pointer = 0
        self.start = datetime.now()
        self._output = []
        self._instructions = instructions
        # print (self._register, self._instructions)
        self._logs = []

    @property
    def register(self):
        return self._register

    def run(self):
        i = 0
        while self._pointer < len(self._instructions):
        # while self._pointer < len(self._instructions) and i < 10:
            # i+=1
            opcode = self._instructions[self._pointer]
            operand = self._instructions[self._pointer + 1]
            self.eval_opcode(opcode, operand)
        # print(f'Output: {self.output}')
        # print(f'Duration: {datetime.now() - self.start}')

    @property
    def output(self):
        return ','.join(f'{x}' for x in self._output)

    def get_combo_operand(self, operand):
        if operand <= 3:
            return operand
        if operand == 4:
            return self._register.A
        if operand == 5:
            return self._register.B
        if operand == 6:
            return self._register.C
        if operand == 7:
            raise ValueError('Invalid operand')
        
    def eval_opcode(self, opcode, operand):
        new_register = None
        result = None
        pointer_skipped = False
        combo = None
        operation = None
        try:
            # adv
            if opcode == 0:
                combo = self.get_combo_operand(operand)
                operation = f'\tadv, {self._register.A}, {2 ** combo} (2**{combo})'
                result = int(self._register.A / (2 ** combo))
                new_register = Register(result, self._register.B, self._register.C)
            # bxl
            elif opcode == 1:
                # print('bxl')
                operation = f'\tbx1, {self._register.B} ^ {operand}'
                result = self._register.B ^ operand
                new_register = Register(self._register.A, result, self._register.C)
            # bst
            elif opcode == 2:
                # print('bst')
                combo = self.get_combo_operand(operand)
                operation = f'\tbst, {combo} % {self._register.B}'
                result = combo % 8
                new_register = Register(self._register.A, result, self._register.C)
            # jnz
            elif opcode == 3:
                # print('jnz')
                operation = f'\tjnz, {self._register.A} != 0 ? pointer = {operand}, skipping pointer increment'
                if self._register.A != 0:
                    self._pointer = operand
                    pointer_skipped = True
            # bxc
            elif opcode == 4:
                # print('bxc')
                operation = f'\tbxc, {self._register.B} ^ {self._register.C}'
                result = self._register.B ^ self._register.C
                new_register = Register(self._register.A, result, self._register.C)
            # out
            elif opcode == 5:
                # print('out')
                combo = self.get_combo_operand(operand)
                operation = f'\tout, {combo} % {self._register.B}, appending to output'
                result = combo % 8
                self._output.append(result)
            # bdv
            elif opcode == 6:
                # print('bdv')
                combo = self.get_combo_operand(operand)
                operation = f'\tbdv, {self._register.A} / {2 ** combo}'
                result = int(self._register.A / (2 ** combo))
                new_register = Register(self._register.A, result, self._register.C)
            # cdv
            elif opcode == 7:
                # print('cdv')
                combo = self.get_combo_operand(operand)
                operation = f'\tcdv, {self._register.A} / {2 ** combo}'
                result = int(self._register.A / (2 **combo))
                new_register = Register(self._register.A, self._register.B, result)
            self._logs.append(f'Iteration: {len(self._logs)+1}\n\t{operation}\n\tOpcode: {opcode} at Pointer: {self._pointer}\n\tOperand: {operand}\n\tCombo: {combo}\n\tRegister: {self._register})\n\tNew Register: {new_register}\n\tResult: {result}\n\tOutput: {self._output}\n\tPointer Skipped: {pointer_skipped}\n')
        except:
            # print(f'Error: {opcode}, {operand}, {combo}, {self._register}')
            print('\n'.join(self._logs))
            print(f'Breaking Iteration:\n\t\n\tOpcode: {opcode} at Pointer: {self._pointer}\n\t{operation}\n\tOperand: {operand}\n\tCombo: {combo}\n\tRegister: {self._register})\n\tNew Register: {new_register}\n\tResult: {result}\n\tOutput: {self._output}\n\tPointer Skipped: {pointer_skipped}\n')
            raise
        if new_register:
            self._register = new_register
        if not pointer_skipped:
            self._pointer += 2
if __name__ == "__main__":
    main()