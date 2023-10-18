# /GIT
--
### /OVERVIEW
* Git is the most widely used version control system <!-- .element: class="fragment fade-up" -->
* enabling tracking of changes to files and easier collaboration among multiple users <!-- .element: class="fragment fade-up" -->
* Git can be accessed via a command line or through a desktop app with a graphical user interface, such as Sourcetree <!-- .element: class="fragment fade-up" -->
--
### /OVERVIEW
* A Git repository contains all project files and their complete revision history, which is stored in a .git subfolder <!-- .element: class="fragment fade-up" -->
* Git allows users to 'stage' and 'commit' files, enabling them to choose specific pieces for version tracking and updates <!-- .element: class="fragment fade-up" -->
* Online hosts such as GitHub and GitLab can be used for storing a copy of the Git repository, enabling smoother collaboration with other developers <!-- .element: class="fragment fade-up" -->
* Git also supports branching and merging, allowing concurrent development workflows and providing robust tools for handling conflicts during merges <!-- .element: class="fragment fade-up" -->
--
### /What is Git?
* Git is the most commonly used version control system <!-- .element: class="fragment fade-up" -->
* Git tracks the changes you make to files, so you have a record of what has been done, and you can revert to specific versions should you ever need to <!-- .element: class="fragment fade-up" -->
* Git also makes collaboration easier, allowing changes by multiple people to all be merged into one source <!-- .element: class="fragment fade-up" -->
--
### /What is Git?
https://www.nobledesktop.com/image/blog/git-branches-merge.png

* Git is software that runs locally <!-- .element: class="fragment fade-up" -->
* Your files and their history are stored on your computer <!-- .element: class="fragment fade-up" -->
* You can also use online hosts (such as GitHub or Bitbucket) to store a copy of the files and their revision history <!-- .element: class="fragment fade-up" -->
--
### /What is Git?
*  Having a centrally located place where you can upload your changes and download changes from others, enable you to collaborate more easily with other developers <!-- .element: class="fragment fade-up" -->
*  Git can automatically merge the changes, so two people can even work on different parts of the same file and later merge those changes without losing each other's work! <!-- .element: class="fragment fade-up" -->
--
### /Git Repositories
* A Git repository (or repo for short) contains all of the project files and the entire revision history <!-- .element: class="fragment fade-up" -->
* You' ll take an ordinary folder of files (such as a website’s root folder), and tell Git to make it a repository <!-- .element: class="fragment fade-up" -->
* This creates a .git subfolder, which contains all of the Git metadata for tracking changes <!-- .element: class="fragment fade-up" -->
--
### /Git clone
* primarily used to point to an existing repo and make a clone or copy of that repo at in a new directory, at another location <!-- .element: class="fragment fade-up" -->
* The original repository can be located on the local filesystem or on remote machine accessible supported protocols <!-- .element: class="fragment fade-up" -->
* The git clone command copies an existing Git repository <!-- .element: class="fragment fade-up" -->
--
### /Git clone
* cloning automatically creates a remote connection called "origin" pointing back to the original repository <!-- .element: class="fragment fade-up" -->
* This makes it very easy to interact with a central repository <!-- .element: class="fragment fade-up" -->
--
### /Git clone
* Clone the repository located at ＜repo＞ to the local machine <!-- .element: class="fragment fade-up" -->

```bash
git clone ssh://john@example.com/path/to/my-project.git
cd my-project
# Start working on the project
```
--
### /Cloning to a specific folder
* Clone the repository located at ＜repo＞ into the folder called ~＜directory＞! on the local machine <!-- .element: class="fragment fade-up" -->

```bash
git clone <repo> <directory>
```
--
### /Tagging
* Like most VCSs, Git has the ability to tag specific points in a repository’s history as being important <!-- .element: class="fragment fade-up" -->
* Typically, people use this functionality to mark release points (v1.0, v2.0 and so on) <!-- .element: class="fragment fade-up" -->
* In this section, you’ll learn how to list existing tags, how to create and delete tags, and what the different types of tags are <!-- .element: class="fragment fade-up" -->
--
### /Listing Tags
* Listing the existing tags in Git is straightforward. Just type git tag (with optional -l or --list): <!-- .element: class="fragment fade-up" -->

