#!/usr/bin/env python3
"""
GitGoblin Setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='gitgoblin',
    version='1.0.0',
    description='👹 A mischievous goblin that automatically commits and pushes your Git changes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='GitGoblin Team',
    url='https://github.com/yourusername/gitgoblin',
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'watchdog>=4.0.0',
        'python-daemon>=3.0.0',
    ],
    entry_points={
        'console_scripts': [
            'gitgoblin=gitgoblin.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control :: Git',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    keywords='git automation commit push development workflow',
)
