from setuptools import find_packages, setup
import os
__version__ = "0.1.0"

setup(
    name='stacksim',
    version="0.0.3",
    description='Stack Visualization Tool',
    packages=find_packages(),
    package_dir={
        "stacksim": "stacksim"
    },
    include_package_data=True,
    package_data={
        'stacksim': ['templates/*.html'],
    },
    scripts=["stacksim/stacksim"], 
    install_requires = ["prompt_toolkit", "Sphinx", "jinja2", "rich", "termcolor"],
    entry_points = {
        'spinx.extension': [ 'stack = stacksim.StackDirective' ]
    }
)
