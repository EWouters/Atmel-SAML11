from experiment.tee import Tee
import os
import sys

path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "hello_log.txt")

with Tee(path):
    print("Hello!")
    print("Error", file=sys.stderr)

    raise ValueError("Some error")
