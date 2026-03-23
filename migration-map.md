# Migration Map: Operate Pinot + Develop & Contribute

## Operate Pinot

### Deployment (Agent 1)
Landing: `operate-pinot/deployment.md` (NEW)
- operators/operating-pinot/setup-cluster.md
- operators/operating-pinot/server-startup-status-checkers.md
- operators/operating-pinot/setup-table.md
- operators/operating-pinot/setup-ingestion.md
- operators/operating-pinot/decoupling-controller-from-the-data-path.md
- operators/cli.md
- operators/configuration-recommendation-engine.md
- developers/advanced/advanced-pinot-setup.md (dissolved from Advanced)

### Production guides (Agent 1)
Landing: `operate-pinot/production-guides.md` (NEW — seed from tutorials/operations/running-pinot-in-production.md)
- tutorials/operations/running-pinot-in-production.md (canonical seed)
- operators/operating-pinot/managing-logs.md

### Security (Agent 2)
Landing: `operate-pinot/security.md` (NEW)
- operators/operating-pinot/access-control.md
- tutorials/operations/authentication/README.md
  - tutorials/operations/authentication/basic-auth-access-control.md
  - tutorials/operations/authentication/zkbasicauthaccesscontrol.md
- tutorials/operations/configuring-tls-ssl.md

### Monitoring (Agent 2)
Landing: `operate-pinot/monitoring.md` (NEW)
- operators/operating-pinot/monitoring.md
- operators/operating-pinot/continuous-jfr.md
- tutorials/operations/monitor-pinot-using-prometheus-and-grafana.md

### Performance tuning (Agent 3)
Landing: operators/operating-pinot/tuning/README.md (REWRITE if thin)
- operators/operating-pinot/tuning/tuning-default-mmap-advice.md
- operators/operating-pinot/tuning/realtime.md
- operators/operating-pinot/tuning/routing.md
- operators/operating-pinot/tuning/query-routing-using-adaptive-server-selection.md
- operators/operating-pinot/tuning/query-scheduling.md
- operators/operating-pinot/tuning/workload-query-isolation.md
- operators/operating-pinot/tuning/segment-pruning.md
- operators/operating-pinot/oom-protection-using-automatic-query-killing.md
- operators/operating-pinot/pause-ingestion-based-on-resource-utilization.md
- operators/operating-pinot/pauseless-consumption.md
- tutorials/operations/performance-optimization-configurations.md
- tutorials/operations/segment-operations-throttling.md

### Segment management (Agent 3)
Landing: `operate-pinot/segment-management.md` (NEW)
- operators/operating-pinot/segment-assignment.md
- operators/operating-pinot/segment-lifecycle-and-repair.md
- operators/operating-pinot/instance-assignment.md
- operators/operating-pinot/rebalance/README.md
  - operators/operating-pinot/rebalance/rebalance-servers/README.md
    - operators/operating-pinot/rebalance/rebalance-servers/examples-and-scenarios.md
  - operators/operating-pinot/rebalance/rebalance-brokers.md
  - operators/operating-pinot/rebalance/rebalance-tenant.md
- operators/operating-pinot/separating-data-storage-by-age/README.md
  - operators/operating-pinot/separating-data-storage-by-age/moving-segments-across-tenants.md
  - operators/operating-pinot/separating-data-storage-by-age/using-multiple-directories.md
- operators/operating-pinot/pinot-managed-offline-flows.md
- operators/operating-pinot/minion-merge-rollup-task.md
- operators/operating-pinot/purge-task.md
- operators/operating-pinot/refresh-segment-task.md
- operators/operating-pinot/segment-generation-and-push-task.md
- operators/operating-pinot/upsert-compaction-task.md
- operators/operating-pinot/upsert-compact-merge-task.md
- operators/operating-pinot/upsert-merge-compact-task.md
- operators/operating-pinot/consistent-push-and-rollback.md
- tutorials/operations/segment-reload.md (MOVED from Operations root to Segment management)

