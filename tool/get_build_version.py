#!/bin/python3

# pip install --user gitpython

import logging
import git
import argparse
import common
from pprint import pprint

from versioning import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pattern-name", help="Example: revision, semantic")
    parser.add_argument(
        "--name", help="Example: MyApp")
    parser.add_argument(
        "--enable-rc", help="add sufix '-rc' when version isn't released", action="store_true")
    parser.add_argument(
        "--verbose", help="", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    logger = logging.getLogger(__file__)
    ################################################################################################
    ################################################################################################
    versioning_patterns = load_versioning_patterns()

    prefix = '' if args.name is None else args.name + '-'

    repo = git.Repo(search_parent_directories=True)
    previous_release_tag = common.husk_previous_release(
        args.name, prefix, repo)

    if args.pattern_name is None:
        args.pattern_name = common.discover_versioning_style(
            versioning_patterns, previous_release_tag)

    if not common.check_versioning_style(args.pattern_name, versioning_patterns):
        exit(1)

    start_commit, end_commit, commits_to_release_messages = common.get_commits_message(
        repo, None, previous_release_tag)

    if len(commits_to_release_messages) < 1:
        print(new_release_tag)
        exit(0)

    new_release_tag = common.generate_new_version(start_commit, end_commit, args.pattern_name,
                                                  commits_to_release_messages, prefix,
                                                  previous_release_tag, versioning_patterns)
    if args.enable_rc and new_release_tag not in repo.tags:
        print(f"{new_release_tag}-rc")
    else:
        print(new_release_tag)
