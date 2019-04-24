import unittest

from version.style.VersionSemanticStyle import VersionSemanticStyle
from version.VersiON import load_config


class TestSemanticVersion(unittest.TestCase):

    def test_Should_return_same_version_When_no_version_calculations_made(self):
        style = VersionSemanticStyle(load_config())
        style.set_current_version("v1.0.0")
        self.assertEqual("v1.0.0", style.get_current_version())

    def test_Should_bump_patch_When_patch_counts(self):
        style = VersionSemanticStyle(load_config())
        style.set_current_version("v3.0.0")
        style.bump_patch = 5
        self.assertEqual("v3.0.5", style.get_current_version())
        style.bump_patch = 1
        self.assertEqual("v3.0.1", style.get_current_version())
        style.bump_patch = 100
        self.assertEqual("v3.0.100", style.get_current_version())

    def test_Should_bump_minor_When_minor_counts(self):
        style = VersionSemanticStyle(load_config())
        style.set_current_version("v3.0.0")
        style.bump_minor = 5
        self.assertEqual("v3.5.0", style.get_current_version())
        style.bump_minor = 1
        self.assertEqual("v3.1.0", style.get_current_version())
        style.bump_minor = 100
        self.assertEqual("v3.100.0", style.get_current_version())

    def test_Should_bump_major_When_major_counts(self):
        style = VersionSemanticStyle(load_config())
        style.set_current_version("v3.0.0")
        style.bump_major = 5
        self.assertEqual("v5.0.0", style.get_current_version())
        style.bump_major = 1
        self.assertEqual("v1.0.0", style.get_current_version())
        style.bump_major = 100
        self.assertEqual("v100.0.0", style.get_current_version())
