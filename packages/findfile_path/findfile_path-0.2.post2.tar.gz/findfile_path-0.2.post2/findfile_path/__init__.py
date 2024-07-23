#! /usr/bin/env python

import importlib.metadata
__version__=importlib.metadata.version("findfile_path")

from .findfile_path import findfile_path
