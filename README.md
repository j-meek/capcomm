# `capcomm`
**c**oordinate **a**nd **p**olygon **comm**unities

Query species occurrence records (from GBIF) to calculate biodiversity metrics and infer number/type of ecological communities for a geographic polygon of interest. Community inference is based on species abundances, geographic distances between occurrences, and climate data (WorldClim).

### in development

To contribute:
```
conda install numpy pandas requests geopandas -c conda-forge

git clone https://github.com/j-meek/capcomm
cd ./capcomm
pip install -e .
```
