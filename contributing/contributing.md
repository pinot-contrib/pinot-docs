# Contributing to the Pinot docs

Pinot documentation is powered by [GitBook](https://www.gitbook.com/).

A bidirectional GitHub integration exists as a back-up for content. You can find it at [https://github.com/pinot-contrib/pinot-docs](https://github.com/pinot-contrib/pinot-docs).

To suggest updates to the documentation, follow the directions below.

## Make suggested updates

### Fork and clone the Pinot documentation repository
If you are familiar with using Git and GitHub, you can [fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the [pinot-docs](https://github.com/pinot-contrib/pinot-docs) repository. This will create your own version of the repository, which you can find at `https://github.com/{yourusername}/pinot-docs`, where `{yourusername}` is the username you created in GitHub. 

[Clone from the fork](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to your local machine.

### Make changes
Modify the documentation locally on your machine. When you commit, write a meaningful and clear commit message, such as:

`git commit -m 'Fixes a typo on the Update Documentation page'`

Then, push your changes to your fork on GitHub.

### Submit a pull request
Use the GitHub web interface to create a pull request (PR) for review.

### Get and incorporate review 
Wait. The Pinot documentation team will usually review pull requests within a few days. Suggestions or changes may be requested. You can make these by updating in your local branch and pushing those changes.

Once the PR is approved, it will be merged by one of the code owners. When that happens, the changes will automatically applied to the corresponding GitBook pages.

Note that all GitBook documentation follows [Markdown Syntax](https://www.markdownguide.org/basic-syntax/).

## Edit directly on GitBook

If you're an active and trusted contributor, you can request access to edit the documentation directly with the [GitBook UI](https://app.gitbook.com/@apache-pinot/s/apache-pinot-cookbook/). 

Contact the site admin by emailing [dev@pinot.apache.org](mailto:dev@pinot.apache.org) with your request for edit permission and a description of the content you would like to edit or add.

Changes made using this method are automatically merged into the GitHub repo, as can be seen in [this commit](https://github.com/pinot-contrib/pinot-docs/commit/40184fd7563402a7527674991b6abbf9ae2ce7c3).

## Style and formatting

All of Pinot's documentation is written in [Markdown](https://en.wikipedia.org/wiki/Markdown). 

For style guidelines, see the [Apache Pinot style guide](https://github.com/pinot-contrib/pinot-docs/blob/latest/contributing/style-guide.md).