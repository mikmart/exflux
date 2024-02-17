from dataclasses import dataclass, field
from pathlib import Path

import certifi
from influxdb_client_3 import InfluxDBClient3, flight_client_options


def read_root_certificate() -> str:
    """
    A root certificate is required for validating SSL and TLS. The location
    on Windows is not well-known, so needs to be discovered with certifi.
    """
    return Path(certifi.where()).read_text()


@dataclass
class InfluxClientFactory:
    """
    A convenience class to create clients for different buckets in a cluster.
    """

    cluster_url: str
    api_token: str
    certificate: str = field(default_factory=read_root_certificate)

    def create_client(self, bucket: str) -> InfluxDBClient3:
        return InfluxDBClient3(
            host=self.cluster_url,
            database=bucket,
            token=self.api_token,
            flight_client_options=flight_client_options(
                tls_root_certs=self.certificate
            ),
        )
