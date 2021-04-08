#!/usr/bin/env python

"""
Load in polygon data and download occurrence records within a specific polygon
from GBIF and save as version to be used with capcomm.
"""
import pandas as pd
import geopandas
import requests
import matplotlib.pyplot as plt
from pygbif import species
from loguru import logger
import shapely
from shapely.geometry import Polygon, MultiPolygon


def options():
    """
    return list of strings that can be used to load in data
    """
    return ['world', 'large', 'africa', 'asia', 'australia', 'europe',
            'greenland', 'n_america', 'oceania', 's_america']


def load(file):
    """
    load in .geojson files for mountain polygons
    (converted from GMBA shapefiles using `geopandas`;
    https://ilias.unibe.ch/goto_ilias3_unibe_cat_1000515.html)
    """
    if file == 'large':
        # "large-scale set" of mountain polygons (17 polygons)
        data = geopandas.read_file("../data/geojson_files/large.geojson")

    elif file == 'world':  
        # Mountain polygons for "entire_world" (1,048 polygons)
        data = geopandas.read_file("../data/geojson_files/world.geojson")

    elif file == 'africa':
        data = geopandas.read_file("../data/geojson_files/africa.geojson")

    elif file == 'asia':
        data = geopandas.read_file("../data/geojson_files/asia.geojson")

    elif file == 'australia':
        data = geopandas.read_file("../data/geojson_files/australia.geojson")

    elif file == 'europe':
        data = geopandas.read_file("../data/geojson_files/europe.geojson")

    elif file == 'greenland':
        data = geopandas.read_file("../data/geojson_files/greenland.geojson")

    elif file == 'n_america':
        data = geopandas.read_file("../data/geojson_files/n_america.geojson")

    elif file == 'oceania':
        data = geopandas.read_file("../data/geojson_files/oceania.geojson")

    elif file == 's_america':
        data = geopandas.read_file("../data/geojson_files/s_america.geojson")

    return data


def taxon_info(taxon):
    """
    use pygbif.species to get GBIF taxonKey info
    """
    info = species.name_suggest(taxon)
    return info


class Dataset:
    """
    Create individual Region objects for each row of .geojson data
    """
    def __init__(self, gdf):       
        self.gdf = gdf
        self.region = [
            Region(name, poly) for name, poly in [
                gdf.iloc[i][["Name", "geometry"]]
                for i in range(len(gdf))]
        ]

    def filter_name(self, name=None):
        """
        subselect by name
        """
        fname = self.gdf[self.gdf.Name == name]
        return fname

    def filter_country(self, country=None):
        """
        subselect by country
        """
        fcountry = self.gdf[self.gdf.Country == country]
        return fcountry


class Region:
    """
    Region holds shape information for plotting a polygon, and a
    dataframe of points inside that polygon, and ...

    Parameters:
    -----------
    name: user-defined
    polygon: geojson polygon format object.
    """
    def __init__(self, name, polygon):
        self.name = name
        self.polygon = polygon

    def get_occurrences(self, taxonKey, offset=0, limit=20, tol=0):
        """
        Returns a GBIF REST query for occurrence records within self.polygon
        and between offset and offset + limit and return as JSON.

        GBIF can only handle geometry strings up to about 4000 characters.
        To get around this, this function uses the shapely function simplify(),
        which approximates a Polygon shape in fewer points. The tol parameter
        (tolerance) controls how far the "simplified" points can be from the
        originals. This creates a tradeoff between shape accuracy and string
        length, so we leave the option to the user. If your GBIF query returns
        a JSON decode error, increase the 'tol' parameter.
        """

        res = requests.get(
            url="https://api.gbif.org/v1/occurrence/search/",
            params={
                "taxonKey": taxonKey,
                "geometry": self.polygon.simplify(tolerance=tol),
                "hasCoordinate": "true",
                "offset": offset,
                "limit": limit,
               }
        )
        return res.json()

    def get_all_occurrences(self, taxonKey, tol=0):
        """
        Iterate requests over incremental offset positions until
        all records have been fetched. When the last record has
        been fetched the key 'endOfRecords' will be 'true'. Takes
        the API params as a dictionary. Returns result as a list
        of dictionaries.
        """
        # for storing results
        alldata = []

        # continue until we call 'break'
        offset = 0
        while 1:

            # get JSON data for a batch 
            jdata = self.get_occurrences(taxonKey, offset, 300, tol)

            # increment counter by 300 (the max limit)
            offset += 300

            # add this batch of data to the growing list
            alldata.extend(jdata["results"])

            # stop when end of record is reached
            if jdata["endOfRecords"]:
                print(f'Done. Found {len(alldata)} records')
                break

            # print a dot on each rep to show progress
            print('.', end='')

        return alldata

    def convert_json_to_dataframe(self, json):
        """
        json = get_occurrences_in_polygon()
        """

        #convert res.json() to pandas df
        df = pd.json_normalize(json)

        #filter df to include only species, latitude, longitude. 2 possible ways.
        #visit https://stackoverflow.com/questions/11285613/selecting-multiple-columns-in-a-pandas-dataframe
        #for further ways/explanations on how to organize dataframes to your liking!

        #1 - organize by column name
        new_df = df[['species', 'longitude', 'latitude']]

        #2 - organize by column position (the bottom examples include columns 0 & 1)
        #newDf = df.iloc[:, 0:2] or
        #newDf = df.iloc[0, 0:2].copy() To avoid the case where changing df1 also changes df

        return newDf

    def plot_with_mpl(self, df):
        """
        I could not test this code to know if it works or not but it was taken
        from the documentation here which I think would be helpful for you! It
        specifically talks about longitude and latitude. Hopefully this code
        ends up working or helps!
        https://geopandas.org/gallery/create_geopandas_from_pandas.html
        """
        gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))

        #visualize to make sure df is ok
        print(gdf.head())

        #get mountain area
        mtn = geopandas.read_file("Users/liortal/hacks/capcomm/data/GMBA_mountain_inventory_V1.2_entire_world/GMBA_Mountain_Inventory_v1.2-World.shp")

        #restrict to species?
        ax = mtn[mtn.species == 'groenlandica'].plot(color='white', edgecolor='black')

        # We can now plot our GeoDataFrame
        gdf.plot(ax=ax, color='red')
        plt.show()


if __name__ == "__main__":

    # Read in mountain polygons
    world = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_entire_world/GMBA Mountain Inventory_v1.2-World.shp")

    # get example polygon (load with geopandas from ...)
    example_poly = "..."

    # create example Polygon object
    pol = Polygon(name="test", polygon=example_poly)
    print(pol)

    # get json records from
    r = pol.get_occurrences_in_polygon(taxa=6)

    #convert to df and filter
    df = pol.convert_json_to_dataframe(r)

    #plot
    pol.plot_with_mpl(df)
