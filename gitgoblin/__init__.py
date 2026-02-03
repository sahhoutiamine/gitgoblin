"""
GitGoblin - Automatic Git Commit & Push
A mischievous little goblin that watches your files and commits them to GitHub
"""

__version__ = '1.0.0'
__author__ = 'GitGoblin Team'

from .core import GoblinWatcher
from .utils import GoblinStatus

__all__ = ['GoblinWatcher', 'GoblinStatus']
