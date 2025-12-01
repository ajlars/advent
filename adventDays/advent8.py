f = open('adventInputs/dayEight.txt', 'r')
puzzle = f.read().splitlines()
minipuzzle = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""".splitlines()

def main():
    # map = minipuzzle
    map = puzzle
    part2(map)

def part1(_map):
    map = []
    nodes = {}
    antinodes = {}
    for y in range(len(_map)):
        row = list(_map[y])
        map.append(list(_map[y]))
        for x in range(len(row)):
            if row[x] != '.' and row[x] not in list(antinodes.keys()):
                nodes[row[x]] = [[x, y]]
                antinodes[row[x]] = []
            elif row[x] != '.':
                nodes[row[x]].append([x, y])
    keys = list(nodes.keys())
    for key in keys:
        for a in range(len(nodes[key])):
            node_a = nodes[key][a]
            _nodes = nodes[key].copy()
            _nodes.pop(a)
            for b in range(len(_nodes)):
                node_b = _nodes[b]
                gap_x, gap_y = node_b[0] - node_a[0], node_b[1] - node_a[1]
                antinode_a = [node_a[0] - gap_x, node_a[1] - gap_y]
                antinode_b = [node_b[0] + gap_x, node_b[1] + gap_y]
                _print = a == 0 and b == 0 and key == 'e'
                if _print: print(f'node_a: {node_a}\nnode_b: {node_b}\ngap: {gap_x, gap_y}\nantinode_a: {antinode_a}\nantinode_b: {antinode_b}')
                if(antinode_a not in antinodes[key]): antinodes[key].append(antinode_a)
                if(antinode_b not in antinodes[key]): antinodes[key].append(antinode_b)
    print(nodes)
    print(antinodes)
    count = 0
    unique_antinode_coords = []
    for key in keys:
        for coords in antinodes[key]:
            if coords not in unique_antinode_coords and 0 <= coords[0] < len(map[0]) and 0 <= coords[1] < len(map):
                unique_antinode_coords.append(coords)
                count+=1
    print(f'Antinodes: {count}\nUnique locations: {len(unique_antinode_coords)}')

def part2(_map):
    map = []
    nodes = {}
    antinodes = []
    for y in range(len(_map)):
        row = list(_map[y])
        map.append(row)
        for x in range(len(row)):
            if row[x] != '.' and row[x] not in list(nodes.keys()):
                nodes[row[x]] = [[x, y]]
            elif row[x] != '.':
                nodes[row[x]].append([x, y])
    keys = list(nodes.keys())
   
    for key in keys:
        _nodes = nodes[key].copy()
        count = 0
        while len(_nodes) > 1:
            node_a = _nodes.pop(0)
            for node_b in _nodes:
                [x, y] = node_a
                gap_x = x - node_b[0]
                gap_y = y - node_b[1]
                # print(key, x, y, gap_x, gap_y)
                while(0 <= x < len(map[0]) and 0 <= y < len(map)):
                    if([x, y] not in antinodes):
                        antinodes.append([x, y])
                    x +=gap_x
                    y +=gap_y
                [x, y] = node_b
                while(0 <= x < len(map[0]) and 0 <= y < len(map)):
                    if([x, y] not in antinodes):
                        antinodes.append([x, y])
                    x -=gap_x
                    y -=gap_y
                #     if map[node_a[1]][node_a[0]] == '#':
                #         break
                #     if node_a not in antinodes[key]:
                #         antinodes[key].append(node_a)

        # for a in range(len(nodes[key])):
        #     _nodes.pop(0)
        #     node_a = nodes[key][a]
        #     for b in range(len(_nodes)):
        #         node_b = _nodes[b]
        #         gap_x, gap_y = node_b[0] - node_a[0], node_b[1] - node_a[1]
        #         count += 1
        #         print(key, node_a, node_b, gap_x, gap_y)
        # print(key, antinodes)

    print(len(antinodes))
    # print(nodes)
    # print(antinodes)
    # count = 0
    # unique_antinode_coords = []
    # for key in keys:
    #     for coords in antinodes[key]:
    #         if coords not in unique_antinode_coords and 0 <= coords[0] < len(map[0]) and 0 <= coords[1] < len(map):
    #             unique_antinode_coords.append(coords)
    #             count+=1
    # unique_antinode_coords.sort()
    # # print(f'Nodes: {nodes}')
    # # print(f'Antinodes: {count}\nUnique locations: {len(unique_antinode_coords)}')
    # # print(unique_antinode_coords, len(map[0]), len(map))
    # for key in keys:
    #     print(f'{key}: \n\tnodes:{len(nodes[key])}\n\tantinodes:{len(antinodes[key])}')

main()