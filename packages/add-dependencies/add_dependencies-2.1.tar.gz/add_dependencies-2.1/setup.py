from setuptools import setup, find_packages
setup(
    name='add-dependencies',
    version='2.1',
    packages=find_packages(),
    install_requires=[
        #Add dependencies here.
        #e.g 'flask>=0.5'
    ],
    #entry_points={
    #    "console_scripts": [
    #        "add-dependencies = add-dependencies:hello",
    #    ],
    #},
)