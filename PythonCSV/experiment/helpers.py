from pydgilib_extra import DGILibAverages
import os

def restore_averages(experiment="exp1", ending="hash-32"):
    avg = DGILibAverages(None)
    avg.read_from_csv(os.getcwd() + "\\output\\" + experiment + "\\" + experiment + "-averages-" + str(ending) + ".csv", 1)

    return avg