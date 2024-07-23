from setuptools import setup, find_packages

setup(
    name="sisense-automl",
    version="0.1.2",
    description="A package for automating machine learning processes using Sisense and AutoML.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hnegi01/sisense_automl.git",
    author="Himanshu Negi",
    author_email="himanshu.negi.08@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'joblib',
        'scikit-learn==0.24.0',
        'auto-sklearn',
        'seaborn',
        'matplotlib',
        'Cython' 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
