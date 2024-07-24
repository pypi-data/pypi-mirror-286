# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['yoshi_seals',
 'yoshi_seals.eigen',
 'yoshi_seals.insert',
 'yoshi_seals.process',
 'yoshi_seals.scan',
 'yoshi_seals.shared',
 'yoshi_seals.write']

package_data = \
{'': ['*']}

install_requires = \
['cython>=3.0.10,<4.0.0', 'numpy>=2.0.0,<3.0.0', 'pandas>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'yoshi-seals',
    'version': '2.1.0.post1',
    'description': '',
    'long_description': '# Seals - Numeric Calculus\n\nThis python namespace is made for applied Numeric Calculus of Linear Algebra. It is made with the following objectives in mind:\n\n* Scan *csv* files to make a numpy matrix.\n\n* Write a matrix into a *csv* file.\n\n* Insert user input into a matrix or a vector.\n\n* Calculate Eigenvalues and his Eigenvectors.\n\n* Use methods to proccess the matrices.\n  * Identity Matrix\n  * Gauss Elimination\n  * Inverse Matrix\n  * Cholesky Decomposition\n  * LU Decomposition\n  * Cramer\n\n## Syntax\n\nTo call the package *scan* use the syntax: `from yoshi_seals import scan`. The package also has a function for *Numpy* arrays and *Pandas* dataframes, and used the following syntax `scan.np(path)` for *Numpy* and `scan.pd(path)` for *Pandas*, where `path` is the path to your directory.\n\nTo call the package *write* use the syntax: `from yoshi_seals import write`. The package also has a function for *Numpy* arrays and *Pandas* dataframes, and uses the following syntax `write.np(array,path)` for *Numpy*, where `array` is the matrix that you desire to output and `path` is the path to your directory, and `write.pd(df,path)` for *Pandas*, where `df` is the matrix that you desire to output and `path` is the path to your directory.\n\nTo call the package *insert* use the syntax: `from yoshi_seals import insert`. The package also has a function for *matrix* and another for *vector*, and it has the following syntax `insert.function(array)`, where `insert` is the *Python Module* and `function` is either a `matrix` or a `vector` and `array` is either a *matrix* or a *vector*.\n\nThere is also a function that given a matrix it return all real eigenvalues and all real eigenvectors, this function uses the power method to find the eigenvalues and inverse power method for the eigenvector.\n\n### Processes\n\nTo call the module `process` use the syntax: `from yoshi_seals import process as sl`, where `sl` is an alias and will be used to call functions: `sl.inverse(array)`.\n\n* The function *gauss* returns a *numpy* vector containing the vector of variables from the augmented matrix. `sl.gauss(A,b)`, which `A` is the coefficient matrix and `b` is the constants vector.\n\n* The function *inverse* returns a *numpy* inverse matrix of the matrix passed into to it, and it has the following syntax `sl.inverse(matrix)`, which `matrix` is a square matrix.\n\n* The function *cholesky* returns a *numpy* vector containing the vector of variables from the coefficient matrix and the constants vector, and it has the following syntax `sl.cholesky(A,b)`, which `A` is the coefficient matrix and `b` is the constants vector.\n  \n* The function *decomposition* returns a *numpy* vector containing the vector of variables from the coefficient matrix and the constants vector, and it has the following syntax `sl.decomposition(A,b)`, which `A` is the coefficient matrix and `b` is the constants vector.\n\n* The function *cramer* returns a *numpy* vector containing the vector of variables from the coefficient matrix and the constants vector, and it has the following syntax `sl.cramer(A,b)`, which `A` is the coefficient matrix and `b` is the constants vector.\n\n## Installation\n\nTo install the package from source `cd` into the directory and run:\n\n`pip install .`\n\nor run\n\n`pip install yoshi-seals`\n',
    'author': 'Vitor Hideyoshi Nakazone Batista',
    'author_email': 'vitor.h.n.batista@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
