# Code Setup

## Dev Environment Setup

To contribute to Pinot, follow the instructions below.

### Git

Pinot uses git for source code management. If you are new to Git, it will be good to review [basics](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control) of Git and a common tasks like [managing branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) and [rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing).

### Getting the Source Code

#### Create a fork

To limit the number of branches created on the Apache Pinot repository, we recommend that you create a fork by clicking on the fork button [in this page](https://github.com/apache/pinot). Read more about [fork workflow here](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow)

#### Clone the repository locally

```
$ mkdir workspace
$ cd workspace
$ git clone git@github.com:<github username>/pinot.git
$ cd pinot
# set upstream
$ git remote add upstream https://github.com/apache/pinot
# check that the upstream shows up correctly
$ git remote -v
```

### Maven

Pinot is a Maven project and familiarity with Maven will help you work with Pinot code. If you are new to Maven, you can read about Maven [here](https://maven.apache.org/) and [get a quick overview here](http://maven.apache.org/guides/getting-started/maven-in-five-minutes.html).

Run the following maven command to set up the project.

```
# compile, download sources
$mvn install package -DskipTests -Pbin-dist -DdownloadSources -DdownloadJavadocs
```

### Set up IDE

Import the project into your favorite IDE. Set up stylesheet according to your IDE. We have provided instructions for intellij and eclipse. If you are using other IDEs, ensure you use stylesheet based on [this](https://github.com/apache/pinot/blob/master/config/codestyle-intellij.xml).

#### Intellij

To import the Pinot stylesheet this launch intellij and navigate to `Preferences` (on Mac) or `Settings` on Linux.

* Navigate to `Editor` -> `Code Style` -> `Java`
* Select `Import Scheme` -> `Intellij IDES code style XML`
* Choose `codestyle-intellij.xml` from `pinot/config` folder of your workspace. Click Apply.

![](../../.gitbook/assets/.unused/import\_scheme.png)

#### Eclipse

To import the Pinot stylesheet this launch eclipse and navigate to `Preferences` (on Mac) or `Settings` on Linux.

* Navigate to Java->Code Style->Formatter
* Choose `codestyle-eclipse.xml` from `pinot/config folder` of your workspace. Click Apply.

![](../../.gitbook/assets/.unused/eclipse\_style.png)

Once the IDE is set up, you can run [`Batch QuickStart`](https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally#batch) for batch mode or [`Realtime QuickStart`](https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally#streaming) for real-time mode.

**Batch Quickstart**

* start all Pinot components (ZK, Controller, Server, Broker) in the same JVM
* create Baseball Stats table

Go to localhost:9000 in your browser and play with the query console.

**Real-time Quickstart**

* start all Pinot components (ZK, Controller, Server, Broker) in the same JVM
* Start Kafka in the same JVM
* create MeetUpRSVP table.
* Live stream meetup events into Kafka

Go to localhost:9000 in your browser and play with the meetup RSVP table.
