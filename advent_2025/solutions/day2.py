day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().split(',')
# input_2 = f2.read().split(',')
input_2 = ""
test_1 = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124".split(",")
test_2 = "".split(',')

class range_checker():
    def __init__(self, range):
        self.range = range
        self.start = int(range.split("-")[0])
        self.end = int(range.split("-")[1])
        self.invalid_ids = []

    def check_range(self):
        for i in range(self.start, self.end+1):
            if not self.is_valid(i):
                self.invalid_ids.append(i)
        return self.invalid_ids
    
    def is_valid(self, id):
        id_str = str(id)
        half = len(id_str)//2
        if (len(id_str)%2 == 0) and (id_str[:half] == id_str[half:]):
            return False
        return True
        
    def sum_invalid(self):
        return sum(self.invalid_ids)
    
class range_checker_part2(range_checker):
    def is_valid(self, id):
        id_str = str(id)
        length = len(id_str)
        for size in range(1, length//2 + 1):
            # print(size)
            if(length % size == 0):
                segment = id_str[:size]
                segments_match = True
                for i in range(0, int(length/size)):
                    if id_str[i*size:(i+1)*size] != segment:
                        segments_match = False
                        break
                if segments_match:
                    # print(f'Invalid ID found: {id_str} with segment {segment}')
                    return False
        return True
    
def solution_1(input):
    count_invalid = 0
    sum_invalid = 0
    for range_str in input:
        rc = range_checker(range_str)
        invalid_ids = rc.check_range()
        count_invalid += len(invalid_ids)
        sum_invalid += rc.sum_invalid()
    print(f'Count invalid IDs: {count_invalid}')
    print(f'Sum of all invalid IDs: {sum_invalid}')

def solution_2(input):
    count_invalid = 0
    sum_invalid = 0
    for range_str in input:
        rc = range_checker_part2(range_str)
        invalid_ids = rc.check_range()
        count_invalid += len(invalid_ids)
        sum_invalid += rc.sum_invalid()
    print(f'Count invalid IDs: {count_invalid}')
    print(f'Sum of all invalid IDs: {sum_invalid}')

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_1
    else:
        input = input_1 if part == 1 else input_1
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)