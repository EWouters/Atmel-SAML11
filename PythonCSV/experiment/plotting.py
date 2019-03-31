import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

import pandas as pd
import os
from sys import platform

from experiment.averages import Averages

# https://stackoverflow.com/questions/13872533/plot-different-dataframes-in-the-same-figure
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
# https://github.com/pandas-dev/pandas/issues/1710
# https://stackoverflow.com/questions/22483588/how-can-i-plot-separate-pandas-dataframes-as-subplots

def output_comparison_plot(filename_1, filename_2, max_iter, legend_1="", legend_2=""):
	column_names = ['Iteration','Roll', 'Pitch', 'Gyro X Angle', 'Gyro Y Angle', 'Comp Angle X', 'Comp Angle Y', 'Kalman Angle X', 'Kalman Angle Y']
	df1 = pd.read_csv(filename_1, header = None, names=column_names)
	df2 = pd.read_csv(filename_2, header = None, names=column_names)

	df1 = df1[:max_iter]
	df2 = df2[:max_iter]

	#print(df1[:5])
	#print(df2[:5])

	#df2.Iteration = df2.Iteration + 2

	fig, axes = plt.subplots(nrows=2, ncols=4)

	for i in range(1,len(column_names)):
		row = int((i-1)/4)
		column = int((i-1)%4)
		df1.plot(kind='line', x='Iteration', y=column_names[i], ax=axes[row, column], color='red')
		df2.plot(kind='line', x='Iteration', y=column_names[i], ax=axes[row, column], color='green')
		axes[row, column].legend([legend_1, legend_2])
		axes[row, column].set_title(column_names[i])

	#print(df1[:5])
	#print(df2[:5])

	plt.show()

	return fig

def output_comparison_plot_single(filename_1, filename_2, max_iter, column, legend_1="", legend_2=""):
	column_names = ['Iteration','Roll', 'Pitch', 'Gyro X Angle', 'Gyro Y Angle', 'Comp Angle X', 'Comp Angle Y', 'Kalman Angle X', 'Kalman Angle Y']
	df1 = pd.read_csv(filename_1, header = None, names=column_names)
	df2 = pd.read_csv(filename_2, header = None, names=column_names)

	df1 = df1[1:max_iter]
	df2 = df2[2:max_iter]

	df2.Iteration = df2.Iteration + 2

	#sprint(df2[:5])

	fig, axes = plt.subplots()

	index = column_names.index(column)
	df1.plot(kind='line', x='Iteration', y=column_names[index], ax=axes, color='blue')
	df2.plot(kind='line', x='Iteration', y=column_names[index], ax=axes, color='red')
	axes.legend([legend_1, legend_2])
	axes.set_title(column_names[index])

	plt.show()

	return fig

def error_barchart():
	n_groups = 5

	means_men = (20, 35, 30, 35, 27)
	std_men = (2, 3, 4, 1, 2)

	means_women = (25, 32, 34, 20, 25)
	std_women = (3, 5, 2, 3, 3)

	fig, ax = plt.subplots()

	index = np.arange(n_groups)
	bar_width = 0.35

	opacity = 0.4
	error_config = {'ecolor': '0.3'}

	rects1 = ax.bar(index, means_men, bar_width,
					alpha=opacity, color='b',
					yerr=std_men, error_kw=error_config,
					label='Men')

	rects2 = ax.bar(index + bar_width, means_women, bar_width,
					alpha=opacity, color='r',
					yerr=std_women, error_kw=error_config,
					label='Women')

	ax.set_xlabel('Group')
	ax.set_ylabel('Scores')
	ax.set_title('Scores by group and gender')
	ax.set_xticks(index + bar_width / 2)
	ax.set_xticklabels(('A', 'B', 'C', 'D', 'E'))
	ax.legend()

	fig.tight_layout()
	plt.show()

	return fig

def wait_for_plot(fig, check_os=False):
    if platform == "linux" or platform == "linux2":
        while plt.fignum_exists(fig.number):
            plt.pause(0.000001)

if __name__ == "__main__":

	good_results_path = os.path.join(os.getcwd(),"good_results")

	original_output = os.path.join(good_results_path, "original_output.csv")

	baseline_output = os.path.join(good_results_path, "baseline_100iter_output.csv")
	baseline_averages = os.path.join(good_results_path, "baseline_100iter_averages.csv")

	hash_8_output = os.path.join(good_results_path, "hash_8_mod_5_100iter_output.csv")
	hash_32_output = os.path.join(good_results_path, "hash_32_mod_6_100iter_output.csv")

	hash_8_averages = os.path.join(good_results_path, "hash_8_mod_5_100iter_averages.csv")
	hash_32_averages = os.path.join(good_results_path, "hash_32_mod_6_100iter_averages.csv")

	avg_baseline = DGILibAverages(None)
	avg_baseline.read_from_csv(baseline_averages)

	avg_hash8 = DGILibAverages(None)
	avg_hash8.read_from_csv(hash_8_averages)

	avg_hash32 = DGILibAverages(None)
	avg_hash32.read_from_csv(hash_32_averages)

	print("")
	print("-- Baseline --")
	avg_baseline.calculate_averages_for_pin(2)
	avg_baseline.print_averages_for_pin(2, 5)
	
	print("")
	print("-- Hash 8 --")
	avg_hash8.calculate_averages_for_pin(2)
	avg_hash8.print_averages_for_pin(2, 5)
	
	print("")
	print("-- Hash 32 --")
	avg_hash32.calculate_averages_for_pin(2)
	avg_hash32.print_averages_for_pin(2, 5)

	f1 = comparison_plot(original_output, hash_8_output, 100, "Original", "Hash 8")
	f2 = comparison_plot(original_output, hash_32_output, 100, "Original", "Hash 32")
	wait_for_plot(f1)
	wait_for_plot(f2)

	