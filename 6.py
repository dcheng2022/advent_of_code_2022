with open ('./6.txt', mode='r', encoding='utf-8') as f:
	datastream = f.readline()

def find_marker(datastream):

	def is_unique(buffer):
		if len(buffer) == 1:
			return True
		elif buffer[0] in buffer[1:]:
			return False
		else:
			return is_unique(buffer[1:])

	buffer = []
	# Part 1:
	# marker_length = 4
	marker_length = 14

	for i in range(len(datastream)):
		char = datastream[i]

		if len(buffer) < marker_length:
			buffer.append(char)
		else:
			if is_unique(buffer):
				return i
			else:
				buffer = buffer[1:] + [char]

if __name__ == '__main__':
	marker = find_marker(datastream)
	print(marker)

	# Part 1:
	# test_markers = {
	# 'bvwbjplbgvbhsrlpgdmjqwftvncz': 5,
	# 'nppdvjthqldpwncqszvftbrmjlhg': 6,
	# 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg': 10,
	# 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw': 11
	# }

	test_markers = {
	'mjqjpqmgbljsphdztnvjfqwrcgsmlb': 19,
	'bvwbjplbgvbhsrlpgdmjqwftvncz': 23,
	'nppdvjthqldpwncqszvftbrmjlhg': 23,
	'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg': 29,
	'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw': 26
	}

	for m, p in test_markers.items():
		output = find_marker(m)

		assert output == p, f'expected {p}, got {output} instead'