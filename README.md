# geocint-mapaction

This repository contains opensource geodata ETL/CI/CD pipeline developed by [Kontur](https://www.kontur.io/about/) for [MapAction](http://mapaction.org). 
It is based on Kontur Geocint technology.

## What does this pipeline do?

This pipeline downloads data from various sources, including OpenStreetMap, HDX and others, and produces geospatial datasets, in form of geojsons and ESRI shapefiles.

## Installation and configuration

In order to make it running, you need two other repositories:

* https://github.com/mapaction/geocint-runner

For more information on geocint installation and basic configuration please see [Geocint readme](https://github.com/mapaction/geocint-runner/blob/main/README.md) and [Geocint documentation](https://github.com/mapaction/geocint-runner/blob/main/DOCUMENTATION.md).

### geocint-mapaction configuration

1. To generate data for a country there should be a json file with country boundaries in the directory `static_data/countries`.
Currently there are 25 countries from MapAction priority country linst in this directory. 
To add another countries you can copy corresponding json files from `static_data/countries_world` to `static_data/countries`.

## Generating population tabular data from HDX

Because of ununiform naming of population tabular data on HDX it was implemented using `static_data/hdx_admin_pop_urls.json` file.
The script filters values using country code and downloads this layers.

__TO ADD OR UPDATE NEW LAYER__

1. add OR update `static_data/hdx_admin_pop_urls.json`
