import argparse

from .settings import Settings, create_export_destination, create_exporter


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--settings-file", metavar="PATH", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    settings = Settings.load(args.settings_file)
    exporter = create_exporter(settings.database)
    for export in settings.exports:
        destination = create_export_destination(export.destination)
        exporter.export(export.source.bucket, export.source.query, destination)


if __name__ == "__main__":
    main()
