from collections import defaultdict

print('Day 7 of Advent of Code!')

DIR_PRV = '..'
DIR_HOME = '/'

CMD_CD = 'cd'
CMD_LS = 'ls'
CMD_DIR = 'dir'

CMDS = {CMD_CD, CMD_LS, CMD_DIR}

TOTAL_SPACE = 70_000_000
REQUIRED_SPACE = 30_000_000

def calculate_folder_sizes(commands):
    folder_sizes = defaultdict(int)
    current_path = []

    for line in commands:
        if line.split()[1] in CMDS:
            cmd = line.split()[1]

        if cmd == CMD_CD:
            new_dir = line.split().pop()
            if new_dir == DIR_PRV:
                current_path.pop()
            elif new_dir == DIR_HOME:
                current_path = [DIR_HOME]
            else:
                current_path.append(new_dir)

        else:
            value, name = line.split()
            if value.isnumeric():
                size = int(value)
                for i in range(1, len(current_path)+1):
                    pathname = '/'.join(current_path[:i])
                    folder_sizes[pathname] += size               

    return folder_sizes


test_data = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k'''

print('Testing...')
raw_data = test_data.splitlines()
folder_sizes = calculate_folder_sizes(raw_data)
unused_space = TOTAL_SPACE - folder_sizes['/']
to_free = REQUIRED_SPACE - unused_space
deletion_candidates = sorted([folder for folder in folder_sizes if folder_sizes[folder] >= to_free], key=lambda folder: folder_sizes[folder])
print('Folders below 100k:', sum(folder_sizes[folder] for folder in folder_sizes if folder_sizes[folder] <= 100_000) == 95437)
print('Minimum size to delete:', folder_sizes[deletion_candidates[0]] == 24933642)

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read().splitlines()
    folder_sizes = calculate_folder_sizes(raw_data)
    unused_space = TOTAL_SPACE - folder_sizes['/']
    to_free = REQUIRED_SPACE - unused_space
    deletion_candidates = sorted([folder for folder in folder_sizes if folder_sizes[folder] >= to_free], key=lambda folder: folder_sizes[folder])
    print('Folders below 100k:', sum(folder_sizes[folder] for folder in folder_sizes if folder_sizes[folder] <= 100_000))
    print('Minimum size to delete:', folder_sizes[deletion_candidates[0]])
