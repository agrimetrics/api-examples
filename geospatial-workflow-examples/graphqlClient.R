source("utils.R")

installPackages(c('ghql', 'logging'))

library(ghql)

logR <- logging::getLogger('graphqlClient')

getConnection <- function(apiKey) {

  connection <- GraphqlClient$new(
      url = "https://api.agrimetrics.co.uk/graphql",
      headers <- c(
        "Accept" = "application/json",
        "Ocp-Apim-Subscription-Key" = apiKey,
        "Content-Type" = "application/json",
        "Accept-Encoding" = "gzip, deflate, br"
      )
    )

  print(paste("Connection acquired:", toString(connection$url)))

  return (connection)
}


getData <- function(con, inputQuery, variables) {
    qry <- ghql::Query$new()
    qry$query(
        "newQuery",
        inputQuery
    )
    result <- con$exec(qry$queries$newQuery, variables)
    return (result)
}


runQuery <- function(con, inputQuery, variables) {
    qry <- ghql::Query$new()
    qry$query(
        "newQuery",
        inputQuery
    )
    result <- con$exec(qry$queries$newQuery, variables)
    return (fromJSON(result, flatten=FALSE))
}
