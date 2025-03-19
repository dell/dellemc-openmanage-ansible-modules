<!--
Copyright (c) 2022 Dell Inc., or its subsidiaries. All Rights Reserved.

Licensed under the GPL, Version 3.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.gnu.org/licenses/gpl-3.0.txt
-->

# How to Contribute

Become one of the contributors to this project! We thrive to build a welcoming and open community for anyone who wants to use the project or contribute to it. There are just a few small guidelines you need to follow. To help us create a safe and positive community experience for all, we require all participants to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md).

## Table of Contents

* [Become a contributor](#Become-a-contributor)
* [Contributor agreement](#Contributor-agreement)
* [Submitting issues](#Submitting-issues)
* [Triage issues](#Triage-issues)
* [Your first contribution](#Your-first-contribution)
* [Branching](#Branching)
* [Signing your commits](#Signing-your-commits)
* [Pull requests](#Pull-requests)
* [Code reviews](#Code-reviews)
* [Code Style](#Code-style)

## Become a contributor

You can contribute to this project in several ways. Here are some examples:

* Contribute to the project documentation and codebase.
* Report and triage bugs.
* Feature requests
* Write technical documentation and blog posts, for users and contributors.
* Help others by answering questions about this project.

## Contributor Agreement
All contributions shall be made under the Developer Certification of Origin ("DCO") (see http://elinux.org/Developer_Certificate_Of_Origin) which is reproduced below. Specifically, the Git commit message for the contribution should contain the following tag information signifying use of the DCO:


"Signed-off-by: [Your Name] [youremail@company.com]"


________________________________________
### Developer's Certificate of Origin 1.1
By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I have the right to submit it under the open source license indicated in the file; or

(b) The contribution is based upon previous work that, to the best of my knowledge, is covered under an appropriate open source license and I have the right under that license to submit that work with modifications, whether created in whole or in part by me, under the same open source license (unless I am permitted to submit under a different license), as indicated in the file; or

(c) The contribution was provided directly to me by some other person who certified (a), (b) or (c) and I have not modified it.

(d) I understand and agree that this project and the contribution are public and that a record of the contribution (including all personal information I submit with it, including my sign-off) is maintained indefinitely and may be redistributed consistent with this project or the open source license(s) involved.

## Submitting issues

All issues related to the associated Ansible modules, roles, playbooks, regardless of the service/repository the issue belongs to (see table above), should be submitted [here](https://github.com/dell/dellemc-openmanage-ansible-modules/issues). Issues will be triaged and labels will be used to indicate the type of issue. This section outlines the types of issues that can be submitted.  

### Report bugs

We aim to track and document everything related to the repository via the Issues page. The code and documentation are released with no warranties or SLAs and are intended to be supported through a community driven process.

Before submitting a new issue, make sure someone hasn't already reported the problem. Look through the [existing issues](https://github.com/dell/dellemc-openmanage-ansible-modules/issues) for similar issues.

Report a bug by submitting a [bug report](https://github.com/dell/dellemc-openmanage-ansible-modules/issues/new?labels=type%2Fbug%2C+needs-triage&template=bug_report.md&title=%5BBUG%5D%3A). Make sure that you provide as much information as possible on how to reproduce the bug.

When opening a Bug please include the following information to help with debugging:

1. Version of relevant software: this software, Python version, Dell Server/Storage Platform, etc.
2. Details of the issue explaining the problem: what, when, where
3. The expected outcome that was not met (if any)
4. Supporting troubleshooting information. __Note: Do not provide private company information that could compromise your company's security.__

An Issue __must__ be created before submitting any pull request. Any pull request that is created should be linked to an Issue.

### Feature request

If you have an idea of how to improve this project, submit a [feature request](https://github.com/dell/dellemc-openmanage-ansible-modules/issues/new?labels=type%2Ffeature-request%2C+needs-triage&template=feature_request.md&title=%5BFEATURE%5D%3A).

### Answering questions

If you have a question and you can't find the answer in the documentation or issues, the next step is to submit a [question.](https://github.com/dell/dellemc-openmanage-ansible-modules/issues/new?labels=type%2Fquestion&template=ask-a-question.md&title=%5BQUESTION%5D%3A)

We'd love your help answering questions being asked by other CSM users.

## Triage issues

Triage helps ensure that issues resolve quickly by:

* Ensuring the issue's intent and purpose is conveyed precisely. This is necessary because it can be difficult for an issue to explain how an end user experiences a problem and what actions they took.
* Giving a contributor the information they need before they commit to resolving an issue.
* Lowering the issue count by preventing duplicate issues.
* Streamlining the development process by preventing duplicate discussions.

If you don't have the knowledge or time to code, consider helping with _issue triage_. The Dell Ansible community will thank you for saving them time by spending some of yours.

Read more about the ways you can [Triage issues](ISSUE_TRIAGE.md).

## Your first contribution

Unsure where to begin contributing? Start by browsing issues labeled `beginner friendly` or `help wanted`.

* [Beginner-friendly](https://github.com/dell/dellemc-openmanage-ansible-modules/issues?q=is%3Aopen+is%3Aissue+label%3A%22beginner+friendly%22) issues are generally straightforward to complete.
* [Help wanted](https://github.com/dell/dellemc-openmanage-ansible-modules/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22) issues are problems we would like the community to help us with regardless of complexity.

When you're ready to contribute, it's time to create a pull request.

## Testing
See [here](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/tests/README.md) for further information on testing.

## Debugging
To debug OpenManage Ansible Modules using IDE, see [here](https://github.com/dell/dellemc-openmanage-ansible-modules/tree/collections/docs/DEBUG.md)

## Branching

* [Branching Strategy](BRANCHING.md)

## Signing your commits

We require that developers sign off their commits to certify that they have permission to contribute the code in a pull request. This way of certifying is commonly known as the [Developer Certificate of Origin (DCO)](https://developercertificate.org/). We encourage all contributors to read the DCO text before signing a commit and making contributions.

GitHub will prevent a pull request from being merged if there are any unsigned commits.

### Signing a commit

GPG (GNU Privacy Guard) will be used to sign commits.  Follow the instructions [here](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/signing-commits) to create a GPG key and configure your GitHub account to use that key.

Make sure you have your user name and e-mail set.  This will be required for your signed commit to be properly verified.  Check the following references:

* Setting up your github user name [reference](https://help.github.com/articles/setting-your-username-in-git/)
* Setting up your e-mail address [reference](https://help.github.com/articles/setting-your-commit-email-address-in-git/)

Once Git and your GitHub account have been properly configured, you can add the -S flag to the git commits:

```console
$ git commit -S -m your commit message
# Creates a signed commit
```

### Commit message format

This repository uses the guidelines for commit messages outlined in [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)

## Pull Requests

If this is your first time contributing to an open-source project on GitHub, make sure you read about [Creating a pull request](https://help.github.com/en/articles/creating-a-pull-request).

A pull request must always link to at least one GitHub issue. If that is not the case, create a GitHub issue and link it.

To increase the chance of having your pull request accepted, make sure your pull request follows these guidelines:

* Title and description matches the implementation.
* Commits within the pull request follow the formatting guidelines.
* The pull request closes one related issue.
* The pull request contains necessary tests that verify the intended behavior.
* If your pull request has conflicts, rebase your branch onto the main branch.

If the pull request fixes a bug:

* The pull request description must include `Fixes #<issue number>`.
* To avoid regressions, the pull request should include tests that replicate the fixed bug.

The owning team _squashes_ all commits into one when we accept a pull request. The title of the pull request becomes the subject line of the squashed commit message. We still encourage contributors to write informative commit messages, as they becomes a part of the Git commit body.

We use the pull request title when we generate change logs for releases. As such, we strive to make the title as informative as possible.

Make sure that the title for your pull request uses the same format as the subject line in the commit message.

### Quality Gates for pull requests

GitHub Actions are used to enforce quality gates when a pull request is created or when any commit is made to the pull request. These GitHub Actions enforce our minimum code quality requirement for any code that get checked into the code repository. If any of the quality gates fail, it is expected that the contributor will look into the check log, understand the problem and resolve the issue. If help is needed, please feel free to reach out the maintainers of the project for [support](SUPPORT.md).

#### Code build/test/coverage

[GitHub action](https://github.com/dell/dellemc-openmanage-ansible-modules/actions) that runs unit tests and checks that the code coverage of each package meets a configured threshold (currently 90%). An error is flagged if a given pull request does not meet the test coverage threshold and blocks the pull request from being merged.

## Code Reviews

All submissions, including submissions by project members, require review. We use GitHub pull requests for this purpose. Consult [GitHub Help](https://help.github.com/articles/about-pull-requests/) for more information on using pull requests.

A pull request must satisfy following for it to be merged:

* A pull request will require at least 2 maintainer approvals.
* Maintainers must perform a review to ensure the changes adhere to guidelines laid out in this document.
* If any commits are made after the PR has been approved, the PR approval will automatically be removed and the above process must happen again.

## Code Style

For the Python code in the repository, we expect the code styling outlined in [Ansible python guide]( https://docs.ansible.com/ansible/latest/dev_guide/developing_python_3.html). In addition to this, we have the following supplements:
* Contributions should adhere to ansible Coding standard guidelines as we follow these standards.
* Should include [test](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/tests/) scripts for your changes.
* Do not submit a contribution request on our deprecated modules. They are just meant for backward compatibility.

### Handle Errors
TBD
