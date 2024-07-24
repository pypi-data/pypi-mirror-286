import sys
import getpass
import os
from tabulate import tabulate
from pySQLExport.cli import CLI
from pySQLExport.config import load_config
from pySQLExport.database import Database
from pySQLExport.query import Query
from pySQLExport.export import Export
from pySQLExport.utils import print_colored


class PySQLExport:
    def __init__(self):
        self.cli = CLI()
        self.args = self.cli.parse_args(sys.argv[1:])
        self.interactive = len(sys.argv) == 1
        self.config = {}
        self.password = None
        self.db = None
        self.results = None
        self.query = ''
        self.outfile = None
        self.output = None
        self.columns = None

        if not self.interactive:
            if not self.args.config_file or not self.args.query:
                print_colored("Error: Non-interactive mode requires both --config-file and --query arguments.", "red")
                sys.exit(1)

    def load_config(self):
        if self.interactive:
            self.get_db_info()
        else: 
            if self.args.config_file and os.path.isfile(self.args.config_file):
                try:
                    self.config = load_config(self.args.config_file)
                except Exception as e:
                    print_colored(f"Failed to load config file: {e}", "red")
                    sys.exit(1)
            else:
                print_colored("Config file not found. Please provide the database information.", "yellow")
                self.get_db_info()

            self.query = self.args.query

    def get_db_info(self):
        self.config['host'] = input("Enter database host: ")
        self.config['user'] = input("Enter database user: ")
        self.config['database'] = input("Enter database name: ")
        self.config['port'] = input("Enter database port (default 3306): ")
        self.config['port'] = int(self.config['port']) if  self.config['port'] else 3306


    def get_password(self):
        self.password = getpass.getpass(prompt='Enter database password: ')

    def connect_to_database(self):
        try:
            self.db = Database(
                self.config['host'], self.config['user'],
                self.password, self.config['database'], self.config['port']
            )
        except Exception as e:
            print_colored(f"Failed to connect to the database: {e}", "red")
            sys.exit(1)

    def execute_query(self):
        try:
            query = Query(self.db)
            self.results,  self.columns = query.execute(self.query)
        except Exception as e:
            print_colored(f"Failed to execute query: {e}", "red")
            sys.exit(1)

    def export_results(self):
        if self.args.output:
            if self.args.output not in ['csv', 'json', 'html', 'xml']:
                while True:
                    print_colored("Invalid output type. Current options are csv, json, html, xml.", "red")
                    print_colored("Please enter a supported file type (csv, json, html, xml): ", 'yellow', end='')
                    self.output = input()
                    if self.output in ['csv', 'json', 'html', 'xml']:
                        break
            self.output = self.args.output

            if not self.args.outfile:
                print_colored("Please provide an output file path: ", "yellow", end='')
                self.outfile = input()
            else:
                self.outfile = self.args.outfile

        else:
            while True:
                print_colored("Please enter a supported file type (csv, json, html, xml): ", 'white', end='')
                self.output = input()
                if self.output in ['csv', 'json', 'html', 'xml']:
                    break
                else:
                    print_colored("Invalid output type. Current options are CSV, JSON, html, xml.", "red")
            
            print_colored("Please provide an output file path: ", "white", end='')
            self.outfile = input()
        try:
            exporter = Export(self.results, self.outfile, self.columns)
            exporter.export(self.output)
            print_colored(f"Results have been exported to {self.outfile} ({len(self.results)} rows) ", "green")
        except Exception as e:
            print_colored(f"Failed to export results: {e}", "red")
            sys.exit(1)

    def show_results(self):
        if self.results and self.columns:
            print_colored(tabulate(self.results, headers=self.columns, tablefmt='grid'), 'cyan')


    def get_query_summary(self):
        return f"\nResults: Query on database '{self.config['database']}' returned {len(self.results)} rows."


    def interactive_menu(self):
        first_run = True
        while True:
            if first_run:
                print_colored("\nEnter SQL Query: ", 'white', end='')
                self.query = input()
                self.execute_query()
                print_colored(self.get_query_summary(), 'cyan')
                first_run = False
            else:
                print("\n")
                print_colored("1. Run another query", 'white')
                print_colored("2. Print results of last query", 'white')
                print_colored("3. Export results of last query", 'white')
                print_colored("4. Exit\n", 'white')
                print_colored("Choose an option: ", 'white', end='')
                choice = input().strip()
                print()
                if choice == '1':
                    print_colored("\nEnter SQL Query: ", 'white', end='')
                    self.query = input()
                    self.execute_query()
                    print_colored(self.get_query_summary(), 'cyan')
                elif choice == '2':
                    if self.results:
                        self.show_results()
                    else:
                        print_colored("\n\nNo results to show. Run a query first.\n", "yellow")                
                elif choice == '3':
                    if self.results:
                        self.export_results()
                    else:
                        print_colored("\n\nNo results to export. Run a query first.\n", "yellow")
                elif choice == '4':
                    print_colored("\nExiting...\n", 'red')
                    break            
                else:
                    print_colored("Invalid choice. Please try again.", "red")


    def run(self):
        try:
            self.load_config()
            self.get_password()
            self.connect_to_database()
            if self.interactive:
                self.interactive_menu()
            else:
                self.execute_query()
                if self.args.output:
                    self.export_results()
                else:
                    self.show_results()
        except KeyboardInterrupt:
            print_colored("\nExiting...\n", 'red')
            sys.exit(0)
        except Exception as e:
            print_colored(f"An unexpected error occurred: {e}", "red")
            sys.exit(1)
