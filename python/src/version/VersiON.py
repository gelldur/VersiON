import logging
import re
import logging
import configparser


class VersiON:
    def __init__(self, config_path=None):
        self.config = load_config(config_path)
        self.logger = logging.getLogger("VersiON")

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


def load_config(config_path=None):
    import os
    from pathlib import Path

    config = configparser.ConfigParser()
    if config_path is None:
        root_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
        version_patterns = root_path/'..'/'..'/'..'/'config'/'version_patterns.ini'
        config.read(version_patterns)
    else:
        config.read(config_path)

    logger = logging.getLogger("config")

    for section in config.sections():
        pattern = config[section]['pattern']
        regex = config[section]['regex']
        logger.debug(f"Section {section}")
        logger.debug(f"\tpattern: {pattern} with regex: {regex}")
        regex = re.compile(regex)
        assert regex.match(pattern) is not None
    return config
