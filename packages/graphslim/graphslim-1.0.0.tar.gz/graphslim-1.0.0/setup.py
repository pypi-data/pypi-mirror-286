# import os
# import sys
#
# if os.path.abspath('..') not in sys.path:
#     sys.path.append(os.path.abspath('..'))
from setuptools import find_packages, setup

name = 'graphslim'
requires_list = [
    'click >= 8.1.0',
    'deeprobust == 0.2.10',
    'gdown == 5.2.0',
    'matplotlib >= 3.8.4',
    'networkit >= 11.0',
    'networkx >= 3.1',
    'numpy >= 2.0.0',
    'ogb >= 1.3.0',
    'PyGSP == 0.5.1',
    'scikit_learn >= 1.4.0',
    'scipy >= 1.14.0',
    'sortedcontainers >= 2.4.0',
    'torch >= 2.0.0',
    'torch_geometric >= 2.4.0',
    'torch_scatter == 2.1.2',
    'torch_sparse == 0.6.18',
    'tqdm >= 4.0.0',
]

setup(
    name=name,  # 包名同工程名，这样导入包的时候更有对应性
    version='1.0.0',
    author="Rockcor",
    author_email='jshmhsb@gmail.com',
    description="Slimming the graph data for graph learning",
    packages=find_packages(),
    package_data={"": ["*"]},  # 数据文件全部打包
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
