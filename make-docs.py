import subprocess
try:
    import sphinx
except:
    exit('sphinx must be installed via pip')

subprocess.check_call(['sphinx-build', 'docsrc', 'docs'])
