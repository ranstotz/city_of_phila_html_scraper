# Filename: html_scraper.py
#
# Author: Ryan Anstotz
# Last Revision: 2018-09-27
#
# Description:
#  This Python program is designed to parse the HTML of the City of
#  Philadelphia's Real Estate Lookup Application. All data is then written
#  to a json file in a separate folder. URL and Account No data is taken from
#  an http_data.conf file in the same directory as this file. Please modify
#  variables from there.
#
# =============================================================================

# Import necessary modules
import sys
import os
import configparser
import requests
import signal
import pandas as pd
import collections
import json
import uuid

# Enter main function
def main(argv):

    # Declare output directory file location for json output text files
    output = './out/'
    ext = '.json'

    # set url timeout time
    timeout_time = 10
    
    # Parse config file according to filename
    config_file = 'http_data.conf'
    header = 'DATA'
    url_base = 'URL_BASENAME'
    account = 'ACCOUNT_NO'

    # get necessary variables from config file
    # these are the url basename and specified account number
    url_basename = get_config(config_file, header, url_base) 
    account_no = get_config(config_file, header, account)

    # Combine url_basename and account_no for full url path
    url_path = url_basename + account_no

    # set time limit on call to get url information/page data
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_time)

    # try to open url with the time constraint
    try:
        page = requests.get(url_path)

    except Exception:
        raise Exception("URL call timed out after ", timeout_time,
                        " seconds")
        exit(-1)

    # remove the alarm if the program makes it this far
    signal.alarm(0)

    # store page status if page loads for documentation
    page_status_code = page.status_code

    # this try block tests to see if account exists, raise exception if not
    try:
        # store table data from html using pandas library
        tables = pd.read_html(page.text)
    # raise exception
    except Exception:
        raise Exception("Account", account_no, " does not exist.")
    
    # this creates two panda's Data Frame objects
    temp_customer_data = tables[0]
    temp_real_estate_data = tables[1]

    # get relevant customer and real estate data from parsing function
    customer_data = parse_customer_data(temp_customer_data)
    real_estate_data = parse_real_estate_data(temp_real_estate_data)

    # generate unique filename for each account number search, encode
    # account number at end
    unique_filename = str(uuid.uuid4()) + '_' + account_no + ext

    # write customer data to json
    with open(os.path.join(output, unique_filename), 'a') as f:
        json.dump(customer_data, f, sort_keys=True, indent=4)

    # write balances and other data to same json file
    for element in real_estate_data:
        with open(os.path.join(output, unique_filename), 'a') as f:
            json.dump(element,f, sort_keys=True, indent=4)

    # Return from main function
    return

# =============================================================================
# Functions
# =============================================================================

# function to parse config file
def get_config(config_file_a, header, variable):

    # try to parse the confige file, raise error if not
    try: 
        config = configparser.ConfigParser()
        config.read(config_file_a)

        # Data is stored under "DATA" tag and named according to variables
        # in keys below. Store data to variables.
        data = config[header]
        config_variable = data[variable]

    # raise error if config cannot be parsed
    except:
        print('Error occurred in handline config file in "parse_config" function')
        exit(-1)

    # return the variable string
    return config_variable
    
# function to handle timeouts when getting url data
def timeout_handler(signum, frame):
    raise Exception("Url timed out. ")

# function: get customer data in usable format from table 
# (list of list pairs) pass in panda's Data Frame object, return dict
def parse_customer_data(temp_customer_data_a):

    # convert to dictionary
    temp_customer_data_a = temp_customer_data_a.to_dict()
    # store customer data to a list from the dict
    temp_customer_data_a = temp_customer_data_a[0][0]
    # split by double space, this is due to existing formatting
    temp_customer_data_a = temp_customer_data_a.split('  ')

    # loop over fields and separate data by colon, due to
    # existing formatting
    customer_data_a = []
    for field in temp_customer_data_a:
        if ':' not in field:
            pass
        else:
            customer_data_a.append(field.split(':'))

    # create ordered dict to store data
    cust_dict = collections.OrderedDict()
    for element in customer_data_a:
        cust_dict[element[0]] = element[1]
        
    # return dict of data
    return cust_dict

# function to get real estate table data from table in usable format
# pass in panda's Data Frame object, return list of defaultdicts
def parse_real_estate_data(real_estate_a):

    # set data frame to dictionary
    real_estate_a = real_estate_a.to_dict()

    # open list and iterate through nested dictionary
    # appending new dicts to a list and processing data
    real_estate_list = []
    for i in range(len(real_estate_a)):
        
        d = collections.defaultdict(list)
        # due to formatting, headers are stored this way
        val = real_estate_a[i][0]
        
        for j in range(1, len(real_estate_a[i])-1):
            d[val].append(real_estate_a[i][j])

        real_estate_list.append(d)

    # now get totals since diff format
    d = collections.defaultdict(list)
    val = real_estate_a[0][len(real_estate_a[0])-1]
    # again the above and below is due to the formatting from tables
    for tot in range(1,len(real_estate_a)):
        d[val].append(real_estate_a[tot][len(real_estate_a[0])-1])
    real_estate_list.append(d)

    # return a list of defaultdict objects
    return real_estate_list

# =============================================================================

# Execute program 
if __name__ == "__main__":
    main(sys.argv[:])

# End of file
