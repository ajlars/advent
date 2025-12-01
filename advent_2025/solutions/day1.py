day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
input_2 = input_1
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
test_2 = test_1

class dial():
    def __init__(self, start=50, size=100):
        self.start = start
        self.size = size
        self.position = self.start
        self.zero_stops = 0
        self.zero_clicks = 0

    def step(self, instruction):
        direction = instruction[0]
        _steps = int(instruction[1:])
        self.zero_clicks += _steps // self.size
        steps = _steps % self.size
        if direction == 'L':
            if(self.position-steps)<=0 and self.position!=0:
                self.zero_clicks += 1
            self.turn_left(steps)
        elif direction == 'R':
            if(self.position+steps)>=self.size and self.position!=0:
                self.zero_clicks += 1
            self.turn_right(steps)
        if self.position == 0:
            self.zero_stops += 1

    def turn_left(self, steps):
        self.position -= steps
        if self.position < 0:
            self.position += self.size

    def turn_right(self, steps):
        self.position += steps
        if self.position >= self.size:
            self.position -= self.size

    def get_zero_stops(self):
        return self.zero_stops

    def get_zero_clicks(self):
        return self.zero_clicks
    

def solution_1(input):
    _dial = dial()
    for line in input:
        _dial.step(line)
    print(_dial.get_zero_stops())


def solution_2(input):
    _dial = dial()
    for line in input:
        _dial.step(line)
    print(_dial.get_zero_clicks())

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)