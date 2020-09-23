# Example geospatial data workflows in R following data query through the Agrimetrics GraphQL API

This directory contains examples of various geospatial data workflows after initially querying the Agrimetrics GraphQL API to obtain geospatial data. It illustratates

1. Saving the outputs to common geospatial file formats such as shapefiles for usage in other software (e.g. ArcGIS/QGIS).
2. Aligning geospatial data from multiple sources to enable their analysis.
3. Working with geospatial and temporal data (e.g. weather time series) together.
4. Analysing the queried geospatial data together in a spatial analysis.
5. Leveraging various helper functions to make the analyses simpler and less prone to coding error.

The examples are executed in the R programming language within Jupyter notebooks. 

## Notebook Tutorials

* [Geospatial_analysis_demo.ipynb](Geospatial_analysis_demo.ipynb]) &mdash; Spatial interpolation of point data using Inverse Distance Weighting (IDW).
* [Rothamsted_static_geospatial_query_demo.ipynb](Rothamsted_static_geospatial_query_demo.ipynb]) &mdash; Retrieving static geospatial data from a Gra
* [Rothamsted_timeseries_geospatial_query_demo.ipynb](Rothamsted_timeseries_geospatial_query_demo.ipynb]) &mdash; Retrieving time series geospatial data from a GraphQL query.

## Jupyter Lab

The Jupyter notebooks can be run locally using [Jupyter lab](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html):
```bash
$ jupyter notebook
```
Then use the Jupyter interface in your browser to navigate to one of the notebooks.

