# Contribution Guidelines

Before you begin to contribute, make sure you have reviewed [Dev Environment Setup](code-setup.md) and [Code Modules and Organization](code-modules-and-organization.md) sections and that you have created your own fork of the pinot source code.

## Pinot Enhancement Proposal Workflow

The Apache Pinot community encourages members to contribute to the overall growth and success of the project. All contributors are expected to follow the following guidelines when proposing an enhancement (aka PEP - Pinot Enhancement Proposal):

All enhancements, regardless of scope/size, must start with a [Github issue](https://github.com/apache/pinot/issues). The issue should clearly state the following information:

* What needs to be done?
* Why the feature is needed (e.g. describing the use case).&#x20;
* It may also include an initial idea/proposal on how as well.
* The Github issue must be tagged with the label PEP-Request.

Once the Github issue is filed:

* The PMC would decide if a detailed proposal/design-doc is required or can simply be followed by a PR.
* There should be enough time (e.g. 5 business days) given for the PMC to review the issue/proposal before moving to implementation.&#x20;
* One +1 and zero -1 votes from the PMC may be used to proceed with the implementation.&#x20;
* If during the course of the implementation it is found that the feature is much more complex than initially anticipated, the PMC may request for a detailed design doc.

The PMC would use the following guideline when deciding whether a PEP requires an explicit proposal/design doc, or can simply be followed by a PR that includes a link to the Github issue.

* Any new major feature, subsystem, or piece of functionality.
* Any change that may potentially create backward incompatibility:
  * Any change that impacts the public interfaces of the project.
  * Any changes to SPI
  * Adding new API resources, or changing broker-server-controller communications.
* Any change that can impact performance.

If the requests get at least one +1 and no -1 from the PMC to directly go to the PR stage, the requestor can then submit the PR along with a link to the Github issue.

If the request requires a proposal, then the requestor is expected to provide a proposal design doc before submitting a PR for review. The design doc should have public read and comment access. (If your organization does not allow public access, look to other freely available platforms to host your document). The design doc must include the following:

* **Motivation:** Describe the problem to be solved including the details on why such as use-case, etc.
* **Proposed Change:** Describe the new thing that needs to be done. This may be fairly extensive and have large subsections of its own. Or it may be a few sentences, depending on the scope of the change. Also, describe “How” with details and possible POC.
* **New or Changed Public Interfaces:** impact to any of the "compatibility commitments" described above. We want to call these out in particular so everyone thinks about them.
* **Deployment, Migration Plan and Compatibility:** if this feature requires additional support for a no-downtime upgrade describe how that will work
* **Rejected Alternatives:** What are the other alternatives you considered and why are they worse? The goal of this section is to help people understand why this is the best solution now, and also to prevent churn in the future when old alternatives are reconsidered.
* **PMC Review Status:** The proposal/design doc may also contain a review status table at the beginning of the doc that includes the reviewer names along with their review status.

**The proposal/design doc should be in a google doc that has comment access enabled by default to any community member (should not require asking for permissions)**. Only exceptions are small features where the initial proposal in the issue is generally accepted. Once the proposal/design doc is approved (all questions/comments resolved), it must be transferred into a common Google Drive where all Pinot proposal/design docs must be submitted.

* If there are meetings/discussions offline with a subset of members, the meeting notes should be captured and added to the doc.
* General Guidelines
  * Smaller PRs that are easier to review
  * Pure refactoring PRs must be separated from PRs that change functionality. Refactoring PRs may state so, as an aid for the reviewers. For example, package moves may show up as huge diff’s in the PR.

## Create a design document

If your change is relatively minor, you can skip this step. If you are adding new major feature, we suggest that you add a design document and solicit comments from the community before submitting any code.

[Here](https://docs.pinot.apache.org/developers/design-documents) is a list of current design documents.

## Create an issue for the change

Create a Pinot issue [here](https://github.com/apache/pinot/issues) for the change you would like to make. Provide information on why the change is needed and how you plan to address it. Use the conversations on the issue as a way to validate assumptions and the right way to proceed. Be sure to review sections on [Backward and Forward compatibility changes](contribution-guidelines.md#backward-and-forward-compatibility-changes) and [External libraries](contribution-guidelines.md#external-libraries).

If you have a design document, refer to the design documents in your Issue. You may even want to create multiple issues depending on the extent of your change.

Once you are clear about what you want to do, proceed with the next steps listed below.

## Create a branch for your change

```
$ cd pinot
#
# ensure you are starting from the latest code base
# the following steps, ensure your fork's (origin's) master is up-to-date
#
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
# create a branch for your issue
$ git checkout -b <your issue branch>
```

Make the necessary changes. If the changes you plan to make are too big, make sure you break it down into smaller tasks.

## Making the changes

Follow the recommendations/best-practices noted here when you are making changes.

### Code documentation

Ensure your code is adequately documented. Some things to consider for documentation:

* Always include class level java docs. At the top class level, we are looking for information about what functionality is provided by the class, what state is maintained by the class, whether there are concurrency/thread-safety concerns and any exceptional behavior that the class might exhibit.
* Document public methods and their parameters.

### Logging

* Ensure there is adequate logging for positive paths as well as exceptional paths. As a corollary to this, ensure logs are not noisy.
* Do not use System.out.println to log messages. Use the `slf4j` loggers.
* Use logging levels correctly: set level to `debug` for verbose logs useful for only for debugging.
* Do not log stack traces via `printStackTrace` method of the exception.

### Exceptions and Exception-Handling

* Where possible, throw specific exceptions, preferably checked exceptions, so the callers can easily determine what the erroneous conditions that need to be handled are.
* Avoid catching broad exceptions (i.e., `catch (Exception e)` blocks), except for when this is in the `run()` method of a thread/runnable.

Current Pinot code does not strictly adhere to this, but we would like to change this over time and adopt best practices around exception handling.

### Backward and Forward compatibility changes

If you are making any changes to state stored, either in Zookeeper or in segments, make sure you consider both backward and forward compatibility issues.

* For backward compatibility, consider cases where one component is using the new version and another is still on the old version. E.g., when the request format between broker and server is updated, consider resulting behaviors when a new broker is talking to an older server. Will it break?
* For forward compatibility, consider rollback cases. E.g., consider what happens when state persisted by new code is handled by old code. Does the old code skip over new fields?

### External libraries

Be cautious about pulling in external dependencies. You will need to consider multiple things when faced with a need to pull in a new library.

* What capability is the addition of the library providing you with? Can existing libraries provide this functionality (may be with a little bit of effort)?
* Is the external library maintained by an active community of contributors?
* What are the licensing terms for the library. For more information about handling licenses, see [License Headers for newly added files](contribution-guidelines.md#license-headers-for-newly-added-files).
* Are you adding the library to [Foundational modules](code-modules-and-organization.md#foundational-modules) modules? This will affect the rest of the Pinot code base. If the new library pulls in a lot of transitive dependencies, then we might encounter unexpected issues with multiple classes in the classpath. These issues are hard to catch with tests as the order of loading the libraries at runtime matters. If you absolutely need the support, consider adding it via extension modules, see [Extension modules](code-modules-and-organization.md#extension-modules).

### Testing your changes

Automated tests are always recommended for contributions. Make sure you write tests so that:

1. You verify the correctness of your contribution. This serves as proof to you as well as the reviewers.
2. You future proof your contributions against code refactors or other changes. While this may not always be possible (see [Testing Guidelines](contribution-guidelines.md#testing-guidelines)), it's a good goal to aim for.

Identify a list of tests for the changes you have made. Depending on the scope of changes, you may need one or more of the following tests:

*   Unit Tests

    Make sure your code has the necessary class or method level unit tests. It is important to write both positive case as well as negative case tests. Document your tests well and add meaningful assertions in the tests; when the assertions fail, ensure that the right messages are logged with information that allows other to debug.
*   Integration Tests

    Add integration tests to cover End-to-End paths without relying on _mocking_ (see note below). You `MUST` add integration tests for REST APIs, and must include tests that cover different error codes; i.e., 200 OK, 4xx or 5xx errors that are explicit contracts of the API.

### Testing Guidelines

*   **Mocking**

    Use [Mockito](https://site.mockito.org/) to mock classes to control specific behaviors - e.g., simulate various error conditions.

{% hint style="info" %}
**Note**

DO NOT use advanced mock libraries such as [PowerMock](https://github.com/powermock/powermock). They make bytecode level changes to allow tests for static/private members but this typically results in other tools like jacoco to fail. They also promote incorrect implementation choices that make it harder to test additional changes. When faced with a choice to use PowerMock or advanced mocking options, you might either need to refactor the code to work better with mocking or you actually need to write an integration test instead of a unit test.
{% endhint %}

*   **Validate assumptions in tests**

    Make sure that adequate asserts are added in the tests to verify that the tests are passing for the right reasons.
*   **Write reliable tests**

    Make sure you are writing tests that are reliable. If the tests depend on asynchronous events to be fired, do not add `sleep` to your tests. Where possible, use appropriate mocking or condition based triggers.

### License Headers for newly added files

All source code files should have license headers. To automatically add the header for any new file you plan to checkin, run in `pinot` top-level folder:

```
mvn license:format
```

Note

If you checkin third-party code or files, make sure you review Apache guidelines:

* [Licences that can be included](https://www.apache.org/legal/resolved.html#what-can-we-include-in-an-asf-project-category-a)
* [Licences that may be included](https://www.apache.org/legal/resolved.html#what-can-we-maybe-include-in-an-asf-project-category-b)
* [Licenses that should not be included](https://www.apache.org/legal/resolved.html#what-can-we-not-include-in-an-asf-project-category-x)

Once you determine the code you are pulling in adhere to the guidelines above, go ahead pull the changes in. Do not add license headers for them. Follow these instructions to ensure we are compliant with Apache Licensing process:

* Under `pinot/licenses` add a LICENSE-\<newlib> file that has the license terms of the included library.
* Update the `pinot/LICENSE` file to indicate the newly added library file paths under the corresponding supported Licenses.
* Update the exclusion rules for `license` and `rat` maven plugins in the parent pom: `pinot/pom.xml`.

If attention to the licensing terms in not paid early on, they will be caught much later in the process, when we prepare to make a new release. Updating code at that time to work with the right libraries at that time might require bigger refactoring changes and delay the release process.

## Creating a Pull Request (PR)

*   **Verifying code-style**

    Run the following command to verify the code-style before posting a PR

```
mvn checkstyle:check
```

*   **Run tests**

    Before you create a review request for the changes, make sure you have run the corresponding unit tests for your changes. You can run individual tests via the IDE or via maven command-line. Finally run all tests locally by running `mvn clean install -Pbin-dist`.

    For changes that are related to performance issues or race conditions, it is hard to write reliable tests, so we recommend running manual stress tests to validate the changes. You `MUST` note the manual tests done in the PR description.
*   **Push changes and create a PR for review**

    Commit your changes with a meaningful commit message.

```
$ git add <files required for the change>
$ git commit -m "Meaningful oneliner for the change"
$ git push origin <your issue branch>

After this, create a PullRequest in `github <https://github.com/apache/pinot/pulls>`_. Include the following information in the description:

  * The changes that are included in the PR.

  * Design document, if any.

  * Information on any implementation choices that were made.

  * Evidence of sufficient testing. You ``MUST`` indicate the tests done, either manually or automated.

Once the PR is created, the code base is compiled and all tests are run via ``travis``. Make sure you followup on any issues flagged by travis and address them.
If you see test failures that are intermittent, create an issue to track them.

Once the ``travis`` run is clear, request reviews from atleast 2 committers on the project and be sure to gently to followup on the issue with the reviewers.
```

*   Once you receive comments on github on your changes, be sure to respond to them on github and address the concerns. If any discussions happen offline for the changes in question, make sure to capture the outcome of the discussion, so others can follow along as well.

    It is possible that while your change is being reviewed, other changes were made to the master branch. Be sure to pull rebase your change on the new changes thus:

```
# commit your changes
$ git add <updated files>
$ git commit -m "Meaningful message for the udpate"
# pull new changes
$ git checkout master
$ git merge upstream/master
$ git checkout <your issue branch>
$ git rebase master

At this time, if rebase flags any conflicts, resolve the conflicts and follow the instructions provided by the rebase command.

Run additional tests/validations for the new changes and update the PR by pushing your changes:
```

```
$ git push origin <your issue branch>
```

* When you have addressed all comments and have an approved PR, one of the committers can merge your PR.
* After your change is merged, check to see if any documentation needs to be updated. If so, create a PR for documentation.

## Update Documentation

Usually for new features, functionalities, API changes, documentation update is required to keep users up to date and keep track of our development.

Follow this link to [Update Document](update-document.md) accordingly
