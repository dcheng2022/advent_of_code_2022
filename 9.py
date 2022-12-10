def parse_input(rel_path):
	head_moves = []

	with open(rel_path, mode='r', encoding='utf-8') as f:
		for line in f.readlines():
			line = line.replace('\n', '')
			direction, steps = line.split()

			head_moves.append({'direction': direction, 'steps': int(steps)})

	return head_moves


class Knot:
	def __init__(self, name):
		self.name = name
		self.pos = [1, 1]
		self.pos_history = []
		self.tail = None

	def move(self, direction):
		direction_steps = {
			'L': (-1, 0),
			'U': (0, 1),
			'R': (1, 0),
			'D': (0, -1),
			'UL': (-1, 1),
			'UR': (1, 1),
			'DR': (1, -1),
			'DL': (-1, -1)
		}
		x_step, y_step = direction_steps[direction]

		self.pos[0] += x_step
		self.pos[1] += y_step

		return self.pos

	def is_knot_adjacent(self, knot):
		my_pos_x, my_pos_y = self.pos[0], self.pos[1]
		other_pos_x, other_pos_y = knot.pos[0], knot.pos[1]

		if abs(other_pos_x - my_pos_x) <= 1 and abs(other_pos_y - my_pos_y) <= 1:
			return True
		else:
			return False

	def add_pos_to_history(self):
		if not self.pos in self.pos_history:
			self.pos_history.append(self.pos.copy())
		else:
			return None

	# Only works for 9_small.txt
	# def find_spaces_visited(self):
	# 	def helper(pos_list):
	# 		if len(pos_list) == 1:
	# 			return pos_list
	# 		else:
	# 			smaller_list = helper(pos_list[1:])

	# 			if pos_list[0] in smaller_list:
	# 				return smaller_list
	# 			else:
	# 				return [pos_list[0]] + smaller_list

	# 	return helper(self.pos_history)

	def __str__(self):
		return f'name: {self.name:} pos: ({self.pos})'


def make_knots(number):
	knots = []

	for i in range(number):
		if i == 0:
			knot = Knot('head')
		elif i == number-1:
			knot = Knot('tail')
			knots[i-1].tail = knot
		else:
			knot = Knot(i+1)
			knots[i-1].tail = knot

		knots.append(knot)

	return knots


def update_positions(knot):
	while knot:
		knot.add_pos_to_history()
		knot = knot.tail

	return None


def move_tails(head, tail, head_direction):
	def find_tail_move(move_type, shared_dim=None):
		if move_type == 'straight':
			if shared_dim == 'row':
				if 'U' in head_direction:
					tail_direction = 'U'
				else:
					tail_direction = 'D'
			elif shared_dim == 'col':
				if 'L' in head_direction:
					tail_direction = 'L'
				else:
					tail_direction = 'R'
		elif move_type == 'diagonal':
			head_higher = head.pos[1] > tail.pos[1]
			head_farther = head.pos[0] > tail.pos[0]

			match (head_higher, head_farther):
				case (True, True):
					tail_direction = 'UR'
				case (True, False):
					tail_direction = 'UL'
				case (False, False):
					tail_direction = 'DL'
				case (False, True):
					tail_direction = 'DR'
		else:
			return None

		return tail_direction

	if tail.is_knot_adjacent(head):
		return None
	else:
		if head.pos[0] == tail.pos[0]:
			tail_direction = find_tail_move('straight', 'row')
		elif head.pos[1] == tail.pos[1]:
			tail_direction = find_tail_move('straight', 'col')
		else:
			tail_direction = find_tail_move('diagonal')

		tail.move(tail_direction)

		if tail.name != 'tail':
			move_tails(tail, tail.tail, tail_direction)


def move_knots(head, head_moves):
	for move in head_moves:
		direction, steps = move.values()
		steps_taken = 0

		while steps_taken < steps:
			head.move(direction)
			move_tails(head, head.tail, direction)

			copy = head

			# Debug Prints:
			# while copy:
			# 	print(copy)
			# 	copy = copy.tail

			update_positions(head)
			steps_taken += 1


if __name__ == '__main__':
	rel_path_small = './9_small.txt'
	rel_path_small_two = './9_small_two.txt'
	rel_path_large = './9.txt'
	head_moves = parse_input(rel_path_large)

	number_of_knots = 10
	knots = make_knots(number_of_knots)
	head = knots[0]
	tail = knots[-1]

	move_knots(head, head_moves)

	tail_history = tail.pos_history
	print(len(tail_history))

	# Part 1:
	# Test for 9_small.txt
	# assert len(tail_history) == 13, f'small_test failed, got {len(tail_history)} instead'
	# Test for 9.txt
	# assert len(tail_history) == 6236, f'large_test failed, got {len(tail_history)} instead'

	# Test for 9_small_two.txt
	# assert len(tail_history) == 36, f'small_two test failed, got {len(tail_history)} instead'

	# print(tail_history)

	assert len(tail_history) == 2449, f'large_test failed, got {len(tail_history)} instead'