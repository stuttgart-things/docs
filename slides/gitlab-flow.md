# /GITLAB-FLOW
https://about.gitlab.com/topics/version-control/what-are-gitlab-flow-best-practices/
--
### /Use feature branches..
* ..rather than direct commits on the main branch
* feature branches is a simple way to develop
* keep the source code clean
* developers should create a branch for anything they're working on
* -> contributors can easily start the code review process before merging.
--
### /Test all commits, not only ones on the main branch.
* Some developers set up their CI to only test what has been merged into the main branch,
* but this is too late in the software development lifecyle, and everyone - from developers to product managers
* should feel feel confident that the main branch always has green tests.
* It's inefficient for developers to have to test main before they start developing new features.
--
### /Run every test on all commits.
* If tests run longer than 5 minutes, they can run in parallel
* When working on a feature branch and adding new commits, run tests right away.
* If the tests are taking a long time, try running them in parallel.
* Do this server-side in merge requests, running the complete test suite. If there is a test suite for development and another only for new versions, it's worthwhile to set up [parallel] tests and run them all.
--
### /Perform code reviews before merging into the main branch.
* Don't test everything at the end of a week or project.
* Code reviews should take place as soon as possible
* find problems earlier, they'll have an easier time creating solutions.
--
### /Deployments are automatic based on branches or tags.
* If developers don't want to deploy main every time, they can create a production branch.
* Rather than using a script or doing it manually, teams can use automation or have a specific branch that triggers a production deploy.
--
### /Deployments are automatic based on branches or tags.
* Tags are set by the user, not by CI.
* Developers should use tags so that the CI will perform an action rather than having the CI change the repository.
* If teams require detailed metrics, they should have a server report detailing new versions.
--
### /Releases are based on tags.
* Each tag should create a new release.
* This practice ensures a clean, efficient development environment.
--
### /Everyone starts from main and targets main.
* This tip prevents long branches
* Developers check out main, build a feature, create a merge request, and target main again.
* They should do a complete review before merging and eliminating any intermediate stages.
--
### /Fix bugs in main first and release branches second.
* After identifying a bug, a problematic action someone could take is fix it in the just-released version and not fix it in main.
* To avoid it, developers should always fix forward by pushing the change in main, then cherry-pick it into another patch-release branch.
--
### /Commit messages reflect intent.
* Developers should not only say what they did, but also why they did it.
* An even more useful tactic is to explain why this option was selected over others to help future contributors understand the development process.
* Writing descriptive commit messages is useful for code reviews and future development.