from setuptools import setup, find_packages

setup(
    name='map_network_viz',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'geopandas',
        'geopy',
        'matplotlib',
        'osmnx>=1.8.0'
    ],
)