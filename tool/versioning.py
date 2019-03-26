import re
from enum import Enum


class Versioning(Enum):
    Semantic = 1
    Revision = 2


# Semantic versioning
# example: v1.0.2 v[MAJOR.MINOR.PATCH]
versioning_semantic = re.compile(r"(.+?)?v([0-9]+).([0-9]+).([0-9]+)$")

# Revision versioning (changes count)
# example: r241 r[REVISION_NUMBER]
versioning_revision = re.compile("(.+?)?r([0-9]+)$")


def what_versioning(version_pattern):
    if versioning_semantic.match(version_pattern):
        return Versioning.Semantic

    if versioning_revision.match(version_pattern):
        return Versioning.Revision
    raise Exception("Unknown versioning pattern: {}".format(version_pattern))


def extract_prefix(version_pattern):
    if versioning_semantic.match(version_pattern):
        return versioning_semantic.search(version_pattern).group(1)

    if versioning_revision.match(version_pattern):
        return versioning_revision.search(version_pattern).group(1)
    raise Exception("Unknown versioning pattern: {}".format(version_pattern))


#############################################################
# Quick test
assert what_versioning('v1.0.0') == Versioning.Semantic
assert what_versioning('v0.0.0') == Versioning.Semantic
assert what_versioning('r1') == Versioning.Revision
assert what_versioning('r100') == Versioning.Revision
