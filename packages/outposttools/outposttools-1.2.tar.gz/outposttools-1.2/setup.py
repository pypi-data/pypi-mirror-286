from setuptools import setup, find_packages

setup(
    name='outposttools',
    version='1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'outpost=outpost.main:main',  # Update with correct entry point
        ],
    },
    package_data={
        'outposttools': ['images/*.ico', 'images/*.png'],  # Include image files
    },
)