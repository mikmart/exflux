from __future__ import annotations

import os
from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self, cast

from omegaconf import OmegaConf


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
    cluster_url: str
    api_token: str
    exports: list[ExportConfig] = field(default_factory=list)


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
