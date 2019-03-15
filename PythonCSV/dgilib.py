
from pydgilib_extra import *
from config import *

def energy_measurements_worker(queue1, queue2, measurement_duration = config["measurement_duration"]):
    
    with DGILibExtra(**dgilib_config_dict) as dgilib:
        data = dgilib.logger.log(10)

        dgilib.logger.plotobj.calculate_averages(2, dgilib.data)
        dgilib.logger.plotobj.print_averages(2)

        dgilib.logger.keep_plot_alive()