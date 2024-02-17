from exporter import Exporter
from settings import Settings


def main():
    settings = Settings.load("settings.yaml")
    exporter = Exporter.from_settings(settings)
    for export_config in settings.exports:
        exporter.export(export_config)


if __name__ == "__main__":
    main()
