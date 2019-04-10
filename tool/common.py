import logging
import git

from commit_weight import *
from versioning import *
from bump_style import bump_version

logger = logging.getLogger(__name__)


def discover_versioning_style(versioning_patterns, previous_release_tag):
    if previous_release_tag is None:
        raise Exception(
            f"Can't auto discover versioning style. Please provide one.")
    style = what_versioning(versioning_patterns, previous_release_tag)
    logger.info(f"Auto discover of versioning style is: {style}")
    return style


def check_versioning_style(style_name, versioning_patterns):
    logger.info(f"Picked versioning style: {style_name}")
    if style_name not in versioning_patterns:
        logger.error(f"Unknown versioning style: {style_name}")
        logger.info(f"Available styles: {versioning_patterns.sections()}")
        return False
    return True


def husk_previous_release(name, prefix, repo):
    if name is None:
        recent_tag = repo.git.tag('--sort=-creatordate').split('\n', 1)
    else:
        logger.info(f"Searching for last release tag with prefix: {prefix}")
        recent_tag = repo.git.tag(
            '-l', f'{prefix}*', '--sort=-creatordate').split('\n', 1)
        recent_tag = list(filter(None, recent_tag))  # remove empty ones

    if len(recent_tag) > 0:
        previous_release_tag = recent_tag[0]
        logger.info(f"Previous release: {previous_release_tag}")
    else:
        previous_release_tag = None
        logger.info("No previous release")

    return previous_release_tag


def get_commits_message(repo, last_commit_sha1, previous_release_tag):
    start_commit = None
    if last_commit_sha1 is not None:
        try:
            repo.git.show(last_commit_sha1)  # check does sha works
            start_commit = last_commit_sha1
        except Exception:
            logger.exception(f"Invalid sha1: {last_commit_sha1}")
    else:
        start_commit = repo.head.commit.hexsha  # HEAD

    end_commit = '' if previous_release_tag is None else '...' + previous_release_tag

    commits_to_release = repo.git.log(
        ["--pretty=format:%H", f"{start_commit}{end_commit}"])
    commits_to_release = [x.strip()
                          for x in commits_to_release.split('\n')]
    commits_to_release = list(filter(None, commits_to_release))

    if len(commits_to_release) < 1:
        logger.info(
            f"Nothing to release. Recent release: {previous_release_tag}")
        return (start_commit, end_commit, [])

    commits_to_release_messages = []
    for sha in commits_to_release:
        commit = repo.git.log(
            ["-1", "--pretty=format:SHA:%H BODY:%B %N", "{}".format(sha)])
        commits_to_release_messages.append(commit)
    return (start_commit, end_commit, commits_to_release_messages)


def generate_new_version(start_commit, end_commit, pattern_name, commits_to_release_messages, prefix, previous_release_tag, versioning_patterns):
    weight = weight_of_commits(pattern_name, commits_to_release_messages)
    logger.debug(
        f"Weight of commits: {start_commit}{end_commit} is {weight}")
    if weight <= 0:
        logger.info(
            f"Nothing to release in range: {start_commit}{end_commit}")
        return ''

    if previous_release_tag is not None:
        bump_from = previous_release_tag
    else:
        bump_from = prefix + versioning_patterns[pattern_name]['pattern']

    new_release_tag = bump_version(
        versioning_patterns, pattern_name, bump_from, weight)
    logger.info(f"New release available: {new_release_tag}")
    return new_release_tag
