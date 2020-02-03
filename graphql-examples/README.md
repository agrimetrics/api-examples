# GraphQL API Examples

This directory contains examples of accessing the Agrimetrics GraphQL
API.

## Notebook Tutorials

* [using_graphql_intro.ipynb](using_graphql_intro.ipynb) &mdash; a basic introduction to making GraphQL queries from Python.
* [geo_search.ipynb](geo_search.ipynb) &mdash; explore the different methods of querying for geospatial objects.
* [using_cursors.ipynb](using_cursors.ipynb) &mdash; how to retrieve large query results in smaller batches.

The Jupyter notebooks can be run locally using [Jupyter lab](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html):
```bash
$ export API_KEY=<insert API key here>
$ jupyter notebook
```
Then use the Jupyter interface in your browser to navigate to one of
the notebooks.

## Simple Example Scripts

* [field_examples.py](field_examples.py) &mdash; simple examples of accessing most of the properties of fields through the GraphQL API, with minimal explanations.
* [graphql_utils.py](graphql_utils.py) &mdash; a library file containing supporting functions for other examples.

The `field_examples.py` example does the following:
* Get the soil information for the area specified by a custom polygon.
* Get the soil information for the area within 3500m of the default point location.
* Get the area, altitude and soil information for a specific field.
* For a given field id, get all the total daily rainfall since the start of the month.
* Get the ids of all fields that lie within a 10000m radius of the default point location.

```bash
$ export API_KEY=<insert API key here>
$ python field_examples.py
```
