#!/usr/bin/env python

"""
A program to specify polygon or multipolygon shape and infer ecological
community structure within based on species occurrence records.
"""

#import numpy as np
#import pandas as pd
import geopandas
import requests

# GBIF with geopandas

# Read in mountain polygons
mountains = geopandas.read_file("./layers/GMBA_mountain_inventory_V1.2_entire_\
                                world/GMBA Mountain Inventory_v1.2-World.shp")


class Polygon:
    """
    Create polygon or upload shapefile
    """
    def __init__(self):
        self.name = name

    def convert_shape(self):
        """
        convert shapefile formats (e.g., .shp file to .geojson)
        """
        self.to_file("{self}.geojson", driver='GeoJSON')

    def getspecies(self, region=0, taxa=6):
        """
        query GBIF for occurrence records within polygon
        """
        res = requests.get(url="https://api.gbif.org/v1/occurrence/search/",
                           params={
                                    "kingdomKey": taxa,
                                    "geometry": self.geometry[region],
                                    "hasCoordinate": "true",
                                    "offset": 0,
                                    "limit": 100,
                                   }
                           )
        print(res.url)
