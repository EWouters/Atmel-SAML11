import sys
from setuptools import setup

#needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
#pytest_runner = ["pytest-runner"] if needs_pytest else []

setup(
    name="atmel_csv_sender",
    version="0.1",
    description="",
    url="https://github.com/EWouters/Atmel-SAML11/tree/master/Python/pydgilib",
    author="Dragoș Perju",
    author_email="dsperju(at)kth.se",
    license="MIT",
    packages=["atmel_csv_sender"],
    dependency_links=[],
    zip_safe=False,
    setup_requires=[
        "serial"
    ], #+ pytest_runner,
    tests_require=[], #"pytest", "pytest-benchmark"
)
