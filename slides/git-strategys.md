# /GIT-STRATEGYS
--
### /OVERVIEW
A good git/branching strategy should have the following characteristics:
* Provides a clear path for the development process from initial changes to production <!-- .element: class="fragment fade-up" -->
* Allows users to create workflows that lead to structured releases <!-- .element: class="fragment fade-up" -->
* Enables parallel development <!-- .element: class="fragment fade-up" -->
--
# /OVERVIEW
A good git/branching strategy should have the following characteristics:
* Optimizes developer workflow without adding any overhead <!-- .element: class="fragment fade-up" -->
* Enables faster release cycles <!-- .element: class="fragment fade-up" -->
* Efficiently integrates with all DevOps practices and tools such as different version control systems <!-- .element: class="fragment fade-up" -->
* Offers the ability to enable GitOps (if you require it) <!-- .element: class="fragment fade-up" -->
--
## /FEATURE-BRANCHES
* a developer or a group of developers create a branch usually from trunk (also known as main or mainline) <!-- .element: class="fragment fade-up" -->
* work in isolation on that branch until the feature they are building is complete <!-- .element: class="fragment fade-up" -->
* When the team considers the feature ready to go, they merge the feature branch back to trunk <!-- .element: class="fragment fade-up" -->
--
## /TRUNK-BASED DEVOLPMENT
[<img src="https://statusneo.com/wp-content/uploads/2022/12/Beginners%20Guide%20to%20Trunk-Based%20Development.png" width="600"/>](www.google.com)
* Trunk-based development (TBD) is a source control workflow model that enables continuous integration <!-- .element: class="fragment fade-up" -->
* The primary purpose of trunk-based development is to avoid the creation of long-lived branches by merging partial changes to the entire feature <!-- .element: class="fragment fade-up" -->
--
* Developers can achieve this by committing straight to the main branch or by using short-lived branches with an efficient code review process <!-- .element: class="fragment fade-up" -->
* Branches, by definition, should only live a few days <!-- .element: class="fragment fade-up" -->
--
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
### /GIT-FLOW VS. trunk-based development
* The main difference between Gitflow and trunk-based development is that the former has longer-lived branches with larger commits <!-- .element: class="fragment fade-up" -->
* Meanwhile, the latter has shorter-lived branches with fewer commits <!-- .element: class="fragment fade-up" -->
* All developers work on the main branch in trunk-based development <!-- .element: class="fragment fade-up" -->
--