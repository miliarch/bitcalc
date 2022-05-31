from setuptools import setup, find_packages
from pathlib import Path
BASE_DIR = Path(__file__).parent
long_description = (BASE_DIR / "README.md").read_text()
setup(
    name="bitcalc",
    version="1.7",
    packages=find_packages(),
    python_requires='>=3',
    install_requires=[],
    author='Marcus Bowman',
    author_email='miliarch.mb@gmail.com',
    description='A python module for managing bit/byte unit manipulation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='bit byte bitcalc binary decimal base-2 base-10 data rate transfer time',
    url='https://github.com/miliarch/bitcalc',
    project_urls={
        'Source Code': 'https://github.com/miliarch/bitcalc',
    },
    entry_points={
        'console_scripts': ['bitcalc=bitcalc.interface:main']
    }
)
