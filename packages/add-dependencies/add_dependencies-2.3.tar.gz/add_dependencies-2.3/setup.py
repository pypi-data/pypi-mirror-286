from setuptools import setup, find_packages
setup(
    name='add-dependencies',
    version='2.3',
    packages=find_packages(),
    install_requires=[
        #Add dependencies here.
        'flask<=0.5',
    ],
    #entry_points={
    #    "console_scripts": [
    #        "add-dependencies = add-dependencies:hello",
    #    ],
    #},
)