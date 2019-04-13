import re
import logging
import configparser
from enum import Enum


def load_versioning_patterns(config_path=None):
    import os
    from pathlib import Path

    config = configparser.ConfigParser()
    if config_path is None:
        root_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
        version_patterns = root_path / 'config' / 'version_patterns.ini'
        config.read(version_patterns)
    else:
        config.read(config_path)

    logger = logging.getLogger(__name__)

    for section in config.sections():
        pattern = config[section]['pattern']
        regex = config[section]['regex']
        logger.debug(f"Section {section}")
        logger.debug(f"\tpattern: {pattern} with regex: {regex}")
        regex = re.compile(regex)
        assert regex.match(pattern) is not None
    return config


def what_versioning(versioning_patterns, version_pattern):
    for section in versioning_patterns.sections():
        pattern = versioning_patterns[section]['pattern']
        regex = versioning_patterns[section]['regex']
        regex = re.compile(regex)
        if regex.match(version_pattern) is not None:
            return section
    raise Exception(f"Unknown versioning pattern: {version_pattern}")
