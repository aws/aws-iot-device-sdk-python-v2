#!/usr/bin/env python3
import argparse
import fnmatch
from genericpath import isfile
import os
import subprocess
import sys

CODEGEN_PHRASES = [
    'This file is generated',
]

IGNORE_PATTERNS = [
    'utils/*',  # this script has the phrase in it
]

ERROR_MSG = """
ERROR: You have changed code-generated files.

If you edited these files by hand, your changes will be erased when the
code-generator is run again. An SDK team member MUST update the code-gen
templates with corresponding changes before merging this Pull Request.

You can ignore this error if you are in fact running the code generator.
"""


def main():
    parser = argparse.ArgumentParser(
        description="Detect edits to code-generated files")
    parser.add_argument('--diff-branch', default='main',
                        help="Branch/commit to diff against")
    parser.add_argument('--diff-repo', default='origin',
                        help="Repository to diff against")
    args = parser.parse_args()

    # chdir to project root
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))

    # get all files with diffs
    git_cmd = ['git', 'diff', '--name-only',
               f"{args.diff_repo}/{args.diff_branch}"]
    git_result = subprocess.run(git_cmd, check=True, stdout=subprocess.PIPE)
    diff_files = git_result.stdout.decode().splitlines()

    # figure out which files were code-generated
    print('Checking files with diffs...')
    any_codegen = False
    for filepath in diff_files:
        is_codegen = False
        ignore = False
        if not os.path.isfile(filepath):
            ignore = True
        if any([fnmatch.fnmatch(filepath, pat)
                for pat in IGNORE_PATTERNS]):
            ignore = True
        if not ignore:
            with open(filepath) as f:
                text = f.read()
                for phrase in CODEGEN_PHRASES:
                    if phrase in text:
                        is_codegen = True
                        any_codegen = True
                        break
        if is_codegen:
            print(f"  ⛔️ GENERATED - {filepath}")
        elif ignore:
            print(f"  ✅ ignored   - {filepath}")
        else:
            print(f"  ✅ normal    - {filepath}")

    if any_codegen:
        print(ERROR_MSG)
        sys.exit(-1)
    else:
        print("No code-generated files were changed.")


if __name__ == '__main__':
    main()
