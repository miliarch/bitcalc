from setuptools import setup, find_packages
setup(
    name="bitcalc",
    version="1.0",
    packages=find_packages(),
    install_requires=[],
    author='Marcus Bowman',
    author_email='miliarch.mb@gmail.com',
    description='A python module for managing bit/byte unit manipulation',
    license='MIT',
    keywords='bit byte bitcalc binary decimal base-2 base-10',
    url='https://github.com/miliarch/bitcalc',
    project_urls={
        'Source Code': 'https://github.com/miliarch/bitcalc',
    },
    entry_points={
        'console_scripts': ['bitcalc=bitcalc.interface:main']
    }
)
