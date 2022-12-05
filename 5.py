import re


crate_rows = []
operation_list = []


with open('./5.txt', mode='r', encoding='utf-8') as f:
	lines = [line.replace('\n', '') for line in f.readlines() if line != '\n']

	crate_pattern = re.compile(r'[\[A-Z\]]+')
	operation_pattern = re.compile(r'move \d+ from \d+ to \d+')

	for line in lines:
		if crate_pattern.search(line):
			crate_rows.append(line)
		elif operation_pattern.match(line):
			operation_list.append(line)
		else:
			num_cols = int(line.strip()[-1])


class Stack:
	def __init__(self):
		self.stack = []

	def top(self):
		return self.stack[-1]

	def pop(self):
		removed = self.top()
		self.stack = self.stack[:-1]

		return removed

	def push(self, item):
		self.stack.append(item)

		return item

	def __str__(self):
		return f'{str(self.stack):100}'


def instantiate_stacks(num_stacks):
	return [Stack() for i in range(num_stacks)]


def fill_stacks(stacks, crate_rows):
	col_length = 4

	for row in crate_rows[::-1]:
		matches = crate_pattern.finditer(row)

		for match in matches:
			crate = match.group()
			char_pos = match.start()
			s_index = int(char_pos/col_length)

			stacks[s_index].push(crate)


def complete_operations(stacks, operation_list):
	num_match = re.compile(r'\d+')

	for operation in operation_list:
		operation_nums = [int(match) for match in num_match.findall(operation)]
		num_to_move, start_p, end_p = operation_nums

		# Part 1:
		# for i in range(num_to_move):
		# 	stacks[end_p-1].push(stacks[start_p-1].pop())

		crates_to_move = []
		
		for i in range(num_to_move):
			crates_to_move.append(stacks[start_p-1].pop())
		for crate in crates_to_move[::-1]:
			stacks[end_p-1].push(crate)


if __name__ == '__main__':
	stacks = instantiate_stacks(num_cols)
	fill_stacks(stacks, crate_rows)

	complete_operations(stacks, operation_list)

	top_crates = []
	for stack in stacks:
		top_crates.append(stack.top()[1])
	print(''.join(top_crates))
