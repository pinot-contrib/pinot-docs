---
description: Integrate with Presto for ad-hoc queries with Full SQL
---

# Presto

Start running [Presto Image](https://hub.docker.com/repository/docker/apachepinot/pinot-presto) with pre-built [Presto Pinot connector](https://prestodb.io/docs/current/connector/pinot.html).

{% tabs %}
{% tab title="Docker" %}
Run below command to start a standalone Presto coordinator.

```text
docker run \
  --network pinot-demo \
  --name=presto-coordinator \
  -p 8080:8080 \
  -d apachepinot/pinot-presto:latest
```

Then you can connect to presto with [Presto-Cli](https://prestodb.io/docs/current/installation/cli.html).

```text
if [[ ! -f "/tmp/presto-cli" ]]; then
    curl -L https://repo1.maven.org/maven2/com/facebook/presto/presto-cli/0.228/presto-cli-0.228-executable.jar -o /tmp/presto-cli
    chmod +x /tmp/presto-cli
fi
/tmp/presto-cli --server localhost:8080 --catalog pinot_quickstart --schema default
```

Then write your own queries;

```text
presto:default> show tables;
    Table
--------------
 airlinestats
(1 row)

Query 20200211_185652_00006_w6yfz, FINISHED, 1 node
Splits: 19 total, 19 done (100.00%)
0:00 [1 rows, 29B] [3 rows/s, 99B/s]
```

```text
presto:default> select count(*) as flights_from_ca_to_ny from airlinestats where originstate='CA' and deststate='NY';
 flights_from_ca_to_ny
-----------------------
                    67
(1 row)

Query 20200211_190136_00018_w6yfz, FINISHED, 1 node
Splits: 17 total, 17 done (100.00%)
0:00 [1 rows, 8B] [5 rows/s, 42B/s]
```

```text
presto:default> select * from airlinestats limit 1;
 flightnum | origin | quarter | lateaircraftdelay | divactualelapsedtime | divwheelsons | divwheelsoffs | airtime | arrdel15 | divtotalgtimes | deptimeblk | destcitymarketid | divairportseqids | dayssinceepoch | deptime | month | crselapsedtime | deststatename | carrier |
-----------+--------+---------+-------------------+----------------------+--------------+---------------+---------+----------+----------------+------------+------------------+------------------+----------------+---------+-------+----------------+---------------+---------+
       122 | DFW    |       1 |       -2147483648 |          -2147483648 |              |               |     202 |        0 |                | 0700-0759  |            32457 |                  |          16088 |     715 |     1 |            235 | California    | AA      |
(1 row)

Query 20200211_185719_00007_w6yfz, FINISHED, 1 node
Splits: 17 total, 17 done (100.00%)
0:02 [1 rows, 325B] [0 rows/s, 133B/s]
```

Meanwhile you can access [Presto Cluster UI](http://localhost:8080/ui/) to see query stats.

![Presto Cluster UI](../.gitbook/assets/image%20%2816%29.png)
{% endtab %}
{% endtabs %}

