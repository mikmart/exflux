import argparse
import time

from .settings import Settings, create_export_destination, create_exporter


def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--settings-file", metavar="PATH", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    log(f"Reading export settings from {args.settings_file}...")
    settings = Settings.load(args.settings_file)
    exporter = create_exporter(settings.database)
    for export in settings.exports:
        log(f"Exporting from {export.source.bucket} to {export.destination.name}...")
        destination = create_export_destination(export.destination)
        exporter.export(export.source.bucket, export.source.query, destination)


if __name__ == "__main__":
    main()
