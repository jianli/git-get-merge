**git get-merge** is a `git` command to locate the merge that introduced a
given commit into a given branch in your repository ("master" by default). It
is correct with very high probability.

## Installation

```sh
> pip install git-get-merge
```

## Usage

```sh
> git get-merge d50a9d6
commit bf9629e38ec3f280704fa868e70fbcbfbcc5f442
Merge: 622bc4f d50a9d6
Author: Jian
Date:   Fri Jul 4 02:01:40 2014 +0200

    Merge pull request #5 from lowks/patch-1

    Update setup.py

```

## More Info

```sh
> git get-merge help
usage: git get-merge <sha> [branch]

Attempt to find when commit <sha> was merged to <branch>, where <branch> is
"master" by default. Two methods are used:

# method 1

    Stupid algorithm which works most of the time.

    Follow the commit downstream and return the first merge into another
    branch, as opposed to a merge from another branch. Hopefully, this other
    branch is <branch>.

    Abort if the graph starts branching or terminates.


# method 2

    Find the earliest common commit between ancestry-path and first-parent.

    Source: http://stackoverflow.com/a/8492711

    This is the correct algorithm assuming a properly-maintained git
    history. However, if there has ever been a fast-forward merge of a feature
    branch into <branch>, the first-parent history of <branch> will have been
    tampered with and this "correct" approach could fail.
```

