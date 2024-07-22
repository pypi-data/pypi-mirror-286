import pandas as pd
import math
import importlib.resources as pkg_resources

class Postcodinator:
    def __init__(self, data_path=None):
        if data_path is None:
            data_path = pkg_resources.files('postcodinator').joinpath('data/postcode_data.parquet')
        # Load the Parquet file into a DataFrame
        self.df = pd.read_parquet(data_path)

    def _normalize_postcode(self, postcode):
        # Normalize the postcode by removing spaces and converting to uppercase
        return postcode.replace(" ", "").upper()

    def get_latitude(self, postcode):
        # Get the latitude for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'latitude']
        return result.values[0] if not result.empty else None

    def get_longitude(self, postcode):
        # Get the longitude for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'longitude']
        return result.values[0] if not result.empty else None

    def get_easting(self, postcode):
        # Get the easting for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'easting']
        return result.values[0] if not result.empty else None

    def get_northing(self, postcode):
        # Get the northing for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'northing']
        return result.values[0] if not result.empty else None

    def get_status(self, postcode):
        # Get the status for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'status']
        return result.values[0] if not result.empty else None

    def get_usertype(self, postcode):
        # Get the user type for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'usertype']
        return result.values[0] if not result.empty else None

    def get_positional_quality_indicator(self, postcode):
        # Get the positional quality indicator for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'positional_quality_indicator']
        return result.values[0] if not result.empty else None

    def get_country(self, postcode):
        # Get the country for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'country']
        return result.values[0] if not result.empty else None

    def get_postcode_fixed_width_seven(self, postcode):
        # Get the fixed width seven character postcode for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'postcode_fixed_width_seven']
        return result.values[0] if not result.empty else None

    def get_postcode_fixed_width_eight(self, postcode):
        # Get the fixed width eight character postcode for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'postcode_fixed_width_eight']
        return result.values[0] if not result.empty else None

    def get_postcode_area(self, postcode):
        # Get the postcode area for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'postcode_area']
        return result.values[0] if not result.empty else None

    def get_postcode_district(self, postcode):
        # Get the postcode district for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'postcode_district']
        return result.values[0] if not result.empty else None

    def get_postcode_sector(self, postcode):
        # Get the postcode sector for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'postcode_sector']
        return result.values[0] if not result.empty else None

    def get_outcode(self, postcode):
        # Get the outcode for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'outcode']
        return result.values[0] if not result.empty else None

    def get_incode(self, postcode):
        # Get the incode for a given postcode
        normalized_postcode = self._normalize_postcode(postcode)
        result = self.df.loc[self.df['postcode_no_space'] == normalized_postcode, 'incode']
        return result.values[0] if not result.empty else None
    
    def find_nearest_postcode(self, latitude, longitude):
        # Calculate distances using the Haversine formula
        self.df['distance'] = self.df.apply(
            lambda row: haversine_distance(latitude, longitude, row['latitude'], row['longitude']), axis=1)
        # Find the nearest postcode
        nearest = self.df.loc[self.df['distance'].idxmin()]
        return nearest['postcode'], nearest['distance'] * 1000  # Convert km to meters

def haversine_distance(lat1, lon1, lat2, lon2):
    # Calculate the Haversine distance between two sets of GPS coordinates
    R = 6371.0  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance
