def parse_input(rel_path):
	instructions = []

	with open(rel_path, mode='r', encoding='utf-8') as f:
		for line in f.readlines():
			line = line.replace('\n', '')
			instructions.append(line)

	return instructions


def find_signal_strengths(instructions, start, interval):
	def calc_strength():
		if cycle % interval == start: 
			strength = cycle * x_register
			sig_strengths.append(strength)
		else:
			return None

	sig_strengths = []
	cycle = 1
	x_register = 1

	for command in instructions:
		cycle +=1 
		calc_strength()

		if command.startswith('addx'):
			cycle += 1
			x_register += int(command.split(' ')[-1])
			calc_strength()

	return sig_strengths


def draw_pixels(instructions):
	def draw_pixel():
		if abs(x_register - (cycle % interval -1)) <= 1:
			print('#', end='')
		else:
			print('.', end='')

		if cycle % interval == 0:
			print()

	interval = 40
	cycle = 1
	x_register = 1

	for command in instructions:
		if cycle == 1:
			draw_pixel()

		cycle += 1
		draw_pixel()

		if command.startswith('addx'):
			cycle += 1
			x_register += int(command.split(' ')[-1])
			draw_pixel()


if __name__ == '__main__':
	s = './10_small.txt'
	r = './10.txt'

	instructions = parse_input(r)
	sig_strengths = find_signal_strengths(instructions, 20, 40)
	sum_sig_strengths = sum(sig_strengths)
	print(sum_sig_strengths)

	draw_pixels(instructions)

	# Part 1:
	# Test for 10_small.txt
	# assert sum_sig_strengths == 13140, f'expected 13140 but got {sum_sig_strengths} instead'
	# Test for 10.txt
	assert sum_sig_strengths == 17380, f'expected 17380 but got {sum_sig_strengths} instead'