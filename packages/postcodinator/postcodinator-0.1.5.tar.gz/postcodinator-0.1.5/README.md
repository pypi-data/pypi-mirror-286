# Postcodinator
Postcodinator is a Python package designed to return information on UK post codes. It provides functionalities to easily access and query post code data.

## Features
- Load and query post code data from a Parquet file.
- Simple and easy-to-use interface.
- Fast lookup of post code information.

## Installation

You can install the package from PyPI using `pip`:

```bash
pip install postcodinator
```

## Usage
Here is an example of how to use Postcodinator:
```
from postcodinator import Postcodinator

# Initialize the locator
locator = Postcodinator()

# Example: Get the latitude for a given post code
latitude = locator.get_latitude('EC1A 1BB')
print(f'Latitude: {latitude}')

# Example: Get the longitude for a given post code
longitude = locator.get_longitude('EC1A 1BB')
print(f'Longitude: {longitude}')

# Example: Get the easting for a given post code
easting = locator.get_easting('EC1A 1BB')
print(f'Easting: {easting}')

# Example: Get the northing for a given post code
northing = locator.get_northing('EC1A 1BB')
print(f'Northing: {northing}')

# Example: Get the status for a given post code
status = locator.get_status('EC1A 1BB')
print(f'Status: {status}')

# Example: Get the user type for a given post code
usertype = locator.get_usertype('EC1A 1BB')
print(f'User Type: {usertype}')

# Example: Get the positional quality indicator for a given post code
positional_quality_indicator = locator.get_positional_quality_indicator('EC1A 1BB')
print(f'Positional Quality Indicator: {positional_quality_indicator}')

# Example: Get the country for a given post code
country = locator.get_country('EC1A 1BB')
print(f'Country: {country}')

# Example: Get the fixed width seven character post code for a given post code
postcode_fixed_width_seven = locator.get_postcode_fixed_width_seven('EC1A 1BB')
print(f'Post code Fixed Width Seven: {postcode_fixed_width_seven}')

# Example: Get the fixed width eight character post code for a given post code
postcode_fixed_width_eight = locator.get_postcode_fixed_width_eight('EC1A 1BB')
print(f'Post code Fixed Width Eight: {postcode_fixed_width_eight}')

# Example: Get the post code area for a given post code
postcode_area = locator.get_postcode_area('EC1A 1BB')
print(f'Post code Area: {postcode_area}')

# Example: Get the post code district for a given post code
postcode_district = locator.get_postcode_district('EC1A 1BB')
print(f'Post code District: {postcode_district}')

# Example: Get the post code sector for a given post code
postcode_sector = locator.get_postcode_sector('EC1A 1BB')
print(f'Post code Sector: {postcode_sector}')

# Example: Get the outcode for a given post code
outcode = locator.get_outcode('EC1A 1BB')
print(f'Outcode: {outcode}')

# Example: Get the incode for a given post code
incode = locator.get_incode('EC1A 1BB')
print(f'Incode: {incode}')

# Example: Find the nearest post code for given latitude and longitude
latitude = 51.5074  # Example: Latitude for London
longitude = -0.1278  # Example: Longitude for London
nearest_postcode, distance = locator.find_nearest_postcode(latitude, longitude)
print(f'Nearest post code: {nearest_postcode}')
print(f'Distance: {distance} meters')
```

## License
This project is licensed under the MIT License.

## Author
Stephen Bourne

### Additional Information
If you have any questions, feel free to reach out at hello@stephenbourne.dev
