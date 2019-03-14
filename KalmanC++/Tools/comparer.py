
import sys

# TODO: do in floats

# def compare_cells(cell_1, cell_2):
#   intg_wrong_positions = []
#   flot_wrong_positions = []

#   if "." in cell_1:
#       (intg1, flot1) = cell_1.split(".")
#       (intg2, flot2) = cell_2.split(".")
#   else:
#       intg1 = cell_1
#       intg2 = cell_2

#   smaller_string_len = min(len(intg1), len(intg2))

#   for i in range(smaller_string_len - 1, -1, -1):
#       if intg1[i] != intg2[i]:
#           intg_wrong_positions.append(i)
#           print(i, intg1[i], intg2[i], "Wrong!")

#   intg_wrong_positions.sort()
#   if len(intg1) != len(intg2):
#       bigger_string_len = max(len(intg1), len(intg2))
#       intg_wrong_positions.extend(range(smaller_string_len+1, bigger_string_len+1))
#       print("Extended!")
    
#   print(intg1, intg2, intg_wrong_positions)

#   return intg_wrong_positions

# def compare_lines(line_1, line_2):
#   line_1_split = line_1.split(",")
#   line_2_split = line_2.split(",")

#   line_1_split = [cell.strip() for cell in line_1_split]
#   line_2_split = [cell.strip() for cell in line_2_split]

#   assert(len(line_1_split) == len(line_2_split))
#   #assert(len(line_1_split) == 2)

#   for i in range(len(line_1_split)):
#       ret = compare_cells(line_1_split[i], line_2_split[i])
    
#       #print(line_1_split[i], line_2_split[i], ret)

#   return 0

approximation_allowed = 0.000001

REDBG = "\033[0;37;41m"
CLEAR = "\033[0;0;0m"

def compare_cells(cell_1, cell_2):
    cell_1 = cell_1.strip()
    cell_2 = cell_2.strip()

    try:
        cell1_flt = float(cell_1)
    except ValueError:
        print("Cannot convert cell_1 " + cell_1 + "to float")
    
    try:
        cell2_flt = float(cell_2)
    except ValueError:
        print("Cannot convert cell_2 " + cell_2 + "to float")

    if abs(cell1_flt - cell2_flt) < approximation_allowed:
        return 0
    else:
        #print(cell1_flt, cell2_flt)
        return 1

def compare_lines(line_1, line_2):
    line_1_split = line_1.split(",")
    line_2_split = line_2.split(",")

    different = 0.0
    all_iterations = 0

    for i in range(len(line_1_split)):
        cell_1 = line_1_split[i]
        cell_2 = line_2_split[i]

        ret = compare_cells(cell_1, cell_2)

        if ret > 0:
            line_1_split.pop(i)
            line_1_split.insert(i, REDBG + cell_1 + CLEAR)
            line_2_split.pop(i)
            line_2_split.insert(i, REDBG + cell_2 + CLEAR)

            line_1 = ",".join(line_1_split)
            line_2 = ",".join(line_2_split)

        different = different + ret
        all_iterations = all_iterations + 1

    if different > 0:
        print(line_1.strip())
        print(line_2.strip())

    return different / all_iterations

#iterations = 1000

print("")

with open(sys.argv[1], "r") as origf:
    with open(sys.argv[2], "r") as compf:
        line_1 = " "
        line_2 = " "

        different = 0
        iteration = 0
        approximation = 0.0

        while line_1 and line_2: 
        #for i in range(iterations):

            line_1 = origf.readline()
            line_2 = compf.readline()

            line_1 = line_1.strip()
            line_2 = line_2.strip()

            if len(line_1) == 0: continue
            if len(line_2) == 0: continue

            ret = compare_lines(line_1, line_2)
            approximation += ret
            #print(str(approximation), end=' ')
            if (ret > 0): different += 1
            iteration += 1

            break

        print("")

        if iteration > 0:
            print(str(round(approximation * 100 / iteration, 6)) + "%")
            print("There are " + str(different) + " different lines")
        else:
            print("")
            print(0)

