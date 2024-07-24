# import os
# import sys
#
# if os.path.abspath('..') not in sys.path:
#     sys.path.append(os.path.abspath('..'))
from setuptools import find_packages, setup

name = 'graphslim'
requires_list = [
    'click >= 8.1.0',
    'deeprobust',
    'gdown',
    'networkit',
    'networkx',
    'numpy',
    'ogb',
    'PyGSP',
    'scikit_learn',
    'scipy',
    'sortedcontainers >= 2.4.0',
    'torch >= 2.0.0',
    'torch_geometric',
    'tqdm >= 4.0.0',
]

setup(
    name=name,  # 包名同工程名，这样导入包的时候更有对应性
    version='1.0.3',
    author="Rockcor",
    author_email='jshmhsb@gmail.com',
    description="Slimming the graph data for graph learning",
    packages=find_packages(),
    python_requires='>=3.8',
    include_package_data=True,  # 自动包含受版本控制(svn/git)的数据文件
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
    ],
    license="MIT",
    install_requires=requires_list
)
