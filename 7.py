import operator

with open('./7.txt', mode='r', encoding='utf-8') as f:
	def parse_file(file_lines):
		directories = {}
		path = []
		level = -1

		for line in file_lines:
			line = line.replace('\n', '')

			if line.startswith('$ cd'):
				if line.endswith('..'):
					level -= 1
					path = path[:-1]
				else:
					level += 1
					name = line.split(' ')[-1]
					path.append(name)

					if directories.get(level):
						directories[level].append({'path': path.copy(), 'name': name, 'contents': []})
					else:
						directories[level] = [{'path': path.copy(), 'name': name, 'contents': []}]

			elif not line.startswith('$'):
				directory = [d for d in directories[level] if d['name'] == name and d['path'] == path][0]
				directory['contents'].append(line)

		return directories

	directories = parse_file(f.readlines())


class Node:
	def __init__(self, name):
		self.name = name
		self.children = []

	def add_children(self, child):
		self.children.append(child)

	def __str__(self):
		return self.name


class Tree:
	def __init__(self, root):
		self.root = root

	def find_dir(self, name, path):
		def helper(node, current_path):
			if node.name == name and current_path == path:
				return node
			else:
				for child in node.children:
					if type(child) == Node:
						result = helper(child, current_path + [child.name])

						if result: return result

		return helper(self.root, [self.root.name])

	def find_dir_size(self, name, path):
		def helper(node, total_size):
			for child in node.children:
				if type(child) == Node:
					total_size += helper(child, 0)
				else:
					total_size += child['size']

			return total_size

		directory = self.find_dir(name, path)
		return helper(directory, 0)

	# Part 1:
	# def find_smaller_dirs(self, directories, size):
	# 	smaller_dirs = []
	# 	for dirs in directories.values():
	# 		for directory in dirs:
	# 			dir_name = directory['name']
	# 			dir_path = directory['path']
	# 			dir_size = self.find_dir_size(dir_name, dir_path)

	# 			if dir_size <= size:
	# 				smaller_dirs.append({'name': dir_name, 'size': dir_size})

	# 	return smaller_dirs

	def find_dirs_by_size(self, directories, size, inequality):
		operators = {
			'>': operator.gt,
			'<': operator.lt,
			'>=': operator.ge,
			'<=': operator.le
		}
		result_dirs = []
		
		for dirs in directories.values():
			for directory in dirs:
				dir_name = directory['name']
				dir_path = directory['path']
				dir_size = self.find_dir_size(dir_name, dir_path)

				if operators[inequality](dir_size, size):
					result_dirs.append({'name': dir_name, 'size': dir_size})

		return result_dirs

	def __str__(self):
		def print_node(node, parent):
			print(f'{parent}: {node}')

			for child in node.children:
				if type(child) == Node:
					print_node(child, node)
				else:
					print(f'{node}: {child}')
		
		print_node(self.root, 'root')
		return ''


def make_tree(directories):
	def helper(node, current_path, current_level):
		node_directory = [d for d in directories[current_level] if d['name'] == node.name and d['path'] == current_path][0]

		for content in node_directory['contents']:
			if content.startswith('dir'):
				name = content.split(' ')[-1]
				child_node = Node(name)
				node.add_children(child_node)
				helper(child_node, current_path + [child_node.name], current_level + 1)
			else:
				file_size, file_name = content.split(' ')
				node.add_children({'name': file_name, 'size': int(file_size)})

	root = Node('/')
	helper(root, ['/'], 0)

	return Tree(root)


if __name__ == '__main__':
	file_system = make_tree(directories)
	root_path = ['/']
	total_disk_space = 70000000
	update_size = 30000000

	filled_space = file_system.find_dir_size('/', root_path)
	remaining_space = total_disk_space - filled_space
	needed_space = update_size - remaining_space

	result_dirs = file_system.find_dirs_by_size(directories, needed_space, '>=')
	print(sorted(result_dirs, key=lambda x: x['size'])[0])

	# Prints:
	# print(file_system)
	# for level, d in directories.items():
	# 	print(f'level: {level} d: {d}\n')
	#
	# Part 1:
	# Tests for 7_small.txt
	# size_tests = (
	# 	('e', ['/', 'a', 'e'], 584),
	# 	('a', ['/', 'a'], 94853),
	# 	('d', ['/', 'd'], 24933642),
	# 	('/', ['/'], 48381165)
	# )
	#
	# Tests for 7.txt
	# size_tests = (
	# 	('cmvvd', 9, 193725)
	# )
	# for dir_name, path, size in size_tests:
	# 	calculated_size = file_system.find_dir_size(dir_name, path)
	#
	# 	assert calculated_size == size, f'we expected {size} but got {calculated_size} instead'
	#
	# result_dirs = file_system.find_dirs_by_size(directories, 100000, '<=')
	# print(sum([d['size'] for d in result_dirs]))
	# assert sum([d['size'] for d in result_dirs]) == 1427048