
import pandas as pd
import geopandas as gpd

# Get a dataframe from our csv voter file.
csv_filepath = "./state_data/straight_party.csv"
df = pd.read_csv(csv_filepath)

# Generate the FIPS codes for each county. Also specify the primitive type of
# the FIPS codes because, for some reason, they're in different formats
# (who stores FIPS codes as *floats*??!?). Follows the standardized format for
# FIPS codes in states, which, for n counties,  is 001, 003, 005, ..., 2n - 1,
# padded by zeroes on the left if necessary.
num_counties = 29
fips_type = float
odds = range(1, num_counties * 2, 2)
codes = [fips_type(odd) for odd in odds]

# Assign county FIPS codes to county and write back to the csv. Also note that,
# in order to properly marry the voting data to the county shapefile, we have to
# create a FIPS code column (or unique identifier column) on the voter file that
# has the same name as the FIPS code column (or unique ID column) on the shapefile.
same_shp_column = "FIPS"
df["FIPS"] = codes
df.to_csv("./state_data/fips_straight_party.csv")

# Read the voting data from the csv (bad programming practice, I know,
# but this is just easier for now).
voting = pd.read_csv("./state_data/fips_straight_party.csv")

# First, get the filepath to the county shapefile. Then, specify the column
# we'll be merging on.
county_filepath = "./Counties/Counties.shp"
merge_column = "FIPS"

# Read in the counties shapefile and merge on the FIPS codes. Assign
# unique IDs, then write back to a shapefile.
counties = gpd.read_file(county_filepath)
counties = counties.merge(voting, on=merge_column)
counties["ID"] = list(range(len(counties)))
counties.to_file("./Counties/merged_county_data.shp")

# Do the same as above, but don't do a merge.
block_filepath = "./tl_2012_49_vtd10/tl_2012_49_vtd10.shp"
vtds = gpd.read_file(block_filepath)
vtds["ID"] = list(range(len(vtds)))
vtds.to_file("./tl_2012_49_vtd10/vtds_assigned_ids.shp")
