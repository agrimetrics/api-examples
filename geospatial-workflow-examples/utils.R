options("Ncpus" = parallel::detectCores())

#' Take a list of packages and attempt to build and install them only if needed
#'
#' @param packages - a list of packages requiring installation
installPackages <- function(packages) {
  # Check for and install any of the specified packages
  if (length(setdiff(packages, rownames(installed.packages()))) > 0) {
    print("Installing packages...")
    install.packages(
        setdiff(
            packages,
            rownames(installed.packages())),
        Ncpus=getOption("Ncpus", 1L),
        INSTALL_opts='--no-lock',
        clean=TRUE
    )
  }
}