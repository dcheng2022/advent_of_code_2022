with open('./4.txt', mode='r', encoding='utf-8') as f:
	pair_list = [pair.replace('\n', '') for pair in f.readlines()]

overlapping_sections = 0

def do_sections_overlap(lsec, rsec):
	lstart, lend = [int(num) for num in lsec.split('-')]
	rstart, rend = [int(num) for num in rsec.split('-')]

	# Part 1:
	# if lstart >= rstart and lend <= rend:
	# 	return True
	# elif rstart >= lstart and rend <= lend:
	# 	return True
	# else:
	# 	return False

	if rstart >= lstart and rstart <= lend:
		return True
	elif lstart >= rstart and lstart <= rend:
		return True
	else:
		return False

for pair in pair_list:
	left_section, right_section = pair.split(',')

	if do_sections_overlap(left_section, right_section):
		overlapping_sections += 1

print(overlapping_sections)

if __name__ == '__main__':
	assert do_sections_overlap('4-9', '4-4') == True, 'we expected this to be true'
	assert do_sections_overlap('1-6', '14-24') == False, 'we expected this to be false'
	assert do_sections_overlap('2-6', '7-10') == False, 'we expected this to be false'
	assert do_sections_overlap('5-7', '7-9') == True, 'we expected this to be true'
	assert do_sections_overlap('2-8', '3-7') == True, 'we expected this to be true'
	assert do_sections_overlap('6-6', '4-6') == True, 'we expected this to be true'
	assert do_sections_overlap('2-6', '4-8') == True, 'we expected this to be true'