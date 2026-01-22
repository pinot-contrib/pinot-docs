FROM metabase/metabase:v0.55.7

RUN mkdir -p /plugins && \
    curl -L -o /plugins/pinot.metabase-driver.jar \
    https://github.com/startreedata/metabase-pinot-driver/releases/download/v1.0.1/pinot.metabase-driver-v1.0.1.jar

ENV MB_PLUGINS_DIR=/plugins
