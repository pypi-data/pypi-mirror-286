# pySQLExport

A command line tool to interact with multiple databases and export to various formats.

## Installation

You can install the package using pip:

```sh
pip install pySQLExport
```
## Configuration

Before using `pySQLExport`, ensure you have a configuration file or environment variables set up for your database connection.

## Usage

### Command Line Interface

#### Running a Query

To run a query and display the results in the terminal:

```sh
pySQLExport --query "SELECT * FROM employees" --config_file config.yaml
```

#### Exporting Results

To export query results to a CSV file:

```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.yaml --output=csv --outfile results.csv
```

To export query results to a JSON file:

```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.yaml --output=json --outfile results.json
```

### Interactive Mode

If you run `pySQLExport` without arguments, it will start in interactive mode:

```sh
pySQLExport
```

In interactive mode, you can enter the database information, run queries, and choose how to export the results.

### Example

Here’s a complete example of how to use `pySQLExport`:

```sh
pySQLExport --query "SELECT * FROM employees" --config-file config.json --output csv --outfile results.csv
```

1. **Run the command above.**
2. **The results will be exported to a file named `results.csv`.**

### Summary of Commands

- **Run a query and display results**:
  ```sh
  pySQLExport --query "YOUR_QUERY_HERE" --config_file config.json
  ```

- **Export results to CSV**:
  ```sh
  pySQLExport --query "YOUR_QUERY_HERE" --config_file config.json --output csv --outfile results.csv
  ```

- **Export results to JSON**:
  ```sh
  pySQLExport --query "YOUR_QUERY_HERE" --config_file config.json --output json --outfile results.json
  ```

- **Run in interactive mode**:
  ```sh
  pySQLExport
  ```

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.
