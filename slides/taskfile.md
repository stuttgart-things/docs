# /TASKFILE
--
### /What is Taskfile?
[<img src="https://tsh.io/wp-content/uploads/2021/04/taskfile-preference-meme.png" width="700"/>](https://www.sva.de/index.html)
--
### /What is Taskfile?
*  tool designed to make executing terminal commands or even lists of commands needed for specific operations easier <!-- .element: class="fragment fade-up" -->
* Task is a tool written in Golang <!-- .element: class="fragment fade-up" -->
* The syntax is based on YAML, which requires a specific structure <!-- .element: class="fragment fade-up" -->
* It's a much simpler solution compared to GNU make <!-- .element: class="fragment fade-up" -->
* Getting started with Taskfile is very easy <!-- .element: class="fragment fade-up" -->
--
### /What is make?
[<img src="https://tsh.io/wp-content/uploads/2021/04/gnu-make-meme.jpg" width="700"/>](https://www.sva.de/index.html)
--
### /What is make?
* GNU make is probably the most popular tool for automation setup <!-- .element: class="fragment fade-up" -->
* It's fairly easy to run… and tremendously hard to implement <!-- .element: class="fragment fade-up" -->
* The Makefile documentation proves that this tool has many features for automating processes such as string editing, conditions, loops, recipes, functions, etc. <!-- .element: class="fragment fade-up" -->
--
### /Example #1

```yaml
# Taskfile.yml
version: '3'

tasks:
  greet:
    cmds:
      - echo "Hello World"
```
* To execute the command, you simply run task greet from the same directory as the Taskfile.yml file <!-- .element: class="fragment fade-up" -->
```
task greet
```
--
### /Example #2

```
version: 3
vars:
  PROJECT_NAME:
    sh: pwd | grep -o "[^/]*$"
  DATE:
    sh: date +"%y.%m%d.%H%M"
  UPDATED_TAG:
    sh: old_tag=$(git describe --tags --abbrev=0 | cut -d "." -f3 | cut -d "-" -f1); new_tag=$((old_tag+1)); echo $new_tag
  UPDATED_TAG_VERSION:
    sh: t1=$(git describe --tags --abbrev=0 | cut -f1 -d'.'); t2=$(git describe --tags --abbrev=0 | cut -f2 -d'.'); echo $t1.$t2.{{ .UPDATED_TAG }}
  BRANCH:
    sh: if [ $(git rev-parse --abbrev-ref HEAD) != "main" ]; then echo -$(git rev-parse --abbrev-ref HEAD) ; fi

tasks:
  tag:
    desc: Commit, push & tag the module
    deps: [lint, test]
    cmds:
      - task: git-push
      - rm -rf dist
      - go mod tidy
      - git pull --tags
      - git tag -a {{ .UPDATED_TAG_VERSION }}{{ .BRANCH }} -m 'updated for stuttgart-things {{ .DATE }} for tag version {{ .UPDATED_TAG_VERSION }}{{ .BRANCH }}'
      - git push origin --tags
```
--