from setuptools import setup, find_packages

setup(
    name='fluidsymbolic',
    version='0.0.1',
    author='Alexandre Delaisement',
    author_email='',
    description='A module dedicated to Symbolic Mathematics '
                'and Fluid Mechanics',
    long_description='A module  dedicated to Symbolic Mathematics '
                     'using Sympy and to Fluid Mechanics being plottable '
                     'and animatable in matplotlib.',
    long_description_content_type='text/markdown',
    url='https://github.com/AlexandreDela/fluidsymbolic',
    packages=['fluidsymbolic'],
      package_dir={'fluidsymbolic': 'src/fluidsymbolic'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        #'Topic :: Software Development :: Libraries :: Python Modules ::'
        #' System Engineering',
    ],
    keywords='symbolic fluid mechanics',
    python_requires='>=3.8',
    install_requires=[
        "sympy>=1.11.1",
        "numpy>=1.21.0",
        "matplotlib>=3.3.0",
        "scipy>=1.10.0",
        "sphinx >= 7.1.0",
        "furo >= 2024.1.29",
        "pytest >= 8.1.1"
    ],
    project_urls={
        'Source': 'https://github.com/AlexandreDela/fluidsymbolic',
    },
)