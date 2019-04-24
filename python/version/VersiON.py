import logging
import re
import configparser

from version.style.VersionStyleFactory import create_version_style


# style.VersionStyle(style_name, self.config[style_name])


class VersiON(object):
    def __init__(self, style_name, config_path=None):
        self.logger = logging.getLogger("VersiON")
        self.config = load_config(config_path)
        self.style = create_version_style(style_name, self.config)

    def identify_style(self, version_name):
        '''
        Return matching style for version name variable. e.g. v1.2.3 will return 'semantic'
        '''
        for section in self.config.sections():
            pattern = self.config[section]['pattern']
            regex = self.config[section]['regex']
            regex = re.compile(regex)
            if regex.match(version_name) is not None:
                return section
        raise Exception(f"Unknown versioning pattern: {version_name}")

    def match_style(self, version_pattern):
        return self.style.match_style(version_pattern)

    def bump_version(self, previous_release_tag, commits_to_release_messages):
        if previous_release_tag is None:
            previous_release_tag = self.style.get_current_version()

        if len(commits_to_release_messages) < 1:
            return previous_release_tag

        self.style.set_current_version(previous_release_tag)
        version_after_bump = self.style.bump_version(
            commits_to_release_messages)
        self.logger.debug(f"From version:{previous_release_tag}")
        return version_after_bump


def load_config(config_path=None):
    import os
    from pathlib import Path

    config = configparser.ConfigParser()
    if config_path is None:
        file_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
        version_patterns = file_path / '..' / 'config' / 'version_patterns.ini'
        print(version_patterns)
        config.read(version_patterns)
    else:
        config.read(config_path)

    logger = logging.getLogger("config")

    for section in config.sections():
        pattern = config[section]['pattern']
        regex = config[section]['regex']
        logger.debug(f"Section {section}")
        logger.debug(f"\tpattern: {pattern} with regex: {regex}")
    return config
