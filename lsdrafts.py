"""lsdrafts - list draft files"""

import argparse
from collections import defaultdict
import os
import re

__version__ = '0.1'
RELEASED_REGEX = re.compile(r'(.*-rev[A-Z]+) .*(\.\w+)$')
DRAFT_REGEX = re.compile(r'(.*-rev[A-Z]+)\d+ .*(\.\w+)$')


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('root', help='Root directory to search')
    return parser.parse_args()


def list_drafts(root_dir):
    """Recursively search root_dir for draft files which have a
    released version."""
    allfilenames = []
    released = []
    drafts = defaultdict(list)

    # Find all the released files
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            allfilenames.append(f)
            if RELEASED_REGEX.match(f):
                released.append(f)

    # For each released file, find drafts
    for releasedf in released:
        for f in allfilenames:
            if is_draft(releasedf, f):
                drafts[releasedf].append(f)

    return drafts


def is_draft(released, f):
    """Return True if f is a draft of released, otherwise False."""
    draft_match = DRAFT_REGEX.match(f)
    if draft_match:
        released_match = RELEASED_REGEX.match(released)
        if released_match.groups() == draft_match.groups():
            return True
    return False


if '__main__' == __name__:
    args = parse_args()
    drafts = list_drafts(args.root)

    for released_name in drafts:
        print('Drafts of', released_name)
        for draft in drafts[released_name]:
            print(' ' * 9, draft)
