minimap_a = """0123
1234
8765
9876""".splitlines()

minimap_b = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""".splitlines()

f = open("adventInputs/day10.txt", "r")
bigmap = f.read().splitlines()

def main():
    map = []
    for _line in bigmap:
        line = []
        for char in _line:
            line.append(int(char))
        map.append(line)
    trails = find_trails(map)
    sum_trailhead_scores(trails)

def find_trails(map):
    trailheads = []
    trails = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 0:
                trailheads.append([x, y])
    ongoing = []
    for [x, y] in trailheads:
        ongoing.append({'0': [x, y]})
        print('ongoing, 0:', ongoing)
        steps = get_next_steps(map, x, y, 0)
        current = 1
        while(steps != [] and current < 9):
            print(f'height: {current}, steps: {steps}')
            next_steps = []
            for [_x, _y] in steps:
                new_steps = get_next_steps(map, _x, _y, current)
                for step in new_steps:
                    if step not in next_steps: next_steps.append(step)
            current += 1
            steps = next_steps
        
        steps = get_next_steps(map, x, y, 0)
        current = 1
        _ongoing = []
        for path in ongoing.copy():
            try:
                if path[str(current -1)] == [x,y]:
                    for step in steps:
                        _path = path.copy()
                        _path[str(current)] = [step[0], step[1]]
                        _ongoing.append(_path.copy())
            except:
                pass
        ongoing = _ongoing.copy()
        print('ongoing 1:', ongoing)
        while(steps != [] and current < 9):
            _ongoing = []
            next_steps = []
            for [_x, _y] in steps:
                new_steps = get_next_steps(map, _x, _y, current)
                for path in ongoing.copy():
                    try:
                        if path[str(current)] == [_x,_y]:
                            for step in new_steps:
                                _path = path.copy()
                                _path[str(current+1)] = [step[0], step[1]]
                                _ongoing.append(_path.copy())
                    except:
                        pass
                for step in new_steps:
                    next_steps.append(step)
            current += 1
            steps = next_steps
            ongoing = _ongoing.copy()
            print(f'ongoing {current}:', ongoing)
                
        
        trails.append([x, y, len(steps), 0])
        print(f'trailhead: [{x, y}], score: {len(steps)}, splits: {0}\n\n')
    return trails

def sum_trailhead_scores(trails):
    scores = 0
    ratings = 0
    for trail in trails:
        scores += trail[2]
        ratings += trail[3]
    print(f'Sum of Trailhead Scores: {scores}')
    print(f'Sum of Trailhead Ratings: {ratings}')
    
def get_next_steps(map, x, y, current):
    steps = []
    if(x-1 >= 0 and map[y][x-1] == current + 1):
        steps.append([x-1, y])
    if(x+1 < len(map[y]) and map[y][x+1] == current + 1):
        steps.append([x+1, y])
    if(y-1 >= 0 and map[y-1][x] == current + 1):
        steps.append([x, y-1])
    if(y+1 < len(map) and map[y+1][x] == current + 1):
        steps.append([x, y+1])
    # print(f'height {current+1} from [x,y]: [{x, y}], next steps: {steps}')
    return steps

if __name__ == '__main__':
    main()