<!--
Copyright (c) 2022 Dell Inc., or its subsidiaries. All Rights Reserved.

Licensed under the GPL, Version 3.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.gnu.org/licenses/gpl-3.0.txt
-->

# Triage issues

The main goal of issue triage is to categorize all incoming issues and make sure each issue has all basic information needed for anyone else to understand and be able to start working on it.

> **Note:** This information is for project Maintainers, Owners, and Admins. If you are a Contributor, then you will not be able to perform most of the tasks in this topic.

The core maintainers of this project are responsible for categorizing all incoming issues and delegating any critical or important issue to other maintainers. Triage provides an important way to contribute to an open source project.

Triage helps ensure issues resolve quickly by:

- Ensuring the issue's intent and purpose is conveyed precisely. This is necessary because it can be difficult for an issue to explain how an end user experiences a problem and what actions they took.
- Giving a contributor the information they need before they commit to resolving an issue.
- Lowering the issue count by preventing duplicate issues.
- Streamlining the development process by preventing duplicate discussions.

If you don't have the knowledge or time to code, consider helping with triage. The community will thank you for saving them time by spending some of yours.

## 1. Find issues that need triage

The easiest way to find issues that haven't been triaged is to search for issues with the `needs-triage` label.

## 2. Ensure the issue contains basic information

Make sure that the issue's author provided the standard issue information. This project utilizes GitHub issue templates to guide contributors to provide standard information that must be included for each type of template or type of issue.

### Standard issue information that must be included

The following section describes the various issue templates and the expected content.

#### Bug reports

Should explain what happened, what was expected and how to reproduce it together with any additional information that may help giving a complete picture of what happened such as screenshots, output and any environment related information that's applicable and/or maybe related to the reported problem:

 - OS/Version: [e.g. RHEL 8.5]
 - Python Version [e.g. 3.9]
 - Ansible Version [e.g. 2.13]
 - Any other additional information...

#### Feature requests

Should explain what feature that the author wants to be added and why that is needed.

#### Ask a Question requests

In general, if the issue description and title is perceived as a question no more information is needed.

### Good practices

To make it easier for everyone to understand and find issues they're searching for it's suggested as a general rule of thumbs to:

- Make sure that issue titles are named to explain the subject of the issue, has a correct spelling and doesn't include irrelevant information and/or sensitive information.
- Make sure that issue descriptions doesn't include irrelevant information.
- Make sure that issues do not contain sensitive information.
- Make sure that issues have all relevant fields filled in.
- Do your best effort to change title and description or request suggested changes by adding a comment.

> **Note:** Above rules are applicable to both new and existing issues.

### Dealing with missing information

Depending on the issue, you might not feel all this information is needed. Use your best judgement. If you cannot triage an issue using what its author provided, explain kindly to the author that they must provide the above information to clarify the problem. Label issue with `triage/needs-information`.

If the author provides the standard information but you are still unable to triage the issue, request additional information. Do this kindly and politely because you are asking for more of the author's time.  Label issue with `triage/needs-information`.

If the author does not respond to the requested information within the timespan of a week, close the issue with a kind note stating that the author can request for the issue to be reopened when the necessary information is provided.

If you receive a notification with additional information provided but you are not anymore on issue triage and you feel you do not have time to handle it, you should delegate it to the current person on issue triage.

## 3. Categorizing an issue

### Duplicate issues

Make sure it's not a duplicate by searching existing issues using related terms from the issue title and description. If you think you know there is an existing issue, but can't find it, please reach out to one of the maintainers and ask for help. If you identify that the issue is a duplicate of an existing issue:

1. Add a comment `duplicate of #<issue number>`
2. Add the `triage/duplicate` label

### Bug reports

If it's not perfectly clear that it's an actual bug, quickly try to reproduce it.

**It's a bug/it can be reproduced:**

