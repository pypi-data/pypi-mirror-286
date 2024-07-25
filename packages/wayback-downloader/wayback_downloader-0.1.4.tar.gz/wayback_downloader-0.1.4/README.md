# Wayback Downloader

Wayback Downloader is a powerful and user-friendly command-line tool designed to retrieve and archive historical versions of websites from the Internet Archive's Wayback Machine. This Python-based utility empowers users to effortlessly capture and preserve web content across time, making it an invaluable resource for researchers, developers, and digital archivists.

## Key Features:

1. **Efficient Retrieval**: Quickly download multiple snapshots of a website within a specified date range.
2. **Selective Archiving**: Save only unique content, avoiding duplicate snapshots to conserve storage space.
3. **Recursive Crawling**: Automatically discover and download linked pages within the same domain.
4. **Flexible Date Range**: Specify custom start and end dates for targeted historical content retrieval.
5. **Robust Error Handling**: Implements retry mechanisms and comprehensive error reporting for reliable operation.
6. **User-Friendly CLI**: Simple command-line interface for easy integration into workflows and scripts.
7. **Customizable Output**: Option to specify the output directory for downloaded archives.
8. **Verbose Logging**: Detailed progress and diagnostic information available with verbose mode.

Wayback Downloader simplifies the process of accessing and preserving web history, making it easier than ever to study website evolution, recover lost content, or create comprehensive web archives. Whether you're conducting academic research, performing due diligence, or simply curious about the past state of the web, Wayback Downloader provides a streamlined solution for accessing the vast archives of the Wayback Machine.

Get started with Wayback Downloader today and unlock the power of web history at your fingertips!

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
