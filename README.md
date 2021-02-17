# project
Outline of `capcom` program

### Description of project goal:
Infer number and type of plant communities for a geographic polygon of interest.

### Description of the code:
From GBIF, pull in all plant occurrence records for a given polygon and circumscribe community types based on species abundances and geographic distances.
`numpy`
`pandas`
`pygbif`
`geopandas`
`PySAL`

### Description of the data:
pandas DataFrame with species, latitude, longitude
matrix of geographic distances between each occurrence record of the same species

### Description of user interaction:
Example: user specifies region of interest using lat, long coordinates
```
# example command line interface
capcom --xmin 128 --xmax 101 --ymin 30 -ymax 50
```