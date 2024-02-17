# stuttgart-things/docs/git

## SNIPPETS

<details><summary>BRANCHES</summary>

```bash
# LIST ALL EXISTING BRANCHES
git branch

# DELETE LOCAL BRANCH
git branch -d [branch]

# SWITCH YOUR HEAD TO BRANCH
git checkout [branch]

# CREATE A NEW BRANCH BASED ON YOUR CURRENT HEAD
git branch [new-branch]

# CREATE A NEW BRANCH BASED ON YOUR CURRENT HEAD AND SWITCH
git checkout -b [new-branch]

# PUSH LOCAL BRANCH TO REMOTE BRANCH
git push -u origin [new-branch]

# CHECK OUT REMOTE BRANCH
git fetch && git checkout [remote-branch-name] # e.g. remotes/origin/feature/issue-1/test
```

</details>

<details><summary>LOG</summary>

```bash
# SHOW LATEST n commits
git log --pretty=format:"%h"  --first-parent -n [count-commits] [branch-name]
# e.g. git log --pretty=format:"%h"  --first-parent -n 3 remotes/origin/feature/issue-1/test
```

</details>

<details><summary>TAGS</summary>

```bash
# PULL/FETCH TAGS
git fetch --tags --force
git pull --tags

# LIST TAGS
git tag

# CREATE LOCAL TAG
git tag [tagname]

# PUSH SINGLE TAG TO REMOTE
git push origin [tagname]

# PUSH ALL TAGS TO REMOTE
git push origin --tags

# DELETE LOCAL TAG
git tag --delete [tagname]

# DELETE REMOTE TAG '1.0.0'
git push origin :refs/tags/1.0.0
```

</details>
