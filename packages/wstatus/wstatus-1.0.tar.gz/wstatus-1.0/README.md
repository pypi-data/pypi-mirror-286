# wstatus

`wstatus` is a simple and effective tool to check the status of multiple websites. With this tool, you can verify whether websites are active and available, choose between HTTP `GET` or `POST` methods, and save the results to a file for later analysis.

## Installation

To install `web_status_checker`, use `pip`:

    pip install wstatus


## Usage

### Using in Code

You can use `web_status_checker` directly in your Python code. Here’s an example:

    from wstatus import check_websites
    
    urls = [
        "https://www.google.com",
        "https://www.example.com",
        "https://www.nonexistentwebsite.com"
    ]
    
    results = check_websites(urls)
    for result in results:
        print(result)

### Command Line Usage

You can use `wstatus` from the command line to check the status of websites. 

    wstatus [options] <url>

Here are some examples:

#### GET Method (default)

Check the status of websites using the `GET` method:

    wstatus https://www.google.com https://www.example.com

#### POST Method

Check the status of websites using the `POST` method:

    wstatus -p https://www.google.com https://www.example.com

#### Long Option

You can also use the long option for the `POST` method:

    wstatus --post https://www.google.com https://www.example.com

#### Save Results to a File

To save the results to a file, use the `-o` option:

    wstatus -o results.txt https://www.google.com https://www.example.com

#### POST Method and Save to a File

Combine the `POST` method with saving the results to a file:

    wstatus -p -o results.txt https://www.google.com https://www.example.com

## Error Handling

`wstatus` provides detailed error messages to help you diagnose issues with website connectivity. For example:

- If a URL is invalid or cannot be resolved, you will receive an error message indicating the problem.
- Common errors like typos or incorrect URL formats will be flagged with descriptive messages.

### Example Errors

- **Invalid URL Format**: `Invalid URL format: wwww.example.com`
- **Connection Error**: `https://www.nonexistentwebsite.com is down! Error: HTTPSConnectionPool(host='www.nonexistentwebsite.com', port=443): Max retries exceeded with url: / (Caused by NameResolutionError: Failed to resolve 'www.nonexistentwebsite.com')`

## Running Tests

To run the unit tests for the package, use the following command:

    python -m unittest

This will execute all the tests defined in `tests.py` to ensure everything is working correctly.

## Contributing

If you want to contribute to the development of `wstatus`, please follow these steps:

1.  Fork the repository.
2.  Create a branch for your feature or bug fix (`git checkout -b feature/new-feature`).
3.  Make your changes and commit (`git commit -am 'Add new feature'`).
4.  Push the changes to your repository (`git push origin feature/new-feature`).
5.  Create a pull request to the original repository.


...


***Thank you for using `wstatus`!***