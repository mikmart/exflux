from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Self

import pandas as pd
from .client import InfluxClientFactory
from .settings import ExportConfig, ExportDestinationConfig, Settings


@dataclass
class Exporter:
    client_factory: InfluxClientFactory

    def export(self, config: ExportConfig) -> None:
        destination = create_export_destination(config.destination)
        self._export(config.source.bucket, config.source.query, destination)

    def _export(self, bucket: str, query: str, destination: ExportDestination) -> None:
        with self.client_factory.create_client(bucket=bucket) as client:
            table, ts = client.query(query), pd.Timestamp.utcnow()
            destination.send(table.to_pandas(), ts)

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        return cls(InfluxClientFactory(settings.cluster_url, settings.api_token))


class ExportDestination(Protocol):
    def send(self, df: pd.DataFrame, timestamp: pd.Timestamp) -> None:
        ...


def create_export_destination(config: ExportDestinationConfig) -> ExportDestination:
    # TODO: Maybe a class and dynamically register export destinations like plugins?
    match config.kind:
        case "csv":
            return CsvExportDestination(config.name)
        case kind:
            raise TypeError(f"Unsupported export destination kind: {kind}")


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
