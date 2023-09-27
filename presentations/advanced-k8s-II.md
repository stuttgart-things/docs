# KUBERNETES WORKSHOP II

### Kubernetes Workshop DAY2
<!-- .slide: data-transition="zoom" -->
---
# /AGENDA DAY2
* QUIZ <!-- .element: class="fragment fade-up" -->
* CI/CD <!-- .element: class="fragment fade-up" -->
* GIT-STRATEGYS <!-- .element: class="fragment fade-up" -->
* EXERCISE: BRANCH/PULL-REUEST <!-- .element: class="fragment fade-up" -->
--
# /AGENDA DAY2
* PIPELING <!-- .element: class="fragment fade-up" -->
* EXERCISE: TASKFILE <!-- .element: class="fragment fade-up" -->
* GITHUB EXAMPLE PIPELINE WORKFLOW <!-- .element: class="fragment fade-up" -->
* AZURE PIPELINES VS. GITHUB ACTIONS <!-- .element: class="fragment fade-up" -->
--
# /AGENDA DAY2
* ARGO-CD <!-- .element: class="fragment fade-up" -->
* EXERCISE: ARGO-CD <!-- .element: class="fragment fade-up" -->
* SUMMARY + QA <!-- .element: class="fragment fade-up" -->
---
### /QUIZ
What's a shortcut to staging all the changes you have?
* git add <!-- .element: class="fragment fade-up" -->
* This command is used to stage all the changes you have made in your local repository <!-- .element: class="fragment fade-up" -->
* It allows you to prepare the changes for the next commit <!-- .element: class="fragment fade-up" -->
* By using "GIT add", you are indicating to Git which files or changes you want to include in the next commit <!-- .element: class="fragment fade-up" -->
--
What is k9s?
--
What is kube-linter?
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
# /CI/CD
--
### /Kontinuierlicher Entwicklungsprozess
[<img src="https://artifacts.tiab.labda.sva.de/images/kubernetes/cicdcd.png" width="700"/>](https://www.sva.de/index.html)
--
### /Continuous Integration
* Änderungen an der gemeinsam genutzten Quellcode-Basis einer Applikation werden i.d.R. von mehreren Softwareentwicklern durchgeführt, welche parallel an verschiedenen Programmteilen bzw. Funktionen (engl. features) arbeiten <!-- .element: class="fragment fade-up" -->
* Durch jede Änderung an der Codebasis wird beim Continuous Integration-Ansatz eine automatische Kompilierung (engl. build) der Software ausgelöst <!-- .element: class="fragment fade-up" -->
--
### /Continuous Integration
* Bei diesem Vorgang werden durch anschließende Tests aufgetretene Fehler zurückgemeldet <!-- .element: class="fragment fade-up" -->
* Die Zusammenführung (engl. merge) der Änderungen und die Integration in die Hauptlinie der Quellcodeverwaltung soll auf täglicher Basis und (weitestgehend) automatisiert stattfinden <!-- .element: class="fragment fade-up" -->
--
### /Continuous Integration
* Das Ziel von CI ist die Schaffung eine stabile Code-Basis, welche Risiken von fehlgeschlagenen und aufwendigen Integrationen zu späteren, unregelmäßigen Zeitpunkten minimieren soll <!-- .element: class="fragment fade-up" -->
--
### /Continuous Delivery
* Software-Releases in die Produktion zu bringen, ist mit grundsätzlichen Risiken verbunden, wie z.B. Programmfehlern, Inkompatibilitäten mit Fremdsystemen oder vorhandener Datenstämme oder unvorhergesehener Zeitverzögerungen bei der Bereitstellung <!-- .element: class="fragment fade-up" -->
* Um den Risiken von Deployments aus dem Weg zu gehen, wird "in der klassischen IT" versucht, diese mit einem maximal möglich großen Programm-Funktionsumfang und möglichst selten durchzuführen <!-- .element: class="fragment fade-up" -->
--
### /Continuous Delivery
* Im Gegensatz dazu steht der Continuous Delivery Ansatz dafür, möglichst häufige Releases mit kleinen Änderungen auf eine Produktionsumgebung zu bringen <!-- .element: class="fragment fade-up" -->
* So soll die Fehler-Wahrscheinlichkeit minimiert werden <!-- .element: class="fragment fade-up" -->
* Die Voraussetzungen dafür sind erprobte und optimierte automatisierte Prozesse von der Quellcode-Zusammenführung, Testing bis hin zur Erstellung von Build-Paketen welche auf Entwicklungs und Integrationsumgebungen (engl. Staging) erprobt wurden <!-- .element: class="fragment fade-up" -->
--
### /Continuous Deployment:
* Auf Basis in der Continuous Delivery-Phase erstellter, produktionsreifer Build-Pakete kann durch Implementierung von Continuous Deployment auch die produktive Freigabe einer Applikation und die entsprechende Bereitstellung automatisiert werden <!-- .element: class="fragment fade-up" -->
--
### /Continuous Deployment:
* Continuous Deployment bedeutet, dass Quellcode-Änderungen der Entwickler innerhalb kürzester Zeit produktiv bereitstehen, sofern alle automatisierten Tests erfolgreich durchlaufen wurden <!-- .element: class="fragment fade-up" -->
--
### /CI-CD Prozess
[<img src="https://artifacts.tiab.labda.sva.de/images/kubernetes/cicdprocess.png" width="700"/>](https://www.sva.de/index.html)
--
### /Pipelining
* CI/CD Pipelines werden eingesetzt um: <!-- .element: class="fragment fade-up" -->
  * schnelles Feedback auf Änderungen an der Codebasis zu erhalten <!-- .element: class="fragment fade-up" -->
  * um einen iterativen, automatisierten und möglichst oft erprobten Weg zu entwickeln in Bezug auf die Überführung von Software in einen produktiven Status <!-- .element: class="fragment fade-up" -->
--
### /Pipelining
* Die detaillierte Umsetzung einer CI/CD Pipeline variieret zwischen Unternehmen bzw. Einsatzszenariio, da sie auch von gegebenen Geschäftsprozessen wie z.B. den Softwarefreigabe-Mechanismen oder Compliance-Richtlinien abhängen können <!-- .element: class="fragment fade-up" -->
* Eine CI/CD-Pipeline ist in unterschiedliche Stufen (engl. stages) untergliedert um einzelne Prozessphase logisch voneinander abzugrenzen zu können <!-- .element: class="fragment fade-up" -->
--
### /Möglicher Prozessablauf einer CI/CD Pipeline
* Die folgende Beschreibung zu einem möglichen Prozessablauf einer CI/CD Pipeline bezieht sich auf einen iterativ entwickelten und containerisierten Microservice für die Zielplattform Kubernetes <!-- .element: class="fragment fade-up" -->
--
### /Code commit
* Die erste Phase des Prozessablaufs wird  durch eine Änderung der Code-Basis (engl. code commit) ausgelöst <!-- .element: class="fragment fade-up" -->
* Jede Änderung am zentralen Quellcode-Bestand resultiert in einer Ausführung (engl. run) der Pipeline-Definition <!-- .element: class="fragment fade-up" -->
--
### /Software-Build
* Im Prozessschritt Build wird aus der vorliegenden Code-Basis eine ausführbare Applikation gebildet und als Software-Artefakt z.B. als ausführbare Binärdatei gespeichert <!-- .element: class="fragment fade-up" -->
* Die Ausführung statischer und dynamischer Codeanalysen und in vielen Fällen spezifische Software-Funktionstests erlaubt es Entwicklern zu bestimmen, welcher Software-Build sich für eine produktive Bereitstellung eignet <!-- .element: class="fragment fade-up" -->
--
### /Artefakte
* Für die Weiterverwendung von erstellten Artefakten, werden diese in einem entsprechenden Repository gespeichert <!-- .element: class="fragment fade-up" -->
* Sollten in diesem Stadium keine Fehler gefunden werden, wird automatisch die nächste Stufe der Pipeline ausgeführt <!-- .element: class="fragment fade-up" -->
--
### /Container-Build
* Um vollumfängliche CI/CD Pipelines mittels des Infrastructure as Code Ansatzes umsetzen zu können, bietet sich beispielsweise die DevOps-Plattformlösung <!-- .element: class="fragment fade-up" --> [GitLab](https://about.gitlab.com/) an.
--
### /Ausschnitt einer möglichen CI/CD-Pipeline in GitLab
```
 stages:
 - build
 build_container:
   stage: build
   image: buildah:1.15.0
   script:
     - buildah bud -t ${IMAGE_NAME}:${CI_COMMIT_SHA} .
     - buildah push ${IMAGE_NAME}:${CI_COMMIT_SHA}
       docker://${IMAGE_NAME}:${CI_COMMIT_SHA}
```
<!-- .element: class="fragment fade-up" -->
--
### /Ausschnitt einer möglichen CI/CD-Pipeline in GitLab
* Container-Images werden im gegebenen Beispiel über das OCI-konforme Werkzeug <!-- .element: class="fragment fade-up" --> [Buildah](https://github.com/) realisiert
* Die zugehörige Pipeline-Definition ist eine Mischung aus deklarativen Angaben zum Status bzw. Konfiguration der Pipeline (Zeile:1-5) und imperativen, nacheinander auszuführenden Befehlen (Z:7-9) <!-- .element: class="fragment fade-up" -->
* Mittels Buildah wird ein neuer Container gebaut und anschließend als Artefakt in eine Container Registry verschoben <!-- .element: class="fragment fade-up" -->
--
### /Staging
* Software wird im Entwicklungsprozess i.d.R. auf verschiedenen Betriebsumgebungen (engl. stage) getestet, um etwaige Programmfehler feststellen zu können und die Kommunikation bzw. Zusammenspiel mit Drittsystemen sicherstellen zu können <!-- .element: class="fragment fade-up" -->
* Die technische Bereitstellung kann mittels Infrastructure-as-Code automatisiert innerhalb einer Pipeline-Definition bis zum finalen Stadium "Produktion" (engl. release stage) nach dem Ansatz Continous Deployment realisiert werden <!-- .element: class="fragment fade-up" -->
---
# /GIT-STRATEGYS
--
### /characteristics git/branching strategy
* Provides a clear path for the development process from initial changes to production <!-- .element: class="fragment fade-up" -->
* Allows users to create workflows that lead to structured releases <!-- .element: class="fragment fade-up" -->
* Enables parallel development <!-- .element: class="fragment fade-up" -->
--
### /characteristics git/branching strategy
* Optimizes developer workflow without adding any overhead <!-- .element: class="fragment fade-up" -->
* Enables faster release cycles <!-- .element: class="fragment fade-up" -->
* Efficiently integrates with all DevOps practices and tools such as different version control systems <!-- .element: class="fragment fade-up" -->
* Offers the ability to enable GitOps (if you require it) <!-- .element: class="fragment fade-up" -->
--
### /FEATURE-BRANCHES
* a developer or a group of developers create a branch usually from trunk (also known as main or mainline) <!-- .element: class="fragment fade-up" -->
* work in isolation on that branch until the feature they are building is complete <!-- .element: class="fragment fade-up" -->
* When the team considers the feature ready to go, they merge the feature branch back to trunk <!-- .element: class="fragment fade-up" -->
--
### /TRUNK-BASED DEVOLPMENT
[<img src="https://statusneo.com/wp-content/uploads/2022/08/tbd_workflow.drawio-1-1.png" width="600"/>](www.google.com)
* Trunk-based development (TBD) is a source control workflow model that enables continuous integration <!-- .element: class="fragment fade-up" -->
--
### /TRUNK-BASED DEVOLPMENT
* The primary purpose of trunk-based development is to avoid the creation of long-lived branches by merging partial changes to the entire feature <!-- .element: class="fragment fade-up" -->
* Developers can achieve this by committing straight to the main branch or by using short-lived branches with an efficient code review process <!-- .element: class="fragment fade-up" -->
* Branches, by definition, should only live a few days <!-- .element: class="fragment fade-up" -->
--
### /TRUNK-BASED DEVOLPMENT
* trunk-based development, where each developer divides their own work into small batches and merges that work into trunk at least once (and potentially several times) a day <!-- .element: class="fragment fade-up" -->
* The key difference between these approaches is scope <!-- .element: class="fragment fade-up" -->
* Feature branches typically involve multiple developers and take days or even weeks of work <!-- .element: class="fragment fade-up" -->
--
* In contrast, branches in trunk-based development typically last no more than a few hours, with many developers merging their individual changes into trunk frequently <!-- .element: class="fragment fade-up" -->
--
# /GITLAB-FLOW best practices
[what-are-gitlab-flow-best-practices](https://about.gitlab.com/topics/version-control/what-are-gitlab-flow-best-practices/)
--
### /Use feature branches..
* ..rather than direct commits on the main branch <!-- .element: class="fragment fade-up" -->
* feature branches is a simple way to develop <!-- .element: class="fragment fade-up" -->
* keep the source code clean <!-- .element: class="fragment fade-up" -->
* developers should create a branch for anything they're working on <!-- .element: class="fragment fade-up" -->
* -> contributors can easily start the code review process before merging <!-- .element: class="fragment fade-up" -->
--
### /Test all commits, not only ones on the main branch.
* Some developers set up their CI to only test what has been merged into the main branch <!-- .element: class="fragment fade-up" -->
* but this is too late in the software development lifecyle, and everyone - from developers to product managers <!-- .element: class="fragment fade-up" -->
* should feel feel confident that the main branch always has green tests.
* It's inefficient for developers to have to test main before they start developing new features <!-- .element: class="fragment fade-up" -->
--
### /Run every test on all commits.
* If tests run longer than 5 minutes, they can run in parallel <!-- .element: class="fragment fade-up" -->
* When working on a feature branch and adding new commits, run tests right away <!-- .element: class="fragment fade-up" -->
* If the tests are taking a long time, try running them in parallel <!-- .element: class="fragment fade-up" -->
* Do this server-side in merge requests, running the complete test suite <!-- .element: class="fragment fade-up" -->
* If there is a test suite for development and another only for new versions, it's worthwhile to set up [parallel] tests and run them all <!-- .element: class="fragment fade-up" -->
--
### /Perform code reviews before merging into the main branch.
* Don't test everything at the end of a week or project <!-- .element: class="fragment fade-up" -->
* Code reviews should take place as soon as possible <!-- .element: class="fragment fade-up" -->
* find problems earlier, they'll have an easier time creating solutions <!-- .element: class="fragment fade-up" -->
--
### /Deployments are automatic based on branches or tags.
* If developers don't want to deploy main every time, they can create a production branch <!-- .element: class="fragment fade-up" -->
* Rather than using a script or doing it manually, teams can use automation or have a specific branch that triggers a production deploy <!-- .element: class="fragment fade-up" -->
--
### /Deployments are automatic based on branches or tags.
* Tags are set by the user, not by CI <!-- .element: class="fragment fade-up" -->
* Developers should use tags so that the CI will perform an action rather than having the CI change the repository <!-- .element: class="fragment fade-up" -->
* If teams require detailed metrics, they should have a server report detailing new versions <!-- .element: class="fragment fade-up" -->
--
### /Releases are based on tags.
* Each tag should create a new release <!-- .element: class="fragment fade-up" -->
* This practice ensures a clean, efficient development environment <!-- .element: class="fragment fade-up" -->
--
### /Everyone starts from main and targets main.
* This tip prevents long branches <!-- .element: class="fragment fade-up" -->
* Developers check out main, build a feature, create a merge request, and target main again <!-- .element: class="fragment fade-up" -->
* They should do a complete review before merging and eliminating any intermediate stages <!-- .element: class="fragment fade-up" -->
--
### /Fix bugs in main first and release branches second.
* After identifying a bug, a problematic action someone could take is fix it in the just-released version and not fix it in main <!-- .element: class="fragment fade-up" -->
* To avoid it, developers should always fix forward by pushing the change in main, then cherry-pick it into another patch-release branch <!-- .element: class="fragment fade-up" -->
--
### /Commit messages reflect intent.
* Developers should not only say what they did, but also why they did it <!-- .element: class="fragment fade-up" -->
* An even more useful tactic is to explain why this option was selected over others to help future contributors understand the development process <!-- .element: class="fragment fade-up" -->
* Writing descriptive commit messages is useful for code reviews and future development <!-- .element: class="fragment fade-up" -->
--
### /GIT-FLOW
* one main development branch with strict access to it <!-- .element: class="fragment fade-up" -->
* It's often called the develop branch <!-- .element: class="fragment fade-up" -->
* Developers create feature branches from this main branch and work on them <!-- .element: class="fragment fade-up" -->
--
### /GIT-FLOW
* Once they are done, they create pull requests. In pull requests, other developers comment on changes and may have discussions, often quite lengthy ones <!-- .element: class="fragment fade-up" -->
* It takes some time to agree on a final version of changes <!-- .element: class="fragment fade-up" -->
--
### /GIT-FLOW
* Once it's agreed upon, the pull request is accepted and merged to the main branch <!-- .element: class="fragment fade-up" -->
*  Once it's decided that the main branch has reached enough maturity to be released, a separate branch is created to prepare the final version <!-- .element: class="fragment fade-up" -->
--
### /GIT-FLOW VS. trunk-based development
* The main difference between Gitflow and trunk-based development is that the former has longer-lived branches with larger commits <!-- .element: class="fragment fade-up" -->
* Meanwhile, the latter has shorter-lived branches with fewer commits <!-- .element: class="fragment fade-up" -->
* All developers work on the main branch in trunk-based development <!-- .element: class="fragment fade-up" -->
---
# EXERCISE: BRANCH/PULL-REUEST
--
### /EXERCISE: BRANCH/PULL-REUEST
---
# PIPELINING
--
### /GOAL
* CI/CD is not the goal.. <!-- .element: class="fragment fade-up" -->
* ..The goal is better, faster software development.. <!-- .element: class="fragment fade-up" -->
* ..with fewer preventable bugs and better team cooperation <!-- .element: class="fragment fade-up" -->
--
### /GOAL
* CI should always be configured to the task at hand and the project itself <!-- .element: class="fragment fade-up" -->
* the end goal should be kept in mind at all times <!-- .element: class="fragment fade-up" -->
--
### /GOAL
You can think of CI as the answer to these questions:
* How to make sure that tests run on all code that will be deployed? <!-- .element: class="fragment fade-up" -->
* How to make sure that the main branch is deployable at all times? <!-- .element: class="fragment fade-up" -->
* How to ensure that builds will be consistent and will always work on the platform it'd be deploying to? <!-- .element: class="fragment fade-up" -->
* How to make sure that the changes don't overwrite each other? <!-- .element: class="fragment fade-up" -->
* How to make deployments happen at the click of a button or automatically when one merges to the main branch? <!-- .element: class="fragment fade-up" -->
--
### /TASKS
* Lint: to keep our code clean and maintainable <!-- .element: class="fragment fade-up" -->
* Build: put all of our code together into runnable software bundle <!-- .element: class="fragment fade-up" -->
* Test: to ensure we don't break existing features <!-- .element: class="fragment fade-up" -->
* Package: Put it all together in an easily movable batch <!-- .element: class="fragment fade-up" -->
* Deploy: Make it available to the world <!-- .element: class="fragment fade-up" -->
--
### /Code always kept deployable
* Having code that's always deployable makes life easier <!-- .element: class="fragment fade-up" -->
* if a bug is found and it needs to be fixed <!-- .element: class="fragment fade-up" -->
  * pull a copy of the main branch (knowing it is the code running in production) <!-- .element: class="fragment fade-up" -->
  * fix the bug <!-- .element: class="fragment fade-up" -->
  * make a pull request back to the main branch <!-- .element: class="fragment fade-up" -->
--
### /Code not kept deployable
If main branch and production are very different: <!-- .element: class="fragment fade-up" -->
 * main branch is not deployable <!-- .element: class="fragment fade-up" -->
 * find out what code is running in production <!-- .element: class="fragment fade-up" -->
 * pull a copy of that <!-- .element: class="fragment fade-up" -->
 * fix the bug <!-- .element: class="fragment fade-up" -->
 * figure out a way to push it back <!-- .element: class="fragment fade-up" -->
 * work out how to deploy that specific commit -> not great and completely  different workflow from a normal deployment <!-- .element: class="fragment fade-up" -->
--
### /Types of CI setup
* Having a separate server for the purpose minimizes the risk that something else interferes with the CI/CD process and causes it to be unpredictable <!-- .element: class="fragment fade-up" -->
* There are two options: host our own server or use a cloud service <!-- .element: class="fragment fade-up" -->
--
### /Jenkins (and other self-hosted setups)
* Jenkins is the most popular <!-- .element: class="fragment fade-up" -->
* It's extremely flexible and there are plugins for almost anything <!-- .element: class="fragment fade-up" -->
* using a self-hosted setup means that the entire environment is under your control, the number of resources can be controlled <!-- .element: class="fragment fade-up" -->
--
### /Jenkins (and other self-hosted setups)
* Jenkins is quite complicated to set up <!-- .element: class="fragment fade-up" -->
* CI/CD must be set up with Jenkins' own domain-specific language <!-- .element: class="fragment fade-up" -->
* With self-hosted options, the billing is usually based on the hardware <!-- .element: class="fragment fade-up" -->
* You pay for the server. What you do on the server doesn't change the billing <!-- .element: class="fragment fade-up" -->
--
### /GitHub Actions (and other cloud-based solutions)
* cloud-hosted setup = the setup of the environment is not something you need to worry about <!-- .element: class="fragment fade-up" -->
* put a file in your repository and then telling the CI system to read the file <!-- .element: class="fragment fade-up" -->
* actual CI config for the cloud-based options is often a little simpler <!-- .element: class="fragment fade-up" -->
* there are often resource limitations on cloud-based platforms <!-- .element: class="fragment fade-up" -->
--
# EXERCISE: TASKFILE
--
### EXERCISE: TASKFILE
---
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
# AZURE PIPELINES VS. GITHUB ACTIONS
--
### /Pipelines as code
* Benefit from standard source control practices (such as code reviews via pull request and versioning) <!-- .element: class="fragment fade-up" -->
* Can be audited for changes just like any other files in the repository <!-- .element: class="fragment fade-up" -->
* Don't require accessing a separate system or UI to edit <!-- .element: class="fragment fade-up" -->
* Can fully codify the build, test, and deploy process for code <!-- .element: class="fragment fade-up" -->
* Can usually be templatized to empower teams to create standard processes across multiple repositories <!-- .element: class="fragment fade-up" -->
--
### /Azure Pipelines trigger
* A trigger tells a Pipeline to run <!-- .element: class="fragment fade-up" -->
```
# app-ci YAML pipeline
resources:
  pipelines:
  - pipeline: securitylib
    source: security-lib-ci
    trigger:
      branches:
        include:
        - releases/*
```
<!-- .element: class="fragment fade-up" -->
--
### /Azure Pipelines stages
* A pipeline is made up of one or more stages <!-- .element: class="fragment fade-up" -->

```
# this pipeline has one implicit stage
jobs:
- job: A
  steps:
  - bash: echo "A"
- job: B
  steps:
  - bash: echo "B"
```
--
### /Azure Pipelines jobs
* A stage is a way of organizing jobs in a pipeline and each stage can have one or more jobs <!-- .element: class="fragment fade-up" -->

```
jobs:
- job: myJob
  timeoutInMinutes: 10
  pool:
    vmImage: 'ubuntu-latest'
  steps:
  - bash: echo "Hello world"
```
<!-- .element: class="fragment fade-up" -->

--
### /Azure Pipelines environments
*  A pipeline can deploy to one or more environments <!-- .element: class="fragment fade-up" -->

```
environment:
  name: 'smarthotel-dev'
  resourceName: myVM
  resourceType: virtualMachine
```
<!-- .element: class="fragment fade-up" -->
--
### /Azure Pipelines vs. GitHub Actions
* GitHub Actions and Azure Pipelines share several configuration similarities <!-- .element: class="fragment fade-up" -->
* migrating to GitHub Actions relatively straightforward <!-- .element: class="fragment fade-up" -->
--
### /similarities
* Workflow configuration files are written in YAML and are stored in the code's repository <!-- .element: class="fragment fade-up" -->
* Workflows include one or more jobs <!-- .element: class="fragment fade-up" -->
* Jobs include one or more steps or individual commands <!-- .element: class="fragment fade-up" -->
* Steps or tasks can be reused and shared with the community <!-- .element: class="fragment fade-up" -->
--
* Jobs contain a series of steps that run sequentially <!-- .element: class="fragment fade-up" -->
* Jobs run on separate virtual machines or in separate containers <!-- .element: class="fragment fade-up" -->
* Jobs run in parallel by default, but can be configured to run sequentially <!-- .element: class="fragment fade-up" -->
--
### /Key differences
When migrating from Azure Pipelines, consider the following differences:
* Azure Pipelines supports a legacy classic editor, which lets you define your CI configuration in a GUI editor instead of creating the pipeline definition in a YAML file <!-- .element: class="fragment fade-up" -->
* GitHub Actions uses YAML files to define workflows and does not support a graphical editor <!-- .element: class="fragment fade-up" -->
--
### /Key differences
* Azure Pipelines allows you to omit some structure in job definitions. For example, if you only have a single job, you don't need to define the job and only need to define its steps <!-- .element: class="fragment fade-up" -->
* GitHub Actions requires explicit configuration, and YAML structure cannot be omitted <!-- .element: class="fragment fade-up" -->
* Azure Pipelines supports stages defined in the YAML file, which can be used to create deployment workflows <!-- .element: class="fragment fade-up" -->
* GitHub Actions requires you to separate stages into separate YAML workflow files <!-- .element: class="fragment fade-up" -->
* On-premises Azure Pipelines build agents can be selected with capabilities. GitHub Actions self-hosted runners can be selected with labels <!-- .element: class="fragment fade-up" -->
---
# /GitOps
--
### /GitOps
* GitOps is a way to do Kubernetes cluster management and application delivery <!-- .element: class="fragment fade-up" -->
* It works by using Git as a single source of truth for declarative infrastructure and applications <!-- .element: class="fragment fade-up" -->
--
### /Argo CD
* declarative continuous delivery tool for Kubernetes <!-- .element: class="fragment fade-up" -->
[<img src="https://argoproj.github.io/static/argo-cd-ui-87dce328a7ab3be2d13f7926831068eb.gif" width="700"/>](https://www.sva.de/index.html)
--
### /Argo CD
* Kubernetes-native continuous deployment (CD) tool <!-- .element: class="fragment fade-up" -->
* Argo CD can pull updated code from Git repositories and deploy it directly to Kubernetes resources <!-- .element: class="fragment fade-up" -->
* It enables developers to manage both infrastructure configuration and application updates in one system <!-- .element: class="fragment fade-up" -->
--
### /key features and capabilities
* Manual or automatic deployment of applications to a Kubernetes cluster <!-- .element: class="fragment fade-up" -->
* Automatic synchronization of application state to the current version of declarative configuration <!-- .element: class="fragment fade-up" -->
* Web user interface and command-line interface (CLI) <!-- .element: class="fragment fade-up" -->
--
### /key features and capabilities
*  Ability to visualize deployment issues, detect and remediate configuration drift <!-- .element: class="fragment fade-up" -->
* Role-based access control (RBAC) enabling multi-cluster management <!-- .element: class="fragment fade-up" -->
* Single sign-on (SSO) with providers such as GitLab, GitHub, Microsoft, OAuth2, OIDC, LinkedIn, LDAP, and SAML 2.0 <!-- .element: class="fragment fade-up" -->
* Support for webhooks triggering actions in GitLab, GitHub, and BitBucket.
This is part of an extensive series of guides about Kubernetes <!-- .element: class="fragment fade-up" -->
--
### /Argo CD process
--
* A developer makes changes to an application <!-- .element: class="fragment fade-up" -->
* pushing a new version of Kubernetes resource definitions to a Git repo <!-- .element: class="fragment fade-up" -->
* Continuous integration is triggered = new container image saved to a registry <!-- .element: class="fragment fade-up" -->
* A developer issues a pull request = changing Kubernetes manifests (manually or automatically) <!-- .element: class="fragment fade-up" -->
--
### /Argo CD process
* The pull request is reviewed and changes are merged to the main branch <!-- .element: class="fragment fade-up" -->
* This triggers a webhook which tells Argo CD a change was made <!-- .element: class="fragment fade-up" -->
* Argo CD clones the repo and compares the application state with the current state of the Kubernetes cluster <!-- .element: class="fragment fade-up" -->
* It applies the required changes to cluster configuration <!-- .element: class="fragment fade-up" -->
--
### /Argo CD process
* Kubernetes uses its controllers to reconcile the changes required to cluster resources, until it achieves the desired configuration <!-- .element: class="fragment fade-up" -->
* Argo CD monitors progress and when the Kubernetes cluster is ready = reports that the application is in sync <!-- .element: class="fragment fade-up" -->
* ArgoCD also works in the other direction, monitoring changes in the Kubernetes cluster and discarding them if they don't match the current configuration in Git <!-- .element: class="fragment fade-up" -->
---
# EXERCISE: ARGO-CD
--
### EXERCISE: ARGO-CD
---
# SUMMARY
--
### SUMMARY + QA
---