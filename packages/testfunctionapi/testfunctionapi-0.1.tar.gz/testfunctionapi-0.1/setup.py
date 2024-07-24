from setuptools import setup, find_packages

setup(
    name='testfunctionapi',
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # List any dependencies here
    entry_points={
        'console_scripts': [
            'functionname=testfunctionapi.function1:my_function',  # Command to run your function from the CLI
        ],
    },
    author='Munshira',
    author_email='munshira@lentra.ai',
    description='A simple example package',
    url='https://github.com/Munshira/PackageTest/testfunctionapi',
)
