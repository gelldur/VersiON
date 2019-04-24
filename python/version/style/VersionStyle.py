import re
import logging


class VersionStyle(object):
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(name)

    def set_variable(self, variable_name, value):
        for key in self.config:
            self.config[key] = self.config[key].replace(variable_name, value)

    def match_style(self, version_pattern):
        return re.match(self.config['regex'], version_pattern)

    def bump_version(self, commits):
        for commit in commits:
            self.calculate_for_commit(commit)
        return self.get_current_version()

    def set_current_version(self, version_name):
        raise NotImplementedError

    def calculate_for_commit(self, commit_message):
        raise NotImplementedError

    def get_current_version(self):
        raise NotImplementedError
