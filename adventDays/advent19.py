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

test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""".splitlines()

test_results = 6

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
    sorter = TowelSorter(input)
    return sorter.get_counts()[0]

def solver_two(input):
    print(f'\nAdvent of Code Day: {day} - Solution Two{' - Test' if test else ''}')
    sorter = TowelSorter(input)
    return sorter.eval_patterns()
    pass

class TowelSorter:
    def __init__(self, input):
        self.input = input
        self._pattern_memory = {}
        self._towels = []
        self._patterns = []
        self._combinations = {}
        self._impossible = []
        self._longest = 0
        for line in input:
            if ',' in line:
                towels = line.split(', ')
                for i, towel in enumerate(towels):
                    self._longest = max(self._longest, len(towel))
                    self._towels.append(towel)
            elif len(line) > 0:
                self._patterns.append(line)
        # print(f'Available: {self._towels}')
        # print(f'Patterns:\n\t{"\n\t".join(self._patterns)}')
# 883443544805484

    def _get_pattern_count(self, pattern, r_count = 0):
        if len(pattern) == 0:
            # print(f'\t{'\t'*r_count}len 0')
            return 1
        if pattern in self._pattern_memory:
            # print(f'\t{'\t'*r_count} {pattern} len in memory {self._pattern_memory[pattern]}')
            return self._pattern_memory[pattern]
        count = 0
        i = 0
        # print(f'\t{'\t'*r_count}looping for {pattern}')
        while i <= self._longest and i <= len(pattern):
            # print(f'\t{'\t'*r_count}- sliced {pattern[:i]}')
            if pattern[:i] in self._towels:
                # count += 1    
                # print(f'\t{'\t'*r_count}Found that in towels... recursing for {pattern[i:]}')
                res = self._get_pattern_count(pattern[i:], r_count + 1)
                # print(f'\t{'\t'*r_count}Count: {count} + Res: {res}')
                count += res
            i += 1
        self._pattern_memory[pattern] = count
        # print(f'\t{'\t'*r_count}** Count: {count} for {pattern} **')
        return count

    def eval_patterns(self):
        res = 0
        for pattern in self._patterns:
            # print('eval', pattern)
            pattern_count = self._get_pattern_count(pattern)
            print(f'Pattern count for {pattern}: {pattern_count}')
            res+= pattern_count
        return res

        
    def get_combinations(self):
        for pattern in self._patterns:
            self._combinations[pattern] = []
            potentials = []
            for towel in self._towels:
                if pattern.startswith(towel[1]):
                    # if(pattern == 'gbbr'):
                    #     print(f'Potential start for {pattern}: {towel}')
                    potentials.append([towel])
            i = 0
            while len(potentials) > 0:
                # if(pattern == 'gbbr'):
                #     print(f'Potentials for {pattern}:\n\t{"\n\t".join([''.join([f'{t[0], t[1]}' for t in x]) for x in potentials])}')
                print(i)
                _potentials = []
                for potential in potentials:
                    if pattern == ''.join([x[1] for x in potential]) and potential not in self._combinations[pattern]:
                        # if(pattern == 'gbbr'):
                        #     print('\tmatch found')
                        self._combinations[pattern].append(potential)
                        continue
                    for towel in self._towels:
                        # if(pattern == 'gbbr'):
                        #     print(f'Potential: {potential}')
                        #     print(f'Towel: {towel}')
                        new_potential = ''.join([x[1] for x in potential]) + towel[1]
                        while new_potential not in _potentials and new_potential in pattern:
                            # print('\tappending')
                            _potentials.append(potential.copy() + [towel])
                            new_potential += towel[1]
                potentials = _potentials
                i+=1
        # print(f'Combinations:')
        # for combination in self._combinations:
        #     print(f'\t{combination}:')
        #     for i, pattern in enumerate(self._combinations[combination]):
        #         print(f'\t\t{i}: {pattern}')
        return self._combinations
    

    
    def get_counts(self):
        self.get_combinations()
        possible = 0
        impossible = 0
        combo = 0
        for pattern in self._combinations:
            if len(self._combinations[pattern]) > 0:
                possible += 1
                combo += len(self._combinations[pattern])
            else:
                impossible += 1
                self._impossible.append(pattern)
        # print(f'Possible: {possible}\nImpossible: {impossible}')
        return (possible, impossible, combo)

if __name__ == "__main__":
    main()

# _towels=set()
# _patterns=[]
# max_towel=0
# with open('adventInputs/day19.txt','r') as f:

#     temp=f.readline()
#     temp=temp.strip()
#     temp=temp.split(',')
#     for tow in temp:
#         towel=tow.strip()
#         max_towel=max(len(towel),max_towel)
#         _towels.add(towel)
#     f.readline()   
#     for line in f:
#         _patterns.append(line.strip())
# #print(patterns)
# #print(towels)


# def part1():
#     def dfs(_pattern):
#         if len(_pattern) == 0:
#             return True
#         flag=False
#         for _towel in _towels:
#             if len(_towel) <= len(_pattern) and _towel == _pattern[:len(_towel)]:
#                 # print(pattern)
#                 # print(towel[len(pattern):])
#                 if dfs(_pattern[len(_towel):]):
#                     return True
#         return False
#     count=0
#     for _pattern in _patterns:
#         if dfs(_pattern):
#             #print(towel)
#             count+=1
#     print(count)

# #part1()
# def part2():
#     mem={}
#     def dfs(_pattern):
#         #print(towel)
#         if len(_pattern) == 0:    
#             return 1
#         if _pattern in mem:
#             return mem[_pattern]
#         res=0
#         for i in range(0,max_towel+1):
#             if i <= len(_pattern) and _pattern[:i] in _towels:
#                 res+=dfs(_pattern[i:]) 
#         mem[_pattern]=res
#         return res
#     res=0
#     for i,_pattern in enumerate(_patterns):
#         print(i, _pattern)
#         res+=dfs(_pattern)
#         mem={}
#     print(res)

# def main():
#     print(max_towel,"max pattern")
#     part2()
#     print(_towels)

# if __name__ == "__main__":
#     main()