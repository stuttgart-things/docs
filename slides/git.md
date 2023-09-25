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


https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Git-Branch-Create-Example-Command-Checkout-Commit-Tag
https://www.educative.io/answers/how-to-delete-a-git-branch-locally-and-remotely?utm_campaign=brand_educative&utm_source=google&utm_medium=ppc&utm_content=performance_max&eid=5082902844932096&utm_term=&utm_campaign=%5BNew%5D+Performance+Max&utm_source=adwords&utm_medium=ppc&hsa_acc=5451446008&hsa_cam=18511913007&hsa_grp=&hsa_ad=&hsa_src=x&hsa_tgt=&hsa_kw=&hsa_mt=&hsa_net=adwords&hsa_ver=3&gclid=Cj0KCQjwvL-oBhCxARIsAHkOiu2Qq0skPhHr5fB2RNuDihM29oFojv2oxLlYi0KiHGVhABTZTHDZ_AgaAo0aEALw_wcB

https://itknowledgeexchange.techtarget.com/coffee-talk/files/2021/10/create-git-branches.jpg
--
### /Forking


--
### /Pull Requests
* Pull requests are a way to discuss changes before merging them into your codebase <!-- .element: class="fragment fade-up" -->
* A developer makes changes on a new branch and would like to merge that branch into the master <!-- .element: class="fragment fade-up" -->
* They can create a pull request to notify you to review their code <!-- .element: class="fragment fade-up" -->
* You can discuss the changes, and decide if you want to merge it or not <!-- .element: class="fragment fade-up" -->
--
