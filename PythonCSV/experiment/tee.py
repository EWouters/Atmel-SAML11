
import os
import sys
from time import time
from shutil import copy
import math

from pydgilib_extra import LOGGER_CSV, LOGGER_PLOT, DGILibExtra
from experiment.averages import Averages
from experiment.plotting import *
from experiment.helpers import *

import dgilib_threaded as dgi_t
from atprogram.atprogram import atprogram, get_project_size

import traceback
import errno


class Tee(object):

    def __init__(self, log_file_path, output_to_file=True,
                 output_to_console=True):
        self.stdout_tee = SubTee(log_file_path, "stdout",
                                 output_to_file=output_to_file,
                                 output_to_console=output_to_console)
        self.stderr_tee = SubTee(log_file_path, "stderr",
                                 output_to_file=output_to_file,
                                 output_to_console=output_to_console)

    def __enter__(self):
        self.stdout_tee.enable()
        self.stderr_tee.enable()
        return self

    def __exit__(self, etype, value, tb):
        self.stderr_tee.exception_print(etype, value, tb)
        self.stdout_tee.disable()
        self.stderr_tee.disable()

    def __del__(self):
        self.stdout_tee.disable()
        self.stderr_tee.disable()


class SubTee(object):

    def __init__(self, log_file_path, capture="stdout", fileflags=None,
                 output_to_console=True,
                 output_to_file=True):
        self.stdhandle_name = capture
        self.stdhandle = None
        self.fileflags = fileflags
        if capture == "stdout":
            self.stdhandle = sys.stdout
            if self.fileflags is None:
                self.fileflags = "w"
        elif capture == "stderr":
            self.stdhandle = sys.stderr
            if self.fileflags is None:
                self.fileflags = "a"

        self.output_to_file = output_to_file
        self.output_to_console = output_to_console

        self.log_file_path = log_file_path

        self.log_file_handler = None
        self.create_file_handler()

    def create_file_handler(self):
        if self.output_to_file is False:
            return

        if not os.path.exists(os.path.dirname(self.log_file_path)):
            try:
                os.makedirs(os.path.dirname(self.log_file_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        if self.log_file_handler is None:
            self.log_file_handler = open(self.log_file_path, self.fileflags)

    def exception_print(self, exctype, value, tb):
        if value is None:
            return
        if self.log_file_handler is not None:
            print(''.join(traceback.format_exception(exctype, value, tb)),
                  file=self.log_file_handler)

    def enable(self):
        if self.stdhandle_name == "stdout":
            sys.stdout = self
        elif self.stdhandle_name == "stderr":
            sys.stderr = self

    def disable(self):
        if self.stdhandle_name == "stdout":
            sys.stdout = self.stdhandle
        elif self.stdhandle_name == "stderr":
            sys.stderr = self.stdhandle
        if self.log_file_handler is not None:
            self.log_file_handler.close()

    def write(self, data):
        if self.log_file_handler is not None:
            self.log_file_handler.write(data)
        if self.output_to_console:
            self.stdhandle.write(data)

    def flush(self):
        if self.log_file_handler is not None:
            self.log_file_handler.flush()
        if self.output_to_console:
            self.stdhandle.flush()

    # def __del__(self):
    #     self.disable()

    # def __enter__(self):
    #     self.enable()
    #     return self

    # def __exit__(self, exctype, value, tb):
    #     self.exception_print(exctype, value, tb)
    #     self.disable()
