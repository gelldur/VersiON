from version.acme import *
from version.style.VersionSemanticStyle import VersionSemanticStyle


class VersionComponentSemanticStyle(VersionSemanticStyle):
    def __init__(self, config):
        super().__init__(config, 'component_semantic')
        self.commit_filters = get_list(self.config['commit_filters'])

    def set_variable(self, variable_name, value):
        super().set_variable(variable_name, value)
        # Need refresh for case if we search for commits that contain {component_name}
        self.commit_filters = get_list(self.config['commit_filters'])

    def calculate_for_commit(self, commit_message):
        if contains(self.commit_filters, commit_message):
            super().calculate_for_commit(commit_message)
