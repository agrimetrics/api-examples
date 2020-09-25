options(stringsAsFactors = FALSE)

source("utils.R")

installPackages(c('logging', 'ghql', 'stringr', 'dplyr', 'jsonlite', 'MASS'))

library(logging)
library(stringr)
library(dplyr)
library(jsonlite)
library(MASS)
require(knitr)

logR <- getLogger('transformData')

source("graphqlClient.R")

apiKey <- Sys.getenv("API_KEY")

monthlyMeasuresToDataFrame <- function(dataFrame) {
  combinedDataFrame <- data.frame()

  for (i in seq_along(dataFrame)) {
    name <- names(dataFrame)[[i]]
    value <- dataFrame[[i]]

    currentMeasure <- as.data.frame(value)
    names(currentMeasure) <- c("dateTime", name)

    if (length(names(combinedDataFrame)) == 0) {
      combinedDataFrame <- currentMeasure
    } else {
      combinedDataFrame <- merge(combinedDataFrame, currentMeasure, by="dateTime", all=TRUE)
    }

  }

  return(combinedDataFrame)
}


#' Convert a geospatialMeasure response to an R dataframe
#'
#' @param response - the response from querying the Agrimetrics GraphQL API
#' @param flatten - (boolean) flatten the resulting dataframe
geospatialMeasuresToDataFrame <- function(response, flatten=FALSE) {
  return (jsonlite::fromJSON(response, flatten=flatten)$data$geospatialMeasures)
}


#' Convert a geospatialMeasure response to an R dataframe
#'
#' @param response - the response from querying the Agrimetrics GraphQL API
#' @param measures - list of measures in the response that are to be added to the dataframe
griddedTemporalMeasuresToDataFrame <- function(response, measures) {
  dataFrame <- geospatialMeasuresToDataFrame(response)

  combinedDataFrame <- data.frame()

  for (measure in measures) {
    currentMeasure <- dataFrame[[measure]]
    measureGridData <- data.frame()

    for (grid in 1:length(currentMeasure$datapoints)) {
      currentGrid <- currentMeasure[grid, ]$datapoints[[1]]
      names(currentGrid) <- c("Date", measure)
      currentGrid$location <- toJSON(unbox(currentMeasure$location[grid, ]))

      measureGridData <- rbind.data.frame(measureGridData, currentGrid)
    }

    if (length(names(combinedDataFrame)) == 0) {
      combinedDataFrame <- measureGridData
    } else {
      combinedDataFrame <- merge(combinedDataFrame, measureGridData, by=c("Date", "location"), all=TRUE)
    }

  }

  return(combinedDataFrame)
}


