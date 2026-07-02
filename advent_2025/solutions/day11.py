from itertools import combinations, permutations
from os import path
import networkx as nx
day = __file__.split("\\")[-1][3:-3]
f1 = open(f"inputs/day{day}_1.txt", "r")
# f2 = open(f"inputs/day{day}_2.txt", "r")
input_1 = f1.read().splitlines()
# input_2 = f2.read().splitlines()
input_2 = input_1
test_1 = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".splitlines()
test_2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".splitlines()
# test_2 = test_1

def solution_1(input):
    network = ReactorNetwork(input)
    paths = network.get_paths('you')
    print(f'Solution 1: Total distinct paths from "you" to "out" = {len(paths)}')

def solution_2(input):
    network = ReactorNetwork(input)
    paths = network.get_paths_with_stops('svr', ['fft', 'dac'])
    print(f'Solution 2: Total distinct paths from "svr" to "out" = {paths}')

class ReactorNetwork():
    def __init__(self, docs: list[str]) -> None:
        self.docs = docs
        self.graph:nx.DiGraph[str] = nx.DiGraph()
        self.end = "out"
        self.parse_docs()

    def parse_docs(self) -> dict[str, list[str]]:
        devices = {}
        for i in range(len(self.docs)):
            line = self.docs[i]
            name, rest = line.split(': ')
            outputs = rest.split(' ')
            devices[name] = outputs
            for output in outputs:
                self.graph.add_edge(name, output)
        # Check for cycles and report them
        try:
            cycles = list(nx.simple_cycles(self.graph))
            if cycles:
                print(f'WARNING: Graph contains {len(cycles)} cycle(s):')
                for cycle in cycles[:5]:  # Show first 5 cycles
                    print(f'  Cycle: {" -> ".join(cycle + [cycle[0]])}')
                if len(cycles) > 5:
                    print(f'  ... and {len(cycles) - 5} more cycles')
        except:
            pass
        return devices
    
    def get_paths(self, start, end = None, cutoff = None) -> list[list[str]]:
        # print(f'DEBUG: Getting paths from {start} to {end if end else self.end}')
        if end is None:
            end = self.end
        path_exists = nx.has_path(self.graph, start, end)
        # print(f'DEBUG: Path exists: {path_exists}')
        if not path_exists:
            return []
        
        paths = list(nx.all_simple_paths(self.graph, start, end))
        # print(f'DEBUG: Found {len(paths)} paths')
        return paths
    
    def count_paths(self, start, end) -> int:
        if not nx.has_path(self.graph, start, end):
            return 0
        try:
            can_be_reached = nx.descendants(self.graph, start) | {start}
            can_reach_end = nx.ancestors(self.graph, end) | {end}
            nodes_on_paths = can_be_reached & can_reach_end
            path_graph = nx.DiGraph(self.graph.subgraph(nodes_on_paths))

            topo_order = list(nx.topological_sort(path_graph))

            count = {node: 0 for node in topo_order}
            count[start] = 1
            for node in topo_order:
                if count[node] > 0:
                    for successor in path_graph.successors(node):
                        count[successor] += count[node]

            return count[end]
        except any:
            print(f'Warning: error counting paths from {start} to {end}')
        return 0

    
    def get_paths_with_stops(self, start, stops) -> int:
        path_count = 0
        for node_a, node_b in permutations(stops, 2):
            connections = self.count_paths(node_a, node_b)
            if connections > 0:
                start_to_a = self.count_paths(start, node_a)
                b_to_end = self.count_paths(node_b, self.end)
                additional_paths = (start_to_a * connections * b_to_end)
                path_count += additional_paths
                print(f'DEBUG:\n\t{start} to {node_a}: {start_to_a}\n\tPaths from {node_a} to {node_b}: {connections}\n\t{node_b} to {self.end}: {b_to_end}\n\tAdditional paths now {additional_paths}\n\tUpdated path count: {path_count}')
        # paths_to_find = [(start, self.end), (start, stops[0]), (start, stops[1]), (stops[0], stops[1]), (stops[1], stops[0]), (stops[0], self.end), (stops[1], self.end)]
        # for pair_a, pair_b in paths_to_find:
        #     count = self.count_paths(pair_a, pair_b)
        #     print(f'DEBUG: Paths from {pair_a} to {pair_b}: {count}')
        #     path_count += count
        return path_count

    # def path_through_nodes(self, start, end, nodes: list[str]) -> list[list[str]]:

def main(part, mode):
    input = None
    solution = solution_1 if part == 1 else solution_2
    if mode == "test":
        input = test_1 if part == 1 else test_2
    else:
        input = input_1 if part == 1 else input_2
    print(f'Running Advent of Code 2025: Day {day}, Part {part}, Mode {mode}')
    solution(input)