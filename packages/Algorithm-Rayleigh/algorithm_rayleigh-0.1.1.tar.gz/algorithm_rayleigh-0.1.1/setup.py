from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "Algorithm_Rayleigh.main",
        ["Algorithm_Rayleigh/main.pyx"],
        include_dirs=[np.get_include()],
    ),
    Extension(
        "Algorithm_Rayleigh.dataPreProcessing",
        ["Algorithm_Rayleigh/dataPreProcessing.pyx"],
        include_dirs=[np.get_include()],
    ),
    Extension(
        "Algorithm_Rayleigh.algorithmRayleigh",
        ["Algorithm_Rayleigh/algorithmRayleigh.pyx"],
        include_dirs=[np.get_include()],
    ),
]

setup(
    name="Algorithm_Rayleigh",
    version="0.1.1",
    author="ZimuZhang",
    author_email="zhang0418zimu@163.com",
    description="Rayleigh algorithm processing for lidar data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    ext_modules=cythonize(extensions),
    include_dirs=[np.get_include()],  # 全局添加 NumPy 头文件路径
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "scipy",
        "cython",
    ],
)
