from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd

from .client import InfluxClientFactory


@dataclass
class Exporter:
    client_factory: InfluxClientFactory

    def export(self, bucket: str, query: str, destination: ExportDestination) -> None:
        with self.client_factory.create_client(bucket) as client:
            table, ts = client.query(query), pd.Timestamp.utcnow()
            destination.send(table.to_pandas(), ts)


class ExportDestination(Protocol):
    def send(self, df: pd.DataFrame, timestamp: pd.Timestamp) -> None: ...


@dataclass
class CsvExportDestination(ExportDestination):
    name: str

    def send(self, df: pd.DataFrame, timestamp: pd.Timestamp) -> None:
        df.time = df.time.dt.tz_localize("UTC").map(zuluformat)
        df.to_csv(self._create_filename(timestamp), index=False)

    def _create_filename(self, timestamp: pd.Timestamp) -> str:
        ts = zuluformat(timestamp, timespec="seconds")
        return "{}_{}.csv".format(self.name, ts.replace(":", ""))


def zuluformat(timestamp: pd.Timestamp, **kwargs) -> str:
    """
    Format a timestamp using the "Zulu" timezone specifier for UTC.
    """
    return timestamp.isoformat(**kwargs).replace("+00:00", "Z")
