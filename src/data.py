#!/usr/bin/env python

"""
Load in polygona data and download occurrence records within a specific polygon
from GBIF and save as version to be used with capcomm.
"""
import geopandas


def load(file):
    """
    load in GMBA shapefiles for mountain polygons
    """
    if file == 'large':
        # "large-scale set" of mountain polygons (17 polygons)
        large = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_\
            supplementary_large-scale-set/GMBA mountain inventory_V1.2\
            -LargeScale.shp")

    elif file == 'world':
        # Mountain polygons for "entire_world" (1,048 polygons)
        world = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_\
            entire_world/GMBA Mountain Inventory_v1.2-World.shp")

    elif file == 'africa':
        africa = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_\
            mega-region/GMBA Mountain Inventory_v1.2-Africa.shp")

    elif file == 'asia':
        asia = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_\
            mega-region/GMBA Mountain Inventory_v1.2-Asia.shp")

    elif file == 'australia':
        australia = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_\
            mega-region/GMBA Mountain Inventory_v1.2-Australia.shp")

    elif file == 'europe':
        europe = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_\
            mega-region/GMBA Mountain Inventory_v1.2-Europe.shp")

    elif file == 'greenland':
        greenland = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_\
            mega-region/GMBA Mountain Inventory_v1.2-Greenland.shp")

    elif file == 'n_america':
        n_america = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_\
            mega-region/GMBA Mountain Inventory_v1.2-NorthAmerica.shp")

    elif file == 'oceania':
        oceania = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_\
            mega-region/GMBA Mountain Inventory_v1.2-Oceania.shp")

    elif file == 's_america':
        s_america = geopandas.read_file("../data/GMBA_mountain_inventory_V1.2_\
            mega-region/GMBA Mountain Inventory_v1.2-SouthAmerica.shp")

    return file

# def download
