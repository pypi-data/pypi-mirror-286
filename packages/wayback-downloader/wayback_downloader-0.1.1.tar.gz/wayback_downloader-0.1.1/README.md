# Wayback Downloader

Wayback Downloader is a command-line tool for downloading archived versions of websites from the Wayback Machine.

## Installation

You can install Wayback Downloader using pip:

```
pip install wayback_downloader
```

## Usage

After installation, you can use Wayback Downloader from the command line:

```
wayback-downloader [URL] [START_DATE] [END_DATE] [-o OUTPUT_DIR] [-v]
```

For example:

```
wayback-downloader http://example.com 20200101 20230101 -o /path/to/output -v
```

This will download archives for example.com from January 1, 2020, to January 1, 2023, save them to the specified output directory, and provide verbose output.

For more information on available options:

```
wayback-downloader --help
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
