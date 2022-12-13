def parse_input(rel_path):
	def char_to_elevation(char):
		num = ord(char)
		shift = 96

		return num - shift

	height_map = []
	start_pos = None
	end_pos = None

	with open(rel_path, mode='r', encoding='utf-8') as f:
		for row, line in enumerate(f.readlines()):
			height_map.append([])
			line = line.replace('\n', '')

			for char in line:
				position = [row, len(height_map[row])]

				if char == 'S':
					elevation = 1
					start_node = Node(position, elevation)
					height_map[row].append(start_node)
				elif char == 'E':
					elevation = 26
					end_node = Node(position, elevation)
					height_map[row].append(end_node)
				else:
					elevation = char_to_elevation(char)
					height_map[row].append(Node(position, elevation))

	return (height_map, start_node, end_node)


class Queue:
	def __init__(self, items):
		self.queue = [items]

	def pop(self):
		removed = self.queue[-1]
		self.queue = self.queue[:-1]

		return removed

	def push(self, item):
		self.queue = [item] + self.queue


class Node:
	def __init__(self, position, elevation):
		self.position = position
		self.elevation = elevation
		self.parent = None

	def find_available_moves(self, height_map, descending=False):
		def validate_adjacency(row, col):
			if row < 0 or row > height_map_rows-1:
				return False
			elif col < 0 or col > height_map_cols-1:
				return False
			else:
				return True

		checks = {
			'left': (0, -1),
			'up': (-1, 0),
			'right': (0, 1),
			'down': (1, 0)
		}
		available_nodes = []
		height_map_rows = len(height_map)
		height_map_cols = len(height_map[0])

		for row_step, col_step in checks.values():
			row, col = self.position
			adjacent_row, adjacent_col = row + row_step, col + col_step

			if not validate_adjacency(adjacent_row, adjacent_col): continue

			adjacent_node = height_map[adjacent_row][adjacent_col]
			elevation = height_map[row][col].elevation
			adjacent_elevation = adjacent_node.elevation

			if adjacent_elevation > elevation + 1 and not descending:
				continue
			else:
				available_nodes.append(adjacent_node)

		return available_nodes


def link_nodes(start, end, height_map):
	queue = Queue(start)
	visited = []

	while queue.queue != []:
		node = queue.pop()
		visited.append(node.position)

		if node.position == end.position:
			break
		else:
			for child_node in node.find_available_moves(height_map):
				if child_node.position not in visited and child_node not in queue.queue:
					child_node.parent = node
					queue.push(child_node)


def find_shortest_descent(end, elevation, height_map):
	queue = Queue(end)
	visited = []

	while queue.queue != []:
		node = queue.pop()
		visited.append(node.position)

		if node.elevation == elevation:
			return node
		else:
			for child_node in node.find_available_moves(height_map, descending=True):
				if child_node.position in visited or child_node in queue.queue: continue

				if node.elevation - child_node.elevation <= 1:
					child_node.parent = node
					queue.push(child_node)


def find_path_length(end):
	node = end
	steps = 0

	while node.parent:
		node = node.parent
		steps += 1

	return steps


if __name__ == '__main__':
	s = './12_small.txt'
	r = './12.txt'

	height_map, start_node, end_node = parse_input(r)

	# Part 1:
	# link_nodes(start_node, end_node, height_map)

	descent_node = find_shortest_descent(end_node, 1, height_map)
	path_length = find_path_length(descent_node)
	print(path_length)

	# Part 1:
	# Test for 12_small.txt
	# assert path_length == 31, f'expected 31 for 12_small.txt but got {path_length}'
	# Test for 12.txt
	# assert path_length == 352, f'expected 352 for 12.txt but got {path_length}'