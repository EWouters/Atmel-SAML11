from experiment.loop import experiment_loop, averages_loop
import sys
import os

iterations = 2887

hash_sizes = [120]
epsilons = [1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
mod_precisions = [10000]
attempts = [1]
stage = "avg"
output_dir = "C:\\Users\\Dragos\\MasThesis_output"

# Initial index:
#  0 - start with baseline
#  1 - skip the baseline, start with hash experiments
start_with = 1

if __name__ == "__main__":

    if len(sys.argv) < 2:
        exp_index = start_with
    else:
        exp_index = int(sys.argv[1])

    # TODO: Slice out reading of the csv so you can process step by step the
    #  power csv, which right now is 1GB+ for 2887 iterations of Kalman
    #  and the print of the outputs
    if sys.maxsize <= 2147483647:  # 32 bit
        print("\nDetected 32bit...")
        if stage == "avg":
            raise ValueError("Stage cannot be 'avg' when Python is 32 bit.")
    else:  # 64 bit
        if stage == "exp":
            raise ValueError("Stage cannot be 'exp' when Python is 64 bit.")
        print("\nDetected 64bit...")

    # The very first index=0 we put useless values because baseline is going to be run
    # This "experiments" array with its values is helpful for hash experiments
    experiments = [(stage, 0, 0.0, 0, 1)]

    for h in hash_sizes:
        for e in epsilons:
            for m in mod_precisions:
                for a in attempts:
                    experiments.append((stage, h, e, m, a))

    print("")
    print("")
    print("############################")
    print("   At index {0}, stage '{1}' ".format(exp_index, stage))
    print("############################")
    print("")

    if exp_index == 0:
        print("Baseline:")
        print("---")
        if stage == "exp":
            loop("baseline", iterations, attempt=1, output_dir=output_dir)
        if stage == "avg":
            averages_loop("baseline", iterations,
                          attempt=1, output_dir=output_dir, verbose=2)
    else:
        (s, h, e, m, a) = experiments[exp_index]

        print(
            "Hash {0}, Epsilon {1}, Mod precision {2}, Attempt {3}:".format(h, e, m, a))
        print("---")

        try:

            if s == "exp":

                experiment_loop("hash", hash_size=h, epsilon=e,
                                mod_precision=m, iterations=iterations,
                                attempt=a, program=True,
                                output_dir=output_dir)

            elif s == "avg":

                averages_loop("hash", hash_size=h, epsilon=e,
                              mod_precision=m, iterations=iterations,
                              attempt=a, program=True,
                              output_dir=output_dir,
                              verbose=2)

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
