from experiment.loops import experiment_loop, averages_loop, sizes_loop
import sys
import os
import numpy as np
from time import time, sleep

# TODO: Slice out reading of the csv so you can process step by step the
#  power csv, which right now is 1GB+ for 2887 iterations of Kalman
#  and the print of the outputs

iterations = 2887

hash_sizes = [120]
#epsilons = [0.1]
epsilons = [x/10 for x in list(range(1, 71, 1))] + [x/100 for x in [1, 5]]
mod_precisions = [10000]
attempts = [3]

# Attempt 3:
# [x/10 for x in list(range(1, 71, 1))] + [x/100 for x in [1, 5]]

thirtytwo_bit_stages = ["exp"]
sixtyfour_bit_stages = ["avg", "size"]
output_dir = "C:\\Users\\Dragos\\MasThesis_output"


def touch(fpath, times=None):
    fhandle = open(fpath, 'a')
    try:
        os.utime(fpath, times)
    finally:
        fhandle.close()


def exist(fpath):
    return os.path.isfile(fpath)


def remove(fpath):
    os.remove(fpath)


if __name__ == "__main__":

    if sys.maxsize <= 2147483647:  # 32 bit
        print("\nDetected 32bit...")
        stages = thirtytwo_bit_stages
    else:  # 64 bit
        print("\nDetected 64bit...")
        stages = sixtyfour_bit_stages

    # Initial index:
    #  0 - start with baseline
    #  len(stages) * len(attempts) - skip the baseline, start with hash experiments
    start_with = len(stages) * len(attempts)

    if len(sys.argv) < 2:
        exp_index = start_with
    else:
        exp_index = int(sys.argv[1])

    # The very first value in experiments, at index = 0, is baseline, so we
    # beforehand put useless values, as this "experiments" array with its
    # values is helpful only to configure hash experiments.
    experiments = []
    for s in stages:
        for a in attempts:
            experiments.append(("baseline", s, 0, 0.0, 0, a))

    for s in stages:
        for h in hash_sizes:
            for e in epsilons:
                for m in mod_precisions:
                    for a in attempts:
                        experiments.append(("hash", s, h, e, m, a))

    (exp, s, h, e, m, a) = experiments[exp_index]

    # We have to have a file as a mutex, since we're doing experiments
    # on separate 32bit and 64bit Python instantiations that need to
    # synchronise somehow (one must start after the other is finished)
    lock_file = os.path.join(output_dir, "lock")
    if exp_index == start_with:
        if exist(lock_file):
            print(
                ("Lock file exists at '{0}', waiting for " +
                 "removal...").format(lock_file))
            while (exist(lock_file)):
                sleep(5)
        touch(lock_file)

    print("")
    print("")
    print("#############################")
    print("   At index {0}, stage '{1}' ".format(exp_index, s))
    print("#############################")
    print("")

    print(
        "Experiment {0}, Hash {1}, Epsilon {2}, Mod precision {3}, Attempt {4}:".format(exp, h, e, m, a))
    print("---")

    try:
        if s == "exp":
            touch(os.path.join(output_dir, "lock"))
            experiment_loop(exp, hash_size=h, epsilon=e,
                            mod_precision=m, iterations=iterations,
                            attempt=a, program=True,
                            output_dir=output_dir, verbose=2)

        elif s == "avg":
            averages_loop(exp, hash_size=h, epsilon=e,
                          mod_precision=m, iterations=iterations,
                          attempt=a,
                          output_dir=output_dir,
                          verbose=2)

        elif s == "size":
            sizes_loop(exp, hash_size=h, epsilon=e,
                       mod_precision=m, iterations=iterations,
                       attempt=a,
                       output_dir=output_dir, verbose=2)
        else:
            raise ValueError("Got unknown stage name '{0}'".format(s))

    except MemoryError:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(("   MEMORY ERROR !!! Retrying at index {0}, " +
               "stage {1}...  ").format(exp_index, s))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        exp_index -= 1

    if (exp_index < (len(experiments) - 1)):
        os.execv(sys.executable, [sys.executable,
                                  __file__] + [str(exp_index + 1)])
    else:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("   Ending at index {0}, stage {1}...  ".format(
            exp_index, s))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    # Deleting the lock-file
    if (exp_index == (len(experiments) - 1)):
        remove(lock_file)
        print("Lock file '{0}' removed...".format(lock_file))
