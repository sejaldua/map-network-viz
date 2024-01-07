from setuptools import setup, find_packages

setup(
    name='map_network_viz',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'osmnx',
        'geopandas',
        'geopy',
        'matplotlib'
    ],
)