from pydgilib_extra import DGILibPlot
from experiment.averages import Averages
from experiment.plotting import wait_for_plot
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import operator
import os

def get_output_dirs():
    def get_immediate_subdirectories(a_dir):
        return [name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name))]

    windows_output_dir = "C:\\Users\\Dragos\\MasThesis_output"
    linux_output_dir = "/home/dragos/MasThesis/MasThesis_output"
    output_dir = ""

    if os.name == "nt":
        output_dir = windows_output_dir
    else:
        output_dir = linux_output_dir

    output_dirs_ = get_immediate_subdirectories(output_dir)

    print(str(output_dirs_))

    output_dirs = []
    for d in output_dirs_:
        if "attempt" in d:
            output_dirs.append(os.path.join(output_dir,d))

    return output_dirs

class ExperimentResult(object):
    
    def __init__(self, folder="baseline_2887iter_1", output_dir=None):        
        self.folder = folder
        self.experiment_name = folder
        self.output_dir = output_dir
        
        self.voltage = 5
        
        self.averages_csv = os.path.join(output_dir, folder, folder + "_averages.csv")
        self.hash_stats_txt = os.path.join(output_dir, folder, folder + "_hash.txt")
        self.size_stats_txt = os.path.join(output_dir, folder, folder + "_size.txt")
        self.output_csv = os.path.join(output_dir, folder, folder + "_output.csv")
        
        self.column_names = ['Iteration', 'Roll', 'Pitch', 'Gyro X Angle', \
            'Gyro Y Angle', 'Comp Angle X', 'Comp Angle Y', 'Kalman Angle X', \
            'Kalman Angle Y']
        
        self.output_axes = None
        self.output_fig = None
        self.output_df = pd.read_csv(self.output_csv, header = None, names = self.column_names)
        self.output_colors = ['red', 'blue', 'black', 'brown']
        self.output_plotted_axes = 0
        
        self.legend = ""
        if "hash" in folder:
            self.legend = " ".join(folder.split("_")[0:6]).title()
        else:
            self.legend = folder.split("_")[0].title()
        
        self.iterations = min(len(self.output_df['Iteration']),
                                int(folder.split("iter")[0].split("_")[-1]))
        self.attempt = int(folder.split("_")[-1])
        
        self.avgobj = Averages()
        
        self.deviation = {
            'Roll': 0,
            'Pitch': 0,
            'Gyro X Angle': 0,
            'Gyro Y Angle': 0,
            'Comp Angle X': 0,
            'Comp Angle Y': 0,
            'Kalman Angle X': 0,
            'Kalman Angle Y': 0,
            'Average': 0            
        }
        
    def plot_output(self, color='red', reference=[]):
        self.output_fig, self.output_axes = plt.subplots(nrows=2, ncols=4)

        fig, axes = self.output_fig, self.output_axes
        dfs = [self.output_df]
        column_names = self.column_names
        legends = [self.legend]
        
        for exp in reference:
            legends.append(exp.legend)
            dfs.append(exp.output_df)
        
        for i in range(1,len(column_names)):
            row = int((i-1)/4)
            column = int((i-1)%4)
            
            color_idx = 0
            for df in dfs:
                df.plot(kind='line', x='Iteration', y=column_names[i],
                        ax=axes[row, column],
                        color=self.output_colors[color_idx])
                axes[row, column].axis([-50, 3000, -200, 200]) # xmin, xmax, ymin, ymax
                color_idx += 1
            
            axes[row, column].legend(legends)
            axes[row, column].set_title(column_names[i])

        self.output_axes = axes
        self.output_fig = fig
        
        return fig, axes
        
    def plot_power_curves(self, reference=None):
        run_name_1 = self.folder
        
        if reference is None:
            reference = ExperimentResult()
        
        run_name_2 = reference.folder
        
        filename_1 = os.path.join(self.output_dir, run_name_1, run_name_1 + "_averages.csv")
        filename_2 = os.path.join(reference.output_dir, run_name_2, run_name_2 + "_averages.csv")

        column_names = ['Pin','Iteration', 'From', 'To', 'Charge']
        df1 = pd.read_csv(filename_1, header = None, names=column_names)
        df2 = pd.read_csv(filename_2, header = None, names=column_names)

        iterations = int(run_name_1.split("iter")[0].split("_")[-1])

        df1 = df1[1:iterations]
        df2 = df2[1:iterations]

        df1["Charge"] = df1["Charge"].astype(float) #pd.to_numeric(df1["Charge"])
        df2["Charge"] = df2["Charge"].astype(float)

        fig, axes = plt.subplots(nrows=1, ncols=1)
        
        df1.plot(kind='line', x='Iteration', y='Charge', ax=axes, color='blue')
        df2.plot(kind='line', x='Iteration', y='Charge', ax=axes, color='black')
        
        axes.legend([self.legend, reference.legend])
        
        return fig, axes
        
        #wait_for_plot(fig)
        
    def calculate_deviation(self, reference=None):
        # If the deviation is already calculated in the 'error' member,
        #  then return and don't do anything
        # if self.error["Average"] > 0.0:
        #     return
        
        # If baseline is not given as a parameter, then the class
        #  instantiated without any parameter should, by default,
        #  become the baseline
        if reference is None:
            reference = ExperimentResult()
            
        self.deviation_reference_name = reference.experiment_name
        
        self.deviation_df_mine = pd.DataFrame()
        self.deviation_df_theirs = pd.DataFrame()
        self.deviation_df = pd.DataFrame()
        self.deviation_df_average = pd.DataFrame([[0.0] * len(self.column_names)], columns = [x + ' (deviation average)' for x in self.column_names])
        
        for c in self.column_names:
            self.deviation_df_mine[c + ' (mine)'] = self.output_df[c]
            self.deviation_df_theirs[c + ' (theirs)'] = reference.output_df[c]
            self.deviation_df[c + ' (deviation)'] = abs(self.deviation_df_mine[c + ' (mine)'] - self.deviation_df_theirs[c + ' (theirs)'])
            self.deviation_df[c + ' (deviation)'] /= abs(self.deviation_df_theirs[c + ' (theirs)'])
        
        self.deviation_df = self.deviation_df.fillna(0)
        
        for c in self.column_names:
            self.deviation_df_average.at[0,c + ' (deviation average)'] = self.deviation_df[c + ' (deviation)'].mean(skipna = False)

        iterations = min(self.iterations, len(reference.output_df['Iteration']))
        self.reference_iterations = iterations
        
        for c in self.column_names:
            self.deviation[c] = self.deviation_df_average[c + ' (deviation average)'].item()
        
        self.deviation['Average'] = self.deviation_df_average.mean(axis=1).item()

    def print_deviation(self,verbose=1):
        if verbose == 1:
            print("Deviation: {0}%".format(self.deviation["Average"]))
        elif verbose == 2:
            for column in self.column_names:
                if 'Iteration' == column: continue
                print("{0}: {1:0.4f}%".format(column, self.deviation[column]))
            print("Average deviation: {0:0.4f}%".format(self.deviation["Average"]))
        elif verbose >= 3:
            display(self.deviation_df)
    
    def calculate_averages(self, ignore_first_average=True):
        self.avgobj.read_from_csv(self.averages_csv)
        self.avgobj.calculate_averages_for_pin(1,
            ignore_first_average=ignore_first_average)
    
    def show_averages(self, verbose=1):
        print_per_iteration=False
        print_total_average=False
        print_benchmark_time=False
        print_energy_and_current=False
        
        if verbose >= 1:
            print_per_iteration = True
        if verbose >= 2:
            print_energy_and_current = True
            print_total_average = True
        if verbose >= 3:
            print_benchmark_time = True
        
        self.avgobj.print_averages_for_pin(1,
            print_per_iteration = print_per_iteration, 
            print_energy_and_current = print_energy_and_current,
            print_total_average = print_total_average,
            print_benchmark_time = print_benchmark_time)
    
    def get_averages(self, pin = 1):
        return {
            'Average per iteration uC': self.avgobj.total_average[pin]*
                         1000 * 1000 / self.avgobj.total_iterations[pin],
            'Average per iteration ms': self.avgobj.total_duration[pin] * 1000
                            / self.avgobj.total_iterations[pin],
            'Total mC': self.avgobj.total_average[pin] * 1000,
            'Total duration sec': self.avgobj.total_duration[1],
            "Average mW": self.avgobj.total_average[pin] * 1000 * self.voltage / self.avgobj.total_duration[pin],
            'Iterations': self.avgobj.total_iterations[pin]
        }
    
    def get_deviation(self):
        return {
            'Average': self.deviation["Average"], 
            'List': list(self.deviation.values())[:-1],
            'Maximum': max(list(self.deviation.values())[:-1]),
            'Maximum name': max(self.deviation.items(),
                                key=operator.itemgetter(1))[0]
        }
    
    def get_hash_stats(self, verbose=0):
        epsilon = 0
        epsilon_mod = 0
        mod_precision = 0
        hash_size = 0
        utilizied = 0
        found = 0
        stored = 0

        for line in open(self.hash_stats_txt, "r"):
            if ("Epsilon:" in line):
                epsilon = float(line.split(" ")[-1])
            elif ("Epsilon mod" in line):
                epsilon_mod = int(line.split(" ")[-1])
            elif ("Mod precision" in line):
                mod_precision = int(line.split(" ")[-1])
            elif ("Hash size" in line):
                hash_size = int(line.split(" ")[-1])
            elif ("HashTable population" in line):
                utilized = int(line.split(" ")[-3])
            elif ("found" in line):
                found = int(line.split(" ")[-1])
            elif ("stored" in line):
                stored = int(line.split(" ")[-1])
            if verbose>0:print(line, end='')
        return {
            'Epsilon': epsilon,
            'Epsilon Mod': epsilon_mod, 
            'Mod precision': mod_precision,
            'Hash size': hash_size,
            'Utilized': utilized,
            'Found': found,
            'Stored': stored
        }
    
    def get_size_stats(self, verbose=0):
        text = 0
        data = 0
        bss = 0
        dec = 0
        hex_ = 0
        filename = 0

        for line in open(self.size_stats_txt, "r"):
            if ("text:" in line):
                text = int(line.split(" ")[-1])
            elif ("data:" in line):
                data = int(line.split(" ")[-1])
            elif ("bss:" in line):
                bss = int(line.split(" ")[-1])
            elif ("dec:" in line):
                dec = int(line.split(" ")[-1])
            elif ("hex:" in line):
                hex_ = int(line.split(" ")[-1])
            elif ("filename:" in line):
                filename = line.split(" ")[-1].strip()

            if verbose > 0:
                print(line, end='')

        return {
            'text': text,
            'data': data, 
            'bss': bss,
            'dec': dec,
            'hex': hex_,
            'flash': text + data,
            'ram': data + bss,
            'filename': filename
        }
        
