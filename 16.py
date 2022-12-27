import re


def parse_input(rel_path):
	nodes = {}
	valve_pattern = re.compile(r'[A-Z]{2}')
	rate_pattern = re.compile(r'\d+')

	with open(rel_path, mode='r', encoding='utf-8') as f:
		for line in f.readlines():
			valves = valve_pattern.findall(line)
			node_str, neighbors_str = valves[0], valves[1:]
			rate = int(rate_pattern.search(line).group())

			if node_str in nodes.keys():
				node = nodes[node_str]
			else:
				node = Node(node_str)
				nodes[node_str] = node

			node.add_rate(rate)

			for neighbor_str in neighbors_str:
				if neighbor_str in nodes.keys():
					neighbor = nodes[neighbor_str]
				else:
					neighbor = Node(neighbor_str)
					nodes[neighbor_str] = neighbor

				node.add_neighbor(neighbor)

	return {i: n for (i, n) in enumerate(sorted(nodes.values(), key=lambda x: x.name))}


class Node:
	def __init__(self, name):
		self.name = name
		self.distance = float('inf')
		self.neighbors = []

	def add_rate(self, rate):
		self.rate = rate

	def add_neighbor(self, neighbor):
		self.neighbors.append(neighbor)

	def __str__(self):
		return f'Valve {self.name}:\n\tFlow: {self.rate}\n\tNeighbors: {[n.name for n in self.neighbors]}'


def floyd_warshall(graph):
	size = len(graph)
	dist = [[float('inf') for n in range(size)] for m in range(size)]

	for i in range(size):
		start = graph[i]

		for j in range(size):
			end = graph[j]

			if start == end:
				dist[i][j] = 0
			elif end in start.neighbors:
				dist[i][j] = 1

	for k in range(size):
		for m in range(size):
			for n in range(size):
				dist[m][n] = min(dist[m][n], dist[m][k] + dist[k][n])

	return dist


def find_positive_flow_valves(graph):
	return {k: v for (k, v) in graph.items() if v.rate > 0}


# Memoization
memo = {}

def dfs(graph, pos_valves, root_id, time=30, bitstring=0b0):
	state = (root_id, bitstring, time)

	if state in memo.keys(): return memo.get(state)
	
	max_flow = 0

	for (c, id_valve) in enumerate(pos_valves.items()):
		idt, valve = id_valve

		if bitstring & (1 << c) != 0:
			continue
		else:
			cost = dist[root_id][idt]
			time_remaining = time - (cost + 1)

			if time_remaining < 0: continue 

			new_bitstring = bitstring | (1 << c)
		
		flow = dfs(graph, pos_valves, idt, time_remaining, new_bitstring) + valve.rate * time_remaining

		max_flow = max(max_flow, flow)

	memo[state] = max_flow

	return max_flow


def team_dfs(graph, pos_valves, root_id):
	num_valves = len(pos_valves)
	open_bitstring = (1 << num_valves)-1
	max_flow = 0

	for i in range(open_bitstring):
		j = i ^ open_bitstring

		flow = dfs(graph, pos_valves, root_id, 26, i) + dfs(graph, pos_valves, root_id, 26, j)
		max_flow = max(max_flow, flow)

	return max_flow


if __name__ == '__main__':
	s = './16_small.txt'
	r = './16.txt'

	# Part 1
	# minutes = 30
	minutes = 26

	nodes = parse_input(r)
	# print(nodes)

	# for node in nodes.values():
	# 	print(node)

	dist = floyd_warshall(nodes)

	print('SHORTEST DISTANCE MATRIX')
	for r in dist:
		print(r)

	pos_flow = find_positive_flow_valves(nodes)
	print(f'VALVES WITH POSITIVE FLOW:\n{pos_flow}')

	# Part 1
	# pressure = dfs(nodes, pos_flow, 0, minutes)
	pressure = team_dfs(nodes, pos_flow, 0)
	print(pressure)

	# Part 1
	# assert pressure == 1651, f'expected 1651 pressure released for 16_small.txt, got {pressure} instead'

	# assert pressure == 1707, f'expected 1707 pressure for 16_small.txt, got {pressure} instead'