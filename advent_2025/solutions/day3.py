day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
# input_2 = f2.read().splitlines()
input_2 = input_1
test_1 = """987654321111111
811111111111119
234234234234278
818181911112111""".splitlines()
test_2 = test_1

def solution_1(input):
    b = batteries(input)
    print(f'Max joltage: {b.get_max_capacity()}')
    print(f'Max override joltage: {b.get_max_override_capacity()}')

def solution_2(input):
    b = batteries(input, 12)
    
    print(f'Max override joltage: {b.get_max_override_capacity()}')

class batteries():
    banks = []
    max_joltages = []
    max_override_joltages = []
    capacity = 0
    override_capacity = 0
    active_count = 0
    def __init__ (self, banks, active_count=2):
        self.active_count = active_count
        for bank in banks:
            self.banks.append([int(x) for x in bank])
    def get_max_capacity(self):
        self.get_max_joltages()
        self.capacity = sum(self.max_joltages)
        return self.capacity
    def get_max_joltages(self):
        self.max_joltages = []
        for bank in self.banks:
            self.max_joltages.append(self.get_bank_joltage(bank))
        return self.max_joltages
    def get_bank_joltage(self, bank):
        max1 = max(bank[0:-1])
        max2 = max(bank[bank.index(max1)+1:])
        return int(f'{max1}{max2}')
    def get_max_override_capacity(self):
        self.get_max_override_joltages()
        self.override_capacity = sum(self.max_override_joltages)
        return self.override_capacity
    def get_max_override_joltages(self):
        self.max_override_joltages = []
        for bank in self.banks:
            self.max_override_joltages.append(self.get_bank_override_joltage(bank))
        return self.max_override_joltages
    def get_bank_override_joltage(self, bank):
        candidates = set()
        maxLength = self.active_count

        def get_next_candidates(bank_str, offset):
            if(len(bank_str) == 0):
                return set()
            if(len(bank_str) == 1):
                return {(int(bank_str), '')}
            bank = [int(x) for x in bank_str.split(',')]
            candidates = set()
            _max = max(bank)
            indeces = []
            
            if(offset == 0):
                return {( _max, '')}

            for val in reversed(range(1,_max+1)):
                _indeces = [i for i, v in enumerate(bank[0:-offset]) if (v == val )]
                if(len(_indeces) > 0):
                    _max = val
                    indeces = _indeces
                    break
            for i in indeces:
                _bank_str = ','.join(str(x) for x in bank[(i+1):])
                _candidate = (_max, _bank_str)
                candidates.add(_candidate)
            return candidates
        
        for i in reversed(range(maxLength)):
            if(len(candidates) == 0):
                candidates = get_next_candidates(','.join(str(x) for x in bank), i)
            else:
                newCandidates = set()
                for candidate in candidates:
                    next_candidates = get_next_candidates(candidate[1], i)
                    for next_candidate in next_candidates:
                        val = int(f'{candidate[0]}{next_candidate[0]}')
                        bank_str = next_candidate[1]
                        new_candidate = (val, bank_str)
                        newCandidates.add(new_candidate)
                candidates = newCandidates
            # print(f'i: {i}, candidates: {candidates}')
        max_joltage = max([c[0] for c in candidates])
        return max_joltage
        #             for next_candidate in next_candidates:
        #                 newCandidates.add((int(f'{candidate[0]}{next_candidate[0]}'), next_candidate[1]))
        #         candidateValues = [get_candidate_joltage(c) for c in newCandidates]
        #         maxCandidateValue = max(candidateValues)
        #         filteredCandidates = [c for c, v in zip(newCandidates, candidateValues) if v == maxCandidateValue]
        #         candidates = filteredCandidates
        #     print(f'i: {i}, candidates: {[c[0] for c in candidates]}')
        # finalCandidateValues = [get_candidate_joltage(c) for c in candidates]
        # return max(finalCandidateValues)
        
            

        


def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)