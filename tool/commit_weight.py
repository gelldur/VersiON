import re
import logging
from versioning import Versioning


def weight_of_commits(versioning, commits):
    logger = logging.getLogger('release')
    if versioning == Versioning.Semantic:
        major = 0
        minor = 0
        patch = 0
        for commit_message in commits:
            if '[MAJOR]' in commit_message:
                major += 1
            elif '[MINOR]' in commit_message:
                minor += 1
            elif '[PATCH]' in commit_message:
                patch += 1
        if patch == 0 and len(commits) > 0:
            patch = 1
        logger.debug("Counted sematic changes: major:{} minor:{} patch:{}".format(
            major, minor, patch))
        if major > 0:
            return 1000000
        if minor > 0:
            return minor * 1000
        return patch
    elif versioning == Versioning.Revision:
        # Revision versioning is interested only in changes count
        return len(commits)
    return 0


#############################################################
# Quick test
commit_major = 'Add Totally new version of app\n\n[MAJOR]\n\nFi far foo bar'
commit_minor = 'Update log API\n\n[MINOR] Foo bar fo fo bar'
commit_patch = 'Fix memory corruption\n\n[PATCH] Blah blah blah'
commit_none = 'Refactor code\n\nWaiting too long with this change'

assert weight_of_commits(Versioning.Semantic, [commit_major]) == 1000000
assert weight_of_commits(Versioning.Semantic, [commit_minor]) == 1000
assert weight_of_commits(Versioning.Semantic, [commit_patch]) == 1
assert weight_of_commits(Versioning.Semantic, [commit_none]) == 1

assert weight_of_commits(Versioning.Semantic, [
                         commit_major, commit_major]) == 1000000
assert weight_of_commits(Versioning.Semantic, [
                         commit_minor, commit_minor]) == 2000
assert weight_of_commits(Versioning.Semantic, [
                         commit_patch, commit_patch]) == 2
assert weight_of_commits(Versioning.Semantic, [commit_none, commit_none]) == 1

assert weight_of_commits(Versioning.Semantic, [
                         commit_major, commit_major, commit_minor]) == 1000000
assert weight_of_commits(Versioning.Semantic, [
                         commit_minor, commit_minor, commit_patch]) == 2000
assert weight_of_commits(Versioning.Semantic, [
                         commit_patch, commit_patch, commit_none]) == 2
assert weight_of_commits(Versioning.Semantic, [
                         commit_none, commit_none, commit_none]) == 1

assert weight_of_commits(Versioning.Semantic, [
                         commit_major, commit_major, commit_patch]) == 1000000
assert weight_of_commits(Versioning.Semantic, [
                         commit_minor, commit_minor, commit_major]) == 1000000
assert weight_of_commits(Versioning.Semantic, [
                         commit_patch, commit_minor, commit_none]) == 1000
assert weight_of_commits(Versioning.Semantic, [
                         commit_patch, commit_none, commit_none]) == 1
