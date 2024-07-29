from __future__ import annotations

import os
from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self, cast

from omegaconf import OmegaConf

from .client import InfluxClientFactory
from .exporter import CsvExportDestination, ExportDestination, Exporter


class Loadable(ABC):
    @classmethod
    def load(cls, path: str | os.PathLike) -> Self:
        """
        Load structured configuration from a file.
        """
        schema = OmegaConf.structured(cls)
        config = OmegaConf.load(Path(path))
        return cast(cls, OmegaConf.merge(schema, config))


@dataclass
class Settings(Loadable):
    database: DatabaseConfig
    exports: list[ExportConfig] = field(default_factory=list)


@dataclass
class DatabaseConfig:
    cluster_url: str
    api_token: str


@dataclass
class ExportConfig:
    source: ExportSourceConfig
    destination: ExportDestinationConfig


@dataclass
class ExportSourceConfig:
    bucket: str
    query: str


@dataclass
class ExportDestinationConfig:
    kind: str
    name: str


def create_exporter(config: DatabaseConfig) -> Exporter:
    return Exporter(InfluxClientFactory(config.cluster_url, config.api_token))


def create_export_destination(config: ExportDestinationConfig) -> ExportDestination:
    # TODO: Maybe a class and dynamically register export destinations like plugins?
    match config.kind:
        case "csv":
            return CsvExportDestination(config.name)
        case kind:
            raise TypeError(f"Unsupported export destination kind: {kind}")
