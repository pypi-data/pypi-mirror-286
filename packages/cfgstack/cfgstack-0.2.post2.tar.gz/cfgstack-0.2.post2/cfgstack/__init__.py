#! /usr/bin/env python

from __future__ import absolute_import

import importlib.metadata
__version__=importlib.metadata.version("cfgstack")

from .cfgstack import CfgStack
