#!/usr/bin/env python

"""
A program to specify polygon or multipolygon shape and infer ecological
community structure based on species occurrence records.
"""

import pandas as pd
import geopandas
import requests
import matplotlib.pyplot as plt
from loguru import logger
import shapely
from shapely.geometry import Polygon, MultiPolygon

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------


# Not sure what Henry meant to do here, but it works with Polygon(name, poly),
# but doesn't work here. See dev notebook.
class Data:
    """
    Create individual Polygon objects for each row of shape data
    """

    # HL: GeoDataFrames already have a geometry column with Polygon objects, so it might be easier to save the whole thing to a class
    # object and subset them out as needed.  Relatedly, I don't know if you need a separate draw function, unles you want it to do 
    # something more specific than display shapes.
    def __init__(self, gdf):
        self.gdf = gdf
        self.polygons = [
            (name, poly) for name, poly in [
                gdf.iloc[i][["Name", "geometry"]]
                for i in range(len(gdf))]
        ]

    def filter_range(self, name = None, country = None):
        """
        subselect by name or country
        """
        if name:
            fname = self.gdf[self.gdf.Name == name]
            return fname
        elif country:
            fcountry = self.gdf[self.gdf.Country == country]
            return fcountry

    def draw(self, index):
        """
        TODO...
        """
        print(self.polygons[index].name)
        self.polygons[index].polygon


class Polygon:
    """
    Polygon holds shape information for plotting a polygon, and a
    dataframe of points inside that polygon, and ...

    Parameters:
    -----------
    name:
    polygon: geojson polygon format object.
    """
    def __init__(self, name, polygon):
        self.name = name
        self.polygon = polygon

    def get_occurrences_in_polygon(self, taxa=6, tol=0.05):
        """
        query GBIF for occurrence records within polygon and return as JSON
        """

        # GBIF can only handle geometry strings up to about 4000 characters.
        # To get around this, you can use the shapely function simplify(),
        # which approximates a Polygon shape in fewer points. It has a
        # parameter called tolerance that controls how far the "simplified"
        # points can be from the originals. This creates a tradeoff between
        # shape accuracy and string length, so I think it's best to leave the
        # option to the user.

        # Separately, did you want to incorporate a while-loop to get around
        # the API's query limit?
        res = requests.get(
            url="https://api.gbif.org/v1/occurrence/search/",
            params={
                "kingdomKey": taxa,
                "geometry": self.polygon.simplify(tolerance=tol),
                "hasCoordinate": "true",
                "offset": 0,
                "limit": 100,
               }
        )
        return res.json()

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
        newDf = df[['species', 'longitude', 'latitude']]

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

    def convert_shape(self):
        """
        convert shapefile formats (e.g., .shp file to .geojson)
        """
        self.to_file("{self}.geojson", driver='GeoJSON')


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
