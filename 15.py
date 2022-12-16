import re

def parse_input(rel_path):
	sensors = []
	number_pattern = re.compile(r'-*\d+')

	with open(rel_path, mode='r', encoding='utf-8') as f:
		for line in f.readlines():
			numbers = [int(n) for n in number_pattern.findall(line)]
			sensor_x, sensor_y, beacon_x, beacon_y = numbers

			sensors.append(Sensor(sensor_x, sensor_y, beacon_x, beacon_y))

	return sensors


class Sensor:
	def __init__(self, x, y, beacon_x, beacon_y):
		self.x = x
		self.y = y
		self.pos = [self.x, self.y]
		self.beacon_x = beacon_x
		self.beacon_y = beacon_y
		self.beacon_pos = [self.beacon_x, self.beacon_y]
		self.distance = abs(self.y - self.beacon_y) + abs(self.x - self.beacon_x)

	def position_in_range(self, loc):
		loc_x, loc_y = loc
		loc_distance = abs(loc_y - self.y) + abs(loc_x - self.x)

		if loc_distance <= self.distance:
			return True
		else:
			return False

	def __str__(self):
		return f'Sensor Location: {self.pos} Beacon Location: {self.beacon_pos} Distance to Beacon: {self.distance}'


def find_overall_dimensions(sensors):
	min_x = min_y = float('inf')
	max_x = max_y = -float('inf')

	for sensor in sensors:
		sensor_x, sensor_y = sensor.pos
		distance = sensor.distance
		beacon_x, beacon_y = sensor.beacon_pos

		if sensor_x - distance < min_x or beacon_x < min_x:
			min_x = min(sensor_x - distance, beacon_x)
		
		if sensor_x + distance > max_x or beacon_x > max_x:
			max_x = max(sensor_x + distance, beacon_x)

		if sensor_y - distance < min_y or beacon_y < min_y:
			min_y = min(sensor_y - distance, beacon_y)
		
		if sensor_y + distance > max_y or beacon_y > max_y:
			max_y = max(sensor_y + distance, beacon_y)

	return [min_x, max_x, min_y, max_y]


def check_row_coverage(sensors, dimensions, row):
	x, x_end = dimensions[0], dimensions[1]
	covered = 0

	while x < x_end:
		pos = [x, row]

		for sensor in sensors:
			if sensor.position_in_range(pos) and sensor.pos != pos and sensor.beacon_pos != pos:
				covered += 1
				break

		x += 1

	return covered


def find_uncovered_pos(sensors, dimensions):
	def check_row(row):
		x = 0

		while x <= x_end:
			pos = [x, row]
			in_sensor_range = list(map(lambda x:x.position_in_range(pos), sensors))

			if any(in_sensor_range):
				sensor = sensors[in_sensor_range.index(True)]
				y_distance = abs(sensor.y - row)
				farthest_x = sensor.distance - y_distance + sensor.x

				x += (farthest_x - x + 1)
			else:
				return pos

		return False

	x_end, y_end = dimensions
	y = 0

	while y <= y_end:
		row_result = check_row(y)

		if row_result: return row_result

		y += 1


	return None


def calculate_tuning_frequency(position):
	x, y = position

	return 4000000 * x + y


if __name__ == '__main__':
	s = './15_small.txt'
	r = './15.txt'

	sensors = parse_input(r)

	# Part 1:
	# dimensions = find_overall_dimensions(sensors)
	# print(dimensions)
	# row = 10
	# covered = check_row_coverage(sensors, dimensions, row)
	# print(covered)

	# dimensions = [20, 20]
	dimensions = [4000000, 4000000]
	uncovered = find_uncovered_pos(sensors, dimensions)
	frequency = calculate_tuning_frequency(uncovered)
	print(frequency)

	# Part 1:
	# assert covered == 26, f'expected 26 positions ruled out for 15_small.txt with row=10, got {covered} instead'
	# assert covered = 4424278, f'expected 4424278 positions ruled out for 15.txt with row=2000000, got {covered} instead'

	# assert frequency == 56000011, f'expected 56000011 as frequency for 15_small.txt, got {frequency} instead'
	assert frequency == 10382630753392, f'expected 10382630753392 as frequency for 15.txt, got {frequency} instead'