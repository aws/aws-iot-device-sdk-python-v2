#!/usr/bin/env python3

import shutil
import subprocess
import sys

try:
    import sphinx
except:
    exit('sphinx must be installed via pip')

# Delete existing docs/, so that old no-longer-used files don't sit around forever
# This slows iteration down, so pass --cache to disable
if not '--cache' in sys.argv:
    shutil.rmtree('docs', ignore_errors=True)

# Run sphinx
subprocess.check_call([
    'sphinx-build',
    '-j', 'auto', # parallel build
    '-W', # warnings as errors
    'docsrc',
    'docs'])

# Create empty .nojekyll file, so that Github Pages shows plain old HTML
with open('docs/.nojekyll', 'w'):
    pass
