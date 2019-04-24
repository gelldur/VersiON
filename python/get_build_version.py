#!/bin/python3

import logging
import argparse

from version.VersiON import VersiON
import version.git_help


def main(args):
    logger = logging.getLogger(__file__)
    versiON = VersiON(args.style_name, args.config)

    if args.name is not None:
        versiON.style.set_variable('{component_name}', args.name)

    logger.info(f"Picked versioning style: {args.style_name}")

    git = version.git_help.GitHelp()

    previous_release_tag = git.get_previous_release_tag(args.sha1, versiON.style.config['regex'])

    if previous_release_tag is not None and not versiON.match_style(previous_release_tag):
        current_pattern = versiON.style.config['pattern']
        raise Exception(
            f"Different version style. Previous release:{previous_release_tag} and currently picked:{current_pattern}")

    commits_to_release_messages = git.get_commits(args.sha1, previous_release_tag)
    if len(commits_to_release_messages) < 1:
        logger.info("Nothing to release")
        print(previous_release_tag)
        return

    release_name = versiON.bump_version(
        previous_release_tag, commits_to_release_messages)

    if args.enable_mark_wip:
        logger.info("New version (WIP):")
        print(
            f"{release_name}{versiON.config['DEFAULT']['work_in_progress_sufix']}")
    else:
        logger.info("New version:")
        print(release_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", help="Config file path, if not specified then default used. Check config/")
    parser.add_argument(
        "--style-name", help="Example: revision, semantic", required=True)
    parser.add_argument(
        "--name", help="Example: MyApp")
    parser.add_argument(
        "--enable-mark-wip", help="add sufix to VERSION when version isn't released. Sufix is set in config file",
        action="store_true")
    parser.add_argument(
        "--verbose", help="", action="store_true")
    parser.add_argument(
        "--sha1", help="you can specify which commit to treat as HEAD", default="HEAD")

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    main(args)
    exit(0)
