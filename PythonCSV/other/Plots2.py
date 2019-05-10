import os
from experiment.experiment_results import ExperimentResult, ResultsTable, get_output_dir

limit = 37


output_dir_ = get_output_dir()

include = ["baseline", "hash"]
exclude = [".stversions", ".ipynb_checkpoints",
           ".vscode", ".stfolder", "broken", "20iter", "other"]

dirs = [x[0] for x in os.walk(output_dir_)]

# Remove output_dir_ itself
dirs = [x for x in dirs if (x != output_dir_)]
dirs = [x for x in dirs if not any(s in x for s in exclude)]
dirs = [x for x in dirs if any(s in x for s in include)]
folders = [x.split(output_dir_)[1].replace('\\', '') for x in dirs]

experiments = [ExperimentResult(folder=x, output_dir=output_dir_)
               for x in folders[:limit]]

for i in range(len(experiments)):
    print(str(i) + ": " + experiments[i].folder)

baseline = experiments[0]

# **Calculate everything**
for e in experiments[:limit]:
    print(e.experiment_name)
    e.calculate_deviation(reference=baseline)
    e.calculate_averages(ignore_first_average=False)

rt = ResultsTable()

for e in experiments[:limit]:
    rt.add_to_table(e)

rt.print_table()

rt.df.to_csv("experiment_results_table.csv")
