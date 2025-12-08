from helpers import Grid


day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
# input_2 = f2.read().splitlines()
input_2 = input_1
test_1 = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".splitlines()
test_2 = test_1

def solution_1(input):
    paper_map = PaperMap(input)
    paper_map.map_movable()
    print(f'Solution 1: Movable Papers = {paper_map.movable_count}')


def solution_2(input):
    paper = PaperMap(input)
    paper.map_movable()
    print(f'Initial Movable Papers = {paper.movable_count}')
    paper.move_all()
    print(f'Solution 2: Moved Papers = {paper.moved_count}')


class PaperMap(Grid):
    def __init__(self, grid_array: list) -> None:
        super().__init__(grid_array)
        self._movable_points = set()
        self._movable_count = 0
        self._moved_points = set()

    def is_movable(self, point):
        value = self.value_at_point(point)
        if(value == '@'):
            paper_count = 0
            for neighbor in self.get_surrounding(point):
                if(self.value_at_point(neighbor) == '@'):
                    paper_count += 1
            return paper_count < 4
        return False

    def map_movable(self):
        self._movable_points = set()
        for point in self.all_points():
            if(self.is_movable(point)):
                self._movable_points.add(point)

    def move_paper(self):
        for point in self._movable_points:
            self.set_value_at_point(point, '.')
        self._moved_points = self._moved_points.union(self._movable_points)
        self._movable_points = set()

    def move_all(self):
        self.map_movable()
        while(self.movable_count > 0):
            self.move_paper()
            self.map_movable()

    @property
    def movable_count(self):
        return len(self._movable_points)

    @property
    def moved_count(self):
        return len(self._moved_points)


def main(part=1, mode="test"):
    print('foo')
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)