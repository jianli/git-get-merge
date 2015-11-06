**git get-merge** is a `git` command to locate the merge that introduced a given commit into your repository's master branch. It is correct with very high probability.

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
