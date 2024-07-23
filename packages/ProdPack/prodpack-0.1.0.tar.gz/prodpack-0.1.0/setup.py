from setuptools import setup, find_packages

setup(
    name='ProdPack',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "pulp>=2.6.0",
        "numpy<2.0.0,>=1.26.0",
        "pandas>=1.3.5",
        "DEAPack>=0.1.2",
    ],
)
