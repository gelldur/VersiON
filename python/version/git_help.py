import git
import re
import logging


class GitHelp(object):
    def __init__(self):
        self.repo = git.Repo(search_parent_directories=True)
        self.logger = logging.getLogger("GitHelp")
        self.start_commit = None
        self.end_commit = None

    def get_previous_release_tag(self, head_commit, prefix=None):
        try:
            self.repo.git.show(head_commit)  # check does sha works
        except Exception:
            self.logger.exception(f"Invalid sha1: {head_commit}")
            raise Exception(f"Commit: {head_commit} does not exist in tree?")

        recent_tag = ''
        for tag in  self.repo.git.tag('--sort=-creatordate', f'--merged={head_commit}').split('\n'):
            if prefix is None and len(tag) > 0:
                recent_tag = tag
                break
            elif re.match(prefix, tag):
                recent_tag = tag
                break

        if len(recent_tag) > 0:
            previous_release_tag = recent_tag
            self.logger.info(f"Previous release: {previous_release_tag}")
        else:
            previous_release_tag = None
            self.logger.info("No previous release")

        return previous_release_tag

    def get_commits(self, last_commit_sha1=None, previous_release_tag=None):
        if last_commit_sha1 is not None:
            try:
                self.repo.git.show(last_commit_sha1)  # check does sha works
                self.start_commit = last_commit_sha1
            except Exception:
                self.logger.exception(f"Invalid sha1: {last_commit_sha1}")
                raise Exception(f"Commit: {last_commit_sha1} does not exist in tree?")
        else:
            self.start_commit = self.repo.head.commit.hexsha  # HEAD

        self.end_commit = '' if previous_release_tag is None else '...' + previous_release_tag

        commits_to_release = self.repo.git.log(
            ["--pretty=format:%H", f"{self.start_commit}{self.end_commit}"])
        commits_to_release = [x.strip()
                              for x in commits_to_release.split('\n')]
        commits_to_release = list(filter(None, commits_to_release))

        end_commit = 'HEAD' if len(self.end_commit) < 1 else self.end_commit
        self.logger.info(
            f"In commit range from:{self.start_commit} to:{end_commit}, commit count:{len(commits_to_release)}")
        if len(commits_to_release) < 1:
            self.logger.info(
                f"Nothing to release. Recent release: {previous_release_tag}")
            return []

        commits_to_release_messages = []
        for sha in commits_to_release:
            commit = self.repo.git.log(
                ["-1", "--pretty=format:SHA:%H BODY:%B %N", "{}".format(sha)])
            commits_to_release_messages.append(commit)
        commits_to_release_messages.reverse()  # our assumption
        return commits_to_release_messages

    def create_tag(self, name, commit_sha):
        self.repo.create_tag(name, commit_sha)

    def is_dirty_repository(self):
        return self.repo.is_dirty()
