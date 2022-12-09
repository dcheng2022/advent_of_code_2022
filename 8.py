forest = []


with open('./8.txt', mode='r', encoding='utf-8') as f:
	for line in f.readlines():
		line = line.replace('\n', '')
		line = [int(n) for n in list(line)]
		forest.append(line)


def find_forest_ends(forest):
	return (len(forest)-1, len(forest[0])-1)


# Part 1:
# def is_tree_visible(forest, height, m, n):
# 	def is_other_tree_taller(row, col):
# 		other_height = forest[row][col]

# 		if other_height >= height:
# 			return True

# 	max_m, max_n = find_forest_ends(forest)
# 	sides = {
# 		'left': (m, 0, 1),
# 		'top': (0, n, 1),
# 		'right': (m, max_n, -1),
# 		'bot': (max_m, n, -1)
# 	}
# 	blocked_sides = 0

# 	for side, markers in sides.items():
# 		row, col, step = markers

# 		if side == 'top' or side == 'bot':
# 			while row != m:
# 				if is_other_tree_taller(row, col):
# 					blocked_sides += 1
# 					break

# 				row += step 
# 		else:
# 			while col != n:
# 				if is_other_tree_taller(row, col):
# 					blocked_sides += 1
# 					break

# 				col += step

# 	if blocked_sides < 4:
# 		return True


# Part 1:
# def find_num_visible(forest):
# 	num_visible = 0

# 	for m, row in enumerate(forest):
# 		for n, tree in enumerate(row):
# 			if is_tree_visible(forest, tree, m, n):
# 				num_visible += 1

# 	return num_visible


def find_tree_visibility(forest, height, m, n):
	def is_other_tree_taller(row, col):
		other_height = forest[row][col]

		if other_height >= height:
			return True

	max_m, max_n = find_forest_ends(forest)

	sides = {
		'left': (m, n-1, -1),
		'top': (m-1, n, -1),
		'right': (m, n+1, 1),
		'bot': (m+1, n, 1)
	}
	trees_per_side = {}

	for side, markers in sides.items():
		row, col, step = markers
		trees_per_side[side] = 0

		if side == 'top' or side == 'bot':
			while row >= 0 and row <= max_m:
				trees_per_side[side] += 1
				if is_other_tree_taller(row, col):
					break

				row += step 
		else:
			while col >= 0 and col <= max_n:
				trees_per_side[side] += 1
				if is_other_tree_taller(row, col):
					break

				col += step

	return trees_per_side


def find_tree_scores(forest):
	def calc_score(values):
		if values == []:
			return 1
		else:
			return values[0] * calc_score(values[1:])

	scores = []

	for m, row in enumerate(forest):
		for n, tree in enumerate(row):
			trees_per_side = find_tree_visibility(forest, tree, m, n)
			scores.append(calc_score(list(trees_per_side.values())))

	return scores


if __name__ == '__main__':
	scores = find_tree_scores(forest)
	highest_score = sorted(scores, reverse=True)[0]
	print(highest_score)

	# Part 1:
	# num_visible = find_num_visible(forest)
	# print(num_visible)
	# Test for 8_small.txt
	# assert num_visible == 21, f'we expected 21 but got {num_visible} instead'
	# Test for 8.txt
	# assert num_visible == 1662, f'we expected 1662 but got {num_visible} instead'