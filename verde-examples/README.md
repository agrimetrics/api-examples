# Verde Field Attributes Examples

This repository contains Jupyter notebook examples of obtaining [Verde
Field Attributes
data](https://app.agrimetrics.co.uk/#/catalog/data-sets/fdebcd1d-9324-401d-b229-fbd21483e584)
over our [GraphQL
API](https://developer.agrimetrics.co.uk/docs/services/graphql/operations/status).

The notebooks are
* `walkthrough.ipynb`: An end to end walkthrough for how to request and obtain Verde data.
* `verde-fetch.ipynb`: Creating time series for each of the Verde field attributes for a specific field.
* `lodging.ipynb`: Developing crop lodging predictions: a use-case inspired example.
* `evapotranspiration.ipynb`: Estimating soil water balance: a use-case inspired example.
* `benchmark.ipynb`: Benchmarking field attributes: a use-case inspired example.

Further instructions and pre-requisites are detailed in each notebook.

The notebooks have Python dependencies that need to be pre-installed.
To set up your Python environment, install the dependencies via:

```bash
$ pip install -r requirements.txt
```

Alternatively, you can use `pipenv`:

```bash
$ pipenv install
```
