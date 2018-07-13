
import pandas as pd
import geopandas as gpd

# Get a dataframe from our csv voter file.
df = pd.read_csv("./state_data/straight_party.csv")

# Generate the FIPS codes for each county.
odds = range(1, 58, 2)
codes = [float(odd) for odd in odds]

# Assign county FIPS codes to county and write back to the csv.
df["FIPS"] = codes
df.to_csv("./state_data/fips_straight_party.csv")

# Read the voting data from the csv (bad programming practice, I know,
# but this is just easier for now).
voting = pd.read_csv("./state_data/fips_straight_party.csv")

# Read in the counties shapefile and merge on the FIPS codes. Assign
# unique IDs, then write back to a shapefile.
counties = gpd.read_file("./Counties/Counties.shp")
counties = counties.merge(voting, on="FIPS")
counties["ID"] = list(range(len(counties)))
counties.to_file("./Counties/merged_county_data.shp")

# Do the same as above, but don't do a merge.
vtds = gpd.read_file("./tl_2012_49_vtd10/tl_2012_49_vtd10.shp")
vtds["ID"] = list(range(len(vtds)))
vtds.to_file("./tl_2012_49_vtd10/tl_2012_49_vtd10.shp")
