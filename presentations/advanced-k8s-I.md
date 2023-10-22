# KUBERNETES WORKSHOP II

### Kubernetes Workshop DAY1

<!-- .slide: data-transition="zoom" -->
---
# /AGENDA DAY1
--
#/SLOT1 [08.30-10.00]
* INTRO
* RECAP/QUESTIONS
* SETUP VM/VSCODE
* GIT: OVERVIEW, REPOSITORY + CLONE
* KUSTOMIZE
* KUSTOMIZE EXERCISE
--
#/SLOT2 [10.00-11.00]
* GIT ADD/COMMIT/PUSH
* RECAP: HELM
* ADVANCED: K9S
* DEPLOYMENT GITEA AKS
* CONFIGURATION GITEA
* GIT EXECRISE #1
--
#/SLOT3 [11.15-12.00]
* GIT BRANCHES/FORKS
* GIT EXECRISE #3
* RECAP: DOCKER-COMPOSE
* RECAP: DOCKER-BUILDS
* RECAP: ENV-VARS/CONFIGURATION
* DEMO WEB-APP EXERCISE #0
--
#/SLOT4 [13.00-14.15]
* QUICK RECAP: SLOT1-3
* DEMO WEB-APP EXERCISE #1
* MARKDOWN
* LOCAL TESTING W/ KIND
* DEMO WEB-APP EXERCISE #2
--
#/SLOT5 [14.30-15.30]
* GIT PULL REQEST WORKFLOW
* LINTING
* DEMO WEB-APP EXERCISE #3
* TASKFILE
* DEMO WEB-APP EXERCISE #4
--
#/SLOT6 [15.45-16.30]
* DEMO WEB-APP EXERCISE #5
* HELMFILE
* DEMO WEB-APP EXERCISE #5
* SUMMARY + PREVIEW DAY #2
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
--
* [<img src="https://tsh.io/wp-content/uploads/2021/04/yaml-file-engineer.jpg" width="600"/>](https://code.visualstudio.com/docs/remote/ssh) <!-- .element: class="fragment fade-up" -->
---
### /QUIZ
What is K8s?
* K8s is another term for Kubernetes <!-- .element: class="fragment fade-up" -->
--
How are Kubernetes and Docker related?
* Docker is an open-source platform used to handle software development <!-- .element: class="fragment fade-up" -->
* main benefit is that it packages the settings and dependencies that the software/application needs to run into a container, which allows for portability and several other advantages <!-- .element: class="fragment fade-up" -->
--
Difference between deploying applications on hosts and containers?
* Deploying Applications consist of an architecture that has an operating system <!-- .element: class="fragment fade-up" -->
* The operating system will have a kernel that holds various libraries installed on the operating system needed for an application <!-- .element: class="fragment fade-up" -->
* Whereas container host refers to the system that runs the containerized processes <!-- .element: class="fragment fade-up" -->
--
What are the features of Kubernetes?
* Kubernetes places control for the user where the server will host the container. It will control how to launch. So, Kubernetes automates various manual processes <!-- .element: class="fragment fade-up" -->
* Kubernetes manages various clusters at the same time <!-- .element: class="fragment fade-up" -->
* It provides various additional services like management of containers, security, networking, and storage <!-- .element: class="fragment fade-up" -->
* Kubernetes self-monitors the health of nodes and containers <!-- .element: class="fragment fade-up" -->
* With Kubernetes, users can scale resources not only vertically but also horizontally that too easily and quickly <!-- .element: class="fragment fade-up" -->
--
What are the main components of Kubernetes architecture?
* There are two primary components of Kubernetes Architecture: the master node and the worker node <!-- .element: class="fragment fade-up" -->
* Each of these components has individual components in them <!-- .element: class="fragment fade-up" -->
--
What is a pod in Kubernetes?
* Pods are high-level structures that wrap one or more containers <!-- .element: class="fragment fade-up" -->
* This is because containers are not run directly in Kubernetes <!-- .element: class="fragment fade-up" -->
* Containers in the same pod share a local network and the same resources, allowing them to easily communicate with other containers in the same pod as if they were on the same machine while at the same time maintaining a degree of isolation <!-- .element: class="fragment fade-up" -->
--
What is a Namespace in Kubernetes?
* Namespaces are used for dividing cluster resources between multiple users <!-- .element: class="fragment fade-up" -->
* They are meant for environments where there are many users spread across projects or teams and provide a scope of resources <!-- .element: class="fragment fade-up" -->
--
What is etcd?
* Kubernetes uses etcd as a distributed key-value store for all of its data, including metadata and configuration data, and allows nodes in Kubernetes clusters to read and write data <!-- .element: class="fragment fade-up" -->
* Although etcd was purposely built for CoreOS, it also works on a variety of operating systems (e.g., Linux, BSB, and OS X) because it is open-source <!-- .element: class="fragment fade-up" -->
* Etcd represents the state of a cluster at a specific moment in time and is a canonical hub for state management and cluster coordination of a Kubernetes cluster <!-- .element: class="fragment fade-up" -->
--
What are the different services within Kubernetes?
* Cluster IP service <!-- .element: class="fragment fade-up" -->
* Node Port service <!-- .element: class="fragment fade-up" -->
* Load Balancer service <!-- .element: class="fragment fade-up" -->
--
What is Kubectl?
* Kubectl is a CLI (command-line interface) that is used to run commands against Kubernetes clusters <!-- .element: class="fragment fade-up" -->
* As such, it controls the Kubernetes cluster manager through different create and manage commands on the Kubernetes component <!-- .element: class="fragment fade-up" -->
--
What is Helm?
* Helm helps you manage Kubernetes applications — Helm Charts help you define, install, and upgrade even the most complex Kubernetes application. Charts are easy to create, version, share, and publish — so start using Helm and stop the copy-and-paste. <!-- .element: class="fragment fade-up" -->
---
### /SETUP VSCODE / Remote - SSH extension
* allows you to open a remote folder on any remote machine with a running SSH server and take full advantage of VS Code's feature set <!-- .element: class="fragment fade-up" -->
* Once connected to a server, you can interact with files and folders anywhere on the remote filesystem <!-- .element: class="fragment fade-up" -->
[<img src="https://code.visualstudio.com/assets/docs/remote/ssh/architecture-ssh.png" width="600"/>](https://code.visualstudio.com/docs/remote/ssh) <!-- .element: class="fragment fade-up" -->
--
### /EXAMPLE SSH CONFIG

* example ssh config

```
Host 172.187.248.49
     AddKeysToAgent yes
     HostName 172.187.248.49
     ForwardAgent yes #FORWARD SSH AGENT
     StrictHostKeyChecking no
     User <USERNAME>
     Port 22
     Protocol 2
     ServerAliveInterval 60
     ServerAliveCountMax 30
```
<!-- .element: class="fragment fade-up" -->
---
# /GIT: OVERVIEW, REPOSITORY + CLONE
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
[<img src="https://www.nobledesktop.com/image/blog/git-branches-merge.png" width="600"/>](https://code.visualstudio.com/docs/remote/ssh) <!-- .element: class="fragment fade-up" -->
--
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

```
git clone <repo> <directory>
```
<!-- .element: class="fragment fade-up" -->
---
# /KUSTOMIZE
--
### /KUSTOMIZE OVERVIEW
* Kustomize is a configuration customization tool for Kubernetes clusters <!-- .element: class="fragment fade-up" -->
* It allows administrators to make declarative changes using untemplated files, leaving original manifests untouched <!-- .element: class="fragment fade-up" -->
* All customization specifications are contained within a kustomization.yaml file, which superimposes specifications on top of existing manifests to generate custom versions of resources <!-- .element: class="fragment fade-up" -->
--
### /USECASE
* With kustomize, your team can ingest any base file updates for your underlying components while keeping use-case specific customization overrides intact <!-- .element: class="fragment fade-up" -->
* Another benefit of utilizing patch overlays is that they add dimensionality to your configuration settings, which can be isolated for troubleshooting misconfigurations or layered to create a framework of most-broad to most-specific configuration specifications <!-- .element: class="fragment fade-up" -->
--
### /reusability
* Base Layer -> Specifies the most common resources <!-- .element: class="fragment fade-up" -->
* Patch Layers -> Specifies use case specific resources <!-- .element: class="fragment fade-up" -->
--
### /Benefits of Using Kustomize
* Reusability <!-- .element: class="fragment fade-up" -->
    * Kustomize allows you to reuse one base file across all of your environments (development, staging, production) and then overlay unique specifications for each <!-- .element: class="fragment fade-up" -->

* Fast Generation <!-- .element: class="fragment fade-up" -->
    * Since Kustomize has no templating language, you can use standard YAML to quickly declare your configurations <!-- .element: class="fragment fade-up" -->

* Easier to Debug <!-- .element: class="fragment fade-up" -->
    * YAML itself is easy to understand and debug when things go wrong <!-- .element: class="fragment fade-up" -->
    * Pair that with the fact that your configurations are isolated in patches, and you’ll be able to triangulate the root cause of performance issues in no time <!-- .element: class="fragment fade-up" -->
    * Simply compare performance to your base configuration and any other variations that are running <!-- .element: class="fragment fade-up" -->
--
### /Kustomise project structure
* A Kustomize project structure typically comprises a base and overlays directory <!-- .element: class="fragment fade-up" -->
* In our sample specification above, the base directory contains a file named kustomization.yaml and manifest files for shared resources <!-- .element: class="fragment fade-up" -->
* The base/kustomization.yaml file declares the resources that Kustomize will include in all environments, while the shared manifest files define specific configurations for these resources <!-- .element: class="fragment fade-up" -->
--
### /Kustomise project structure
```
└── base
│   ├── shared-manifest-file-1.yaml
│   ├── kustomization.yaml
│   └── shared-manifest-file-2.yaml
└── overlays
    ├── env-1
    │   ├── unique-manifest-file-1.yaml
    │   └── kustomization.yaml
    ├── env-2
    │   ├── unique-manifest-file1.yaml
    │   ├── kustomization.yaml
    │   ├── unique-manifest-file2.yaml
    │   └── unique-manifest-file3.yaml
```
--
### /Kustomise project structure
* The overlays directories include customization files (also named kustomization.yaml) that reference configurations within the shared manifests of the base folder and apply defined patches to build custom resources <!-- .element: class="fragment fade-up" -->
* The overlays directory also includes individual manifest files, which Kustomize uses to create resources specific to the environment where the files reside <!-- .element: class="fragment fade-up" -->
--
## Kustomize vs Helm
|                            | Kustomize   | Helm       |
|----------------------------|-------------|------------|
| Method of operation        | overlays    | templating |
| Ease of use                | simple      | complex    |
| Support for packaging      | no          | yes        |
| Native kubectl integration | yes         | no         |
| Declarative/ imperative    | declarative | imperative |
---
# /KUSTOMIZE - EXERCISE
--
### /KUSTOMIZE - EXERCISE
---
# /GIT: ADD/COMMIT/PUSH
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
---
### /RECAP: HELM
--
# /OVERVIEW
* Helm is a package manager for Kubernetes applications that includes templating and lifecycle management functionality <!-- .element: class="fragment fade-up" -->
* It is essentially a package manager for Kubernetes manifests (such as Deployments, ConfigMaps, Services, etc.) that are grouped into charts <!-- .element: class="fragment fade-up" -->
* A chart is just a template for creating and deploying applications on Kubernetes using Helm <!-- .element: class="fragment fade-up" -->
--
### /OVERVIEW
* Charts are written in YAML and contain metadata about each resource in your app (e.g., labels, values, etc.) <!-- .element: class="fragment fade-up" -->
* A chart can be used by itself or combined with other charts into composite charts which can be used as templates for creating new applications or modifying existing ones <!-- .element: class="fragment fade-up" -->
* Helm essentially allows you to manage one chart for your environment <!-- .element: class="fragment fade-up" -->
--
### /Architecture
* Helm Client: The client is the user interface to Helm <!-- .element: class="fragment fade-up" -->
* It is used to create new charts, manage repositories, and release packages <!-- .element: class="fragment fade-up" -->
* The Helm client can be installed on both macOS and Linux <!-- .element: class="fragment fade-up" -->
* Developers also use help to test upgrades before releasing them into production <!-- .element: class="fragment fade-up" -->
--
### /Architecture
* Helm Library: Helm library is a set of client libraries that are used by the clients to interact with the Kubernetes API server to install, upgrade, or roll back charts <!-- .element: class="fragment fade-up" -->
* The tool is installed on every node in the cluster and is a required component for installing any chart <!-- .element: class="fragment fade-up" -->
--
### /What Are Helm Charts?
Chart is the packaging format used by Helm: <!-- .element: class="fragment fade-up" -->
 * it contains the specs that define the Kubernetes objects that the application consists of, such as YAML files and templates, which convert into Kubernetes manifest files <!-- .element: class="fragment fade-up" -->
 * Charts are reusable across environments <!-- .element: class="fragment fade-up" -->
 * This reduces complexity and minimizes duplicates across configurations <!-- .element: class="fragment fade-up" -->
--
### /There are three basic concepts to Helm charts
* Chart: A Helm chart is a pre-configured template for provisioning Kubernetes resources <!-- .element: class="fragment fade-up" -->
* Release: A release represents a chart that has been deployed <!-- .element: class="fragment fade-up" -->
* Repository: A repository is a public or private location for storing charts <!-- .element: class="fragment fade-up" -->
--
### /EXAMPLES
* INSTALL CHARTS:

```
helm repo add loki https://grafana.github.io/loki/charts
helm search repo loki
helm show values loki/loki-stack > loki_values.yaml
helm install loki-stack loki/loki-stack \
-f loki_values.yaml --namespace loki-stack
```
<!-- .element: class="fragment fade-up" -->
--
### /CUSTOM HELM CHARTS
* CREATE CHARTS:

```
helm create mychart
helm install --dry-run --debug ./mychart
helm install --dry-run --debug ./mychart
\--set service.internalPort=8080
helm install example ./mychart --set service.type=NodePort
```
<!-- .element: class="fragment fade-up" -->
---
# /K9s
--
### /What is K9s?
* K9s is a command-line based utility for managing and monitoring Kubernetes clusters <!-- .element: class="fragment fade-up" -->
* It provides a visual interface allowing users to view and manage their Kubernetes resources <!-- .element: class="fragment fade-up" -->
* pods, deployments, and services, in a more intuitive and user-friendly way than using the kubectl command-line tool <!-- .element: class="fragment fade-up" -->
* K9s also offer features such as resource filtering, inline editing, and resource management and deployment tools <!-- .element: class="fragment fade-up" -->
* It is designed to be lightweight, making it a useful tool for developers and administrators who work with Kubernetes clusters on a daily basis <!-- .element: class="fragment fade-up" -->
--
### /Key features
* Resource filtering: Easily filter and find specific resources within your Kubernetes cluster <!-- .element: class="fragment fade-up" -->
* Inline editing: Modify resources directly within K9s, streamlining your workflow <!-- .element: class="fragment fade-up" -->
* Comprehensive resource management and deployment tools: Efficiently manage and deploy resources with an extensive set of tools <!-- .element: class="fragment fade-up" -->
--
### /Key features
* Lightweight design: K9s is designed to be fast and easy to use, making it an ideal choice for daily Kubernetes cluster interactions <!-- .element: class="fragment fade-up" -->
* User-friendly: K9s offers a straightforward and intuitive interface, simplifying Kubernetes management for developers and administrators <!-- .element: class="fragment fade-up" -->
--
### /Viewing resources
* If you are familiar with vim commands, you will be right at home with K9s <!-- .element: class="fragment fade-up" -->
* The way to change what you are seeing is by prefixing the type of resource with a colon <!-- .element: class="fragment fade-up" -->
* in order to view pods in your cluster once you are running K9s, you would type :pods and press enter <!-- .element: class="fragment fade-up" -->
* To switch to viewing nodes, type in :node and press enter <!-- .element: class="fragment fade-up" -->
--
### /USAGE

* CLI:

```
# List all available CLI options
k9s help
# Get info about K9s runtime (logs, configs, etc..)
k9s info
# Run K9s in a given namespace
k9s -n mynamespace
# Run K9s and launch in pod view via the pod command
k9s -c pod
# Start K9s in readonly mode - with all modification commands disable
k9s --readonly
```
<!-- .element: class="fragment fade-up" -->
--
### /Viewing resources
* The way to change what you are seeing is by prefixing the type of resource with a colon <!-- .element: class="fragment fade-up"
* to view pods in your cluster once you are running K9s, you would type :pods and press enter <!-- .element: class="fragment fade-up"
* To switch to viewing nodes, type in :node and press enter <!-- .element: class="fragment fade-up" -->
--
### /Searching
* If you have a lot of resources of a particular type in a cluster, you can quickly search through them using the / command <!-- .element: class="fragment fade-up" -->
* If, for example, you wanted to filter all namespaces you retrieved in the previous section down to just the ones that contain kube in their name, you would type:

```
/kube <enter>
```
<!-- .element: class="fragment fade-up" -->
--
### / ENCODE SECRETS
* SEARCH FOR SECRETS AND ENCODE: <!-- .element: class="fragment fade-up" -->

```
k9s # start
:secrets [NAMESPACE] # show secrets
/mongodb # filter for mongo db
# select secret and encode by pressing x
```
<!-- .element: class="fragment fade-up" -->
---
# /DEPLOYMENT GITEA AKS
---
# /DEPLOYMENT +CONFIGURATION GITEA
---
# /GIT EXECRISES #1
--
Git bietet neben den vorgestellten Konfigurationsmöglichkeiten noch
viele weitere Optionen. Suchen Sie selbstständig nach einer Möglichkeit,
um mit dem config-Befehl die Autokorrektur zu aktivieren. Diese führt
dazu, dass auch bei einem Tippfehler der korrekte Befehl ausgeführt wird.

```bash
git config --global help.autocorrect 1
```

Die Hilfe erreichen Sie über einen der folgenden Befehle: git help init, git
init --help, man git-init (nicht unter Windows) oder git init -h (in
verkürzter Form)
---
# /GIT Branches + Forking
--
### /Branches
* Git lets you branch out from the original code base <!-- .element: class="fragment fade-up" -->
* This lets you more easily work with other developers, and gives you a lot of flexibility in your workflow <!-- .element: class="fragment fade-up" -->
--
### /Branches
* Let's say you need to work on a new feature for a website: <!-- .element: class="fragment fade-up" -->
  * You create a new branch and start working <!-- .element: class="fragment fade-up" -->
  * You haven't finished your new feature, but you get a request to make a rush change that needs to go live on the site today <!-- .element: class="fragment fade-up" -->
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
---
# /MARKDOWN
--
### /MARKDOWN
* Markdown can be converted into other formats (such as HTML) and has been incorporated into many things <!-- .element: class="fragment fade-up" -->
* It's the standard format for ReadMe files in Git <!-- .element: class="fragment fade-up" -->
* John Gruber of Daring Fireball (daringfireball.net) created Markdown <!-- .element: class="fragment fade-up" -->
* He says "Markdown is intended to be as easy-to-read and easy-to-write as is feasible <!-- .element: class="fragment fade-up" -->
* Markdown’s syntax is intended for one purpose: to be used as a format for writing for the web <!-- .element: class="fragment fade-up" -->
--
### /What should a readme file contain?
* Depending on the purpose of a readme file, the following content in particular may be relevant: <!-- .element: class="fragment fade-up" -->
  * A general description of the system or project <!-- .element: class="fragment fade-up" -->
  * The project status is important if the project is still in development <!-- .element: class="fragment fade-up" -->
  * Use the file to mention planned changes and the development direction or indicate the completion date of the project <!-- .element: class="fragment fade-up" -->
  * The requirements on the development environment for integration <!-- .element: class="fragment fade-up" -->
  * A guide to installation and use <!-- .element: class="fragment fade-up" -->
--
### /What should a readme file contain?
* A list of technology used and any links to further information related to this technology <!-- .element: class="fragment fade-up" -->
* Open-source projects that the developers independently modify or expand should be contained in a section on “desired collaboration” in the readme.md file <!-- .element: class="fragment fade-up" -->
* How should problems be handled? How should developers advance the changes? <!-- .element: class="fragment fade-up" -->
  * Known bugs and any bug fixes <!-- .element: class="fragment fade-up" -->
  * FAQ section with all previously asked questions <!-- .element: class="fragment fade-up" -->
  * Copyright and licensing information <!-- .element: class="fragment fade-up" -->
--
### /HEADINGS
```
# header H1
## header H2
### header H3
#### header H4
##### header H5
###### header H6
```
--
### /How to Add image in readme file?
You can add an image as a banner, a gif, a dynamic svg or anything that you like <!-- .element: class="fragment fade-up" -->
Images and gifs are a great way to embed some flair into your profile <!-- .element: class="fragment fade-up" -->

```
<a href="URL_REDIRECT" target="blank"><img align="center" src="URL_TO_YOUR_IMAGE" height="100" /></a>
```
---
# /RECAP: DOCKER-COMPOSE
--
### /DOCKER-COMPOSE
--
* Docker Compose is a tool for running multi-container applications on Docker <!-- .element: class="fragment fade-up" -->
* A Compose file is used to define how one or more containers that make up your application are configured <!-- .element: class="fragment fade-up" -->
* Once you have a Compose file, you can create and start your application with a single command: docker compose up <!-- .element: class="fragment fade-up" -->
--
### /DOCKER-COMPOSE
Using Docker Compose is a three-step process:
* Define your app's environment with a Dockerfile so it can be reproduced anywhere <!-- .element: class="fragment fade-up" -->
* Define the services that make up your app in docker-compose.yml so they can be run together in an isolated environment <!-- .element: class="fragment fade-up" -->
* Lastly, run docker compose up and Compose will start and run your entire app <!-- .element: class="fragment fade-up" -->
--
### /DOCKER-COMPOSE
Example compose file:

```
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
  redis:
    image: redis
```
<!-- .element: class="fragment fade-up" -->
---
# /RECAP: DOCKER-BUILDS
--
### /DOCKER-BUILDS
* A Dockerfile is a text configuration file written using a special syntax <!-- .element: class="fragment fade-up" -->
* It describes step-by-step instructions of all the commands you need to run to assemble a Docker Image <!-- .element: class="fragment fade-up" -->
* The docker build command processes this file generating a Docker Image in your Local Image Cache, which you can then start-up using the docker run command, or push to a permanent Image Repository <!-- .element: class="fragment fade-up" -->
--
### /DOCKERFILE
```
FROM ubuntu:22.04
LABEL maintainer="contact@devopscube.com"
RUN  apt-get -y update && apt-get -y install nginx
COPY files/default /etc/nginx/sites-available/default
COPY files/index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
```
---
# /RECAP: Environment Variables
--
### /Environment Variables
* Environment variables are variables that are available system-wide and are inherited by all spawned child processes and shells <!-- .element: class="fragment fade-up" -->
* The names of the variables are case-sensitive. By convention, environment variables should have UPPER CASE names <!-- .element: class="fragment fade-up" -->
* When assigning multiple values to the variable they must be separated by the colon : character.
There is no space around the equals = symbol <!-- .element: class="fragment fade-up" -->
--
### /list and set environment variables in Linux
* env: The command allows you to run another program in a custom environment without modifying the current one <!-- .element: class="fragment fade-up" -->
* printenv:  The command prints all or the specified environment variables <!-- .element: class="fragment fade-up" -->
* set: The command sets or unsets shell variables. When used without an argument it will print a list of all variables including environment and shell variables, and shell functions <!-- .element: class="fragment fade-up" -->
unset: The command deletes shell and environment variables <!-- .element: class="fragment fade-up" -->
export: The command sets environment variables <!-- .element: class="fragment fade-up" -->
---
# /DEMO APP EXERCISE #1
--
### /DEMO APP EXERCISE #1
---
# /QUICK RECAP: SLOT1-3
--
### /QUICK RECAP: SLOT1-3
---
# /LOCAL TESTING W/ KIND
--
### /What is Kind?
[<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/0*TnRE3e_38kjdBz1j.png" width="400"/>](https://www.metaltoad.com/sites/default/files/inline-images/22605665.jpg)

* Kind that allows to generate clusters on Docker, even multi-node and/or simulating high availability
--
### /Create a Cluster

* CLI commands  <!-- .element: class="fragment fade-up" -->

```
kind create cluster
kind create cluster --name=[cluster-name]
```
<!-- .element: class="fragment fade-up" -->
--
### Create a cluster with more than one node

* config <!-- .element: class="fragment fade-up" -->

```
# three node (two workers) cluster config
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
```
<!-- .element: class="fragment fade-up" -->

* CLI command  <!-- .element: class="fragment fade-up" -->
```
kind create cluster --name=nodes-test --config=workerNodes.yaml
```
--
### How to load a docker image into cluster node
```
kind load docker-image webapp:<username> --name <KIND-CLUSTERNAME>
```
---
# /DEMO APP EXERCISE #2
--
### /DEMO APP EXERCISE #2
---
# /Pull Request Workflow
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
---
# /LINTING
--
### /LINTING
[<img src="https://learnk8s.io/a/4dc900a8608757993b321a4d41489045.svg" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
--
### /LINTING
* Linting is the process of checking the source code for Programmatic as well as Stylistic errors <!-- .element: class="fragment fade-up" -->
* This is most helpful in identifying some common and uncommon mistakes that are made during coding <!-- .element: class="fragment fade-up" -->
--
### /LINTING
* find formatting discrepancies <!-- .element: class="fragment fade-up" -->
* find non-adherence to coding standards and conventions <!-- .element: class="fragment fade-up" -->
* pinpoint possible logical errors in your program <!-- .element: class="fragment fade-up" -->
* Running a lint program over your source code, helps to ensure that source code is legible, readable, less polluted and easier to maintain <!-- .element: class="fragment fade-up" -->
--
### /YAML LINTING
The ecosystem of static checking of Kubernetes YAML files can be grouped in the following categories:

* API validators — Tools in this category validate a given YAML manifest against the Kubernetes API server <!-- .element: class="fragment fade-up" -->
* Built-in checkers — Tools in this category bundle opinionated checks for security, best practices, etc <!-- .element: class="fragment fade-up" -->
* Custom validators — Tools in this category allow writing custom checks in several languages such as Rego and Javascript <!-- .element: class="fragment fade-up" -->
--
### /EXAMPLE: KubeLinter
* KubeLinter analyzes Kubernetes YAML files and Helm charts and checks them against various best practices <!-- .element: class="fragment fade-up" -->
* with a focus on production readiness and security <!-- .element: class="fragment fade-up" -->
--
### /EXAMPLE: KubeLinter
* KubeLinter runs sensible default checks designed to give you useful information about your Kubernetes YAML files and Helm charts <!-- .element: class="fragment fade-up" -->
* Use it to check early and often for security misconfigurations and DevOps best practices <!-- .element: class="fragment fade-up" -->
* Some common issues that KubeLinter identifies are running containers as a non-root user, enforcing least privilege, and storing sensitive information only in secrets <!-- .element: class="fragment fade-up" -->
--
---
# /DEMO APP EXERCISE #3
--
### /DEMO APP EXERCISE #3
---
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

```
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
---
# /DEMO APP EXERCISE #4
--
### /DEMO APP EXERCISE #4
---
# /Helmfile
--
### /OVERVIEW
Helmfile is a declarative spec for deploying helm charts. It lets you... <!-- .element: class="fragment fade-up" -->
    * Keep a directory of chart value files and maintain changes in version control <!-- .element: class="fragment fade-up" -->
    * Apply CI/CD to configuration changes <!-- .element: class="fragment fade-up" -->
    * Periodically sync to avoid skew in environments <!-- .element: class="fragment fade-up" -->
--
### /OVERVIEW
*  Declarative: Write, version-control, apply the desired state file for visibility and reproducibility <!-- .element: class="fragment fade-up" -->
* Modules: Modularize common patterns of your infrastructure, distribute it via Git, S3, etc. to be reused across the entire company <!-- .element: class="fragment fade-up" -->
* Versatility: Manage your cluster consisting of charts, kustomizations, and directories of Kubernetes resources, turning everything to Helm releases <!-- .element: class="fragment fade-up" -->
--
### /EXAMPLE
```
repositories:
- name: prometheus-community
  url: https://prometheus-community.github.io/helm-charts

releases:
- name: prom-norbac-ubuntu
  namespace: prometheus
  chart: prometheus-community/prometheus
  set:
  - name: rbac.create
    value: false
```
--
### /ENVIRONMENTS
```
environments:
  labda-vsphere:
    values:
      - environments/vm.yaml
      - environments/defaults.yaml
      - environments/{{ .Environment.Name }}.yaml
```
--
### /DEFAULTS
```
helmDefaults:
  verify: false
  wait: false
  timeout: 600
  recreatePods: false
  force: true
```
---
# /DEMO APP EXERCISE #5
--
### /DEMO APP EXERCISE #5
---
# /DEMO APP EXERCISE #6
--
### /DEMO APP EXERCISE #6
---
# /SUMMARY
--
### /SUMMARY
* GIT BASICS <!-- .element: class="fragment fade-up" -->
* LINTING / MARKDOWN <!-- .element: class="fragment fade-up" -->
* HELM / KUSTOMIZE <!-- .element: class="fragment fade-up" -->
* KIND <!-- .element: class="fragment fade-up" -->
* TASKFILE <!-- .element: class="fragment fade-up" -->
* PULL REQUEST WORKFLOW <!-- .element: class="fragment fade-up" -->
---