### Kubernetes production (Agent 4)
Landing: `operate-pinot/kubernetes-production.md` (NEW — seed from tutorials/operations/kubernetes/deployment-pinot-on-kubernetes.md)
- tutorials/operations/kubernetes/deployment-pinot-on-kubernetes.md (canonical seed)
- tutorials/operations/kubernetes/helm-chart-reference.md
- tutorials/operations/kubernetes/non-eks-to-eks.md
- tutorials/operations/kubernetes/how-to-connect-pinot-with-amazon-managed-streaming-for-apache-kafka-amazon-msk.md

### Upgrades (Agent 4)
Landing: `operate-pinot/upgrades.md` (NEW)
- operators/operating-pinot/upgrading-pinot-cluster.md
- operators/operating-pinot/upgrade-notes.md

### Troubleshooting (Agent 5)
Landing: troubleshooting/README.md (REWRITE into decision-tree)
- troubleshooting/troubleshooting-pinot.md
  - troubleshooting/general-faq.md
- troubleshooting/query-faq.md
  - troubleshooting/troubleshoot-multi-stage-query-engine.md
- troubleshooting/ingestion-faq.md
  - troubleshooting/realtime-ingestion-stopped.md
- troubleshooting/operations-faq.md
- troubleshooting/pinot-on-kubernetes-faq.md
- troubleshooting/troubleshoot-zookeeper.md

---

## Develop & Contribute

### Codebase basics (Agent 6)
Landing: `develop-contribute/codebase-basics.md` (NEW)
- developers/developers-and-contributors/code-setup.md
- developers/developers-and-contributors/code-modules-and-organization.md
- developers/developers-and-contributors/dependency-management.md
- tutorials/operations/build-docker-images.md (MOVED from Operations)

### Contributing (Agent 6)
Landing: `develop-contribute/contributing.md` (NEW — merges docs-only Contributing section)
- developers/developers-and-contributors/contribution-guidelines.md
- developers/developers-and-contributors/update-document.md
- contributing/contributing.md (merged)
- contributing/style-guide.md (merged)

### Extending Pinot (Agent 7)
Landing: developers/developers-and-contributors/extending-pinot/README.md (REWRITE if thin)
- developers/developers-and-contributors/extending-pinot/custom-aggregation-function.md
- developers/developers-and-contributors/extending-pinot/segment-fetchers.md

### Plugins (Agent 7)
Landing: developers/plugin-architecture/README.md (REWRITE if thin)
- developers/plugin-architecture/write-custom-plugins/README.md
  - developers/plugin-architecture/write-custom-plugins/record-reader.md
  - developers/plugin-architecture/write-custom-plugins/pluggable-storage.md
  - developers/plugin-architecture/write-custom-plugins/write-your-batch.md
  - developers/plugin-architecture/write-custom-plugins/write-your-stream.md
  - developers/plugin-architecture/write-custom-plugins/time-series-language-plugin.md
  - developers/plugin-architecture/write-custom-plugins/segment-uploader-plugin.md
  - developers/plugin-architecture/write-custom-plugins/segment-writer-plugin.md
  - developers/plugin-architecture/write-custom-plugins/metrics-plugin.md
  - developers/plugin-architecture/write-custom-plugins/minion-task-plugin.md

### Design docs (Agent 7)
Landing: developers/design-documents/README.md (REWRITE if thin)
- developers/design-documents/segment-writer-api.md

---

## Dissolved Sections

### Advanced (developers/advanced/)
- v2-multi-stage-query-engine.md → already in Querying Data (no move needed)
- advanced-pinot-setup.md → Operate Pinot > Deployment (Agent 1)
- data-ingestion.md → already in Data Ingestion (no move needed)
- ingestion-level-transformations.md → already in Data Ingestion (no move needed)
- ingestion-level-aggregations.md → already in Data Ingestion (no move needed)
- null-value-support.md → already in Querying Data (no move needed)
- README.md → deleted from nav (no standalone Advanced section)

### Old Contributing (contributing/)
- contributing.md → merged into Develop & Contribute > Contributing (Agent 6)
- style-guide.md → merged into Develop & Contribute > Contributing (Agent 6)

---

## Redirects Needed (.gitbook.yaml)
- operators/operating-pinot/README → operate-pinot/deployment.md (old Operations landing)
- Old Troubleshooting section URLs → preserved (files stay in troubleshooting/)
- developers/developers-and-contributors/README → develop-contribute/codebase-basics.md
- contributing/contributing → develop-contribute/contributing.md
