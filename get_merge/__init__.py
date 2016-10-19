import git
import os
import sys


def validate(repo, parent, branch):
    branch_commits = repo.git.rev_list(branch).split()
    if parent not in set(branch_commits):
        raise ValueError(
            'This commit has not actually been merged into %s' % branch)

    first_parent = repo.git.rev_list(
        branch, first_parent=True).split()
    if parent in set(first_parent):
        raise ValueError(
            'This commit was originally made on the %s branch?' % branch)


def get_first_merge_into(repo, parent, branch):
    """
    Stupid algorithm which works most of the time.

    Follow the commit downstream and return the first merge into another
    branch, as opposed to a merge from another branch. Hopefully, this other
    branch is <branch>.

    Abort if the graph starts branching or terminates.
    """
    children_dict = {}
    for line in repo.git.rev_list(branch, children=True).split('\n'):
        commits = line.split()
        children_dict[commits[0]] = commits[1:]

    parents_dict = {}
    for line in repo.git.rev_list(branch, parents=True).split('\n'):
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
            return None
        if is_second_parent(child, parent):
            return child
        parent = child


def get_ancestry_path_first_parent_match(repo, parent, branch):
    """
    Find the earliest common commit between ancestry-path and first-parent.

    Source: http://stackoverflow.com/a/8492711

    This is the correct algorithm assuming a properly-maintained git
    history. However, if there has ever been a fast-forward merge of a feature
    branch into <branch>, the first-parent history of <branch> will have been
    tampered with and this "correct" approach could fail.
    """
    ancestry_path = repo.git.rev_list(
        parent + '..' + branch, ancestry_path=True).split()
    first_parent = repo.git.rev_list(
        branch, first_parent=True).split()

    for commit in reversed(ancestry_path):
        if commit in first_parent:
            return commit
    return None


def get_merge():
    if 'help' in sys.argv:
        print("""usage: git get-merge <sha> [branch]

Attempt to find when commit <sha> was merged to <branch>, where <branch> is
`master` by default. Two methods are used:

# method 1
%s

# method 2
%s
        """ % (get_first_merge_into.__doc__, get_ancestry_path_first_parent_match.__doc__))
        return 0

    repo = git.Repo(os.getcwd())

    try:
        branch = sys.argv[2]
    except IndexError:
        branch = 'master'

    try:
        parent = repo.git.rev_parse(sys.argv[1])
        repo.git.show(sys.argv[1])  # validate existence
    except (git.exc.GitCommandError, IndexError):
        print('Invalid reference.')
        return 1

    try:
        validate(repo, parent, branch)
    except ValueError as err:
        print('\n'.join(err.args))
        return 1

    guess1 = get_first_merge_into(repo, parent, branch)
    guess2 = get_ancestry_path_first_parent_match(repo, parent, branch)
    if not (guess1 or guess2):
        print('Unable to resolve.')
        return 1
    if (guess1 and guess2) and guess1 != guess2:
        print('Might be either of:')
        print(repo.git.show(guess1))
        print(repo.git.show(guess2))
        return 0
    else:
        print(repo.git.show(guess1 or guess2))
        return 0


if __name__ == '__main__':
    sys.exit(get_merge())
