from setuptools import setup, find_packages

setup(
    name="STVQC_thebiglmaoski",
    version="0.0.1",
    description="Implementation of the ST-VQC in TorchQuantum",
    author="Noah Khan, Hanad Elmi",
    author_email="noahkhan022@gmail.com, slaychomc@gmail.com",
    packages=find_packages(),
    install_requires=[
        "torch>=1.7.0",
        "numpy>=1.19.0",
        "qiskit>=0.39.0",
        "qiskit-ibm-runtime>=0.8.0",
        "matplotlib>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "torchquantum-cli=torchquantum.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
