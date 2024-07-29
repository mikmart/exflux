# exflux

_This project is primarly for personal use and currently subject to change without notice._

exflux is a Python package and CLI for exporting data from InfluxDB.

## Installation

``` shell
python -m pipx install git+https://github.com/mikmart/exflux.git
```

## Usage

``` shell
exflux -f settings.yaml
```

Where `settings.yaml`:

``` yaml
database:
  cluster_url: https://eu-central-1-1.aws.cloud2.influxdata.com
  api_token: ${oc.env:INFLUX_TOKEN}

exports:
  - destination:
      kind: csv
      name: telegraf_weather
    source:
      bucket: Telegraf
      query: >
        SELECT *
        FROM "weather"
        WHERE time >= now() - interval '1 day'
        ORDER BY time
```
