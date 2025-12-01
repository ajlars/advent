from collections import namedtuple
from tqdm import tqdm

def execute(items: list, func):
    for item in tqdm(items):
        func(item)


Point = namedtuple("Point", ["x", "y"])

Point.__add__ = lambda self, other: Point(self.x + other.x, self.y + other.y)
Point.__sub__ = lambda self, other: Point(self.x - other.x, self.y - other.y)

class Grid():
    def __init__(self, grid_array: list) -> None:
        self._array = []
        for row in [list(row) for row in grid_array.copy()]:
            if len(row) > 0:
                self._array.append(row)
        self._width = len(self._array[0])
        self._height = len(self._array)
        self._all_points = [Point(x,y) for y in range(self._height) for x in range(self._width)]
        self._original_all_points = self._all_points.copy()

    def _reset(self):
        self._all_points = self._original_all_points.copy()
    
    def point_as_node(self, point: Point) -> str:
        return f'{point.x},{point.y}'

    def value_at_point(self, point: Point):
        return self._array[point.y][point.x]
    
    def set_value_at_point(self, point: Point, value):
        self._array[point.y][point.x] = value

    def valid_location(self, point: Point) -> bool:
        return 0 <= point.x < self._width and 0 <= point.y < self._height
    
    def find_value(self, value) -> Point:
        for point in self._all_points:
            if self.value_at_point(point) == value:
                return point
            
    def get_neighbors(self, point) -> list[Point]:
        neighbors = []
        for neighbor in [Point(point.x, point.y-1), Point(point.x, point.y+1), Point(point.x-1, point.y), Point(point.x+1, point.y)]:
            if self.valid_location(neighbor):
                neighbors.append(neighbor)
        return neighbors
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    def all_points(self) -> list[Point]:
        return self._all_points
    
    def rows_as_str(self):
        return ["".join(str(char) for char in row) for row in self._array]
    
    def cols_as_str(self):
        cols_list = list(zip(*self._array))
        return ["".join(str(char) for char in col) for col in cols_list]
    
    def __repr__(self) -> str:
        return f"Grid(size={self.width}*{self.height})"
    
    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._array)