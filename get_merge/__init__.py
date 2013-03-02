import git
import os
import sys

repo = git.Repo(os.getcwd(), odbt=git.GitCmdObjectDB)

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


def get_merge():
    try:
        parent = repo.git.rev_parse(sys.argv[1])
    except git.exc.GitCommandError:
        print 'Invalid reference.'
        return 1
    while 1:
        try:
            child, = children_dict[parent]
        except ValueError:
            print 'Unable to resolve.'
            return 1
        if is_second_parent(child, parent):
            print repo.git.show(child)
            return 0
        parent = child


if __name__ == '__main__':
    sys.exit(get_merge())
