# An attempt was made to use recursion in order to solve part 1 of AoC's Day 12 challenge.
# Did it work for the smaller example? Yes. Does the code scale to the actual puzzle input? Absolutely not.
# The lesson here is not to approach shortest-path problems exhaustively. Attempt 2 forthcoming.


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
				if char == 'S':
					elevation = 1
					start_pos = [row, len(height_map[row])]
				elif char == 'E':
					elevation = 26
					end_pos = [row, len(height_map[row])]
				else:
					elevation = char_to_elevation(char)

				height_map[row].append(elevation)

	return (height_map, start_pos, end_pos)


class Person:
	def __init__(self, height_map, position, goal):
		self.height_map = height_map
		self.height_map_rows = len(height_map)
		self.height_map_cols = len(height_map[0])
		self.position = position
		self.goal = goal

		self.path = []

	def find_available_moves(self, path):
		def validate_adjacency(row, col, path):
			if row < 0 or row > self.height_map_rows-1:
				return False
			elif col < 0 or col > self.height_map_cols-1:
				return False
			elif [row, col] in path:
				return False
			else:
				return True

		checks = {
			'left': (0, -1),
			'up': (-1, 0),
			'right': (0, 1),
			'down': (1, 0)
		}
		available_moves = []

		for row_step, col_step in checks.values():
			row, col = self.position
			adjacent_row, adjacent_col = row + row_step, col + col_step

			if not validate_adjacency(adjacent_row, adjacent_col, path): continue

			elevation = self.height_map[row][col]
			adjacent_elevation = self.height_map[adjacent_row][adjacent_col]

			if adjacent_elevation > elevation + 1:
				continue
			else:
				available_moves.append([adjacent_row, adjacent_col])

		return available_moves

	def find_all_paths(self):
		def find_path(current_path):
			# print(f'{self}: exploring {current_path}')
			paths = []
			available_moves = self.find_available_moves(current_path)

			if available_moves == []:
				return current_path
			elif self.goal in available_moves:
				self.position = self.goal

				return current_path + [self.position]
			else:
				for move in available_moves:
					self.position = move
					path = find_path(current_path + [self.position])

					if path: all_paths.append(path)

		all_paths = []
		find_path([])

		return all_paths

	def find_goal_paths(self):
		all_paths = self.find_all_paths()
		goal_paths = []

		for path in all_paths:
			ending_pos = path[-1]
			if ending_pos == self.goal:
				goal_paths.append(path)

		return goal_paths

	def find_shortest_goal_path(self):
		goal_paths = self.find_goal_paths()

		return sorted(goal_paths, key=lambda x: len(x))[0]

	def __str__(self):
		print(f'Person at position {self.position}')
		return ''


if __name__ == '__main__':
	s = './12_small.txt'
	r = './12.txt'

	height_map, start_pos, end_pos = parse_input(s)
	# print(height_map)

	person = Person(height_map, start_pos, end_pos)
	# print(person)
	# print(person.goal)

	# all_paths = person.find_all_paths()
	# for count, path in enumerate(all_paths):
	# 	print(f'path {count}: {path}')

	shortest_goal_path = person.find_shortest_goal_path()
	print(shortest_goal_path)
	print(len(shortest_goal_path))

	# Test for 12_small.txt
	# assert len(shortest_goal_path) == 31, f'expected 31 for 12_small.txt, got {len(shortest_goal_path)} instead'