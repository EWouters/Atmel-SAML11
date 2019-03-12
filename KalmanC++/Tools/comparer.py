
import sys

# TODO: do in floats

def compare_cells(cell_1, cell_2):
	intg_wrong_positions = []
	flot_wrong_positions = []

	if "." in cell_1:
		(intg1, flot1) = cell_1.split(".")
		(intg2, flot2) = cell_2.split(".")
	else:
		intg1 = cell_1
		intg2 = cell_2

	smaller_string_len = min(len(intg1), len(intg2))

	for i in range(smaller_string_len - 1, -1, -1):
		if intg1[i] != intg2[i]:
			intg_wrong_positions.append(i)

	intg_wrong_positions.sort()
	if len(intg1) != len(intg2):
		bigger_string_len = max(len(intg1), len(intg2))
		intg_wrong_positions.extend(range(smaller_string_len, bigger_string_len))
	
	return intg_wrong_positions

def compare_lines(line_1, line_2):
	line_1_split = line_1.split(",")
	line_2_split = line_2.split(",")

	line_1_split = [cell.strip() for cell in line_1_split]
	line_2_split = [cell.strip() for cell in line_2_split]

	assert(len(line_1_split) == len(line_2_split))
	#assert(len(line_1_split) == 2)

	for i in range(len(line_1_split)):
		ret = compare_cells(line_1_split[i], line_2_split[i])
	
		#print(cell1, cell2, ret)

	return 0

with open(sys.argv[1], "r") as origf:
	index_1 = 0
	index_2 = 0

	with open(sys.argv[2], "r") as compf:

		line_1 = origf.readline()
		line_2 = compf.readline()

		approximation = compare_lines(line_1, line_2)

		index_1 += 1
		index_2 += 1

