with open('./1.txt', mode='r', encoding='utf-8') as f:
	calorie_list = f.readlines()

summed_list = []
total_count = 0

for count in calorie_list:
	if len(count) == 1:
		summed_list.append(total_count)
		total_count = 0
	else:
		total_count += int(count[:-1])

top_three_elves = sorted(summed_list, reverse=True)[:3]

print(sum(top_three_elves))