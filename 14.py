def parse_input(rel_path):
	paths = []

	with open(rel_path, mode='r', encoding='utf-8') as f:
		for line in f.readlines():
			line = line.replace('\n', '')
			line = line.split(' -> ')

			converted_path = []

			for str_coords in line:
				x, y = str_coords.split(',')
				x, y = int(x), int(y)
				converted_path.append([x, y])
			
			paths.append(converted_path)

	return paths


def translate_x(paths):
	min_x = float('inf')

	for path in paths:
		for coords in path:
			if coords[0] < min_x:
				min_x = coords[0]

	return list(map(lambda x: [[coords[0] - min_x, coords[1]] for coords in x], paths)), min_x


def generate_barriers(paths):
	def populate_line(constant, start, end, direction):
		length = abs(end - start) + 1
		anchor = min(start, end)
		idx = 0

		while idx < length:
			if direction == 'h':
				unit = [anchor + idx, constant]
			else:
				unit = [constant, anchor + idx]

			if not unit in barriers:
				barriers.append(unit)
			
			idx += 1 

	barriers = []

	for path in paths:
		i = 0

		while i < len(path)-1:
			s_x, s_y = path[i]
			e_x, e_y = path[i+1]

			if s_x == e_x:
				populate_line(s_x, s_y, e_y, 'v')
			else:
				populate_line(s_y, s_x, e_x, 'h')

			i += 1

	return barriers


def find_floor(barriers):
	max_y = 0
	gap = 2

	for coords in barriers:
		y = coords[1]

		if y > max_y:
			max_y = y

	return max_y + gap


def simulate_sand(sand_pos, barriers, floor=None):
	def sand_will_rest():
		sand_x, sand_y = sand_pos[0], sand_pos[1]
		barrier_presence = list(map(lambda x: x[0] == sand_x and x[1] > sand_y , barriers))

		if any(barrier_presence):
			return True
		else:
			return False

	def find_sand_move():
		moves = {
			'D': [0, 1],
			'DL': [-1, 1],
			'DR': [1, 1]
		}
		current_x, current_y = sand_pos

		for move_x, move_y in moves.values():
			potential_pos = [current_x + move_x, current_y + move_y]

			if potential_pos in barriers: continue


			if (floor and potential_pos[1] < floor) or not floor:
				sand_pos[0], sand_pos[1] = potential_pos[0], potential_pos[1]

				return True

		return False

	while find_sand_move():
		if not floor and not sand_will_rest():
			return False

	if floor and sand_pos in barriers:
		return False
	else:
		print(f'Rested at: {sand_pos}')

		barriers.append(sand_pos)
		return True


def dispense_sand(dispenser_loc, barriers, floor=None):
	sand_count = 0

	if floor:
		while simulate_sand(dispenser_loc.copy(), barriers, floor):
			sand_count += 1
	else:
		while simulate_sand(dispenser_loc.copy(), barriers):
			sand_count += 1

	print(sand_count)

	return sand_count


if __name__ == '__main__':
	s = './14_small.txt'
	r = './14.txt'

	paths = parse_input(r)
	# print(paths)
	shifted_paths, shift = translate_x(paths)
	# print(shifted_paths)
	barriers = generate_barriers(shifted_paths)
	# print(barriers)
	floor_y = find_floor(barriers)
	# print(floor_y)
	dispenser_loc = [500-shift, 0]
	count = dispense_sand(dispenser_loc, barriers, floor_y)

	# Part 1:
	# assert count == 24, f'expected 24 grains for 14_small.txt, got {count} instead'
	# assert count == 979, f'expected 979 grains for 14.txt, got {count} instead'

	# assert count == 93, f'expected 93 grains for 14_small.txt, got {count} instead'
	assert count == 29044, f'expected 29044 grains for 14.txt, got {count} instead'
