import argparse

from exporter import Exporter
from settings import Settings


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--settings-file", metavar="PATH", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    settings = Settings.load(args.settings_file)
    exporter = Exporter.from_settings(settings)
    for export_config in settings.exports:
        exporter.export(export_config)


if __name__ == "__main__":
    main()
