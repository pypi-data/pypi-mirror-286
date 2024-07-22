from setuptools import setup, find_packages

setup(
    name='all_parser',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'python-docx',
        'PyPDF2',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': [
            'all_parser=all_parser.cmd:parse',
        ],
    },
)
