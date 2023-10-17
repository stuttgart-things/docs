# KUBERNETES CI/CD WORKSHOP

### K8S CI/CD WORKSHOP

<!-- .slide: data-transition="zoom" -->
---
# /AGENDA
--
#/SLOT1
* INTRO <!-- .element: class="fragment fade-up" -->
* GIT BASICS <!-- .element: class="fragment fade-up" -->
* TRUNK-BASED DEVOLPMENT <!-- .element: class="fragment fade-up" -->
* ARGOCD APPSETS <!-- .element: class="fragment fade-up" -->
* EXECRISE #1: GITHUB ENTERPRISE <!-- .element: class="fragment fade-up" -->
--
#/SLOT2
* CI/CD <!-- .element: class="fragment fade-up" -->
* GITHUB ACTIONS <!-- .element: class="fragment fade-up" -->
* PIPELINING <!-- .element: class="fragment fade-up" -->
* VAULT CSI SECRETS PROVIDER <!-- .element: class="fragment fade-up" -->
* EXECRISE #2: GITHUB ACTIONS <!-- .element: class="fragment fade-up" -->
--
#/SLOT3
* TEKTON <!-- .element: class="fragment fade-up" -->
* EXECRISE #3: TEKTON <!-- .element: class="fragment fade-up" -->
* QUIZ <!-- .element: class="fragment fade-up" -->
* SUMMARY <!-- .element: class="fragment fade-up" -->
---
### /Introduction

<span style="color:orange">#DevOps #CICD #Automation #Cloud #IAC</span>
<span style="color:orange">#Kubernetes #Containerization</span> <br><br>

Patrick Hermann
System-Engineer SVA Stuttgart
patrick.hermann@sva.de
--
### /Introduction
* short introduction <!-- .element: class="fragment fade-up" -->
* container technology / kubernetes experiences/knowledge <!-- .element: class="fragment fade-up" -->
* workshop expectations <!-- .element: class="fragment fade-up" -->
---
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
--
### /OVERVIEW
* Online hosts such as GitHub and GitLab can be used for storing a copy of the Git repository, enabling smoother collaboration with other developers <!-- .element: class="fragment fade-up" -->
* Git also supports branching and merging, allowing concurrent development workflows and providing robust tools for handling conflicts during merges <!-- .element: class="fragment fade-up" -->
--
### /What is Git?
* Git is the most commonly used version control system <!-- .element: class="fragment fade-up" -->
* Git tracks the changes you make to files, so you have a record of what has been done, and you can revert to specific versions should you ever need to <!-- .element: class="fragment fade-up" -->
* Git also makes collaboration easier, allowing changes by multiple people to all be merged into one source <!-- .element: class="fragment fade-up" -->
--
### /What is Git?
[<img src="https://www.nobledesktop.com/image/blog/git-branches-merge.png" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
* Git is software that runs locally <!-- .element: class="fragment fade-up" -->
--
### /What is Git?
* Your files and their history are stored on your computer <!-- .element: class="fragment fade-up" -->
* You can also use online hosts (such as GitHub or Bitbucket) to store a copy of the files and their revision history <!-- .element: class="fragment fade-up" -->
--
### /What is Git?
*  Having a centrally located place where you can upload your changes and download changes from others, enable you to collaborate more easily with other developers <!-- .element: class="fragment fade-up" -->
*  Git can automatically merge the changes, so two people can even work on different parts of the same file and later merge those changes without losing each other's work! <!-- .element: class="fragment fade-up" -->
--
### /Git Repositories
* A Git repository (or repo for short) contains all of the project files and the entire revision history <!-- .element: class="fragment fade-up" -->
* You' ll take an ordinary folder of files (such as a website's root folder), and tell Git to make it a repository <!-- .element: class="fragment fade-up" -->
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

```
git clone ssh://john@example.com/path/to/my-project.git
cd my-project
```
<!-- .element: class="fragment fade-up" -->
--
### /Cloning to a specific folder
* Clone the repository located at ＜repo＞ into the folder called ~＜directory＞! on the local machine <!-- .element: class="fragment fade-up" -->

