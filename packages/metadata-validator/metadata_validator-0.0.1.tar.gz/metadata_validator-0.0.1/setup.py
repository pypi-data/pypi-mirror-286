from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A package to check different sheets within a submission of a spreadsheet.'
LONG_DESCRIPTION = 'The package offers an input of a spreadsheet and a method. Once givin this, the package will check the different sheets associated within the spreadsheet.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="metadata_validator", 
        version=VERSION,
        author="Keaton Hutchinson",
        author_email="keatonhutchinson03@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages('metadata_validator', 'metadata_validator.*' ),
        install_requires=[
            'pyexcel',
            'xlrd',
        ], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        entry_points={
        'console_scripts': [
            # 'bilcheck=metadata_validator.main:outside_bil_check',  # If you have a main function
        ],
    },
        keywords=['python', 'bil'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)