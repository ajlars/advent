import numpy as np

day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().split('\n\n')
# input_2 = f2.read().splitlines()
input_2 = input_1
test_1 = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
""".split('\n\n')
# test_2 = """""".splitlines()
test_2 = test_1

def solution_1(input):
    mapper = GiftMapper(input)
    packed_regions = mapper.pack_gifts()
    print(f"Packed {packed_regions} regions")
    

def solution_2(input):
    print("Solution 2 not yet implemented")

class GiftMapper():
    def __init__(self, gift_strs):
        self.gifts = {}
        for gift_str in gift_strs[:-1]:
            self.parse_gift(gift_str)
        self.regions = [self.parse_region(region_str) for region_str in gift_strs[-1].splitlines()]

    def parse_gift(self, gift_str):
        """Parse gift into a list of (dx, dy) coordinate offsets"""
        lines = gift_str.splitlines()
        gift_id = int(lines[0][:-1])
        shape_str = [list(line) for line in lines[1:]]
        
        # Store as list of coordinate offsets from origin
        coords = []
        for y in range(len(shape_str)):
            for x in range(len(shape_str[y])):
                if shape_str[y][x] == '#':
                    coords.append((x, y))
        
        # Store all 4 rotations to avoid computing them repeatedly
        self.gifts[gift_id] = self.get_rotations(coords)
    
    def get_rotations(self, coords):
        """Get all 4 rotations of a shape"""
        rotations = [coords]  # 0 degrees
        
        # Normalize coords to start at (0,0)
        def normalize(coords):
            if not coords:
                return coords
            min_x = min(c[0] for c in coords)
            min_y = min(c[1] for c in coords)
            return [(x - min_x, y - min_y) for x, y in coords]
        
        # 90 degrees: (x, y) -> (-y, x)
        rot90 = normalize([(-y, x) for x, y in coords])
        rotations.append(rot90)
        
        # 180 degrees: (x, y) -> (-x, -y)
        rot180 = normalize([(-x, -y) for x, y in coords])
        rotations.append(rot180)
        
        # 270 degrees: (x, y) -> (y, -x)
        rot270 = normalize([(y, -x) for x, y in coords])
        rotations.append(rot270)
        
        return rotations
    
    def parse_region(self, region_strs):
        dims, gift_counts = region_strs.split(':')
        width, height = [int(x) for x in dims.split('x')]
        gift_counts = [int(x) for x in gift_counts.strip().split(' ')]
        return {'width': width, 'height': height, 'gift_counts': gift_counts}

    def pack_gifts(self):
        packed_regions = 0
        for i in range(len(self.regions)):
            region = self.regions[i]
            width = region['width']
            height = region['height']
            
            # Build list of gift IDs to place
            gift_list = []
            for gift_id, count in enumerate(region['gift_counts']):
                for _ in range(count):
                    gift_list.append(gift_id)
            
            print(f'\n========== Packing container {i+1}/{len(self.regions)} ({width}x{height}, {len(gift_list)} gifts) ==========')
            result = self.pack_container(width, height, gift_list)
            
            if result:
                self.print_packed_container(width, height, result)
                packed_regions += 1
            else:
                print('Could not pack all gifts')
        return packed_regions

    def pack_container(self, width, height, gift_ids):
        """Pack gifts using grid-based backtracking"""
        # Sort gifts by size (largest first)
        sorted_gift_ids = sorted(gift_ids, key=lambda gid: len(self.gifts[gid][0]), reverse=True)
        
        # Early check: total area of gifts must not exceed container
        total_gift_area = sum(len(self.gifts[gid][0]) for gid in sorted_gift_ids)
        container_area = width * height
        
        if total_gift_area > container_area:
            print(f'Impossible: gift area ({total_gift_area}) > container area ({container_area})')
            return None
        
        # Initialize empty grid
        grid = np.zeros((height, width), dtype=int)
        
        # Add iteration counter to detect likely impossible cases
        self.max_iterations = 100000  # Limit backtracking attempts
        self.iteration_count = 0
        
        result = self.backtrack_pack(grid, sorted_gift_ids, [], 0)
        
        if result is None and self.iteration_count >= self.max_iterations:
            print(f'Gave up after {self.iteration_count} attempts (likely impossible)')
        
        return result
    
    def backtrack_pack(self, grid, gift_ids, placements, gift_index):
        """Backtracking with grid-based collision detection"""
        # Check iteration limit
        self.iteration_count += 1
        if self.iteration_count > self.max_iterations:
            return None
        
        # Base case: all gifts placed
        if gift_index >= len(gift_ids):
            return placements
        
        # Early pruning: check if remaining gifts can fit in remaining space
        remaining_area = np.sum(grid == 0)
        remaining_gift_area = sum(len(self.gifts[gid][0]) for gid in gift_ids[gift_index:])
        
        if remaining_gift_area > remaining_area:
            # Impossible to fit remaining gifts
            return None
        
        gift_id = gift_ids[gift_index]
        rotations = self.gifts[gift_id]
        height, width = grid.shape
        
        # Try each rotation
        for rot_idx, coords in enumerate(rotations):
            # Get bounding box of this rotation
            max_x = max(c[0] for c in coords)
            max_y = max(c[1] for c in coords)
            
            # Try positions where the shape could fit
            for y in range(height - max_y):
                for x in range(width - max_x):
                    # Check if all cells are free
                    can_place = True
                    for dx, dy in coords:
                        if grid[y + dy, x + dx] != 0:
                            can_place = False
                            break
                    
                    if can_place:
                        # Place the gift
                        gift_marker = gift_index + 1
                        for dx, dy in coords:
                            grid[y + dy, x + dx] = gift_marker
                        
                        # Record placement
                        new_placements = placements + [(gift_id, rot_idx, x, y)]
                        
                        # Recurse
                        result = self.backtrack_pack(grid, gift_ids, new_placements, gift_index + 1)
                        
                        if result is not None:
                            return result
                        
                        # Backtrack - remove the gift
                        for dx, dy in coords:
                            grid[y + dy, x + dx] = 0
        
        return None

    def print_packed_container(self, width, height, placements):
        """Print the packed container with letters for each gift"""
        grid = [['.' for _ in range(width)] for _ in range(height)]
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        
        for i, (gift_id, rot_idx, x, y) in enumerate(placements):
            char = chars[i % len(chars)]
            coords = self.gifts[gift_id][rot_idx]
            for dx, dy in coords:
                grid[y + dy][x + dx] = char
        
        print('\nPacked container:')
        for row in grid:
            print(''.join(row))

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)