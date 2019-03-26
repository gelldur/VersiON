#!/bin/python3

# pip install --user gitpython

import logging
import git
import argparse
from pprint import pprint

from versioning import *
from commit_weight import *
from bump_style import bump_version

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sha1", help="pass sha1 of commit which should be marked as release, by default HEAD")
    parser.add_argument(
        "--pattern", help="", required=True)
    parser.add_argument(
        "--dry-run", help="Simulate what would be done", action="store_true")
    parser.add_argument(
        "--verbose", help="", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger('release')

    versioning = what_versioning(args.pattern)
    logger.info("Detected versioning style: {}".format(versioning))

    repo = git.Repo(search_parent_directories=True)

    prefix = extract_prefix(args.pattern)
    if prefix is None:
        recent_tag = repo.git.tag('--sort=-creatordate').split('\n', 1)
    else:
        recent_tag = repo.git.tag(
            '-l', '{}*'.format(prefix), '--sort=-creatordate').split('\n', 1)
        recent_tag = list(filter(None, recent_tag))  # remove empty ones

    if len(recent_tag) > 0:
        previous_release_tag = recent_tag[0]
        logger.info("Previous release: {}".format(previous_release_tag))

        if what_versioning(previous_release_tag) != versioning:
            logger.error("Different versioning!")
            raise Exception()

    else:
        previous_release_tag = None
        logger.info("No previous release")

    start_commit = None
    if args.sha1 is not None:
        try:
            repo.git.show(args.sha1)  # check does sha works
            start_commit = args.sha1
        except Exception:
            logger.exception("Invalid sha1: {}".format(args.sha1))
    else:
        start_commit = repo.head.commit.hexsha  # HEAD

    end_commit = '' if previous_release_tag is None else '...' + previous_release_tag

    commits_to_release = repo.git.log(
        ["--pretty=format:%H", "{}{}".format(start_commit, end_commit)])
    commits_to_release = [x.strip()
                          for x in commits_to_release.split('\n')]
    commits_to_release = list(filter(None, commits_to_release))

    if len(commits_to_release) < 1:
        logger.info("Nothing to release. Recent release: {}".format(
            previous_release_tag))
        exit(0)

    commits_to_release_messages = []
    for sha in commits_to_release:
        commit = repo.git.log(
            ["-1", "--pretty=format:SHA:%H BODY:%B %N", "{}".format(sha)])
        commits_to_release_messages.append(commit)

    weight = weight_of_commits(versioning, commits_to_release_messages)
    logger.debug("Weight of commits: {}{} is {}".format(
        start_commit, end_commit, weight))
    if weight <= 0:
        logger.info("Nothing to release in range: {}{}".format(
            start_commit, end_commit))
        exit(0)

    bump_from = previous_release_tag if previous_release_tag is not None else args.pattern
    new_release_tag = bump_version(bump_from, weight)
    logger.info("New release available: {}".format(new_release_tag))

    if not args.dry_run:
        repo.create_tag(new_release_tag, start_commit)
