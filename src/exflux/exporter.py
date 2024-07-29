from dataclasses import dataclass
from typing import Protocol

import pandas as pd

from .client import InfluxClientFactory


class ExportDestination(Protocol):
    def send(self, df: pd.DataFrame, timestamp: pd.Timestamp) -> None: ...


@dataclass
class Exporter:
    client_factory: InfluxClientFactory

    def export(self, bucket: str, query: str, destination: ExportDestination) -> None:
        # TODO: Feels like this should accept an ExportSource..
        with self.client_factory.create_client(bucket) as client:
            ts = pd.Timestamp.utcnow()
            df = client.query(query).to_pandas()
            assert isinstance(df, pd.DataFrame)
            destination.send(df, ts)


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
