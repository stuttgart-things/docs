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
# /PIPELINES AS CODE
* Benefit from standard source control practices (such as code reviews via pull request and versioning) <!-- .element: class="fragment fade-up" -->
* Can be audited for changes just like any other files in the repository <!-- .element: class="fragment fade-up" -->
* Don't require accessing a separate system or UI to edit <!-- .element: class="fragment fade-up" -->
* Can fully codify the build, test, and deploy process for code <!-- .element: class="fragment fade-up" -->
* Can usually be templatized to empower teams to create standard processes across multiple repositories <!-- .element: class="fragment fade-up" -->
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
