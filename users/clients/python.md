# Python

## Python DB-API and SQLAlchemy dialect for Pinot

Applications can use this python client library to query Apache Pinot.

Pypi Repo: [https://pypi.org/project/pinotdb/](https://pypi.org/project/pinotdb/)

Source Code Repo: [https://github.com/python-pinot-dbapi/pinot-dbapi](https://github.com/python-pinot-dbapi/pinot-dbapi)

### Installation

```
pip install pinotdb
```

Note:

* **pinotdb** version >= **0.3.2** uses the Pinot SQL API (added in Pinot >= 0.3.0) and drops support for PQL API. So this client requires Pinot server version >= **0.3.0** in order to access Pinot.
* **pinotdb** version in **0.2.x** uses the Pinot PQL API, which works with pinot version <= 0.3.0, but may miss some new SQL query features added in newer Pinot version.

### Usage

#### Using the DB API to query Pinot Broker directly:

```
from pinotdb import connect

conn = connect(host='localhost', port=8099, path='/query/sql', scheme='http')
curs = conn.cursor()
curs.execute("""
    SELECT place,
           CAST(REGEXP_EXTRACT(place, '(.*),', 1) AS FLOAT) AS lat,
           CAST(REGEXP_EXTRACT(place, ',(.*)', 1) AS FLOAT) AS lon
      FROM places
     LIMIT 10
""")
for row in curs:
    print(row)
```

#### Using SQLAlchemy:

The db engine connection string is formated like this: `pinot://:?controller=://:/`

```
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *

engine = create_engine('pinot://localhost:8099/query/sql?controller=http://localhost:9000/')  # uses HTTP by default :(
# engine = create_engine('pinot+http://localhost:8099/query/sql?controller=http://localhost:9000/')
# engine = create_engine('pinot+https://localhost:8099/query/sql?controller=http://localhost:9000/')

places = Table('places', MetaData(bind=engine), autoload=True)
print(select([func.count('*')], from_obj=places).scalar())
```

### Examples with Pinot Quickstart

#### Clone the Pinot DB repository

```
git clone git@github.com:python-pinot-dbapi/pinot-dbapi.git
cd pinot-dbapi
```

#### Pinot Batch Quickstart

Run below command to start Pinot Batch Quickstart in docker and expose Pinot controller port 9000 and Pinot broker port 8000.

```
docker run \
  --name pinot-quickstart \
  -p 2123:2123 \
  -p 9000:9000 \
  -p 8000:8000 \
  apachepinot/pinot:latest QuickStart -type batch
```

Once pinot batch quickstart is up, you can run the sample code snippet to query Pinot:

```
python3 examples/pinot-quickstart-batch.py
```

Sample Output:

```
Sending SQL to Pinot: SELECT * FROM baseballStats LIMIT 5
[0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 'NL', 11, 11, 'aardsda01', 'David Allan', 1, 0, 0, 0, 0, 0, 0, 'SFN', 0, 2004]
[2, 45, 0, 0, 0, 0, 0, 0, 0, 0, 'NL', 45, 43, 'aardsda01', 'David Allan', 1, 0, 0, 0, 1, 0, 0, 'CHN', 0, 2006]
[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'AL', 25, 2, 'aardsda01', 'David Allan', 1, 0, 0, 0, 0, 0, 0, 'CHA', 0, 2007]
[1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 'AL', 47, 5, 'aardsda01', 'David Allan', 1, 0, 0, 0, 0, 0, 1, 'BOS', 0, 2008]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'AL', 73, 3, 'aardsda01', 'David Allan', 1, 0, 0, 0, 0, 0, 0, 'SEA', 0, 2009]

Sending SQL to Pinot: SELECT playerName, sum(runs) FROM baseballStats WHERE yearID>=2000 GROUP BY playerName LIMIT 5
['Scott Michael', 26.0]
['Justin Morgan', 0.0]
['Jason Andre', 0.0]
['Jeffrey Ellis', 0.0]
['Maximiliano R.', 16.0]

Sending SQL to Pinot: SELECT playerName,sum(runs) AS sum_runs FROM baseballStats WHERE yearID>=2000 GROUP BY playerName ORDER BY sum_runs DESC LIMIT 5
['Adrian', 1820.0]
['Jose Antonio', 1692.0]
['Rafael', 1565.0]
['Brian Michael', 1500.0]
['Alexander Emmanuel', 1426.0]
```

Using parameters:

```
from pinotdb import connect

conn = connect(host='localhost', port=8000, path='/query/sql', scheme='http')
curs = conn.cursor()

curs.execute("""
    SELECT * 
    FROM baseballStats
    WHERE league IN (%(leagues)s)
    """, {"leagues": ["AA", "NL"]})
for row in curs:
    print(row)
    
curs.execute("""
    SELECT *
    FROM baseballStats
    WHERE baseOnBalls > (%(score)d)
    """, {"score": 0})
for row in curs:
    print(row)
```

####

#### Pinot Hybrid Quickstart

Run the command below to start Pinot Hybrid Quickstart in docker and expose Pinot controller port 9000 and Pinot broker port 8000.

```
docker run \
  --name pinot-quickstart \
  -p 2123:2123 \
  -p 9000:9000 \
  -p 8000:8000 \
  apachepinot/pinot:latest QuickStart -type hybrid
```

Below is an example to query against Pinot Quickstart Hybrid:

```
python3 examples/pinot-quickstart-hybrid.py
```

```
Sending SQL to Pinot: SELECT * FROM airlineStats LIMIT 5
[171, 153, 19393, 0, 8, 8, 1433, '1400-1459', 0, 1425, 1240, 165, 'null', 0, 'WN', -2147483648, 1, 27, 17540, 0, 2, 2, 1242, '1200-1259', 0, 'MDW', 13232, 1323202, 30977, 'Chicago, IL', 'IL', 17, 'Illinois', 41, 861, 4, -2147483648, [-2147483648], 0, [-2147483648], ['null'], -2147483648, -2147483648, [-2147483648], -2147483648, ['null'], [-2147483648], [-2147483648], [-2147483648], 0, -2147483648, '2014-01-27', 402, 1, -2147483648, -2147483648, 1, -2147483648, 'BOS', 10721, 1072102, 30721, 'Boston, MA', 'MA', 25, 'Massachusetts', 13, 1, ['null'], -2147483648, 'N556WN', 6, 12, -2147483648, 'WN', -2147483648, 1254, 1427, 2014]
[183, 141, 20398, 1, 17, 17, 1302, '1200-1259', 1, 1245, 1005, 160, 'null', 0, 'MQ', 0, 1, 27, 17540, 0, -6, 0, 959, '1000-1059', -1, 'CMH', 11066, 1106603, 31066, 'Columbus, OH', 'OH', 39, 'Ohio', 44, 990, 4, -2147483648, [-2147483648], 0, [-2147483648], ['null'], -2147483648, -2147483648, [-2147483648], -2147483648, ['null'], [-2147483648], [-2147483648], [-2147483648], 0, -2147483648, '2014-01-27', 3574, 1, 0, -2147483648, 1, 17, 'MIA', 13303, 1330303, 32467, 'Miami, FL', 'FL', 12, 'Florida', 33, 1, ['null'], 0, 'N605MQ', 13, 29, -2147483648, 'MQ', 0, 1028, 1249, 2014]
[-2147483648, -2147483648, 20304, -2147483648, -2147483648, -2147483648, -2147483648, '2100-2159', -2147483648, 2131, 2005, 146, 'null', 0, 'OO', -2147483648, 1, 27, 17541, 1, 52, 52, 2057, '2000-2059', 3, 'COS', 11109, 1110902, 30189, 'Colorado Springs, CO', 'CO', 8, 'Colorado', 82, 809, 4, -2147483648, [11292], 1, [1129202], ['DEN'], -2147483648, 73, [9], 0, ['null'], [9], [-2147483648], [2304], 1, -2147483648, '2014-01-27', 5554, 1, -2147483648, -2147483648, 1, -2147483648, 'IAH', 12266, 1226603, 31453, 'Houston, TX', 'TX', 48, 'Texas', 74, 1, ['SEA', 'PSC', 'PHX', 'MSY', 'ATL', 'TYS', 'DEN', 'CHS', 'PDX', 'LAX', 'EWR', 'SFO', 'PIT', 'RDU', 'RAP', 'LSE', 'SAN', 'SBN', 'IAH', 'OAK', 'BRO', 'JFK', 'SAT', 'ORD', 'ACY', 'DFW', 'BWI'], -2147483648, 'N795SK', -2147483648, 19, -2147483648, 'OO', -2147483648, 2116, -2147483648, 2014]
[153, 125, 20436, 1, 41, 41, 1442, '1400-1459', 2, 1401, 1035, 146, 'null', 0, 'F9', 2, 1, 27, 17541, 1, 34, 34, 1109, '1000-1059', 2, 'DEN', 11292, 1129202, 30325, 'Denver, CO', 'CO', 8, 'Colorado', 82, 967, 4, -2147483648, [-2147483648], 0, [-2147483648], ['null'], -2147483648, -2147483648, [-2147483648], -2147483648, ['null'], [-2147483648], [-2147483648], [-2147483648], 0, -2147483648, '2014-01-27', 658, 1, 8, -2147483648, 1, 31, 'SFO', 14771, 1477101, 32457, 'San Francisco, CA', 'CA', 6, 'California', 91, 1, ['null'], 0, 'N923FR', 11, 17, -2147483648, 'F9', 0, 1126, 1431, 2014]
[-2147483648, -2147483648, 20304, -2147483648, -2147483648, -2147483648, -2147483648, '1400-1459', -2147483648, 1432, 1314, 78, 'B', 1, 'OO', -2147483648, 1, 27, 17541, -2147483648, -2147483648, -2147483648, -2147483648, '1300-1359', -2147483648, 'EAU', 11471, 1147103, 31471, 'Eau Claire, WI', 'WI', 55, 'Wisconsin', 45, 268, 2, -2147483648, [-2147483648], 0, [-2147483648], ['null'], -2147483648, -2147483648, [-2147483648], -2147483648, ['null'], [-2147483648], [-2147483648], [-2147483648], 0, -2147483648, '2014-01-27', 5455, 1, -2147483648, -2147483648, 1, -2147483648, 'ORD', 13930, 1393003, 30977, 'Chicago, IL', 'IL', 17, 'Illinois', 41, 1, ['null'], -2147483648, 'N903SW', -2147483648, -2147483648, -2147483648, 'OO', -2147483648, -2147483648, -2147483648, 2014]

Sending SQL to Pinot: SELECT count(*) FROM airlineStats LIMIT 5
[17772]

Sending SQL to Pinot: SELECT AirlineID, sum(Cancelled) FROM airlineStats WHERE Year > 2010 GROUP BY AirlineID LIMIT 5
[20409, 40.0]
[19930, 16.0]
[19805, 60.0]
[19790, 115.0]
[20366, 172.0]

Sending SQL to Pinot: select OriginCityName, max(Flights) from airlineStats group by OriginCityName ORDER BY max(Flights) DESC LIMIT 5
['Casper, WY', 1.0]
['Deadhorse, AK', 1.0]
['Austin, TX', 1.0]
['Chicago, IL', 1.0]
['Monterey, CA', 1.0]

Sending SQL to Pinot: SELECT OriginCityName, sum(Cancelled) AS sum_cancelled FROM airlineStats WHERE Year>2010 GROUP BY OriginCityName ORDER BY sum_cancelled DESC LIMIT 5
['Chicago, IL', 178.0]
['Atlanta, GA', 111.0]
['New York, NY', 65.0]
['Houston, TX', 62.0]
['Denver, CO', 49.0]

Sending Count(*) SQL to Pinot
17773

Sending SQL: "SELECT OriginCityName, sum(Cancelled) AS sum_cancelled FROM "airlineStats" WHERE Year>2010 GROUP BY OriginCityName ORDER BY sum_cancelled DESC LIMIT 5" to Pinot
[('Chicago, IL', 178.0), ('Atlanta, GA', 111.0), ('New York, NY', 65.0), ('Houston, TX', 62.0), ('Denver, CO', 49.0)]
```

