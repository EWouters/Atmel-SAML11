from experiment.loop import loop
import sys
import os

initial = 1  # 1 = Don't start with baseline

iterations = 2887

hash_sizes = [120]
epsilon = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
mod_precision = [10000]

values = [(0, 0, 0)]

for i in range(len(hash_sizes)):
    for j in range(len(epsilon)):
        for k in range(len(mod_precision)):
            values.append((hash_sizes[i], epsilon[j], mod_precision[k]))

if __name__ == "__main__":

    if len(sys.argv) < 2:
        to_do = initial
    else:
        to_do = int(sys.argv[1])

    print("At index {0}...".format(to_do))

    if to_do == 0:
        pass
        # print("Baseline:")
        #loop("baseline", iterations, attempt=1, output_dir="output")
    else:
        (h, e, m) = values[to_do]

        try:
            print("Hash {0}, Epsilon {1}, Mod precision {2}:".format(h, e, m))
            loop("hash", hash_size=h, epsilon=e, mod_precision=m, iterations=iterations,
                 attempt=1, program=True, output_dir="C:\\Users\\Dragos\\MasThesis_output")
        except MemoryError:
            print("Retrying at index {0}\n".format(to_do))
            to_do -= 1

        if to_do+1 < len(values):
            os.execv(sys.executable, [sys.executable,
                                      __file__] + [str(to_do + 1)])
        else:
            print("Ending at index {0}...".format(to_do))
