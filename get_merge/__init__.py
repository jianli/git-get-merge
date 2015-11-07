import git
import os
import sys


class NotFound(ValueError):
    pass


def validate(repo, parent):
    master_commits = repo.git.rev_list('master').split()
    if parent not in set(master_commits):
        raise ValueError(
            'This commit has not actually been merged into master.')

    first_parent = repo.git.rev_list(
        'master', first_parent=True).split()
    if parent in set(first_parent):
        raise ValueError(
            'This commit was originally made on the master branch?')


def get_first_merge_into(repo, parent):
    """
    Stupid algorithm which works most of the time.

    Follow the commit downstream and return the first merge into another
    branch, as opposed to a merge from another branch. Hopefully, this other
    branch is master.

    Abort if the graph starts branching or terminates.
    """
    children_dict = {}
    for line in repo.git.rev_list('master', children=True).split('\n'):
        commits = line.split()
        children_dict[commits[0]] = commits[1:]

    parents_dict = {}
    for line in repo.git.rev_list('master', parents=True).split('\n'):
        commits = line.split()
        parents_dict[commits[0]] = commits[1:]

    def is_second_parent(child, parent):
        secondary_parents = parents_dict[child][1:]
        if parent in secondary_parents:
            return True

    while 1:
        try:
            child, = children_dict[parent]
        except (ValueError, KeyError):
            raise NotFound('Unable to resolve.')
        if is_second_parent(child, parent):
            return child
        parent = child


def get_ancestry_path_first_parent_match(repo, parent):
    """
    Find the earliest common commit between ancestry-path and first-parent.

    Source: http://stackoverflow.com/a/8492711

    This is the correct algorithm assuming a properly-maintained git
    history. However, if there has ever been a fast-forward merge of a feature
    branch into master, the first-parent history of master will have been
    tampered with and this "correct" approach could fail.
    """
    ancestry_path = repo.git.rev_list(
        parent + '..master', ancestry_path=True).split()
    first_parent = repo.git.rev_list(
        'master', first_parent=True).split()

    for commit in reversed(ancestry_path):
        if commit in first_parent:
            return commit
    raise NotFound('Unable to resolve.')


def get_merge():
    repo = git.Repo(os.getcwd())

    try:
        parent = repo.git.rev_parse(sys.argv[1])
    except (git.exc.GitCommandError, IndexError):
        print 'Invalid reference.'
        return 1

    commit = None
    try:
        validate(repo, parent)
        try:
            commit = get_first_merge_into(repo, parent)
        except NotFound:
            commit = get_ancestry_path_first_parent_match(repo, parent)
    except ValueError as err:
        print err.message
        return 1

    print repo.git.show(commit)
    return 0


if __name__ == '__main__':
    sys.exit(get_merge())