class ResultsTable(object):
    
    def __init__(self):
        self.column_names = ["Type", "Attempt", "Hash table size",
                            "Epsilon", "Mod precision",
                             "mC/iter", "ms/iter", "Total mC", 
                             "Total sec", "Average mW",
                             "Deviation average",
                             "Deviation maximum", "Deviation maximum name",
                             "Hits from hash", "Writes to hash",
                             "Power averaged iterations",
                             "FLASH memory occupancy (bytes)",
                             "RAM memory occupancy (bytes)"]
        self.df = pd.DataFrame(columns=self.column_names)
        self.df_mean = pd.DataFrame(columns=self.column_names)
        self.df_max = pd.DataFrame(columns=self.column_names)
        self.df_min = pd.DataFrame(columns=self.column_names)
        
    def add_to_table(self, exp):
        attempt = exp.attempt
        averages = exp.get_averages()
        deviation = exp.get_deviation()
        sizes = exp.get_size_stats()
        
        if "baseline" in exp.folder:
            row = ["Baseline", attempt, 0, 0, 0, 
                   averages['Average per iteration uC'],
                   averages['Average per iteration ms'],
                   averages['Total mC'],
                   averages['Total duration sec'], 
                   averages['Average mW'],
                   deviation['Average'],
                   deviation['Maximum'],
                   deviation['Maximum name'],
                   0, 0, averages['Iterations'],
                   sizes['flash'], sizes['ram']]
            assert(len(row) == len(self.column_names))
        else:
            hash_stats = exp.get_hash_stats()
            row = ["Hash", attempt, hash_stats['Hash size'],
                    hash_stats['Epsilon'], hash_stats['Mod precision'],
                    averages['Average per iteration uC'],
                    averages['Average per iteration ms'],
                    averages['Total mC'], averages['Total duration sec'],
                    averages['Average mW'],
                    deviation['Average'], deviation['Maximum'],
                    deviation['Maximum name'],
                    hash_stats['Found'], hash_stats['Stored'],
                    averages['Iterations'],
                    sizes['flash'], sizes['ram']]
            assert(len(row) == len(self.column_names))
        self.df.loc[len(self.df)] = row
        
        self.df["Hash table size"] = self.df["Hash table size"].astype(int)
        self.df["Mod precision"] = self.df["Mod precision"].astype(int)
        self.df["Hits from hash"] = self.df["Hits from hash"].astype(int)
        self.df["Writes to hash"] = self.df["Writes to hash"].astype(int)
        self.df["Power averaged iterations"] = \
            self.df["Power averaged iterations"].astype(int)
        self.df["FLASH memory occupancy (bytes)"] = \
            self.df["FLASH memory occupancy (bytes)"].astype(int)
        self.df["RAM memory occupancy (bytes)"] = \
            self.df["RAM memory occupancy (bytes)"].astype(int)
        
    def group(self, which=None, groups=["Epsilon"]):
        #groups can also be 
        # ["Type", "Hash table size", "Mod precision", "Power averaged iterations",
        # "Epsilon"]

        if which is None:
            return self.df.groupby(groups)
        elif which == "max":
            return self.df.groupby(groups).max()
        elif which == "min":
            return self.df.groupby(groups).min()
        elif which == "mean":
            return self.df.groupby(groups).mean()
        elif which == "std":
            return self.df.groupby(groups).std().fillna(0)

    def print_table(self, which="all"):
        self.df = self.df.sort_values(by=["Attempt", "Epsilon"])

        if which == "all":
            display(self.df.style.format({
                'Deviation average': '{:,.4%}'.format,
                'Deviation maximum': '{:,.4%}'.format,
            }))
        elif which in ["max", "min", "mean", "std"]:
            display(self.group(which).style.format({
                                   'Deviation average': '{:,.4%}'.format,
                                   'Deviation maximum': '{:,.4%}'.format,
                               }))
    
    def plot(self, columns):
        mean = self.group().mean()
        min_ = self.group().min()
        max_ = self.group().max()

        fig, ax = plt.subplots()
        
        for c in columns:
            mean_ = mean[[c]]
            max_ = self.group().max()[[c]]
            min_ = self.group().min()[[c]]

            err = []
            for col in min_:  # Iterate over bar groups (represented as columns)
                err.append([min_[col].values-mean_[col].values, max_[col].values-mean_[col].values])
            err = np.abs(err)  # Absolute error values (you had some negatives)

            mean_.plot(y=c, yerr=err, ax=ax)
            
        return fig, ax
