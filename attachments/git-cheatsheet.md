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

### Create a new branch based on your current HEAD and switch

```bash
git push -u origin [new-branch]
```

### Create a new tracking branch based on a remote branch

```bash
git checkout --track [remote/branch]
```

## for example track the remote branch named feature-branch-foo

git checkout --track origin/feature-branch-foo

## Delete a local branch

git branch -d [branch]

## Tag the current commit

git tag [tag-name]

## List all new or modified files - showing which are to staged to be commited and which are not

git status

## View changes between staged files and unstaged changes in files

git diff

## View changes between staged files and the latest committed version

git diff --cached

## only one file add the file name

git diff --cached [file]

## Add all current changes to the next commit

git add [file]

## Remove a file from the next commit

git rm [file]

## Add some changes in < file> to the next commit

## Watch these video's for a demo of the power of git add -p - http://johnkary.net/blog/git-add-p-the-most-powerful-git-feature-youre-not-using-yet/

git add -p [file]

## Commit all local changes in tracked  files

git commit –a
git commit -am "An inline  commit message"

## Commit previously staged changes

git commit
git commit -m "An inline commit message"

## Unstages the file, but preserve its contents

git reset [file]

## Show all commits, starting from the latest

git log

## Show changes over time for a specific file

git log -p [file]

## Show who changed each line in a file, when it was changed and the commit id

git blame -c [file]

## List all remotes

git remote -v

## Add a new remote at [url] with the given local name

git remote add [localname] [url]

## Download all changes from a remote, but don‘t integrate into them locally

git fetch [remote]

## Download all remote changes and merge them locally

git pull [remote] [branch]

## Publish local changes to a remote

git push [remote] [branch]

## Delete a branch on the remote

git branch -dr [remote/branch]

## Publish your tags to a remote

git push --tags

## Merge [branch] into your current HEAD

git merge [branch]

## Rebase your current HEAD onto [branch]

git rebase [branch]

## Abort a rebase

git rebase –abort

## Continue a rebase after resolving conflicts

git rebase –continue

## Use your configured merge tool to solve conflicts

git mergetool

## Use your editor to manually solve conflicts and (after resolving) mark as resolved

git add <resolved- file>
git rm <resolved- file>

## Discard all local changes and start working on the current branch from the last commit

git reset --hard HEAD

## Discard local changes to a specific file

git checkout HEAD [file]

## Revert a commit by making a new commit which reverses the given [commit]

git revert [commit]

## Reset your current branch to a previous commit and discard all changes since then

git reset --hard [commit]

## Reset your current branch to a previous commit and preserve all changes as unstaged changes

git reset [commit]

##  Reset your current branch to a previous commit and preserve staged local changes

git reset --keep [commit]