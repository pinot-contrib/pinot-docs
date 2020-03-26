# Table of contents

* [Introduction](README.md)
* [Pinot Overview](concepts/README.md)
  * [Concepts](concepts/concepts.md)
  * [Architecture](concepts/architecture.md)
* [Getting started](getting-started/README.md)
  * [Running Pinot locally](getting-started/running-pinot-locally.md)
  * [Running Pinot in Docker](getting-started/running-pinot-in-docker.md)
  * [Running Pinot in Kubernetes](getting-started/kubernetes-quickstart.md)
  * [Running Pinot in the Cloud](getting-started/quickstart/README.md)
    * [AWS Quickstart](getting-started/quickstart/aws-quickstart.md)
    * [GCP Quickstart](getting-started/quickstart/gcp-quickstart.md)
    * [Azure Quickstart](getting-started/quickstart/azure-quickstart.md)
  * [Pinot Data Explorer](getting-started/exploring-pinot.md)
  * [Batch upload sample data](getting-started/pushing-your-data-to-pinot.md)
  * [Stream sample data](getting-started/pushing-your-streaming-data-to-pinot.md)
* [Pinot Components](pinot-components/README.md)
  * [Cluster](pinot-components/cluster.md)
  * [Controller](pinot-components/controller.md)
  * [Broker](pinot-components/broker.md)
  * [Server](pinot-components/server.md)
  * [Minion](pinot-components/minion.md)
  * [Tenant](pinot-components/tenant.md)
  * [Table](pinot-components/table.md)
  * [Schema](pinot-components/schema.md)
  * [Segment](pinot-components/segment.md)
* [User Guide](pinot-user-guide/README.md)
  * [Querying Pinot](pinot-user-guide/querying-pinot-using-standard-sql.md)
  * [Response Format](pinot-user-guide/response-format.md)
  * [Pinot Query Language](pinot-user-guide/pinot-query-language.md)
  * [Pinot Rest Admin Interface](pinot-user-guide/pinot-rest-admin-interface.md)
  * [Pinot Clients](pinot-user-guide/pinot-clients/README.md)
    * [Java](pinot-user-guide/pinot-clients/java.md)
    * [Golang](pinot-user-guide/pinot-clients/golang.md)
* [Manage & Operate](operating-pinot/README.md)
  * [Setup cluster](operating-pinot/setup-cluster.md)
  * [Setup table](operating-pinot/setup-table.md)
  * [Setup ingestion](operating-pinot/setup-ingestion.md)
  * [Monitoring](operating-pinot/monitoring.md)
  * [Tuning](operating-pinot/tuning/README.md)
    * [Realtime](operating-pinot/tuning/realtime.md)
    * [Routing](operating-pinot/tuning/routing.md)
* [Developers and Contributors](developers-and-contributors/README.md)
  * [Extending Pinot](developers-and-contributors/extending-pinot/README.md)
    * [Pluggable Streams](developers-and-contributors/extending-pinot/pluggable-streams.md)
    * [Pluggable Storage](developers-and-contributors/extending-pinot/pluggable-storage.md)
    * [Record Reader](developers-and-contributors/extending-pinot/record-reader.md)
    * [Segment Fetchers](developers-and-contributors/extending-pinot/segment-fetchers.md)
  * [Contribution Guidelines](developers-and-contributors/contribution-guidelines.md)
  * [Code Setup](developers-and-contributors/code-setup.md)
  * [Code Modules and Organization](developers-and-contributors/code-modules-and-organization.md)
  * [Update Document](developers-and-contributors/update-document.md)
* [Releases](releases/README.md)
  * [0.3.0](releases/0.3.0.md)
  * [0.2.0](releases/0.2.0.md)
  * [0.1.0](releases/1.0.md)

## Pinot Features <a id="pinot-features-1"></a>

* [Indexing](indexing.md)
* [Text Search Support](text-search-support.md)

## Integrations

* [ThirdEye](integrations/thirdeye.md)
* [Superset](integrations/superset.md)
* [Presto](integrations/presto.md)
* [PowerBI](integrations/powerbi.md)

## PLUGINS

* [Plugin Architecture](plugins/plugin-architecture.md)
* [pinot-input-format](plugins/pinot-input-format.md)
* [pinot-file-system](plugins/pinot-file-system.md)
* [pinot-batch-ingestion](plugins/pinot-batch-ingestion.md)
* [pinot-stream-ingestion](plugins/pinot-stream-ingestion.md)

## How To

* [AWS Lambda/EC2 to send events to a Kafka running in AWS EKS](how-to/non-eks-to-eks.md)

## POWERED BY PINOT <a id="powered-by-pinot-1"></a>

* [Companies using Pinot](powered-by-pinot-1/powered-by-pinot.md)

## Misc

* [Misc](misc/misc-1/README.md)
  * [Running Pinot in Production](misc/misc-1/running-pinot-in-production.md)
  * [Ingest Data](misc/misc-1/pinot-connectors/README.md)
    * [Batch](misc/misc-1/pinot-connectors/batch/README.md)
      * [Creating Pinot Segments](misc/misc-1/pinot-connectors/batch/create-pinot-segments.md)
      * [Write your batch](misc/misc-1/pinot-connectors/batch/write-your-batch.md)
      * [HDFS](misc/misc-1/pinot-connectors/batch/hdfs.md)
      * [AWS S3](misc/misc-1/pinot-connectors/batch/s3.md)
      * [Azure Storage](misc/misc-1/pinot-connectors/batch/azure.md)
      * [Google Cloud Storage](misc/misc-1/pinot-connectors/batch/gcs.md)
    * [Streaming](misc/misc-1/pinot-connectors/streaming/README.md)
      * [Creating Pinot Segments](misc/misc-1/pinot-connectors/streaming/create-pinot-segments.md)
      * [Write your stream](misc/misc-1/pinot-connectors/streaming/write-your-stream.md)
      * [Kafka](misc/misc-1/pinot-connectors/streaming/kafka.md)
      * [Azure EventHub](misc/misc-1/pinot-connectors/streaming/eventhub.md)
      * [Amazon Kinesis](misc/misc-1/pinot-connectors/streaming/kinesis.md)
      * [Google Pub/Sub](misc/misc-1/pinot-connectors/streaming/google-pub-sub.md)
  * [Store Data](misc/misc-1/store-data/README.md)
    * [Batch Tables](misc/misc-1/store-data/offline-tables.md)
    * [Streaming Tables](misc/misc-1/store-data/realtime-tables.md)
  * [Advanced Pinot Setup](misc/misc-1/advanced-pinot-setup.md)
  * [Pinot Architecture](misc/misc-1/pinot-architecture.md)
  * [Data Ingestion Overview](misc/misc-1/data-ingestion.md)
* [Build Docker Images](misc/build-docker-images.md)

## RESOURCES <a id="community-1"></a>

* [Community](community-1/community.md)
* [Blogs](community-1/blogs.md)
* [Presentations](community-1/blogs-and-presentations.md)
* [Videos](community-1/videos.md)