```bash
git tag
v1.0
v2.0
```
--
### /Creating Tags
* Creating an annotated tag in Git is simple <!-- .element: class="fragment fade-up" -->
* The easiest way is to specify -a when you run the tag command: <!-- .element: class="fragment fade-up" -->

```bash
git tag -a v1.4 -m "my version 1.4"
git tag
v0.1
v1.3
v1.4
```
<!-- .element: class="fragment fade-up" -->
--
### /Git add + Commit
* Each recorded change to a file or set of files is called a commit '
* Before we make a commit, we must tell Git what files we want to commit <!-- .element: class="fragment fade-up" -->
* This is called staging and uses the add command <!-- .element: class="fragment fade-up" -->
--
### /Git add + Commit
* Why must we do this? Why can't we just commit the file directly? <!-- .element: class="fragment fade-up" -->
* Let's say you're working on a two files, but only one of them is ready to commit: <!-- .element: class="fragment fade-up" -->
  * You don't want to be forced to commit both files, just the one that's ready <!-- .element: class="fragment fade-up" -->
  * That's where Git's add command comes in <!-- .element: class="fragment fade-up" -->
  * We add files to a staging area, and then we commit the files that have been staged <!-- .element: class="fragment fade-up" -->
--
### /Git Push
* The git push command is used to upload local repository content to a remote repository <!-- .element: class="fragment fade-up" -->
* Pushing is how you transfer commits from your local repository to a remote repo <!-- .element: class="fragment fade-up" -->
* It's the counterpart to git fetch, but whereas fetching imports commits to local branches, pushing exports commits to remote branches <!-- .element: class="fragment fade-up" -->
--
### /Git Push
*  Remote branches are configured using the git remote <!-- .element: class="fragment fade-up" -->

```
git push <remote> <branch>
```
<!-- .element: class="fragment fade-up" -->
--
### /Branches
* Git lets you branch out from the original code base <!-- .element: class="fragment fade-up" -->
* This lets you more easily work with other developers, and gives you a lot of flexibility in your workflow <!-- .element: class="fragment fade-up" -->

--
* Let's say you need to work on a new feature for a website: <!-- .element: class="fragment fade-up" -->
  * You create a new branch and start working <!-- .element: class="fragment fade-up" -->
  * You haven't finished your new feature, but you get a request to make a rush change that needs to go live on the site today <!-- .element: class="fragment fade-up" -->
  * You switch back to the master branch, make the change, and push it live <!-- .element: class="fragment fade-up" -->
  * Then you can switch back to your new feature branch and finish your work <!-- .element: class="fragment fade-up" -->
  * When you're done, you merge the new feature branch into the master branch and both the new feature and rush change are kept! <!-- .element: class="fragment fade-up" -->
