import argparse

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="pySQLExport CLI Tool")
        self._add_arguments()

    def _add_arguments(self):
        self.parser.add_argument('--config-file', type=str, required=False, help='Path to the database config file')
        self.parser.add_argument('--query', type=str, required=False, help='SQL query to execute')
        self.parser.add_argument('--output', type=str, choices=['csv'], help='Output format (currently only csv is supported)')
        self.parser.add_argument('--outfile', type=str, help='Output file')

    def parse_args(self, args):
        return self.parser.parse_args(args)