with open('./3.txt', mode='r', encoding='utf-8') as f:
	rucksack_list = f.readlines()

priority_sum = 0

# Part 1:
# def find_shared_type(left, right):
# 	for letter in left:
# 		if letter in right:
# 			return letter

def find_priority(letter):
	ascii_num = ord(letter)

	if letter.lower() == letter:
		shift = 96
	else:
		shift = 38

	return ascii_num - shift

# Part 1:
# for rucksack in rucksack_list:
# 	num_items = len(rucksack)-1
# 	halfway_mark = int(num_items/2)
# 	left_compartment = rucksack[:halfway_mark]
# 	right_compartment = rucksack[halfway_mark:]

# 	priority_sum += find_priority(find_shared_type(left_compartment, right_compartment))

def convert_to_unique(rucksack, accu):
	if rucksack == '':
		return [letter for letter in accu if letter != '\n']
	elif rucksack[0] not in accu:
		return convert_to_unique(rucksack[1:], accu + [rucksack[0]])
	else:
		return convert_to_unique(rucksack[1:], accu)

i = 0
while i < len(rucksack_list):
	group_one = convert_to_unique(rucksack_list[i], [])
	group_two = convert_to_unique(rucksack_list[i+1], [])
	group_three = convert_to_unique(rucksack_list[i+2], [])

	for letter in group_one:
		if letter in group_two and letter in group_three:
			priority_sum += find_priority(letter)

	i += 3

print(priority_sum)