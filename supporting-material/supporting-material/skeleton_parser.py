
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        
        # files
        items_file = open('items.dat', 'a')
        bidders_file = open('bidders.dat', 'a')
        sellers_file = open('sellers.dat', 'a')
        bids_file = open('bids.dat', 'a')
        categories_file = open('categories.dat', 'a')
        
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            # item is a dictionary representing the current row
            # items table
            items_file.write(item['ItemID'] + '|') # ItemID, primary key
            items_file.write('\"' + item['Name'].replace('\"', '\"\"') + '\"|') # name of the item
            items_file.write(transformDollar(item['Currently']) + '|') # current highest bid
            try:
                items_file.write(transformDollar(item['Buy_Price']) + '|') # optionally list buy price
            except KeyError:
                items_file.write('-1|')
            items_file.write(transformDollar(item['First_Bid']) + '|') # initial bid
            items_file.write(item['Number_of_Bids'] + '|') # int data type
            items_file.write('\"' + transformDttm(item['Started']).replace('\"', '\"\"') + '\"|')
            items_file.write('\"' + transformDttm(item['Ends']).replace('\"', '\"\"') + '\"|')
            items_file.write('\"' + item['Seller']['UserID'].replace('\"', '\"\"') + '\"|')
            if item['Description'] is not None:
                items_file.write('\"' + str(item['Description'].replace('\"', '\"\"') + '\"\n'))
            else:
                items_file.write('\"NULL\"\n')

            # bidders table
            if item['Number_of_Bids'] != '0': # make sure there are bidders
                current_bids = item['Bids']
                for bid_dict in current_bids:
                    bid = bid_dict['Bid']
                    bidder = bid['Bidder']
                    bidders_file.write('\"' + bidder['UserID'] + '\"|')
                    bidders_file.write(bidder['Rating'] + '|') # double rating
                    try:
                        bidders_file.write('\"' + bidder['Location'].replace('\"', '\"\"') + '\"|')
                    except KeyError:
                        bidders_file.write('\"NULL\"|')
                    try:
                        bidders_file.write('\"' + bidder['Country'] + '\"\n')
                    except KeyError:
                        bidders_file.write('\"NULL\"\n')
            
            # sellers table
            # every item must have a seller, so no need to check
            sellers_file.write('\"' + item['Seller']['UserID'] + '\"|')
            sellers_file.write(item['Seller']['Rating'] + '|')
            sellers_file.write('\"' + item['Location'].replace('\"', '\"\"') + '\"|')
            sellers_file.write('\"' + item['Country'] + '\"\n')
            
            # bids table
            if item['Number_of_Bids'] != '0': # make sure there are bids
                current_bids = item['Bids']
                for bid_dict in current_bids:
                    bid = bid_dict['Bid']
                    bids_file.write(item['ItemID'] + '|')
                    bids_file.write('\"' + bid['Bidder']['UserID'] + '\"|')
                    bids_file.write(bid['Amount'] + '|') # in combination with ItemID and UserID, this creates a primary key for each bid
                    bids_file.write('\"' + bid['Time'] + '\"\n') 

            # categories table
            # an item's categories each get a row, which together form a tuple as a primary key
            categories = list(set(item['Category']))
            for category in categories:
                categories_file.write(item['ItemID'] + '|')
                categories_file.write('\"' + category + '\"\n')
        
        items_file.close()
        bidders_file.close()
        sellers_file.close()
        bids_file.close()
        categories_file.close()

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
