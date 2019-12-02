# Philadelphia Real Estate Tax Scraper

## Description:

This script functions as an HTTP API and pulls real estate tax data from:
http://legacy.phila.gov/revenue/realestatetax/

The tax data is scraped from the html of pages associated with BRT numbers
(account numbers). These numbers are specified in the http_data.conf file
in the source directory.

After the necessary data is parsed from the html of the associated account
number, it is saved in a unique json file in the /source/out directory.
There is a sample json file currently in the /source/out directory after
executing the program once.

## Build Instructions:

1.) Pull the Github repository:
    https://github.com/ranstotz/city_of_phila_html_scraper.git
2.) Change the directory to be in the "source" directory.
3.) Enter "make" into the command line to build the Docker
    image (be sure to be in "source" directory).
4.) "make" also places you inside the Docker container with
    all necessary dependencies.
5.) From there, enter "python3 html_scraper.py".
6.) This runs the script and pulls the Account Number from
    the config file (http_data.conf) in the same directory
    as source in the container.
7.) Unique files are written to the "out" directory.
8.) See comments in source files for more details.
9.) Dockerfile is located in "docker_build" directory.
10.) If you would like to change the account number, please modify it in the
    http_data.conf file in the "source" directory.
11.) All output is saved in the /source/out directory in ".json" files.
     A sample file exists the existing repository. Each filename is
     unique and has the account number encoded prior to the extension.

