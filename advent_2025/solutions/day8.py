import numpy as np
import networkx as nx

day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
# input_2 = f2.read().splitlines()
input_2 = input_1
test_1 = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".splitlines()
# test_2 = """""".splitlines()
test_2 = test_1

def solution_1(input):
    boxes = junction_boxes(input)
    connection_count = 10 if len(input) < 500 else 1000
    # connection_count = 10 if len(input) < 500 else 1000
    boxes.connect_boxes(connection_count)
    sorted_constellations = boxes.sort_constellations()
    val = sorted_constellations[0][0] * sorted_constellations[1][0] * sorted_constellations[2][0]
    print(f'Solution 1: Largest constellations sizes multiplied = {val} (using {connection_count} connections)')

def solution_2(input):
    boxes = junction_boxes(input)
    product = boxes.connect_constellations()
    # product = boxes.connect_constellations()
    # val = sorted_constellations[0][0] * sorted_constellations[1][0] * sorted_constellations[2][0]
    print(f"Solution 2: Product of the last connected boxes' coordinates = {product}")

class junction_boxes:
    def __init__(self, box_lines: list[str]) -> None:
        boxes = []
        for line in box_lines:
            coords = list(map(int, line.split(',')))
            boxes.append(coords)
        self.boxes = np.array(boxes)
        self.box_map = None
        self.connected_graph = nx.Graph()
        self.connected_boxes = []
        self.unconnected_boxes = [i for i in range(len(self.boxes))]
        self.constellations = np.array([])

    def map_distances(self):
        graph = nx.Graph()
        for i in range(len(self.boxes)):
            graph.add_node(i, pos=i)
            for j in range(len(self.boxes)):
                if(i != j):
                    dist = np.linalg.norm(self.boxes[i] - self.boxes[j])
                    graph.add_edge(i, j, weight=dist)
        self.box_map = graph

    def get_sorted_edges(self, count=None):
        self.map_distances()
        if self.box_map is None:
            raise ValueError('Box map has not been created.')
        edges = list(self.box_map.edges(data=True))
        sorted_edges = sorted(edges, key=lambda x: x[2]['weight'])
        if count is not None:
            return sorted_edges[:count]
        return sorted_edges

    def connect_boxes(self, count=None):
        sorted_edges = self.get_sorted_edges()
        connected = 0
        last_connection = ([0,0,0], [0,0,0])
        # print('count', count)
        for edge in sorted_edges:
            self.connected_graph.add_node(edge[0])
            self.connected_graph.add_node(edge[1])
            if count is None and nx.has_path(self.connected_graph, edge[0], edge[1]):
                continue
            # print(f'Connecting boxes {self.boxes[edge[0]]} and {self.boxes[edge[1]]} with distance {edge[2]["weight"]}')
            if edge[0] in self.unconnected_boxes:
                self.unconnected_boxes.remove(edge[0])
            if edge[1] in self.unconnected_boxes:
                self.unconnected_boxes.remove(edge[1])
            self.connected_graph.add_edge(edge[0], edge[1], weight=edge[2]['weight'])
            connected += 1
            last_connection = (self.boxes[edge[0]], self.boxes[edge[1]])
            # print(connected)
            if count is not None and connected >= count:
                break
            print(f'{len(self.connected_boxes)} connected: {len(self.unconnected_boxes)} unconnected')
        print(last_connection)
        return last_connection

    def get_constellations(self):
        if 'connected_graph' not in self.__dict__:
            self.connect_boxes()
        if self.connected_graph is None:
            raise ValueError('Connected graph has not been created.')
        # print(f'Connected components: {list(nx.connected_components(self.connected_graph))}')
        # print(f'Unconnected boxes: {self.unconnected_boxes}')
        connected = list(nx.connected_components(self.connected_graph))
        unconnected = [{i} for i in self.unconnected_boxes]
        # print(f'Found {len(connected)} connected constellations')
        self.constellations = [*connected, *unconnected]
        return self.constellations
    
    def sort_constellations(self):
        self.get_constellations()
        sorted_constellations = sorted(self.constellations, key=lambda x: len(x), reverse=True)
        map_with_size = [(len(c), str(c)) for c in sorted_constellations]
        return map_with_size
    
    def connect_constellations(self):
        # current_constellations = self.get_constellations()
        # print('entry', len(current_constellations))
        last_connection = self.connect_boxes()
        # while len(current_constellations) > 1:
            # self.connect_boxes()
            # current_constellations = self.get_constellations()
            # print('loop', len(current_constellations))
        # print(f'Connected to {len(current_constellations)} constellations')
        return(last_connection[0][0] * last_connection[1][0])

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)