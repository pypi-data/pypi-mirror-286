# Postcode Locator
Postcode Locator is a Python package designed to locate postcodes using a Parquet file. It provides functionalities to easily access and query postcode data.

## Features
- Load and query postcode data from a Parquet file.
- Simple and easy-to-use interface.
- Fast lookup of postcode information.

## Installation

You can install the package from PyPI using `pip`:

```bash
pip install postcodinator
```

## Usage

Here is an example of how to use the Postcode Locator package:
```
from postcodinator import Postcodinator
```

# Initialize the locator with the path to your Parquet file
```
locator = PostcodeLocator('path/to/your_file.parquet')
```

# Example: Find information about a specific postcode
```
postcode_info = locator.find_postcode('EC1A 1BB')
print(postcode_info)
```

## License
This project is licensed under the MIT License.

## Author
Stephen Bourne

### Additional Information
If you have any questions, feel free to reach out at hello@stephenbourne.dev
