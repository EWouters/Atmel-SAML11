from setuptools import setup

setup(
    name="serial_interface",
    version="0.1",
    description="serial_interface",
    url="https://github.com/EWouters/Atmel-SAML11/tree/master/Python/serial_interface",
    author="Erik Wouters",
    author_email="ehwo(at)kth.se",
    license="MIT",
    packages=["serial_interface"],
    zip_safe=False,
    setup_requires=["pyserial"]
)