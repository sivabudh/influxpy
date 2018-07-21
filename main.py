from influxdb import InfluxDBClient
from functional import seq

host_ipaddress = '192.168.100.205'
client = InfluxDBClient(host=host_ipaddress, port=8086)

client.create_database('pyexample')

db_list = client.get_list_database()
assert seq(db_list).exists(lambda db: db['name'] == 'pyexample')

client.switch_database('pyexample')

json_body = [
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-28T8:01:00Z",
        "fields": {
            "duration": 666
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-29T8:04:00Z",
        "fields": {
            "duration": 777
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-30T8:02:00Z",
        "fields": {
            "duration": 888
        }
    }
]

ok = client.write_points(json_body)
assert ok

results = client.query(
    'SELECT "duration" FROM "pyexample"."autogen"."brushEvents" WHERE time > now() - 180d GROUP BY "user"')
points = results.get_points(tags={'user': 'Carol'})
for point in points:
    print(f"Time {point['time']} and Duration {point['duration']}")


print("Program finishes!")
