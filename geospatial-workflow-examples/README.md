# Example geospatial data workflows in R following data query through the Agrimetrics GraphQL API

This directory contains examples of various geospatial data workflows after initially querying the Agrimetrics GraphQL API to obtain geospatial data. It illustratates

1. Saving the outputs to common geospatial file formats such as shapefiles for usage in other software (e.g. ArcGIS/QGIS).
2. Aligning geospatial data from multiple sources to enable their analysis.
3. Working with geospatial and temporal data (e.g. weather time series) together.
4. Analysing the queried geospatial data together in a spatial analysis.
5. Leveraging various helper functions to make the analyses simpler and less prone to coding error.

The examples are executed in the R programming language within Jupyter notebooks.

## Notebook Tutorials

* [Geospatial_analysis_demo.ipynb](./Geospatial_analysis_demo.ipynb) &mdash; Spatial interpolation of point data using Inverse Distance Weighting (IDW).
* [Rothamsted_static_geospatial_query_demo.ipynb](./Rothamsted_static_geospatial_query_demo.ipynb) &mdash; Retrieving static geospatial data from a Gra
* [Rothamsted_timeseries_geospatial_query_demo.ipynb](./Rothamsted_timeseries_geospatial_query_demo.ipynb) &mdash; Retrieving time series geospatial data from a GraphQL query.

## Jupyter Lab

The Jupyter notebooks can be run locally using [Jupyter lab](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html):
```bash
$ jupyter notebook
```
Then use the Jupyter interface in your browser to navigate to one of the notebooks.

## Docker

For convenience and containerisation purposes, a docker image specification has also been included. Building the image will ensure the environment is sufficient to run the above notebooks.

### Building the docker image

There are no build arguments required to build the image. Use the following to build the image and tag it `agrimetrics/api-examples-jupyter`.

```bash
$ docker build . -t agrimetrics/api-examples-jupyter
```

Note: the docker image contains all of the R libraries installed by the notebooks and therefore should reduce the run time of the notebooks.

### Running the Docker image

Once built, running the image can be done as follows:

```bash
$ docker run -it -e API_KEY=<insert your api key> -p 8888:8888 -v "$PWD":/home/ruser agrimetrics/api-examples-jupyter
```

Make sure you insert your API key appropriately and ensure your current working directory is where your notebooks have been stored.

The output from doing the above should provide you with a link which, when clicked, should take you to your locally hosted Jupyter Lab. See below for an example output:

```bash
ruser@19e6699c7824:~$ jupyter notebook --ip=0.0.0.0 --port=8888
[I 22:50:57.930 NotebookApp] Serving notebooks from local directory: /home/ruser
[I 22:50:57.931 NotebookApp] 0 active kernels
[I 22:50:57.931 NotebookApp] The Jupyter Notebook is running at:
[I 22:50:57.931 NotebookApp] http://0.0.0.0:8888/?token=630a164dd6195414de671b4d1c7ad2c1721e7d2d624db047
[I 22:50:57.931 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 22:50:57.944 NotebookApp] No web browser found: could not locate runnable browser.
[C 22:50:57.945 NotebookApp]

    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://0.0.0.0:8888/?token=630a164dd6195414de671b4d1c7ad2c1721e7d2d624db047
```
