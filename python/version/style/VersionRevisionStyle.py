import re
from version.style.VersionStyle import VersionStyle


class VersionRevisionStyle(VersionStyle):
    def __init__(self, config, name='revision'):
        if name not in config:
            raise Exception(f"Missing '{name}' config")
        super().__init__(name, config[name])
        self.revision = 0

        if re.match(self.config['regex'], self.fill_pattern(1)) is None:
            raise Exception("Regex do not match pattern")

    def set_current_version(self, version_name):
        if self.match_style(version_name) == False:
            raise Exception(
                f"Not matching style:{version_name} for {self.name}")
        match = re.search(self.config['regex'], version_name)
        if match is None:
            raise Exception(f"Not matching version: {version_name}")
        self.revision = int(match.group(1))

    def calculate_for_commit(self, commit_message):
        self.revision += 1

    def get_current_version(self):
        return self.fill_pattern(self.revision)

    def fill_pattern(self, revision):
        pattern = self.config['pattern']
        pattern = pattern.replace('{revision}', str(revision))
        return pattern
