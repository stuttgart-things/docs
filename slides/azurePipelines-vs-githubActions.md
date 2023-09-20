# Pipelines as code
Before you compare GitHub Actions and Azure Pipelines, you should consider the benefits of pipelines as code. Pipelines as code:

* Benefit from standard source control practices (such as code reviews via pull request and versioning).
* Can be audited for changes just like any other files in the repository.
* Don’t require accessing a separate system or UI to edit.
* Can fully codify the build, test, and deploy process for code.
* Can usually be templatized to empower teams to create standard processes across multiple repositories.
--
# Azure Pipelines vs. GitHub Actions
* GitHub Actions and Azure Pipelines share several configuration similarities
* migrating to GitHub Actions relatively straightforward.
--
# similarities
* Workflow configuration files are written in YAML and are stored in the code's repository.
* Workflows include one or more jobs.
* Jobs include one or more steps or individual commands.
* Steps or tasks can be reused and shared with the community
--
* Jobs contain a series of steps that run sequentially.
* Jobs run on separate virtual machines or in separate containers.
* Jobs run in parallel by default, but can be configured to run sequentially.
--
# Key differences
When migrating from Azure Pipelines, consider the following differences:

* Azure Pipelines supports a legacy classic editor, which lets you define your CI configuration in a GUI editor instead of creating the pipeline definition in a YAML file.
* GitHub Actions uses YAML files to define workflows and does not support a graphical editor.
* Azure Pipelines allows you to omit some structure in job definitions. For example, if you only have a single job, you don't need to define the job and only need to define its steps.
* GitHub Actions requires explicit configuration, and YAML structure cannot be omitted.
* Azure Pipelines supports stages defined in the YAML file, which can be used to create deployment workflows. GitHub Actions requires you to separate stages into separate YAML workflow files.
* On-premises Azure Pipelines build agents can be selected with capabilities. GitHub Actions self-hosted runners can be selected with labels.
--
