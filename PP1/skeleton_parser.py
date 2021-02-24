
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

items_table = [] #First Table
bid_table = []
category_table = []
person_table = []

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
        for item in items:
            # """
            # TODO: traverse the items dictionary to extract information from the
            # given `json_file' and generate the necessary .dat files to generate
            # the SQL tables based on your relation design
            # """
            # Items Table
            item_id = item['ItemID']
            name = item['Name'].replace('"', '""')
            currently = transformDollar(item['Currently'])
            if "Buy_Price" in item:
                buy_price = transformDollar(item['Buy_Price'])  
            else:
                buy_price = 'NULL'
            first_bid = transformDollar(item['First_Bid'])
            number_of_bids = item['Number_of_Bids']
            if item['Location'] is not None:
                Location = item['Location'].replace('"', '""')
            else:
                Location = ""
            started = transformDttm(item['Started'])
            ends = transformDttm(item['Ends'])
            seller_id = item['Seller']['UserID']
            seller_rating = item['Seller']['Rating']
            if item['Description'] is not None:
                description = item['Description'].replace('"', '""')
            else:
                description = ""

            items_table.append('"' + '"|"'.join([item_id, name, currently, buy_price, first_bid, number_of_bids, 
                Location, started, ends, seller_id, seller_rating, description]) + '"\n')

            if item['Bids'] is not None:
                for bid in item['Bids']:
                    user_id = bid['Bid']['Bidder']['UserID']
                    if 'Location' in bid['Bid']['Bidder']:
                        location = bid['Bid']['Bidder']['Location'].replace('"', '""')
                    else:
                        location = "NULL"
                    if 'Country' in bid['Bid']['Bidder']:
                        country = bid['Bid']['Bidder']['Country']
                    else:
                        country = "NULL"
                    rating = bid['Bid']['Bidder']['Rating']
                    time = transformDttm(bid['Bid']['Time'])
                    amount = transformDollar(bid['Bid']['Amount'])

                    bid_table.append('"' + '"|"'.join([item_id, user_id, time, amount]) + '"\n') # Bid Table
                    person_table.append('"' + '"|"'.join([user_id, rating, location, country])  + '"\n') # Person Table

            if item['Seller']['UserID'] not in person_table:
                user_id = item['Seller']['UserID']
                rating = item['Seller']['Rating']
                location = item['Location'].replace('"', '""')
                country = item['Country']
                person_table.append('"' + '"|"'.join([user_id, rating, location, country])  + '"\n')

            # Category Table
            for cat in item['Category']:
                category_table.append('"' + item_id + '"|"' + str(cat) + '"\n')           

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print('Usage: python skeleton_json_parser.py <path to json files>', file=sys.stderr)
        sys.exit(1)

    # initDicts()
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

    with open("Item.dat", "w") as f: 
        f.write("".join(items_table)) 

    with open("Bid.dat", "w") as f: 
        f.write("".join(bid_table))

    with open("Category.dat", "w") as f: 
        f.write("".join(category_table))

    with open("Person.dat", "w") as f: 
        f.write("".join(person_table))

    f.close()


if __name__ == '__main__':
    main(sys.argv)
