#!/usr/bin/env python

"""
Load in polygona data and download occurrence records within a specific polygon
from GBIF and save as version to be used with capcomm.
"""
import geopandas


def options():
    """
    return list of strings that can be used to load in data
    """
    return ['world', 'large', 'africa', 'asia', 'australia', 'europe',
            'greenland', 'n_america', 'oceania', 's_america']


def load(file):
    """
    load in GMBA shapefiles for mountain polygons
    """
    if file == 'large':
        # "large-scale set" of mountain polygons (17 polygons)
        data = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_supplementary_large-scale-set/GMBA mountain inventory_V1.2-LargeScale.shp")

    elif file == 'world':
        # Mountain polygons for "entire_world" (1,048 polygons)
        data = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_entire_world/GMBA Mountain Inventory_v1.2-World.shp")

    elif file == 'africa':
        data = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_mega-region/GMBA Mountain Inventory_v1.2-Africa.shp")

    elif file == 'asia':
        data = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_mega-region/GMBA Mountain Inventory_v1.2-Asia.shp")

    elif file == 'australia':
        data = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_mega-region/GMBA Mountain Inventory_v1.2-Australia.shp")

    elif file == 'europe':
        data = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_mega-region/GMBA Mountain Inventory_v1.2-Europe.shp")

    elif file == 'greenland':
        data = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_mega-region/GMBA Mountain Inventory_v1.2-Greenland.shp")

    elif file == 'n_america':
        data = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_mega-region/GMBA Mountain Inventory_v1.2-NorthAmerica.shp")

    elif file == 'oceania':
        data = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_mega-region/GMBA Mountain Inventory_v1.2-Oceania.shp")

    elif file == 's_america':
        data = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_mega-region/GMBA Mountain Inventory_v1.2-SouthAmerica.shp")

    return data


def download():
    """
    download occurrence records from GBIF
    move gbif download occurrence functions here
    """
