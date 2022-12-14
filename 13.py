import json

def parse_input(rel_path):
	packet_pairs = []

	with open(rel_path, mode='r', encoding='utf-8') as f:
		packet_pair = []

		for line in f.readlines():
			line = line.replace('\n', '')
			if line == '': continue

			packet = json.loads(line)

			if len(packet_pair) < 2:
				packet_pair.append(packet)
			
			if len(packet_pair) == 2:
				packet_pairs.append(packet_pair)
				packet_pair = []

	return packet_pairs


def print_packet_pairs(pairs):
	for count, pair in enumerate(pairs):
		print(f'Pair {count+1}: {pair}\n')

	return None


def check_order(pair):
	one, two = pair
	index = 0

	while index < len(one):
		if len(two)-1 < index:
			print('Right side ran out of items, inputs not in right order')
			return False

		one_value, one_type = one[index], type(one[index])
		two_value, two_type = two[index], type(two[index])

		if one_type != two_type:
			if one_type != list:
				one_value, one_type = [one_value], list
			else:
				two_value, two_type = [two_value], list

		if one_type == list:
			print(f'Checking left: {one_value} and right: {two_value}')
			subresult = check_order([one_value, two_value])
			if subresult != None: return subresult
		else:
			print(f'Compare {one_value} vs {two_value}')
			if one_value > two_value:
				print('Right side smaller, inputs not in right order')
				return False
			elif one_value < two_value:
				print('Left side smaller, inputs in right order')
				return True

		index += 1

	if len(one) < len(two):
		print('Left side ran out of items, inputs in right order')
		return True


def check_pairs(pairs):
	sum_indices = 0

	for count, pair in enumerate(pairs):
		print(f'Pair {count+1}')
		print(f'Left: {pair[0]}')
		print(f'Right: {pair[1]}')

		outcome = check_order(pair)

		print(f'Ordered Correctly: {outcome}\n')

		if outcome: sum_indices += (count+1)

	return sum_indices


def pairs_to_packets(pairs):
	packets = [] 

	for left, right in pairs:
		packets.append(left)
		packets.append(right)

	return packets


def add_dividers(packets):
	divider_one = [[2]]
	divider_two = [[6]]
	packets.append(divider_one)
	packets.append(divider_two)

	return packets


def order_packets_bubble(packets):
	end = len(packets)-1
	index = 0

	while index < end:
		left, right = packets[index:index+2]
		print(f'Checking left: {left} and right: {right}')
		ordered = check_order([left, right])

		if ordered or ordered == None:
			print('Correctly Ordered...')
			index += 1
		else:
			print('Swapping Orders\nRestarting...')
			packets[index] = right
			packets[index+1] = left
			index = 0

	return packets


def order_packets_merge(packets):
	if len(packets) > 1:
		midpoint = len(packets) // 2
		left = packets[:midpoint]
		right = packets[midpoint:]

		order_packets_merge(left)
		order_packets_merge(right)

		i = j = k = 0

		while i < len(left) and j < len(right):
			if check_order([left[i], right[j]]):
				packets[k] = left[i]
				i += 1
			else:
				packets[k] = right[j]
				j += 1

			k += 1

		while i < len(left):
			packets[k] = left[i]
			i += 1
			k += 1

		while j < len(right):
			packets[k] = right[j]
			j += 1
			k += 1


def find_decoder_key(ordered_packets):
	divider_one = [[2]]
	divider_two = [[6]]

	loc_one = ordered_packets.index(divider_one) + 1
	loc_two = ordered_packets.index(divider_two) + 1
	
	return loc_one * loc_two


if __name__ == '__main__':
	s = './13_small.txt'
	r = './13.txt'

	pairs = parse_input(r)
	packets = pairs_to_packets(pairs)
	packets = add_dividers(packets)

	order_packets_merge(packets)

	key = find_decoder_key(packets)
	print(key)

	# Part 1:
	# sum_indices = check_pairs(pairs)
	# print(sum_indices)

	# Part 1:
	# assert sum_indices == 13, f'expected 13 for 13_small.txt but got {sum_indices} instead'
	# assert sum_indices == 5252, f'expected 5252 for 13.txt but got {sum_indices} instead'

	# assert key == 140, f'expected 140 for 13_small,.txt but got {key} instead'
	assert key == 20592, f'expected 20592 for 13.txt but got {key} instead'