#!/usr/bin/env python

"""
A program to specify polygon or multipolygon shape and infer ecological
community structure within based on species occurrence records.
"""

#import numpy as np
#import pandas as pd
# import geopandas
import requests

# GBIF with geopandas

# Read in mountain polygons
# mountains = geopandas.read_file("./layers/GMBA_mountain_inventory_V1.2_entire_\
                                # world/GMBA Mountain Inventory_v1.2-World.shp")

class Mountain:
    def __init__(self, dataframe):
        self.polygons = [
            Polygon(name, poly) for (name, poly) in 
            dataframe[:, ["name", "geometry"]]
        ]

    def drawing(self):
        """
        TODO...
        """




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


    def get_occurrences_in_polygon(self, taxa=6):
        """
        query GBIF for occurrence records within polygon and return
        as JSON
        """
        res = requests.get(
            url="https://api.gbif.org/v1/occurrence/search/",
            params={
                "kingdomKey": taxa,
                "geometry": self.polygon,
                "hasCoordinate": "true",
                "offset": 0,
                "limit": 100,
               }
        )
        print(res.url)
        return res.json()


    def convert_json_to_dataframe(self):
        """
        TODO:
        """

    def plot_with_mpl(self, ):
        """
        TODO: 
        """


    def convert_shape(self):
        """
        convert shapefile formats (e.g., .shp file to .geojson)
        """
        self.to_file("{self}.geojson", driver='GeoJSON')



if __name__ == "__main__":

    # get example polygon (load with geopandas from ...)
    example_poly = "..."

    # create example Polygon object
    pol = Polygon(name="test", polygon=example_poly)
    print(pol)

    # get json records from 
    pol.get_occurrences_in_polygon(taxa=6)