```
git clone <repo> <directory>
```
<!-- .element: class="fragment fade-up" -->
--
### /Tagging
* Like most VCSs, Git has the ability to tag specific points in a repository's history as being important <!-- .element: class="fragment fade-up" -->
* Typically, people use this functionality to mark release points (v1.0, v2.0 and so on) <!-- .element: class="fragment fade-up" -->
* In this section, you'll learn how to list existing tags, how to create and delete tags, and what the different types of tags are <!-- .element: class="fragment fade-up" -->
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
### /Branches
--
* you need to work on a new feature for a website: <!-- .element: class="fragment fade-up" -->
* You create a new branch and start working <!-- .element: class="fragment fade-up" -->
* You haven't finished your new feature, but you get a request to make a rush change that needs to go live on the site today <!-- .element: class="fragment fade-up" -->
--
### /Branches
--
* You switch back to the master branch, make the change, and push it live <!-- .element: class="fragment fade-up" -->
* Then you can switch back to your new feature branch and finish your work <!-- .element: class="fragment fade-up" -->
* When you're done, you merge the new feature branch into the master branch and both the new feature and rush change are kept! <!-- .element: class="fragment fade-up" -->
--
### /Merging
* When you merge two branches (or merge a local and remote branch) you can sometimes get a conflict <!-- .element: class="fragment fade-up" -->
* For example, you and another developer unknowingly both work on the same part of a file <!-- .element: class="fragment fade-up" -->
* The other developer pushes their changes to the remote repo <!-- .element: class="fragment fade-up" -->
* When you then pull them to your local repo you'll get a merge conflict <!-- .element: class="fragment fade-up" -->
* Luckily Git has a way to handle conflicts, so you can see both sets of changes and decide which you want to keep <!-- .element: class="fragment fade-up" -->
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
Commits also create a transparent history of your work that others can follow to understand what you've done and why <!-- .element: class="fragment fade-up" -->
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
---
# /TRUNK-BASED DEVOLPMENT
--
### /TRUNK-BASED DEVOLPMENT
[<img src="https://wpblog.semaphoreci.com/wp-content/uploads/2023/02/unnamed-9.png" width="600"/>](www.google.com) <!-- .element: class="fragment fade-up" -->
* Trunk-based development (TBD) is a source control workflow model that enables continuous integration <!-- .element: class="fragment fade-up" -->
--
## /TRUNK-BASED DEVOLPMENT
* The primary purpose of trunk-based development is to avoid the creation of long-lived branches by merging partial changes to the entire feature <!-- .element: class="fragment fade-up" -->
* Developers can achieve this by committing straight to the main branch or by using short-lived branches with an efficient code review process <!-- .element: class="fragment fade-up" -->
* Branches, by definition, should only live a few days <!-- .element: class="fragment fade-up" -->
--
## /TRUNK-BASED DEVOLPMENT
* trunk-based development, where each developer divides their own work into small batches and merges that work into trunk at least once (and potentially several times) a day <!-- .element: class="fragment fade-up" -->
* The key difference between these approaches is scope <!-- .element: class="fragment fade-up" -->
* Feature branches typically involve multiple developers and take days or even weeks of work <!-- .element: class="fragment fade-up" -->
--
## /TRUNK-BASED DEVOLPMENT
* In contrast, branches in trunk-based development typically last no more than a few hours, with many developers merging their individual changes into trunk frequently <!-- .element: class="fragment fade-up" -->
---
# /ARGOCD APPSETS
--
### /ARGOCD APPSETS
---
# /EXECRISE #1: GITHUB ENTERPRISE
--
### /EXECRISE #1: GITHUB ENTERPRISE
---
# /CICD
--
## /OVERVIEW
* frequently deliver apps to customers by introducing automation into the stages of app development <!-- .element: class="fragment fade-up" -->
* The main concepts: continuous integration, continuous delivery, and continuous deployment <!-- .element: class="fragment fade-up" -->
--
## /OVERVIEW
![cicdcd](https://www.redhat.com/rhdc/managed-files/styles/wysiwyg_full_width/private/ci-cd-flow-desktop.png?itok=NNRD1Zj0)
--
## /OVERVIEW
* ongoing automation and continuous monitoring throughout the lifecycle of apps -> from integration and testing phases to delivery and deployment  <!-- .element: class="fragment fade-up" -->
* often referred to as a "CI/CD pipeline" <!-- .element: class="fragment fade-up" -->
* supported by development and operations teams working together in an agile way  <!-- .element: class="fragment fade-up" -->
--
## /DIFFERENCE BETWEEN CI AND CD
* "CI" in CI/CD always refers to continuous integration <!-- .element: class="fragment fade-up" -->
* which is an automation process for developers <!-- .element: class="fragment fade-up" -->
* Successful CI means new code changes to an app are regularly built, tested, and merged to a shared repository <!-- .element: class="fragment fade-up" -->
* a solution to the problem of having too many branches of an app in development at once (that might conflict with each other) <!-- .element: class="fragment fade-up" -->
--
## /DIFFERENCE BETWEEN CI AND CD
* "CD" in CI/CD refers to continuous delivery and/or continuous deployment <!-- .element: class="fragment fade-up" -->
* which are related concepts that sometimes get used interchangeably <!-- .element: class="fragment fade-up" -->
* Both are about automating further stages of the pipeline <!-- .element: class="fragment fade-up" -->
* sometimes used separately to illustrate just how much automation is happening <!-- .element: class="fragment fade-up" -->
--
## /CONTINUOUS DELIVERY
* a developer's changes to an application are automatically bug tested and uploaded to a repository (like GitHub or a container registry) <!-- .element: class="fragment fade-up" -->
* where they can then be deployed to a live production environment by the operations team <!-- .element: class="fragment fade-up" -->
--
## /CONTINUOUS DELIVERY
* It's an answer to the problem of poor visibility and communication between dev and business teams <!-- .element: class="fragment fade-up" -->
* To that end, the purpose of continuous delivery is to ensure that it takes minimal effort to deploy new code <!-- .element: class="fragment fade-up" -->
--
## /CONTINUOUS DEPLOYMENT
* Continuous deployment  can refer to automatically releasing a developer's changes from the repository to production <!-- .element: class="fragment fade-up" -->
* It addresses the problem of overloading operations teams with manual processes that slow down app delivery <!-- .element: class="fragment fade-up" -->
* It builds on the benefits of continuous delivery by automating the next stage in the pipeline <!-- .element: class="fragment fade-up" -->
---
# /PIPELINES AS CODE
* Benefit from standard source control practices (such as code reviews via pull request and versioning) <!-- .element: class="fragment fade-up" -->
* Can be audited for changes just like any other files in the repository <!-- .element: class="fragment fade-up" -->
* Don't require accessing a separate system or UI to edit <!-- .element: class="fragment fade-up" -->
* Can fully codify the build, test, and deploy process for code <!-- .element: class="fragment fade-up" -->
* Can usually be templatized to empower teams to create standard processes across multiple repositories <!-- .element: class="fragment fade-up" -->
--
# /GIT REPOSITORY SERVICES
* GitHub is the most popular, with an active community of 100 million developers <!-- .element: class="fragment fade-up" -->
* It hosts 372 million repositories and is a favorite for open-source projects <!-- .element: class="fragment fade-up" -->
* with 28 million public repositories. It also provides robust CI/CD pipelines <!-- .element: class="fragment fade-up" -->
--
# /GIT REPOSITORY SERVICES
* GitLab is similar, providing hosting for code repositories <!-- .element: class="fragment fade-up" -->
* it offers a more comprehensive suite of DevOps tools (security testing, monitoring, and more) than its alternatives <!-- .element: class="fragment fade-up" -->
--
# /GIT REPOSITORY SERVICES
* BitBucket is more specialized <!-- .element: class="fragment fade-up" -->
* It's the native Git tool in Atlassian's Open DevOps solution <!-- .element: class="fragment fade-up" -->
* It's designed as a code repository, but only for Jira and Confluence integrations and software projects <!-- .element: class="fragment fade-up" -->
--
# /GITHUB ADVANTAGES
* Benefit from standard source control practices (such as code reviews via pull request and versioning) <!-- .element: class="fragment fade-up" -->
* GitHub Issues: project management tools are included alongside code repositories, including issue tracking <!-- .element: class="fragment fade-up" -->
* Pull request review process: as part of the platform's version control, product managers and project leaders can monitor pull requests more effectively <!-- .element: class="fragment fade-up" -->
--
# /GITHUB ADVANTAGES
* GitHub Actions: automate your build, test, and deployment workflows using secure CI/CD features <!-- .element: class="fragment fade-up" -->
* Social features: know who's following your work, communicate, collaborate on code, and receive notifications <!-- .element: class="fragment fade-up" -->
* Most active dev community on the planet <!-- .element: class="fragment fade-up" -->
--
# /GITHUB ADVANTAGES
* Extensive wikis for every public and private codebase so that it's easy to document product development and collaborate on projects <!-- .element: class="fragment fade-up" -->
* Project milestones: make collaboration easier with project milestones that align with your product roadmap <!-- .element: class="fragment fade-up" -->
--
# /GITHUB ADVANTAGES
* GitHub Copilot X, an AI pair programmer using OpenAI's GPT-4, will make it easier for devs to write code, support pull requests, and integrate AI-powered software development into workflows <!-- .element: class="fragment fade-up" -->
* Advanced security: make apps and products more secure with GitHub Advanced Security. Scan your source code for security weaknesses and vulnerabilities <!-- .element: class="fragment fade-up" -->
--
# /BITBUCKET ADVANTAGES
* Integrated issue tracking and project management solutions, natively compatible with Jira <!-- .element: class="fragment fade-up" -->
* Native support for Mercurial, while GitHub & GitLab only support Git <!-- .element: class="fragment fade-up" -->
* Private code repositories (similar to the others, but Atlassian focused) <!-- .element: class="fragment fade-up" -->
--
# /BITBUCKET ADVANTAGES
* Code insights, giving team members more visibility into code quality via performance metrics and code review analytics <!-- .element: class="fragment fade-up" -->
* Advanced branch permissions for code review and greater security <!-- .element: class="fragment fade-up" -->
--
# /AZURE PIPELINES VS. GITHUB ACTIONS
* GitHub Actions and Azure Pipelines share several configuration similarities <!-- .element: class="fragment fade-up" -->
* migrating to GitHub Actions relatively straightforward <!-- .element: class="fragment fade-up" -->
--
# /SIMILARITIES
* Workflow configuration files are written in YAML and are stored in the code's repository <!-- .element: class="fragment fade-up" -->
* Workflows include one or more jobs <!-- .element: class="fragment fade-up" -->
* Jobs include one or more steps or individual commands <!-- .element: class="fragment fade-up" -->
* Steps or tasks can be reused and shared with the community <!-- .element: class="fragment fade-up" -->
--
* Jobs contain a series of steps that run sequentially <!-- .element: class="fragment fade-up" -->
* Jobs run on separate virtual machines or in separate containers <!-- .element: class="fragment fade-up" -->
* Jobs run in parallel by default, but can be configured to run sequentially <!-- .element: class="fragment fade-up" -->
--
# /KEY DIFFERENCES
When migrating from Azure Pipelines, consider the following differences:

* Azure Pipelines supports a legacy classic editor, which lets you define your CI configuration in a GUI editor instead of creating the pipeline definition in a YAML file <!-- .element: class="fragment fade-up" -->
* GitHub Actions uses YAML files to define workflows and does not support a graphical editor <!-- .element: class="fragment fade-up" -->
* Azure Pipelines allows you to omit some structure in job definitions. For example, if you only have a single job, you don't need to define the job and only need to define its steps <!-- .element: class="fragment fade-up" -->
--
# /KEY DIFFERENCES
* GitHub Actions requires explicit configuration, and YAML structure cannot be omitted <!-- .element: class="fragment fade-up" -->
* Azure Pipelines supports stages defined in the YAML file, which can be used to create deployment workflows. GitHub Actions requires you to separate stages into separate YAML workflow files <!-- .element: class="fragment fade-up" -->
* On-premises Azure Pipelines build agents can be selected with capabilities. GitHub Actions self-hosted runners can be selected with labels <!-- .element: class="fragment fade-up" -->
--
# /BENEFITS OF USING SELF-HOSTED RUNNER
* Improved Performance: By hosting your runners, you can ensure that the build and deployment processes are faster and more reliable, as you have complete control over the hardware and networking resources <!-- .element: class="fragment fade-up" -->
* Increased Security: GitHub self-hosted runners can be configured to run on your own servers, which provides an extra layer of security compared to using shared runners. This helps to protect sensitive information and data in your workflows <!-- .element: class="fragment fade-up" -->
--
# /BENEFITS OF USING SELF-HOSTED RUNNER
* Customizable Environments: With self-hosted runners, you can create custom environments that match your exact needs, including specific software versions and configurations <!-- .element: class="fragment fade-up" -->
* Cost-Effective: If you have a large number of workflows or use cases that require a lot of resources, self-hosted runners can be more cost-effective than using GitHub's shared runners or cloud-based solutions <!-- .element: class="fragment fade-up" -->
--
# /BENEFITS OF USING SELF-HOSTED RUNNER
* High Availability: With self-hosted runners, you can set up Horizontal Runner Autoscaler, which provides redundancy and high availability for your workflows <!-- .element: class="fragment fade-up" -->
* Greater Control: Self-hosted runners give you complete control over the resources and environment used for your workflows, which can help you optimize performance and ensure that your builds and deployments run smoothly <!-- .element: class="fragment fade-up" -->
--
# /GitHub Actions/WORKFLOW (EXAMPLE)
--
### /GitHub Actions/WORKFLOW (EXAMPLE)
```
# workflow.yaml
name: Run git workflow
on:
  workflow_dispatch:
    inputs:
      dev-cleanup:
        description: "Dev: Check to enable deletion of the deployment"
        required: false
        type: boolean
        default: false
  push:
    branches: [ main ]
```
--
### /GitHub Actions/Job DEV (EXAMPLE)
```
# workflow.yaml
# USE IN MAIN BRANCH ONLY
build-helm-staging:
  if: github.event.ref == 'refs/heads/main'
  name: Staging
  needs:
    - Init
  uses: ./.github/workflows/helm.yaml
  with:
    environment-name: dev
    cancel-concurrent: false
    branch-name: ${{ needs.Init.outputs.branch_name }}
  secrets: inherit
```
--
### /GitHub Actions/Job PROD (EXAMPLE)
```
# workflow.yaml
build-helm-production:
  name: Production
  needs:
    - Init
    - Linting-staging
  uses: ./.github/workflows/helm.yaml
  with:
    environment-name: production
    cancel-concurrent: true
    branch-name: ${{ needs.Init.outputs.branch_name }}
  secrets: inherit
```
--
### /GitHub Actions/Job (EXAMPLE)
```
# build-helm.yaml
on:
  workflow_call:
    inputs:
      environment-name:
        required: true
        type: string
      branch-name:
        required: true
        type: string
```
--
### /GitHub Actions/Job (EXAMPLE)
```
# build-helm.yaml
jobs:
  build-helm:
    environment: ${{ inputs.environment-name }}
    steps:
      - name: CHECKOUT GIT
        uses: actions/checkout@v4
      - name: SETUP HELMFILE
        uses: mamezou-tech/setup-helmfile@v1.2.0
```
---
# /VAULT CSI SECRETS PROVIDER
--
### /VAULT CSI SECRETS PROVIDER
---
# /EXECRISE #2: GITHUB ACTIONS
--
### /EXECRISE #2: GITHUB ACTIONS
---
# /TEKTON
--
### /TEKTON
---
# /EXECRISE #3: TEKTON
--
### /EXECRISE #3: TEKTON
---
### /QUIZ
What's a shortcut to staging all the changes you have?
* git add <!-- .element: class="fragment fade-up" -->
* This command is used to stage all the changes you have made in your local repository <!-- .element: class="fragment fade-up" -->
* It allows you to prepare the changes for the next commit <!-- .element: class="fragment fade-up" -->
* By using "GIT add", you are indicating to Git which files or changes you want to include in the next commit <!-- .element: class="fragment fade-up" -->
--
What is k9s?
* provides a terminal UI to interact with your Kubernetes clusters <!-- .element: class="fragment fade-up" -->
--
What is .gitignore
* specify which files or parts of your project should be ignored by Git <!-- .element: class="fragment fade-up" -->
--
How to generate a private ssh key?
* ssh-keygen <!-- .element: class="fragment fade-up" -->
--
What is kube-linter?
* KubeLinter analyzes Kubernetes YAML files and Helm charts <!-- .element: class="fragment fade-up" -->
* checks them against a variety of best practices <!-- .element: class="fragment fade-up" -->
* with a focus on production readiness <!-- .element: class="fragment fade-up" -->
--
How do you supply a commit message to a commit?
* To supply a commit message to a commit in GIT, the correct way is to use the command "GIT commit -m "I'm coding!". <!-- .element: class="fragment fade-up" -->
--
What's the git command that downloads your repository from a git server to your computer?
* git clone <!-- .element: class="fragment fade-up" -->
--
What is docker-compose?
--
Which is the correct order to submit your changes from the working directory all the way to the remote repository?
* git add, git commit, git push <!-- .element: class="fragment fade-up" -->
--
What is the opposite of a GIT clone?
* git push <!-- .element: class="fragment fade-up" -->
---
# /SUMMARY
--
### /SUMMARY
* GIT BASICS <!-- .element: class="fragment fade-up" -->
* ARGOCD APPSETS <!-- .element: class="fragment fade-up" -->
* CI/CD <!-- .element: class="fragment fade-up" -->
* GITHUB ACTIONS <!-- .element: class="fragment fade-up" -->
* VAULT CSI SECRETS PROVIDER <!-- .element: class="fragment fade-up" -->
* TEKTON <!-- .element: class="fragment fade-up" -->
