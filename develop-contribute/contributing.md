# Contributing

Apache Pinot welcomes contributions of all kinds -- code, documentation, bug reports, and design proposals. This page is the single starting point for anyone who wants to contribute, whether you are fixing a typo in the docs or building a major new feature.

## Contribution paths at a glance

| What you want to do | Guide |
| --- | --- |
| Contribute code (features, bug fixes, tests) | [Contribution Guidelines](../developers/developers-and-contributors/contribution-guidelines.md) |
| Update or improve the documentation (via GitHub PR) | [Contributing to the Apache Pinot Documentation](../contributing/contributing.md) |
| Follow the documentation style conventions | [Pinot Documentation Style Guide](../contributing/style-guide.md) |
| Edit documentation directly in GitBook | [Contributing to the Apache Pinot Documentation -- GitBook section](../contributing/contributing.md#edit-directly-on-gitbook) |
| Understand the documentation toolchain | [Update Documentation](../developers/developers-and-contributors/update-document.md) |

## Code contribution workflow (summary)

The full details live in the [Contribution Guidelines](../developers/developers-and-contributors/contribution-guidelines.md). Here is the high-level flow:

1. **Open a GitHub issue** describing what you plan to change and why.
2. **Get agreement** -- for large features, write a Pinot Enhancement Proposal (PEP) design document and obtain PMC approval.
3. **Create a branch** in your fork, implement the change, and add tests.
4. **Run verification locally** -- `mvn checkstyle:check` and `mvn clean install -Pbin-dist`.
5. **Open a pull request** with a clear description, link to the issue, and evidence of testing.
6. **Respond to review feedback**, rebase on master as needed, and wait for merge.
7. **Update documentation** if the change introduces new user-facing behavior.

## Documentation contribution workflow (summary)

The full details live in [Contributing to the Apache Pinot Documentation](../contributing/contributing.md).

1. **Fork and clone** the [pinot-docs](https://github.com/pinot-contrib/pinot-docs) repository.
2. **Edit locally** using Markdown. Follow the [style guide](../contributing/style-guide.md) for Pinot-specific conventions.
3. **Commit and push** to your fork.
4. **Open a pull request** against the upstream docs repository.
5. **Incorporate review feedback** -- changes appear on GitBook automatically after merge.

Trusted contributors can also edit directly in the GitBook UI. Contact [dev@pinot.apache.org](mailto:dev@pinot.apache.org) to request access.

## Prerequisites

* A GitHub account.
* For code contributions: a working local build (see [Code Setup](../developers/developers-and-contributors/code-setup.md)).
* For documentation contributions: familiarity with Markdown and Git.

## Next step

Connect with the Pinot community for help, discussion, and collaboration:

* [Community](../community-1/community.md)
