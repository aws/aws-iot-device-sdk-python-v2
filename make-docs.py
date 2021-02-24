#!/usr/bin/env python3

import shutil
import subprocess

try:
    import sphinx
except:
    exit('sphinx must be installed via pip')

# Delete existing docs/, so that old no-longer-used files don't sit around forever
shutil.rmtree('docs', ignore_errors=True)

# Run sphinx
subprocess.check_call(['sphinx-build', 'docsrc', 'docs'])

# Create empty .nojekyll file, so that Github Pages shows plain old HTML
with open('docs/.nojekyll', 'w'):
    pass
