from experiment.loop import experiment_loop, averages_loop, sizes_loop
import sys
import os

# TODO: Slice out reading of the csv so you can process step by step the
#  power csv, which right now is 1GB+ for 2887 iterations of Kalman
#  and the print of the outputs

iterations = 20

hash_sizes = [120]
epsilons = [1.0]
mod_precisions = [10000]
attempts = [1]

thirtytwo_bit_stages = ["exp"]
sixtyfour_bit_stages = ["avg", "size"]
output_dir = "C:\\Users\\Dragos\\MasThesis_output"

if __name__ == "__main__":

    if sys.maxsize <= 2147483647:  # 32 bit
        print("\nDetected 32bit...")
        stages = thirtytwo_bit_stages
    else:  # 64 bit
        print("\nDetected 64bit...")
        stages = sixtyfour_bit_stages

    # Initial index:
    #  0 - start with baseline
    #  1 - skip the baseline, start with hash experiments
    start_with = len(stages)

    if len(sys.argv) < 2:
        exp_index = start_with
    else:
        exp_index = int(sys.argv[1])

    # The very first value in experiments, at index = 0, is baseline, so we
    # beforehand put useless values, as this "experiments" array with its
    # values is helpful only to configure hash experiments.
    experiments = []
    for s in stages:
        experiments.append(("baseline", s, 0, 0.0, 0, 1))

    for s in stages:
        for h in hash_sizes:
            for e in epsilons:
                for m in mod_precisions:
                    for a in attempts:
                        experiments.append(("hash", s, h, e, m, a))

    (exp, s, h, e, m, a) = experiments[exp_index]

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
        print("   MEMORY ERROR !!! Retrying at index {0}, stage {1}...  ".format(
            exp_index, s))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        exp_index -= 1

    if exp_index+1 < len(experiments):
        os.execv(sys.executable, [sys.executable,
                                  __file__] + [str(exp_index + 1)])
    else:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("   Ending at index {0}, stage {1}...  ".format(
            exp_index, s))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
