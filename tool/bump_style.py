import re

from versioning import *


def bump_version(versioning_patterns, style, version, importance_of_change=1):
    '''
    Should return name of new version after bump.
    Please implement here your own style of version bump
    '''

    regex = versioning_patterns[style]['regex']

    if style == 'semantic':
        return bump_semantic_version(regex, version, importance_of_change)
    elif style == 'revision':
        return bump_revision(regex, version, importance_of_change)

    raise Exception("Not matching version: {}".format(version))


def bump_semantic_version(regex, version, importance_of_change=1):
    versioning_semantic = re.compile(regex)
    match = versioning_semantic.search(version)
    if match is None:
        raise Exception("Not matching version: {}".format(version))

    major = int(match.group(2))
    minor = int(match.group(3))
    patch = int(match.group(4))

    patch_count = importance_of_change % 1000
    minor_count = int(importance_of_change / 1000) % 1000

    if importance_of_change >= 1000000:
        major += 1
        minor = 0
        patch = 0
    elif importance_of_change >= 1000:
        minor += minor_count
        patch = 0
    elif importance_of_change > 0:
        patch += patch_count

    return "{}v{}.{}.{}".format("" if match.group(1) is None else match.group(1), major, minor, patch)


def bump_revision(regex, version, importance_of_change=1):
    # Revision versioning (changes count)
    # example: r241 r[REVISION_NUMBER]
    versioning_revision = re.compile(regex)
    match = versioning_revision.search(version)
    if match is None:
        raise Exception("Not matching version: {}".format(version))

    # When dealing with revision importance of change is set to changes count
    revision = int(match.group(2)) + importance_of_change

    return "{}r{}".format("" if match.group(1) is None else match.group(1), revision)


#############################################################
# Quick test
# assert bump_version('v1.2.3') == 'v1.2.4'
# assert bump_version('prefix-v1.2.3') == 'prefix-v1.2.4'
# assert bump_version('prefix-v1.2.3', 2) == 'prefix-v1.2.5'
# assert bump_version('v1.2.3', 1000) == 'v1.3.0'
# assert bump_version('prefix-v1.2.3', 1000) == 'prefix-v1.3.0'
# assert bump_version('prefix-v1.2.3', 2000) == 'prefix-v1.4.0'
# assert bump_version('v1.2.3', 1000000) == 'v2.0.0'
# assert bump_version('prefix-v1.2.3', 2000000) == 'prefix-v2.0.0'

# assert bump_version('r1') == 'r2'
# assert bump_version('r1', 9) == 'r10'
