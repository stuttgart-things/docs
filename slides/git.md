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
* Creating an annotated tag in Git is simple.
* The easiest way is to specify -a when you run the tag command:

```bash
git tag -a v1.4 -m "my version 1.4"
git tag
v0.1
v1.3
v1.4
```