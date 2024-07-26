from setuptools import setup
import os

# Read the version from the VERSION file
base_dir = os.path.dirname(os.path.abspath(__file__))
version_file = os.path.join(base_dir, 'VERSION')
with open(version_file, 'r') as f:
    VERSION = f.read().strip()
thisDir = os.path.dirname(os.path.realpath(__file__))

# Read the requirements from the requirements.txt file
def parse_requirements(filename):
    with open(os.path.join(thisDir, filename)) as f:
        required = f.read().splitlines()
    return required

setup(
    name='gai-common',
    version=VERSION,
    author="kakkoii1337",
    author_email="kakkoii1337@gmail.com",
    package_dir={'': 'src'},
    description = """""",
    long_description="Refer to https://gai-labs.github.io/gai for more information",
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3.10',
        "Development Status :: 3 - Alpha",        
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",        
        'Operating System :: OS Independent',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",        
        "Topic :: Scientific/Engineering :: Artificial Intelligence",        
    ],
    python_requires='>=3.10',
    install_requires=[
        parse_requirements("requirements.txt")
    ]
)