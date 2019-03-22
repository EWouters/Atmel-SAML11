from os import path, scandir
import json
import pickle
from math import ceil

from experiments.looped_experiment import looped_experiment
from experiments.repeated_experiment import repeated_experiment

from atprogram.atprogram import get_device_info


class CheckpointEnergy(object):
    looped_config_file = "looped_experiment.json"
    repeated_config_file = "repeated_experiment.json"

    def __init__(self, projects_folder=[path.curdir],
                 security_folder="Security", security_projects=None,
                 workload_folder="Workloads", workload_projects=None):
        self.projects_folder = projects_folder
        self.security_folder = security_folder
        self.workload_folder = workload_folder
        self.security_projects = security_projects
        self.workload_projects = workload_projects
        if self.security_projects is None:
            self.security_projects = [f.name for f in scandir(
                path.join(*self.projects_folder, self.security_folder))
                if f.is_dir()]
        if self.workload_projects is None:
            self.workload_projects = [f.name for f in scandir(
                path.join(*self.projects_folder, self.workload_folder))
                if f.is_dir()]

    def measure_all_security_energy(self, **kwargs):
        for security_project in self.security_projects:
            self.measure_security_energy(security_project, **kwargs)

    def measure_all_workload_energy(self, **kwargs):
        for workload_project in self.workload_projects:
            self.measure_workload_energy(workload_project, **kwargs)

    def measure_security_energy(self, security_project, config_file=None,
                                **kwargs):
        # Get the name of the config file, or use default if not specified
        if config_file is None:
            config_file = self.looped_config_file
        # Get the full path to the config file
        config_file_path = path.abspath(
            path.join(*self.projects_folder, self.security_folder,
                      security_project, config_file))
        if not path.isfile(config_file_path):
            raise IOError(f"Config file not found at {config_file_path}")
        looped_experiment(config_file_path, **kwargs)

    def measure_workload_energy(self, workload_project, config_file=None,
                                **kwargs):
        # Get the name of the config file, or use default if not specified
        if config_file is None:
            config_file = self.repeated_config_file
        # Get the full path to the config file
        config_file_path = path.abspath(
            path.join(*self.projects_folder, self.workload_folder,
                      workload_project, config_file))
        if not path.isfile(config_file_path):
            raise IOError(f"Config file not found at {config_file_path}")
        repeated_experiment(config_file_path, **kwargs)

    def get_security_energy_function(self, config_file=None):
        if config_file is None:
            config_file = self.looped_config_file
        security_charge = {}
        for security_project in self.security_projects:
            config_file_path = path.abspath(
                path.join(*self.projects_folder, self.security_folder,
                          security_project, config_file))
            if not path.isfile(config_file_path):
                raise IOError(f"Config file not found at {config_file_path}")
            pickle_path_base = ""
            with open(path.join(config_file_path)) as json_file:
                config = json.load(json_file)
                pickle_path_base = path.abspath(path.join(
                    *self.projects_folder, self.security_folder,
                    security_project,
                    config["config_dict"].get("file_name_base", "log")))
            security_charge[security_project] = {
                "parsed_data": pickle.load(open(f"{pickle_path_base}_looped.p",
                                                "rb")),
                "model": pickle.load(open(f"{pickle_path_base}_model.p",
                                          "rb"))}

        def get_security_energy(security_type, number_of_bytes,
                                energy_parameter="Charge"):
            if security_type in security_charge.keys():
                power_dict = {}
                for parameter_name in security_charge[security_type][
                        "parsed_data"].keys():
                    index = ceil(
                        number_of_bytes/security_charge[security_type][
                            "parsed_data"][parameter_name].get("x_step", 1))
                    if index < len(security_charge[security_type][
                            "parsed_data"][parameter_name][energy_parameter]):
                        power_dict[parameter_name] = security_charge[
                            security_type]["parsed_data"][parameter_name][
                                energy_parameter][index]
                    else:
                        power_dict[parameter_name] = security_charge[
                            security_type]["model"][parameter_name][
                                energy_parameter]["intercept"] + \
                            number_of_bytes * \
                            security_charge[security_type]["model"][
                                parameter_name][energy_parameter]["slope"]
                return power_dict
            elif security_type is "None":
                return {security_type: 0}  # No security, so 0 C
            else:
                raise ValueError(
                    f"Security type not recognized. Got {security_type}, but" +
                    f" have {list(security_charge.keys())} and 'None'.")
        return get_security_energy

    def get_workload_energy_function(self, config_file=None,
                                     energy_parameter="Charge"):
        if config_file is None:
            config_file = self.repeated_config_file
        workload_charge = {}
        for workload_project in self.workload_projects:
            config_file_path = path.abspath(
                path.join(*self.projects_folder, self.workload_folder,
                          workload_project, config_file))
            if not path.isfile(config_file_path):
                raise IOError(f"Config file not found at {config_file_path}")
            pickle_path_base = ""
            with open(path.join(config_file_path)) as json_file:
                config = json.load(json_file)
                pickle_path_base = path.abspath(path.join(
                    *self.projects_folder, self.workload_folder,
                    workload_project,
                    config["config_dict"].get("file_name_base", "log")))
            workload_charge[workload_project] = pickle.load(
                open(f"{pickle_path_base}_repeated.p", "rb"))

        def get_workload_energy(workload_type, energy_parameter="Charge"):
            if workload_type in workload_charge.keys():
                power_dict = {}
                for parameter_name in workload_charge[workload_type].keys():
                    power_dict[parameter_name] = workload_charge[
                        workload_type][parameter_name][energy_parameter]
                return power_dict
            else:
                raise ValueError(
                    f"workload type not recognized. Got {workload_type}, but" +
                    f" have {list(workload_charge.keys())} and 'None'.")
        return get_workload_energy

    def get_device_info(self, *args, **kwargs):
        self.device_info = get_device_info(*args, **kwargs)
