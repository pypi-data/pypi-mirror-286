from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='bjx_meit1',  # Update this line if you choose a different name
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'opencv-python',
        'tensorflow',
        'keras',
        'matplotlib',
    ],
    description='A toolkit for medical image analysis, including preprocessing, models, and metrics.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Emeka Iwuagwu',
    author_email='e.iwuagwu@hotmail.com',
    url='https://github.com/EmekaIwuagwu/bjx_meit1',  # Update with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)