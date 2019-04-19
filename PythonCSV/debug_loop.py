
from experiment.loop import experiment_loop, averages_loop, size_loop

#loop("baseline", 20, output_dir="C:\\Users\\Dragos\\MasThesis_output")
#averages_loop("baseline", 20, output_dir="C:\\Users\\Dragos\\MasThesis_output")
size_loop("baseline", 20,
          output_dir="C:\\Users\\Dragos\\MasThesis_output", verbose=2)
