# Update Documentation

Pinot documentation is powered by [GitBook](https://www.gitbook.com/).

A bidirectional GitHub integration exists as a back up for content. You can find it at [https://github.com/pinot-contrib/pinot-docs](https://github.com/pinot-contrib/pinot-docs).

If you would like to contribute changes or additions, two methods are available: you can submit a pull request or edit directly on GitBook.

### Submit a Pull Request

If you are familiar with using Git and GitHub, you can fork the [pinot-docs](https://github.com/pinot-contrib/pinot-docs) repo. This will create your own version of the repository, which you can find at `https://github.com/{yourusername}/pinot-docs`, where `{yourusername}` is the username you created in GitHub.

Clone from the fork to your local machine.

Then, modify the documentation locally on your machine. When you commit, please write a meaningful and clear commit message, such as:

`git commit -m 'Fixes a typo on the Update Documentation page'`

Then push your changes to your fork on GitHub.

Use the GitHub web interface to create a pull request (PR) for review.

Wait. The Pinot documentation team will usually review pull requests within a few days. Suggestions or changes may be requested. You can make these by updating in your local branch and pushing those changes.

Once the PR is approved, it will be merged by one of the code owners. When that happens, the changes will automatically applied to the corresponding GitBook pages.

Please note that all GitBook documentation follows [Markdown Syntax](https://www.markdownguide.org/basic-syntax/).

### Edit Directly on GitBook

Some trusted contributors are given the ability to edit any page via the [Pinot GitBook UI](https://app.gitbook.com/@apache-pinot/s/apache-pinot-cookbook/) and then save and merge the changes themselves. This permission is typically granted to active contributors and committers, by request (and review).

Please contact the site admin by emailing [dev@pinot.apache.org](mailto:dev@pinot.apache.org) with your request for edit permission and a description of the content you would like to edit or add.

Changes made using this method are automatically merged into the GitHub repo, such as can be seen in [this commit](https://github.com/pinot-contrib/pinot-docs/commit/40184fd7563402a7527674991b6abbf9ae2ce7c3).
