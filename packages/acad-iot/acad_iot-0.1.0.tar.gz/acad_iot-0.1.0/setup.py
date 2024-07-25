from setuptools import setup, find_packages

setup(
    name="acad_iot",
    version="0.1.0",
    description="Adaptive Clustering and Anomaly Detection for IoT Network Security",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tuase Shola Emmanuel",
    author_email="quadxome@gmail.com",
    url="https://github.com/xquad/acad_iot/acad_iot",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
