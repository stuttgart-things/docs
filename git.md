# stuttgart-things/docs/git

## SNIPPETS

<details><summary>SQUASH COMMITS (e.g. PRE-PR) </summary>

### REQUIREMNT

```
# git branch = e.g. feature branch
# more than one commits on branch
```

### REBASE

```
git rebase -i origin/main
```

* in rebase-editor - pick the first one and squash all others

```bash
# EXAMPLE REBASE - DO NOT COPY THIS LINE
pick 4225ee1 feat: add global storage class
squash d26e006 feat: add the ability for a global storage
squash 0815sfg feat: whatever
```

* save w/ :wq

### COMMIT MESSAGE

* in the commit editor - delete eveything unnessesary, just commit message is important

```bash
# EXAMPLE COMMIT - DO NOT COPY THIS LINE
feat: add global storage class

for deploying vre on multiple sites/clusters
it's important to have the ability for
setting a global storage class for all apps
with one (global) variable. issue:
111-add-the-ability-to-globally-set-storage-class.
```

* save w/ :wq

### FORCE PUSH IN GIVEN BRANCH

```bash
git push origin 111-add-the-ability-to-globally-set-storage-class --force
```

</details>


<details><summary>DELETE LARGE FILES FROM HISTORY</summary>

```bash
git rev-list --objects --all | git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize) %(rest)' |
sort -k3 -n -r | head -n 10

pip3 install git-filter-repo && export PATH=$PATH:~/.local/bin

git-filter-repo --path <FILENAME> --invert-paths --force
```

</details>

<details><summary>SEMANTIC-RELEASE</summary>

## INSTALL

```bash
sudo apt install npm -y
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
source ~/.bashrc
nvm install 20 && nvm use 20
nvm alias default 20
```

```bash
# INSTALL w/ npm
npm install -g --save-dev semantic-release @semantic-release/commit-analyzer @semantic-release/release-notes-generator @semantic-release/changelog @semantic-release/git @semantic-release/github @semantic-release/gitlab
```

## CONFIG (GITLAB; GOLANG)

```bash
---
cat <<EOF > .releaserc
{
  "branches": ["main"],
  "repositoryUrl": "https://codehub.sva.de/Lab/stuttgart-things/homerun/homerun-generic-pitcher.git",
  "gitlabUrl": "https://codehub.sva.de",
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    [
      "@semantic-release/gitlab",
      {
        "assets": ["CHANGELOG.md", "go.mod", "go.sum"],
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
      }
    ]
  ]
}
EOF
```

## POSSIBLE COMMITS

```
git commit -am 'feat: add new authentication middleware' # → Minor version
git commit -am 'fix: resolve panic in user login' # → Patch version
git commit -am 'BREAKING CHANGE: switch to OAuth2 for authentication' # → Major version
```

## DRY RUN

```bash
npx semantic-release --dry-run
```

## RELEASE

```bash
npx semantic-release --debug --no-ci
```

</details>

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
git fetch && git checkout [remote-branch-name]
# e.g. git fetch && git checkout remotes/origin/feature/issue-1/test
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

## TROUBLESHOOTING

<details><summary>PULLING IS NOT POSSIBLE - UNMERGED FILES</summary>

```bash
git reset HEAD~1
git stash
git pull
```

</details>
