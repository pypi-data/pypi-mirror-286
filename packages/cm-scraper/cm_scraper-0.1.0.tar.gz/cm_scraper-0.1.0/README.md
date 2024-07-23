# Channel Myanmar Scraper

This is a command-line tool for scraping movie information from Channel Myanmar and saving links to Yoteshin.

## Installation

You can install this package using pip:

```
pip install cm-scraper
```

## Usage

After installation, you can use the scraper from the command line. Here are some usage examples:

1. Scrape a single page:

```
cm-scraper --page 5 --token your_authentication_token_here
```

This will scrape page 5.

2. Scrape a range of pages:

```
cm-scraper --page-range 1 5 --token your_authentication_token_here
```

This will scrape pages 1 through 5.

3. Specify a custom delay between requests:

```
cm-scraper --page-range 1 5 --token your_authentication_token_here --delay 2
```

This will scrape pages 1 through 5 with a 2-second delay between requests.

4. Default behavior (scrape only page 1):

```
cm-scraper --token your_authentication_token_here
```

This will scrape only page 1 with the default 1-second delay.

## Command-line Options

- `--page PAGE`: Scrape a single specified page.
- `--page-range START END`: Specify the range of pages to scrape. For example, `--page-range 10 40` will scrape pages 10 through 40.
- `--token TOKEN`: Your authentication token (required).
- `--delay SECONDS`: Time delay between requests in seconds (default: 1).

Note: You can use either `--page` or `--page-range`, but not both at the same time.

For more information, use the `--help` option:

```
cm-scraper --help
```

## Note

Please use this tool responsibly and in accordance with the terms of service of the websites being scraped.

## License

[MIT License](LICENSE)