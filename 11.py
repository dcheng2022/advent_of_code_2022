import operator
import re


def define_operator(operation):
		operations = {
			'+': operator.add,
			'-': operator.sub,
			'/': operator.truediv,
			'*': operator.mul,
		}
		
		return operations[operation]


def define_operand(operand):
	num_pattern = re.compile(r'\d+')

	if num_pattern.search(operand):
		return int(operand)
	else:
		return False


def parse_input(rel_path):
	monkeys = []

	with open(rel_path, mode='r', encoding='utf-8') as f:
		lines = [line.replace('\n', '') for line in f.readlines()]
		num_lines = len(lines)
		num_pattern = re.compile(r'\d+')
		operation_pattern = re.compile(r'[+-/*]{1} .+')
		i = 0

		while i < num_lines:
			name = num_pattern.search(lines[i]).group()
			items = [int(num) for num in num_pattern.findall(lines[i+1])]
			operator, operand = operation_pattern.search(lines[i+2]).group().split(' ')
			operator, operand = define_operator(operator), define_operand(operand)
			test, true_monkey, false_monkey = [int(num) for num in num_pattern.findall(''.join(lines[i+3:i+6]))]

			monkeys.append(Monkey(monkeys, name, items, operator, operand, test, true_monkey, false_monkey))
			i += 7

	return monkeys


class Monkey:
	divisors = []

	def __init__(self, monkeys, name, items, operator, operand, test, true_monkey, false_monkey):
		self.monkeys = monkeys
		self.name = name
		self.items = items
		self.operator = operator
		self.operand = operand
		self.test = test
		self.true_monkey = true_monkey
		self.false_monkey = false_monkey
		self.items_inspected = 0

		Monkey.divisors.append(self.test)

	def throw_items(self):
		def calculate_div_product(divs, product):
			if divs == []:
				return product
			else:
				return calculate_div_product(divs[1:], divs[0] * product)

		div_product = calculate_div_product(Monkey.divisors, 1)

		while self.items:
			old_worry = self.items[0]

			if self.operand:
				operand = self.operand
			else:
				operand = old_worry

			# Part 2:
			# Used hint in order to keep worry level "manageable"
			# https://i.redd.it/zrfbgyikac5a1.png
			new_worry = self.operator(old_worry, operand) % div_product

			# Part 1:
			# new_worry = new_worry // 3

			if new_worry % self.test == 0:
				monkeys[self.true_monkey].items.append(new_worry)
			else:
				monkeys[self.false_monkey].items.append(new_worry)

			self.items_inspected += 1
			self.items = self.items[1:]

	def __str__(self):
		print(f'Monkey {self.name}:')
		print(f'\tStarting items: {self.items}')
		print(f'\tOperation: new = old {self.operator} {self.operand}')
		print(f'\tTest: divisible by {self.test}')
		print(f'\t\t If true: throw to monkey {self.true_monkey}')
		print(f'\t\t If false: throw to monkey {self.false_monkey}')
		return ''


def play_keep_away(monkeys, rounds):
	r = 0

	while r < rounds:
		for monkey in monkeys:
			monkey.throw_items()

		r += 1

	return None


def find_monkey_business(monkeys):
	monkey_passes = sorted(monkeys, key=lambda x:x.items_inspected, reverse=True)

	return monkey_passes[0].items_inspected * monkey_passes[1].items_inspected


if __name__ == '__main__':
	s = './11_small.txt'
	r = './11.txt'

	monkeys = parse_input(r)
	rounds = 10000

	play_keep_away(monkeys, rounds)

	monkey_business = find_monkey_business(monkeys)
	print(monkey_business)

	# Part 1:
	# Test for 11_small.txt
	# assert monkey_business == 10605, f'expected 10605 for 11_small.txt but got {monkey_business} instead'
	# Test for 11.txt
	# assert monkey_business == 50172, f'expected 50172 for 11.txt but got {monkey_business} instead'

	# Test for 11_small.txt
	# assert monkey_business == 2713310158, f'expected 2713310158 for 11_small.txt but got {monkey_business} instead'