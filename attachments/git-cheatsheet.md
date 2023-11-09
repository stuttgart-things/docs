# GIT-CHEATSHEET

https://www.codementor.io/@mattgoldspink/git-cheatsheet-du1088tr0

## CREATING REPOSITORIES

### CREATE NEW REPOSITORY IN CURRENT DIRECTORY

```bash
git init
```

### CLONE A REMOTE REPOSITORY

```bash
git clone [url] # git clone https://github.com/jquery/jquery
```

## Branches and Tags

### List all existing branches

```bash
git branch
```

### Switch your HEAD to branch

```bash
git checkout [branch]
```

### Create a new branch based on your current HEAD

```bash
git branch [new-branch]
```

### Create a new branch based on your current HEAD and switch

```bash
git checkout -b [new-branch]
```

### Push local branch to remote branch

```bash
git push -u origin [new-branch]
```

### Create a new tracking branch based on a remote branch

```bash
git checkout --track [remote/branch]
```

## for example track the remote branch named feature-branch-foo

```bash
git checkout --track origin/feature-branch-foo
```

## Delete a local branch

```bash
git branch -d [branch]
```

## Tag the current commit

```bash
git tag [tag-name]
```

## List all new or modified files - showing which are to staged to be commited and which are not

```bash
git status
```

## View changes between staged files and unstaged changes in files

```bash
git diff
```

## View changes between staged files and the latest committed version

```bash
git diff --cached
```

## only one file add the file name

```bash
git diff --cached [file]
```

## Add all current changes to the next commit

```bash
git add [file]
```

## Remove a file from the next commit

```bash
git rm [file]
```

## Add some changes in < file> to the next commit

## Watch these video's for a demo of the power of git add -p - http://johnkary.net/blog/git-add-p-the-most-powerful-git-feature-youre-not-using-yet/

```bash
git add -p [file]
```

## Commit all local changes in tracked  files

```bash
git commit –a
git commit -am "An inline  commit message"
```

## Commit previously staged changes

```bash
git commit
git commit -m "An inline commit message"
```

## Unstages the file, but preserve its contents

```bash
git reset [file]
```

## Show all commits, starting from the latest

```bash
git log
```

## Show changes over time for a specific file

```bash
git log -p [file]
```

## Show who changed each line in a file, when it was changed and the commit id

```bash
git blame -c [file]
```

## List all remotes

```bash
git remote -v
```

## Add a new remote at [url] with the given local name

```bash
git remote add [localname] [url]
```

## Download all changes from a remote, but don‘t integrate into them locally

```bash
git fetch [remote]
```

## Download all remote changes and merge them locally

```bash
git pull [remote] [branch]
```

## Publish local changes to a remote

```bash
git push [remote] [branch]
```

## Delete a branch on the remote

```bash
git branch -dr [remote/branch]
```

## Publish your tags to a remote

```bash
git push --tags
```

## Merge [branch] into your current HEAD

```bash
git merge [branch]
```

## Rebase your current HEAD onto [branch]

```bash
git rebase [branch]
```

## Abort a rebase

```bash
git rebase –abort
```

## Continue a rebase after resolving conflicts

```bash
git rebase –continue
```

## Use your configured merge tool to solve conflicts

```bash
git mergetool
```

## Use your editor to manually solve conflicts and (after resolving) mark as resolved

```bash
git add <resolved- file>
git rm <resolved- file>
```

## Discard all local changes and start working on the current branch from the last commit

```bash
git reset --hard HEAD
```

## Discard local changes to a specific file

```bash
git checkout HEAD [file]
```

## Revert a commit by making a new commit which reverses the given [commit]

```bash
git revert [commit]
```

## Reset your current branch to a previous commit and discard all changes since then

```bash
git reset --hard [commit]
```

## Reset your current branch to a previous commit and preserve all changes as unstaged changes

```bash
git reset [commit]
```

## Reset your current branch to a previous commit and preserve staged local changes

```bash
git reset --keep [commit]
```
