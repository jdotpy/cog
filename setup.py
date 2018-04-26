from setuptools import setup, find_packages

setup(
    name='cog',
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        cog=coglib.cli:init
    ''',
)
