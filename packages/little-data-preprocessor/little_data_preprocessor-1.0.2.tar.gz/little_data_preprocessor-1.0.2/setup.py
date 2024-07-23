from setuptools import setup, find_packages

VERSION = '1.0.2' 
DESCRIPTION = 'A pandas dataframe preprocessing python package'
LONG_DESCRIPTION = 'Contains utility functions that Is used in preprocessing stages of DL/ML implementation'

with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
        name="little_data_preprocessor", 
        version=VERSION,
        author="Ameh Solomon Onyeke",
        author_email="amehsolomon46@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        url="https://github.com/Uncle-Solomon/little_preprocessor", 
        packages=find_packages(),
        install_requires=["pandas", "numpy"],
        
        keywords=['python', 'pandas', 'preprocessing'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        project_urls={  
        'Bug Tracker': 'https://github.com/Uncle-Solomon/little_preprocessor/issues',
        'Documentation': 'https://github.com/Uncle-Solomon/little_preprocessor/wiki',
        'Source Code': 'https://github.com/Uncle-Solomon/little_preprocessor',
    }
)