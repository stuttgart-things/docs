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
Lint: to keep our code clean and maintainable <!-- .element: class="fragment fade-up" -->
Build: put all of our code together into runnable software bundle <!-- .element: class="fragment fade-up" -->
Test: to ensure we don't break existing features <!-- .element: class="fragment fade-up" -->
Package: Put it all together in an easily movable batch <!-- .element: class="fragment fade-up" -->
Deploy: Make it available to the world <!-- .element: class="fragment fade-up" -->
--
### /Code always kept deployable
* Having code that's always deployable makes life easier <!-- .element: class="fragment fade-up" -->
* if a bug is found and it needs to be fixed <!-- .element: class="fragment fade-up" -->
  * pull a copy of the main branch (knowing it is the code running in production) <!-- .element: class="fragment fade-up" -->
  * fix the bug <!-- .element: class="fragment fade-up" -->
  * make a pull request back to the main branch <!-- .element: class="fragment fade-up" -->
### /Code not kept deployable
If main branch and production are very different:
 * main branch is not deployable
 * find out what code is running in production
 * pull a copy of that
 * fix the bug
 * figure out a way to push it back
 * work out how to deploy that specific commit -> not great and completely different workflow from a normal deployment.
--
### /Types of CI setup
* Having a separate server for the purpose minimizes the risk that something else interferes with the CI/CD process and causes it to be unpredictable
* There are two options: host our own server or use a cloud service.
### /Jenkins (and other self-hosted setups)
* Jenkins is the most popular
* It's extremely flexible and there are plugins for almost anything
* using a self-hosted setup means that the entire environment is under your control, the number of resources can be controlled
--
### /Jenkins (and other self-hosted setups)
* Jenkins is quite complicated to set up
* CI/CD must be set up with Jenkins' own domain-specific language
* With self-hosted options, the billing is usually based on the hardware
* You pay for the server. What you do on the server doesn't change the billing
--
### /GitHub Actions (and other cloud-based solutions)
* cloud-hosted setup = the setup of the environment is not something you need to worry about
* put a file in your repository and then telling the CI system to read the file
* actual CI config for the cloud-based options is often a little simpler
* there are often resource limitations on cloud-based platforms








https://www.cncf.io/blog/2020/06/17/testing-kubernetes-deployments-within-ci-pipelines/




docker login -u patrick -p Upaf8GHr27j5STvthY5YLSAaZaifEPYRo4ggSA5Q2y+ACRA71LRz k8sworkshop2.azurecr.io