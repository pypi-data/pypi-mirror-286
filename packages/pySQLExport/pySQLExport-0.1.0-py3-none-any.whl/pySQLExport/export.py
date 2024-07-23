import csv
from pySQLExport.utils import print_colored
class Export:
    def __init__(self, results, outfile):
        self.results = results
        self.outfile = outfile

    def export(self, output_type):
        if output_type == 'csv':
            self.export_to_csv()
        else:
            raise ValueError(f"Unsupported output type: {output_type}")

    def export_to_csv(self):
        try:
            with open(self.outfile, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(self.results)
            print_colored(f"Results have been exported to {self.outfile} ({len(self.results)} rows) ", "green")
        except Exception as e:
            raise RuntimeError(f"Failed to export to CSV: {e}")
