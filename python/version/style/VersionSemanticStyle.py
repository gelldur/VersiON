import re
from version.style.VersionStyle import VersionStyle
from version.acme import *


class VersionSemanticStyle(VersionStyle):
    def __init__(self, config, name='semantic'):
        if name not in config:
            raise Exception(f"Missing '{name}' config")
        super().__init__(name, config[name])
        self.set_from_config(config[name])

    def set_from_config(self, config):
        self.markers_major = get_list(config['markers_major'])
        self.markers_minor = get_list(config['markers_minor'])
        self.markers_patch = get_list(config['markers_patch'])
        self.bump_major = 0
        self.bump_minor = 0
        self.bump_patch = 0

        # Config check
        if re.match(config['regex'], self.fill_pattern(1, 0, 0)) is None:
            raise Exception("Regex do not match pattern")

    def set_current_version(self, version_name):
        if self.match_style(version_name) == False:
            raise Exception(
                f"Not matching style:{version_name} for {self.name}")
        match = re.search(self.config['regex'], version_name)
        if match is None:
            raise Exception(f"Not matching version: {version_name}")
        self.bump_major = int(match.group(1))
        self.bump_minor = int(match.group(2))
        self.bump_patch = int(match.group(3))

    def calculate_for_commit(self, commit_message):
        if contains(self.markers_major, commit_message):
            self.bump_major += 1
            self.bump_minor = 0
            self.bump_patch = 0
        elif contains(self.markers_minor, commit_message):
            self.bump_minor += 1
            self.bump_patch = 0
        elif contains(self.markers_patch, commit_message):
            self.bump_patch += 1

    def get_current_version(self):
        return self.fill_pattern(self.bump_major, self.bump_minor, self.bump_patch)

    def fill_pattern(self, major, minor, patch):
        pattern = self.config['pattern']
        pattern = pattern.replace('{major}', str(major))
        pattern = pattern.replace('{minor}', str(minor))
        pattern = pattern.replace('{patch}', str(patch))
        return pattern
