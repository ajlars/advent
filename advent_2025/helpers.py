from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

Point.__add__ = lambda self, other: Point(self.x + other.x, self.y + other.y)
Point.__sub__ = lambda self, other: Point(self.x - other.x, self.y - other.y)
Point.__str__ = lambda self: f'({self.x}, {self.y})'

class Grid():
    def __init__(self, grid_array: list) -> None:
        self._array = []
        for row in [list(row) for row in grid_array.copy()]:
            if len(row) > 0:
                self._array.append(row)
        self._width = len(self._array[0])
        self._height = len(self._array)
        self._point_list = [Point(x,y) for y in range(self._height) for x in range(self._width)]
        self._original_points = self._point_list.copy()

    def _reset(self):
        self._point_list = self._original_points.copy()

    def value_at_point(self, point: Point):
        self.location_is_valid(point, True)
        return self._array[point.y][point.x]

    def set_value_at_point(self, point: Point, value):
        self.location_is_valid(point, True)
        self._array[point.y][point.x] = value

    def location_is_valid(self, point: Point, throw_error = False) -> bool:
        is_valid = 0 <= point.x < self._width and 0 <= point.y < self._height
        if not is_valid and throw_error:
            raise ValueError(f'Invalid location: {point}, width: {self._width}, height: {self._height}')
        return is_valid

    def find_value(self, value) -> Point:
        for point in self._point_list:
            if self.value_at_point(point) == value:
                return point
        return None

    def find_all_values(self, value) -> list[Point]:
        found_points = []
        for point in self._point_list:
            if self.value_at_point(point) == value:
                found_points.append(point)
        return found_points

    def get_neighbors(self, point: Point) -> list[Point]:
        neighbors = []
        for neighbor in [Point(point.x, point.y-1), Point(point.x, point.y+1), Point(point.x-1, point.y), Point(point.x+1, point.y)]:
            if self.location_is_valid(neighbor):
                neighbors.append(neighbor)
        return neighbors

    def get_surrounding(self, point: Point) -> list[Point]:
        surroundings = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                neighbor = Point(point.x + dx, point.y + dy)
                if self.location_is_valid(neighbor):
                    surroundings.append(neighbor)
        return surroundings

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def all_points(self) -> list[Point]:
        return self._point_list

    def rows_as_str(self) -> list[str]:
        return ["".join(str(char) for char in row) for row in self._array]

    def cols_as_str(self) -> list[str]:
        cols = []
        for x in range(self._width):
            col = ""
            for y in range(self._height):
                col += str(self._array[y][x])
            cols.append(col)
        return cols

    def __repr__(self) -> str:
        return "\n".join(self.rows_as_str())

    def __str__(self) -> str:
        return "\n".join(self.rows_as_str())
    