--
### /Merging
* When you merge two branches (or merge a local and remote branch) you can sometimes get a conflict
* For example, you and another developer unknowingly both work on the same part of a file
* The other developer pushes their changes to the remote repo
* When you then pull them to your local repo you'll get a merge conflict.
* Luckily Git has a way to handle conflicts, so you can see both sets of changes and decide which you want to keep.
--
### /Fork
* A fork in Git is simply a copy of an existing repository in which the new owner disconnects the codebase from previous committers <!-- .element: class="fragment fade-up" -->
* A fork often occurs when a developer becomes dissatisfied or disillusioned with the direction of a project and wants to detach their work from that of the original project <!-- .element: class="fragment fade-up" -->
--
### /Fork
* When a git fork occurs, previous contributors will not be able to commit code to the new repository without the owner giving them access to the forked repo <!-- .element: class="fragment fade-up" -->
* either by providing developers the publicly accessible Git URL, or by providing explicit access through user permission in tools like GitHub or GitLab <!-- .element: class="fragment fade-up" -->
--
### /Fork
* There is no git fork command <!-- .element: class="fragment fade-up" -->
* From the command line you can clone a Git repo, you can pull from a Git repo and you can fetch updates from a Git repo <!-- .element: class="fragment fade-up" -->
--
### /Pull Requests
* Pull requests are a way to discuss changes before merging them into your codebase <!-- .element: class="fragment fade-up" -->
* A developer makes changes on a new branch and would like to merge that branch into the master <!-- .element: class="fragment fade-up" -->
* They can create a pull request to notify you to review their code <!-- .element: class="fragment fade-up" -->
* You can discuss the changes, and decide if you want to merge it or not <!-- .element: class="fragment fade-up" -->
--
### /Pull Request Workflow
[<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/0*0frm6MvNkCtuQEMg.png" width="700"/>](https://www.sva.de/index.html)
--
### /Pull Request Workflow
* Pull the changes to your local machine (get the most recent base) <!-- .element: class="fragment fade-up" -->
* Create a branch (version) <!-- .element: class="fragment fade-up" -->
* Commit the changes <!-- .element: class="fragment fade-up" -->
* Push your changes <!-- .element: class="fragment fade-up" -->
* Open a pull request (propose changes) <!-- .element: class="fragment fade-up" -->
* Discuss and review your code <!-- .element: class="fragment fade-up" -->
* Rebase and tests <!-- .element: class="fragment fade-up" -->
* Merge your branch to the master branch <!-- .element: class="fragment fade-up" -->
--
### /CREATE BRANCH
[<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/0*AbFP4SPZZa_3RVHW.png" width="700"/>](https://www.sva.de/index.html)
--
### /CREATE BRANCH
* Create a new branch named feature_x and switch to it using <!-- .element: class="fragment fade-up" -->

```
git checkout -b feature_x
```
<!-- .element: class="fragment fade-up" -->
* a branch is not available to others unless you push the branch to your remote repository <!-- .element: class="fragment fade-up" -->

```
git push origin <branch>
```
<!-- .element: class="fragment fade-up" -->
--
### /Add & commit
```
You can propose changes (add it to the Index) using
git add <filename>
git add *
To actually commit these changes use
git commit -m "Commit message"
```
<!-- .element: class="fragment fade-up" -->
--
### /Add & commit
[<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/0*fCDhhg4mTgqDxXzt.png" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->

This process of adding commits keeps track of your progress as you work <!-- .element: class="fragment fade-up" -->
Commits also create a transparent history of your work that others can follow to understand what you’ve done and why <!-- .element: class="fragment fade-up" -->
--
### /Push your changes
A branch is not available to others unless you push the branch to your remote repository
<!-- .element: class="fragment fade-up" -->

```
git push origin <branch>
```
<!-- .element: class="fragment fade-up" -->
--
### /Open a Pull Request
* Pull Requests initiate discussion about your commits <!-- .element: class="fragment fade-up" -->
* Anyone can see exactly what changes would be merged if they accept your request <!-- .element: class="fragment fade-up" -->

[<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/0*7lSbC78AN6pAgaaB.png" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
--
### /Open a Pull Request
You can open a Pull Request at any point:
* when you have little or no code but want to share some screenshots or general ideas <!-- .element: class="fragment fade-up" -->
* when you're stuck and need help or advice <!-- .element: class="fragment fade-up" -->
* when you're ready for someone to review your work <!-- .element: class="fragment fade-up" -->
--
### /Discuss and review your code
[<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/0*pcvtS8aN4qhzfDYC.png" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->

* Once a Pull Request has been opened, the person or team reviewing your changes may have questions or comments (the most often through your git host platform)
--
### /Discuss and review your code
* Perhaps the coding style doesn't match project guidelines <!-- .element: class="fragment fade-up" -->
* the change is missing unit tests <!-- .element: class="fragment fade-up" -->
* Pull Requests are designed to encourage and capture this type of conversation <!-- .element: class="fragment fade-up" -->
--
### /Rebase and tests
[<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/0*_KV_rWe23HSBrj3U.png" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->

* Once your pull request has been reviewed and the branch passes your tests <!-- .element: class="fragment fade-up" -->
* you can rebase your branch on master (it will use the most recent version of the code base) <!-- .element: class="fragment fade-up" -->
* in order to test all the changes together (production) <!-- .element: class="fragment fade-up" -->
--
### /Rebase
* To take all the changes that were committed on master and replay them on the current branch <!-- .element: class="fragment fade-up" -->

```
git rebase master
```
<!-- .element: class="fragment fade-up" -->

* This operation works by resetting the current branch to the same commit as master, and applying each commit of the current branch <!-- .element: class="fragment fade-up" -->
--
### /Merge
[<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/0*cWYTGbMdR-qJiOks.png" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->

Now that your changes have been verified in production, it is time to merge your code into the master branch <!-- .element: class="fragment fade-up" -->

```
git checkout master
git merge <branch> --no-ff
```
<!-- .element: class="fragment fade-up" -->
--