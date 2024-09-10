---
description: >-
  In this Apache Pinot guide, we'll learn how visualize data using the Streamlit
  web framework.
---

# Connect to Streamlit

In this guide you'll learn how to visualize data from Apache Pinot using [Streamlit](https://streamlit.io). Streamlit is a Python library that makes it easy to build interactive data based web applications.

We're going to use Streamlit to build a real-time dashboard to visualize the changes being made to Wikimedia properties.

![Real-Time Dashboard Architecture](https://github.com/pinot-contrib/pinot-docs/blob/latest/img/streamlit.png) _Real-Time Dashboard Architecture_

## Startup components

We're going to use the following Docker compose file, which spins up instances of Zookeeper, Kafka, along with a Pinot controller, broker, and server:

```yaml
version: '3.7'
services:
  zookeeper:
    image: zookeeper:3.5.6
    container_name: "zookeeper-wiki"
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
  kafka:
    image: wurstmeister/kafka:latest
    restart: unless-stopped
    container_name: "kafka-wiki"
    ports:
      - "9092:9092"
    expose:
      - "9093"
    depends_on:
      - zookeeper
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper-wiki:2181/kafka
      KAFKA_BROKER_ID: 0
      KAFKA_ADVERTISED_HOST_NAME: kafka-wiki
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-wiki:9093,OUTSIDE://localhost:9092
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9093,OUTSIDE://0.0.0.0:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,OUTSIDE:PLAINTEXT
  pinot-controller:
    image: apachepinot/pinot:0.10.0
    command: "StartController -zkAddress zookeeper-wiki:2181 -dataDir /data"
    container_name: "pinot-controller-wiki"
    volumes:
      - ./config:/config
      - ./data:/data
    restart: unless-stopped
    ports:
      - "9000:9000"
    depends_on:
      - zookeeper
  pinot-broker:
    image: apachepinot/pinot:0.10.0
    command: "StartBroker -zkAddress zookeeper-wiki:2181"
    restart: unless-stopped
    container_name: "pinot-broker-wiki"
    volumes:
      - ./config:/config
    ports:
      - "8099:8099"
    depends_on:
      - pinot-controller
  pinot-server:
    image: apachepinot/pinot:0.10.0
    command: "StartServer -zkAddress zookeeper-wiki:2181"
    restart: unless-stopped
    container_name: "pinot-server-wiki"
    volumes:
      - ./config:/config
    depends_on:
      - pinot-broker
```

_docker-compose.yml_

Run the following command to launch all the components:

```bash
docker-compose up
```

## Wikimedia recent changes stream

Wikimedia provides provides a continuous stream of structured event data describing changes made to various Wikimedia properties. The events are published over HTTP using the Server-Side Events (SSE) Protocol.

You can find the endpoint at: [stream.wikimedia.org/v2/stream/recentchange](https://stream.wikimedia.org/v2/stream/recentchange)

We'll need to install the SSE client library to consume this data:

```bash
pip install sseclient-py
```

Next, create a file called `wiki.py` that contains the following:

```python
import json
import pprint
import sseclient
import requests

def with_requests(url, headers):
    """Get a streaming response for the given event feed using requests."""    
    return requests.get(url, stream=True, headers=headers)

url = 'https://stream.wikimedia.org/v2/stream/recentchange'
headers = {'Accept': 'text/event-stream'}
response = with_requests(url, headers)
client = sseclient.SSEClient(response)

for event in client.events():
    stream = json.loads(event.data)
    pprint.pprint(stream)
```

_wiki.py_

The highlighted section shows how we connect to the recent changes feed using the SSE client library.

Let's run this script as shown below:

```bash
python wiki.py
```

We'll see the following (truncated) output:

**Output**

```json
{'$schema': '/mediawiki/recentchange/1.0.0',
 'bot': False,
 'comment': '[[:File:Storemyr-Fagerbakken landskapsvernområde HVASSER '
            'Oslofjorden Norway (Protected coastal forest Recreational area '
            'hiking trails) Rituell-kultisk steinstreng sørøst i skogen (small '
            'archeological stone string) Vår (spring) 2021-04-24.jpg]] removed '
            'from category',
 'id': 1923506287,
 'meta': {'domain': 'commons.wikimedia.org',
          'dt': '2022-05-12T09:57:00Z',
          'id': '3800228e-43d8-440d-8034-c68977742653',
          'offset': 3855767440,
          'partition': 0,
          'request_id': '930b17cc-f14a-4656-afa1-d15b79a8f666',
          'stream': 'mediawiki.recentchange',
          'topic': 'eqiad.mediawiki.recentchange',
          'uri': 'https://commons.wikimedia.org/wiki/Category:Iron_Age_in_Norway'},
 'namespace': 14,
 'parsedcomment': '<a '
                  'href="/wiki/File:Storemyr-Fagerbakken_landskapsvernomr%C3%A5de_HVASSER_Oslofjorden_Norway_(Protected_coastal_forest_Recreational_area_hiking_trails)_Rituell-kultisk_steinstreng_s%C3%B8r%C3%B8st_i_skogen_(small_archeological_stone_string)_V%C3%A5r_(spring)_2021-04-24.jpg" '
                  'title="File:Storemyr-Fagerbakken landskapsvernområde '
                  'HVASSER Oslofjorden Norway (Protected coastal forest '
                  'Recreational area hiking trails) Rituell-kultisk '
                  'steinstreng sørøst i skogen (small archeological stone '
                  'string) Vår (spring) '
                  '2021-04-24.jpg">File:Storemyr-Fagerbakken '
                  'landskapsvernområde HVASSER Oslofjorden Norway (Protected '
                  'coastal forest Recreational area hiking trails) '
                  'Rituell-kultisk steinstreng sørøst i skogen (small '
                  'archeological stone string) Vår (spring) 2021-04-24.jpg</a> '
                  'removed from category',
 'server_name': 'commons.wikimedia.org',
 'server_script_path': '/w',
 'server_url': 'https://commons.wikimedia.org',
 'timestamp': 1652349420,
 'title': 'Category:Iron Age in Norway',
 'type': 'categorize',
 'user': 'Krg',
 'wiki': 'commonswiki'}
{'$schema': '/mediawiki/recentchange/1.0.0',
 'bot': False,
 'comment': '[[:File:Storemyr-Fagerbakken landskapsvernområde HVASSER '
            'Oslofjorden Norway (Protected coastal forest Recreational area '
            'hiking trails) Rituell-kultisk steinstreng sørøst i skogen (small '
            'archeological stone string) Vår (spring) 2021-04-24.jpg]] removed '
            'from category',
 'id': 1923506289,
 'meta': {'domain': 'commons.wikimedia.org',
          'dt': '2022-05-12T09:57:00Z',
          'id': '2b819d20-beca-46a5-8ce3-b2f3b73d2cbe',
          'offset': 3855767441,
          'partition': 0,
          'request_id': '930b17cc-f14a-4656-afa1-d15b79a8f666',
          'stream': 'mediawiki.recentchange',
          'topic': 'eqiad.mediawiki.recentchange',
          'uri': 'https://commons.wikimedia.org/wiki/Category:Cultural_heritage_monuments_in_F%C3%A6rder'},
 'namespace': 14,
 'parsedcomment': '<a '
                  'href="/wiki/File:Storemyr-Fagerbakken_landskapsvernomr%C3%A5de_HVASSER_Oslofjorden_Norway_(Protected_coastal_forest_Recreational_area_hiking_trails)_Rituell-kultisk_steinstreng_s%C3%B8r%C3%B8st_i_skogen_(small_archeological_stone_string)_V%C3%A5r_(spring)_2021-04-24.jpg" '
                  'title="File:Storemyr-Fagerbakken landskapsvernområde '
                  'HVASSER Oslofjorden Norway (Protected coastal forest '
                  'Recreational area hiking trails) Rituell-kultisk '
                  'steinstreng sørøst i skogen (small archeological stone '
                  'string) Vår (spring) '
                  '2021-04-24.jpg">File:Storemyr-Fagerbakken '
                  'landskapsvernområde HVASSER Oslofjorden Norway (Protected '
                  'coastal forest Recreational area hiking trails) '
                  'Rituell-kultisk steinstreng sørøst i skogen (small '
                  'archeological stone string) Vår (spring) 2021-04-24.jpg</a> '
                  'removed from category',
 'server_name': 'commons.wikimedia.org',
 'server_script_path': '/w',
 'server_url': 'https://commons.wikimedia.org',
 'timestamp': 1652349420,
 'title': 'Category:Cultural heritage monuments in Færder',
 'type': 'categorize',
 'user': 'Krg',
 'wiki': 'commonswiki'}
```

## Ingest recent changes into Kafka

Now we're going to import each of the events into Apache Kafka. First let's create a Kafka topic called `wiki_events` with 5 partitions:

```bash
docker exec -it kafka-wiki kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic wiki_events \
  --partitions 5
```

Create a new file called `wiki_to_kafka.py` and import the following libraries:

```python
import json
import sseclient
import datetime
import requests
import time
from confluent_kafka import Producer
```

_wiki\_to\_kafka.py_

Add these functions:

```python
def with_requests(url, headers):
    """Get a streaming response for the given event feed using requests."""    
    return requests.get(url, stream=True, headers=headers)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))

def json_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise "Type %s not serializable" % type(obj)
```

_wiki\_to\_kafka.py_

And now let's add the code that calls the recent changes API and imports events into the `wiki_events` topic:

```python
producer = Producer({'bootstrap.servers': 'localhost:9092'})

url = 'https://stream.wikimedia.org/v2/stream/recentchange'
headers = {'Accept': 'text/event-stream'}
response = with_requests(url, headers) 
client = sseclient.SSEClient(response)

events_processed = 0
while True:
    try: 
        for event in client.events():
            stream = json.loads(event.data)
            payload = json.dumps(stream, default=json_serializer, ensure_ascii=False).encode('utf-8')
            producer.produce(topic='wiki_events', 
              key=str(stream['meta']['id']), value=payload, callback=acked)

            events_processed += 1
            if events_processed % 100 == 0:
                print(f"{str(datetime.datetime.now())} Flushing after {events_processed} events")
                producer.flush()
    except Exception as ex:
        print(f"{str(datetime.datetime.now())} Got error:" + str(ex))
        response = with_requests(url, headers) 
        client = sseclient.SSEClient(response)
        time.sleep(2)
```

_wiki\_to\_kafka.py_

The highlighted parts of this script indicate where events are ingested into Kafka and then flushed to disk.

If we run this script:

```bash
python wiki_to_kafka.py
```

We'll see a message every time 100 messages are pushed to Kafka, as shown below:

**Output**

```
2022-05-12 10:58:34.449326 Flushing after 100 events
2022-05-12 10:58:39.151599 Flushing after 200 events
2022-05-12 10:58:43.399528 Flushing after 300 events
2022-05-12 10:58:47.350277 Flushing after 400 events
2022-05-12 10:58:50.847959 Flushing after 500 events
2022-05-12 10:58:54.768228 Flushing after 600 events
```

## Explore Kafka

Let's check that the data has made its way into Kafka.

The following command returns the message offset for each partition in the `wiki_events` topic:

```bash
docker exec -it kafka-wiki kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic wiki_events
```

**Output**

```
wiki_events:0:42
wiki_events:1:61
wiki_events:2:52
wiki_events:3:56
wiki_events:4:58
```

Looks good. We can also stream all the messages in this topic by running the following command:

```bash
docker exec -it kafka-wiki kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic wiki_events \
  --from-beginning
```

**Output**

```
...
{"$schema": "/mediawiki/recentchange/1.0.0", "meta": {"uri": "https://en.wikipedia.org/wiki/Super_Wings", "request_id": "6f82e64d-220f-41f4-88c3-2e15f03ae504", "id": "c30cd735-1ead-405e-94d1-49fbe7c40411", "dt": "2022-05-12T10:05:36Z", "domain": "en.wikipedia.org", "stream": "mediawiki.recentchange", "topic": "eqiad.mediawiki.recentchange", "partition": 0, "offset": 3855779703}, "type": "log", "namespace": 0, "title": "Super Wings", "comment": "", "timestamp": 1652349936, "user": "2001:448A:50E0:885B:FD1D:2D04:233E:7647", "bot": false, "log_id": 0, "log_type": "abusefilter", "log_action": "hit", "log_params": {"action": "edit", "filter": "550", "actions": "tag", "log": 32575794}, "log_action_comment": "2001:448A:50E0:885B:FD1D:2D04:233E:7647 triggered [[Special:AbuseFilter/550|filter 550]], performing the action \"edit\" on [[Super Wings]]. Actions taken: Tag ([[Special:AbuseLog/32575794|details]])", "server_url": "https://en.wikipedia.org", "server_name": "en.wikipedia.org", "server_script_path": "/w", "wiki": "enwiki", "parsedcomment": ""}
{"$schema": "/mediawiki/recentchange/1.0.0", "meta": {"uri": "https://no.wikipedia.org/wiki/Brukerdiskusjon:Haros", "request_id": "a20c9692-f301-4faf-9373-669bebbffff4", "id": "566ee63e-8e86-4a7e-a1f3-562704306509", "dt": "2022-05-12T10:05:36Z", "domain": "no.wikipedia.org", "stream": "mediawiki.recentchange", "topic": "eqiad.mediawiki.recentchange", "partition": 0, "offset": 3855779714}, "id": 84572581, "type": "edit", "namespace": 3, "title": "Brukerdiskusjon:Haros", "comment": "/* Stor forbokstav / ucfirst */", "timestamp": 1652349936, "user": "Asav", "bot": false, "minor": false, "patrolled": true, "length": {"old": 110378, "new": 110380}, "revision": {"old": 22579494, "new": 22579495}, "server_url": "https://no.wikipedia.org", "server_name": "no.wikipedia.org", "server_script_path": "/w", "wiki": "nowiki", "parsedcomment": "<span dir=\"auto\"><span class=\"autocomment\"><a href=\"/wiki/Brukerdiskusjon:Haros#Stor_forbokstav_/_ucfirst\" title=\"Brukerdiskusjon:Haros\">→‎Stor forbokstav / ucfirst</a></span></span>"}
{"$schema": "/mediawiki/recentchange/1.0.0", "meta": {"uri": "https://es.wikipedia.org/wiki/Campo_de_la_calle_Industria", "request_id": "d45bd9af-3e2c-4aac-ae8f-e16d3340da76", "id": "7fb3956e-9bd2-4fa5-8659-72b266cdb45b", "dt": "2022-05-12T10:05:35Z", "domain": "es.wikipedia.org", "stream": "mediawiki.recentchange", "topic": "eqiad.mediawiki.recentchange", "partition": 0, "offset": 3855779718}, "id": 266270269, "type": "edit", "namespace": 0, "title": "Campo de la calle Industria", "comment": "/* Historia */", "timestamp": 1652349935, "user": "Raimon will", "bot": false, "minor": false, "length": {"old": 7566, "new": 7566}, "revision": {"old": 143485393, "new": 143485422}, "server_url": "https://es.wikipedia.org", "server_name": "es.wikipedia.org", "server_script_path": "/w", "wiki": "eswiki", "parsedcomment": "<span dir=\"auto\"><span class=\"autocomment\"><a href=\"/wiki/Campo_de_la_calle_Industria#Historia\" title=\"Campo de la calle Industria\">→‎Historia</a></span></span>"}
^CProcessed a total of 269 messages
```

## Configure Pinot

Now let's configure Pinot to consume the data from Kafka.

We'll have the following schema:

```json
{
    "schemaName": "wikipedia",
    "dimensionFieldSpecs": [
      {
        "name": "id",
        "dataType": "STRING"
      },
      {
        "name": "wiki",
        "dataType": "STRING"
      },
      {
        "name": "user",
        "dataType": "STRING"
      },
      {
        "name": "title",
        "dataType": "STRING"
      },
      {
        "name": "comment",
        "dataType": "STRING"
      },
      {
        "name": "stream",
        "dataType": "STRING"
      },
      {
        "name": "domain",
        "dataType": "STRING"
      },
      {
        "name": "topic",
        "dataType": "STRING"
      },
      {
        "name": "type",
        "dataType": "STRING"
      },
      {
        "name": "uri",
        "dataType": "STRING"
      },
      {
        "name": "bot",
        "dataType": "BOOLEAN"
      },
      {
        "name": "metaJson",
        "dataType": "STRING"
      }
    ],
    "dateTimeFieldSpecs": [
      {
        "name": "ts",
        "dataType": "TIMESTAMP",
        "format": "1:MILLISECONDS:EPOCH",
        "granularity": "1:MILLISECONDS"
      }
    ]
  }
```

_schema.json_

And the following table config:

```json
{
    "tableName": "wikievents",
    "tableType": "REALTIME",
    "segmentsConfig": {
      "timeColumnName": "ts",
      "schemaName": "wikipedia",
      "replication": "1",
      "replicasPerPartition": "1"
    },

    "tableIndexConfig": {
      "invertedIndexColumns": [],
      "rangeIndexColumns": [],
      "autoGeneratedInvertedIndex": false,
      "createInvertedIndexDuringSegmentGeneration": false,
      "sortedColumn": [],
      "bloomFilterColumns": [],
      "loadMode": "MMAP",
      "streamConfigs": {
        "streamType": "kafka",
        "stream.kafka.topic.name": "wiki_events",
        "stream.kafka.broker.list": "kafka-wiki:9093",
        "stream.kafka.consumer.type": "lowlevel",
        "stream.kafka.consumer.prop.auto.offset.reset": "smallest",
        "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
        "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
        "realtime.segment.flush.threshold.rows": "1000",
        "realtime.segment.flush.threshold.time": "24h",
        "realtime.segment.flush.segment.size": "100M"
      },
    "tenants": {
      "broker": "DefaultTenant",
      "server": "DefaultTenant",
      "tagOverrideConfig": {}
    },
      "noDictionaryColumns": [],
      "onHeapDictionaryColumns": [],
      "varLengthDictionaryColumns": [],
      "enableDefaultStarTree": false,
      "enableDynamicStarTreeCreation": false,
      "aggregateMetrics": false,
      "nullHandlingEnabled": false
    },
    "metadata": {},
    "quota": {},
    "routing": {},
    "query": {},
    "ingestionConfig": {
      "transformConfigs": [
        {
          "columnName": "metaJson",
          "transformFunction": "JSONFORMAT(meta)"
        },
        {
          "columnName": "id",
          "transformFunction": "JSONPATH(metaJson, '$.id')"
        },
        {
          "columnName": "stream",
          "transformFunction": "JSONPATH(metaJson, '$.stream')"
        },
        {
          "columnName": "domain",
          "transformFunction": "JSONPATH(metaJson, '$.domain')"
        },
        {
          "columnName": "topic",
          "transformFunction": "JSONPATH(metaJson, '$.topic')"
        },
        {
          "columnName": "uri",
          "transformFunction": "JSONPATH(metaJson, '$.uri')"
        },
        {
          "columnName": "ts",
          "transformFunction": "\"timestamp\" * 1000"
        }
      ]
    },
    "isDimTable": false
  }
```

_table.json_

The highlighted lines are how we connect Pinot to the Kafka topic that contains the events. Create the schema and table by running the following commnad:

```bash
docker exec -it pinot-controller-wiki bin/pinot-admin.sh AddTable \
  -tableConfigFile /config/table.json \
  -schemaFile /config/schema.json \
  -exec
```

Once you've done that, navigate to the [Pinot UI](http://localhost:9000/#/query?query=select+domain%2C+count%28\*%29+%0Afrom+wikievents+%0Agroup+by+domain%0Aorder+by+count%28\*%29+DESC%0Alimit+10\&tracing=false\&pqlSyntax=false) and run the following query to check that the data has made its way into Pinot:

```sql
select domain, count(*) 
from wikievents 
group by domain
order by count(*) DESC
limit 10
```

As long as you see some records, everything is working as expected.

## Building a Streamlit Dashboard

Now let's write some more queries against Pinot and display the results in Streamlit.

First, install the following libraries:

```bash
pip install streamlit pinotdb plotly pandas
```

Create a file called `app.py` and import libraries and write a header for the page:

```python
import pandas as pd
import streamlit as st
from pinotdb import connect
import plotly.express as px

st.set_page_config(layout="wide")
st.header("Wikipedia Recent Changes")
```

_app.py_

Connect to Pinot and write a query that returns recent changes, along with the users who made the changes, and domains where they were made:

```python
conn = connect(host='localhost', port=8099, path='/query/sql', scheme='http')

query = """select
  count(*) FILTER(WHERE  ts > ago('PT1M')) AS events1Min,
  count(*) FILTER(WHERE  ts <= ago('PT1M') AND ts > ago('PT2M')) AS events1Min2Min,     
  distinctcount(user) FILTER(WHERE  ts > ago('PT1M')) AS users1Min,
  distinctcount(user) FILTER(WHERE  ts <= ago('PT1M') AND ts > ago('PT2M')) AS users1Min2Min,
  distinctcount(domain) FILTER(WHERE  ts > ago('PT1M')) AS domains1Min,
  distinctcount(domain) FILTER(WHERE  ts <= ago('PT1M') AND ts > ago('PT2M')) AS domains1Min2Min
from wikievents 
where ts > ago('PT2M')
limit 1
"""

curs = conn.cursor()

curs.execute(query)
df_summary = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
```

_app.py_

The highlighted part of the query shows how to count the number of events from the last minute and the minute before that. We then do a similar thing to count the number of unique users and domains.

### Metrics

Now let's create some metrics based on that data:

```python
metric1, metric2, metric3 = st.columns(3)
metric1.metric(label="Changes", value=df_summary['events1Min'].values[0],
    delta=float(df_summary['events1Min'].values[0] - df_summary['events1Min2Min'].values[0]))

metric2.metric(label="Users", value=df_summary['users1Min'].values[0],
    delta=float(df_summary['users1Min'].values[0] - df_summary['users1Min2Min'].values[0]))

metric3.metric(label="Domains", value=df_summary['domains1Min'].values[0],
    delta=float(df_summary['domains1Min'].values[0] - df_summary['domains1Min2Min'].values[0]))
```

_app.py_

Go back to the terminal and run the following command:

```bash
streamlit run app.py
```

Navigate to [localhost:8501](http://localhost:8501) to see the Streamlit app. You should see something like the following:

![Streamlit Metrics](https://github.com/pinot-contrib/pinot-docs/blob/latest/img/streamlit-metrics.png) _Streamlit Metrics_

### Changes per minute

Next, let's add a line chart that shows the number of changes being done to Wikimedia per minute. Add the following code to `app.py`:

```python
query = """
select ToDateTime(DATETRUNC('minute', ts), 'yyyy-MM-dd hh:mm:ss') AS dateMin, count(*) AS changes, 
       distinctcount(user) AS users,
       distinctcount(domain) AS domains
from wikievents 
where ts > ago('PT1H')
group by dateMin
order by dateMin desc
LIMIT 30
"""

curs.execute(query)
df_ts = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
df_ts_melt = pd.melt(df_ts, id_vars=['dateMin'], value_vars=['changes', 'users', 'domains'])

fig = px.line(df_ts_melt, x='dateMin', y="value", color='variable', color_discrete_sequence =['blue', 'red', 'green'])
fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40), title="Changes/Users/Domains per minute")
fig.update_yaxes(range=[0, df_ts["changes"].max() * 1.1])
st.plotly_chart(fig, use_container_width=True)
```

_app.py_

Go back to the web browser and you should see something like this:

![Streamlit Time Series](https://github.com/pinot-contrib/pinot-docs/blob/latest/img/streamlit-time-series.png) _Streamlit Time Series_

### Auto Refresh

At the moment we need to refresh our web browser to update the metrics and line chart, but it would be much better if that happened automatically. Let's now add auto refresh functionality.

Add the following code just under the header at the top of `app.py`:

```python
if not "sleep_time" in st.session_state:
    st.session_state.sleep_time = 2

if not "auto_refresh" in st.session_state:
    st.session_state.auto_refresh = True

auto_refresh = st.checkbox('Auto Refresh?', st.session_state.auto_refresh)

if auto_refresh:
    number = st.number_input('Refresh rate in seconds', value=st.session_state.sleep_time)
    st.session_state.sleep_time = number
```

_app.py_

And the following code at the very end:

```python
if auto_refresh:
    time.sleep(number)
    st.experimental_rerun()
```

_app.py_

If we navigate back to our web browser, we'll see the following:

![Streamlit Auto Refresh](https://github.com/pinot-contrib/pinot-docs/blob/latest/img/streamlit-animation.gif) _Streamlit Auto Refresh_

The full script used in this example is shown below:

```python
import pandas as pd
import streamlit as st
from pinotdb import connect
from datetime import datetime
import plotly.express as px
import time

st.set_page_config(layout="wide")

conn = connect(host='localhost', port=8099, path='/query/sql', scheme='http')

st.header("Wikipedia Recent Changes")

now = datetime.now()
dt_string = now.strftime("%d %B %Y %H:%M:%S")
st.write(f"Last update: {dt_string}")

# Use session state to keep track of whether we need to auto refresh the page and the refresh frequency

if not "sleep_time" in st.session_state:
    st.session_state.sleep_time = 2

if not "auto_refresh" in st.session_state:
    st.session_state.auto_refresh = True

auto_refresh = st.checkbox('Auto Refresh?', st.session_state.auto_refresh)

if auto_refresh:
    number = st.number_input('Refresh rate in seconds', value=st.session_state.sleep_time)
    st.session_state.sleep_time = number

# Find changes that happened in the last 1 minute
# Find changes that happened between 1 and 2 minutes ago

query = """
select count(*) FILTER(WHERE  ts > ago('PT1M')) AS events1Min,
        count(*) FILTER(WHERE  ts <= ago('PT1M') AND ts > ago('PT2M')) AS events1Min2Min,
        distinctcount(user) FILTER(WHERE  ts > ago('PT1M')) AS users1Min,
        distinctcount(user) FILTER(WHERE  ts <= ago('PT1M') AND ts > ago('PT2M')) AS users1Min2Min,
        distinctcount(domain) FILTER(WHERE  ts > ago('PT1M')) AS domains1Min,
        distinctcount(domain) FILTER(WHERE  ts <= ago('PT1M') AND ts > ago('PT2M')) AS domains1Min2Min
from wikievents 
where ts > ago('PT2M')
limit 1
"""

curs = conn.cursor()

curs.execute(query)
df_summary = pd.DataFrame(curs, columns=[item[0] for item in curs.description])


metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    label="Changes",
    value=df_summary['events1Min'].values[0],
    delta=float(df_summary['events1Min'].values[0] - df_summary['events1Min2Min'].values[0])
)

metric2.metric(
    label="Users",
    value=df_summary['users1Min'].values[0],
    delta=float(df_summary['users1Min'].values[0] - df_summary['users1Min2Min'].values[0])
)

metric3.metric(
    label="Domains",
    value=df_summary['domains1Min'].values[0],
    delta=float(df_summary['domains1Min'].values[0] - df_summary['domains1Min2Min'].values[0])
)

# Find all the changes by minute in the last hour

query = """
select ToDateTime(DATETRUNC('minute', ts), 'yyyy-MM-dd hh:mm:ss') AS dateMin, count(*) AS changes, 
       distinctcount(user) AS users,
       distinctcount(domain) AS domains
from wikievents 
where ts > ago('PT10M')
group by dateMin
order by dateMin desc
LIMIT 30
"""

curs.execute(query)
df_ts = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
df_ts_melt = pd.melt(df_ts, id_vars=['dateMin'], value_vars=['changes', 'users', 'domains'])

fig = px.line(df_ts_melt, x='dateMin', y="value", color='variable', color_discrete_sequence =['blue', 'red', 'green'])
fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40), title="Changes/Users/Domains per minute")
fig.update_yaxes(range=[0, df_ts["changes"].max() * 1.1])
st.plotly_chart(fig, use_container_width=True)

# Refresh the page
if auto_refresh:
    time.sleep(number)
    st.experimental_rerun()
```

_app.py_

## Summary

In this guide we've learnt how to publish data into Kafka from Wikimedia's event stream, ingest it from there into Pinot, and finally make sense of the data using SQL queries run from Streamlit.