1. Add a comment describing detailed steps for how to reproduce it, if applicable.
2. If you know that maintainers won't be able to put any resources into it for some time then label the issue with `help wanted` and optionally `beginner friendly` together with pointers on which code to update to fix the bug. This should signal to the community that we would appreciate any help we can get to resolve this.
3. Move on to [prioritizing the issue](#4-prioritization-of-issues).

**It can't be reproduced:**

1. Either [ask for more information](#2-ensure-the-issue-contains-basic-information) needed to investigate it more thoroughly.  Provide details in a comment.
2. Either [delegate further investigations](#investigation-of-issues) to someone else.  Provide details in a comment.

**It works as intended/by design:**

1. Kindly and politely add a comment explaining briefly why we think it works as intended and close the issue.
2. Label the issue `triage/works-as-intended`.
3. Remove the `needs-triage` label.

**It does not work as intended/by design:**

### Feature requests

1. If the feature request does not align with the product vision, add a comment indicating so, remove the `needs-triage` label and close the issue
2. Otherwise, move on to [prioritizing the issue](#4-prioritization-of-issues).  Assign the appropriate priority label to the issue, add the appropriate comments to the issue, and remove the `needs-triage` label.

## 4. Prioritization of issues
[ANUPAM TO REVIEW THIS AND PROVIDE NECESSARY INPUT]
In general bugs and feature request issues should be labeled with a priority.

This is the most difficult thing with triaging issues since it requires a lot of knowledge, context and experience before being able to think of and start feel comfortable adding a certain priority label.

The key here is asking for help and discuss issues to understand how more experienced project members think and reason. By doing that you learn more and eventually be more and more comfortable with prioritizing issues.

In case there is an uncertainty around the prioritization of an issue, please ask the maintainers for help.

| Label                             | Description                                                                                                              |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `priority/critical`               | Highest priority. Must be actively worked on as someone's top priority right now.                                        |
| `priority/high`                   | Must be worked on soon, ideally in time for the next release.                                                            |
| `priority/low`                    | Lowest priority. Possibly useful, but not yet enough interest in it.                                                     |

### Critical priority

1. If an issue has been categorized and any of the following criteria apply, the issue should be labeled as critical and must be actively worked on as someone's top priority right now.

   - Results in any data loss
   - Critical security or performance issues
   - Problem that makes a feature unusable
   - Multiple users experience a severe problem affecting their business, users etc.

2. Label the issue `priority/critical`.
3. Escalate the problem to the maintainers.
4. Assign or ask a maintainer for help assigning someone to make this issue their top priority right now.
5. Add the issue to the next upcoming release milestone.

### High priority

1. Label the issue `priority/high`.
2. Add the issue to the next upcoming release milestone.
3. Prioritize it or assign someone to work on it now or very soon.
4. Consider requesting [help from the community](#5-requesting-help-from-the-community).

### Low priority

1. If the issue is deemed possibly useful but a low priority label the issue `priority/low`.
2. The amount of interest in the issue will determine if the priority changes to be higher.
3. Consider requesting [help from the community](#5-requesting-help-from-the-community).

## 5. Requesting help from the community

Depending on the issue and/or priority, it's always a good idea to consider signalling to the community that help from community is appreciated and needed in case an issue is not prioritized to be worked on by maintainers. Use your best judgement. In general, requesting help from the community means that a contribution has a good chance of getting accepted and merged.

In many cases the issue author or community as a whole is more suitable to contribute changes since they're experts in their domain. It's also quite common that someone has tried to get something to work using the documentation without success and made an effort to get it to work and/or reached out to the community to get the missing information.

1. Kindly and politely add a comment to signal to users subscribed to updates of the issue.
   - Explain that the issue would be nice to get resolved, but it isn't prioritized to work on by maintainers for an unforeseen future.
   - If possible or applicable, try to help contributors getting starting by adding pointers and references to what code/files need to be changed and/or ideas of a good way to solve/implement the issue.
2. Label the issue with `help wanted`.
3. If applicable, label the issue with `beginner friendly` to denote that the issue is suitable for a beginner to work on.

## Investigation of issues

When an issue has all basic information provided, but the reported problem cannot be reproduced at a first glance, the issue is labeled `triage/needs-information`. Depending on the perceived severity and/or number of upvotes, the investigation will either be delegated to another maintainer for further investigation or put on hold until someone else (maintainer or contributor) picks it up and eventually starts investigating it.

Even if you don't have the time or knowledge to investigate an issue we highly recommend that you upvote the issue if you happen to have the same problem. If you have further details that may help investigating the issue please provide as much information as possible.

## External pull requests

Part of issue triage should also be triaging of external PRs. Main goal should be to make sure PRs from external contributors have an owner/reviewer and are not forgotten.

1. Check new external PRs which do not have a reviewer.
1. Check if there is a link to an existing issue.
1. If not and you know which issue it is solving, add the link yourself, otherwise ask the author to link the issue or create one.
1. Assign a reviewer based on who was handling the linked issue or what code or feature does the PR touches (look at who was the last to make changes there if all else fails).

## GitHub issue management workflow

The following section describes the triage workflow for new GitGHub issues that get created.

### GitHub Issue: Bug

This workflow starts off with a GitHub issue of type bug being created.

1. Collaborator or maintainer creates a GitHub bug using the appropriate GitHub issue template
2. By default a bug will be created with the `type/bug` and `needs-triage` labels
