FROM ubuntu:18.04 as base

EXPOSE 8888

WORKDIR /home/ruser

USER root

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install libudunits2-dev
RUN apt-get -y install software-properties-common
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/'
RUN apt update

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London
RUN apt-get install -y tzdata

RUN apt-get -y install libudunits2-dev jupyter r-base libcurl4-openssl-dev libgdal-dev

RUN groupadd -g 1000 app && useradd -r -u 1000 -g app ruser

RUN chown ruser /home/ruser
RUN usermod -a -G staff ruser

ENV HOME=/home/ruser
RUN R -e "install.packages('IRkernel')"
RUN R -e "IRkernel::installspec(user=FALSE)"

FROM base as production
USER ruser

# For your convenience, all the required libraries for each of the included notebooks have been installed here as part of the build.
# Their inclusion in the build reduces the time of running the notebooks. For clarity the full list per notebook have been included, so there will be duplicates.

# packages needed for Geospatial_analysis_demo
RUN R -e "install.packages(c('gstat', 'httr', 'jsonlite', 'lubridate', 'raster', 'rgdal', 'sp','tidyverse'))"

# packages needed for Rothamsted_static_geospatial_query_demo
RUN R -e "install.packages(c('httr', 'jsonlite', 'lubridate', 'rgdal', 'sp', 'tidyverse'))"

# packages needed for Rothamsted_timeseries_geospatial_query_demo
RUN R -e "install.packages(c('ggplot2', 'httr', 'jsonlite', 'lubridate', 'rgdal', 'sf', 'sp', 'tidyverse'))"

# packages needed for Rothamsted_geospatialMeasures_demo_using_utility_functions
RUN R -e "install.packages(c('stringr', 'dplyr', 'jsonlite', 'geojsonsf', 'sf', 'tmap', 'ggplot2', 'ghql', 'logging', 'MASS'))"


CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888"]
