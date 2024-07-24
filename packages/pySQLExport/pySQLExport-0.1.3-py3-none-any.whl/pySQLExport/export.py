import csv
import json
import pandas as pd
from pandas.errors import ParserError
from pySQLExport.utils import print_colored

class Export:
    def __init__(self, results, outfile,  columns=None):
        self.results = results
        self.outfile = outfile
        self.columns = columns

    def export(self, output_type):
        if output_type == 'csv':
            self.export_csv()
        elif output_type == 'json':
            self.export_json()            
        elif output_type == 'html':
            self.export_html()
        elif output_type == 'xml':
            self.export_xml()
        else:
            raise ValueError(f"Unsupported output type: {output_type}")

    def export_csv(self):
        try:
            df = pd.DataFrame(self.results, columns=self.columns)
            df.to_csv(self.outfile, index=False)
        except Exception as e:
            raise RuntimeError(f"Failed to export to CSV: {e}")
        
    def export_json(self):
        try:
            df = pd.DataFrame(self.results, columns=self.columns)
            df.to_json(self.outfile, orient='records', lines=True)
        except Exception as e:
            raise RuntimeError(f"Failed to export to JSON: {e}")        

    def export_html(self):
        try: 
            df = pd.DataFrame(self.results, columns=self.columns)
            df.to_html(self.outfile, index=False)
        except Exception as e:
            raise RuntimeError(f"Failed to export to HTML: {e}")
    
    def export_xml(self):
        df = pd.DataFrame(self.results, columns=self.columns)
        try:
            df.to_xml(self.outfile, index=False, parser='lxml')
        except ImportError:
            print("lxml not found, falling back to etree parser.")
            df.to_xml(self.outfile, index=False, parser='etree')
        except ParserError as e:
            raise ValueError(f"Failed to export to XML: {e}")