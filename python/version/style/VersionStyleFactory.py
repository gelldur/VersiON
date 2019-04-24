from version.style.VersionSemanticStyle import VersionSemanticStyle
from version.style.VersionRevisionStyle import VersionRevisionStyle
from version.style.VersionComponentSemanticStyle import VersionComponentSemanticStyle


def create_version_style(version_name, config):
    if version_name is None:
        raise Exception("Please set version style")
    if version_name == 'semantic':
        return VersionSemanticStyle(config)
    if version_name == 'component_semantic':
        return VersionComponentSemanticStyle(config)
    if version_name == 'revision':
        return VersionRevisionStyle(config)
    raise Exception(f"Unknown versioning name:{version_name}")
