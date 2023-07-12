from collections import OrderedDict
import pandas as pd

#!/usr/bin/env python
import xml.etree.ElementTree as et
amphibXML = 'file1.xml'
mattsXML = 'file2.xml'

tree=et.parse(amphibXML)
treeRoot = tree.getroot()
list = []
nothing_list = []
indent = 0
database = {}

# Recursively Add the Tags with no text to a second list, while add all tags to a generic list.
def recursiveChildren(root):
    global indent
    #print(' '*indent + '%s: %s' % (root.tag, root.attrib.get('name', root.text)))
    if root.attrib.get('name', root.text) and not root.attrib.get('name', root.text).strip():
        string2 = ' '*indent + root.tag
        nothing_list.append(string2)
    string = ' '*indent + root.tag
    list.append(string)
    indent += 4
    for elem in root:
        recursiveChildren(elem)
    indent -= 4

# Create a Map with Keys of the set (Ex: "Location", "Unit", etc.)
# and Values of Map that has sub-headers and their values (if not null)
# returns a new Map for use (re-usable)
def createMap(unique_set):
    if not unique_set:
        return None
    new_db  = {}
    for header in unique_set:
        #print("Header: " + header.strip())
        itemname = header.strip()
        for item in tree.findall('.//' + itemname):
            # Location(s), Moves, Ammo, Piece, Metadata etc.
            if item.attrib.get('name', item.text) and not item.attrib.get('name', item.text).strip():
                
                if not itemname in new_db.keys():
                    new_db [itemname] = {}

                # elements under Item
                for child in item:
                    #print("Inserting " + item.text.strip())
                    # use name of children as label
                    if child.tag.title() not in new_db[itemname].keys():
                        new_db[itemname][child.tag] = []
                    # only insert if the text isn't empty 
                    # do not use "new_db[itemname][child.tag.title()]" as an if condition!
                    if child.text and child.text.strip():
                        new_db[itemname][child.tag].append(child.text.strip())
    return new_db 

# Add the children of the specific header
# used in combination of bigger subgroups (Ex. Forces, Moves, Unit, etc.)
# currently not under use, can be used to debug createMap's core logic
# warning: May have to go two layers lower rather than one layer for empty headings!
def addAllUnderHeader(headerName):
    temp_map = {}
    for item in tree.findall('.//' + headerName):
        # find all the elements beneath this!
        itemname = item.tag.strip()
        for child in item:
            if child.tag not in temp_map[itemname].keys():
                    temp_map[itemname][child.tag] = []
            if child.text and child.text.strip():
                    temp_map[itemname][child.tag].append(child.text.strip())
    return temp_map

# TESTING ONLY
# Print out various information from database.
def test_database():
    #dataframe = pd.DataFrame({'Database': database})
    #print(dataframe)
    """
    location_data = pd.DataFrame({'Location': database["Location"]})
    print(location_data)

    latitude = database["Location"]["Lat"]
    longitude = database["Location"]["Lon"]

    lat_long = pd.DataFrame({'Lat: ': latitude, "Long: ": longitude })
    print(lat_long)
    """
    moves = pd.DataFrame({'Moves:': database["Moves"]})
    print(moves)

# attempt to print out the entire database db. (Mostly Testing)
def print_database(keyset, db):
    for headers in keyset:
        if headers.strip() in db.keys():
            myframe = pd.DataFrame({headers.strip(): db[headers.strip()]})
            print(myframe)
            print("_"*100)
    pass

# print headers with specifications (add dashes to "empty headers").
def printheader(allHeaders, specialHeaders):
    headerstring = ' '
    for x in allHeaders:
        if x in specialHeaders:
            headerstring += ' -- ' + x + ' -- ' + '\n'
        else:
            headerstring += x + '\n'
    print(headerstring)

# testing, print out each element of specified Set
def printSet(set):
    for x in set:
        print(x)

# MAIN CALLS
# do not use def main(), does not work here!

recursiveChildren(treeRoot)
myset = dict.fromkeys(list)
myset2 = dict.fromkeys(nothing_list)

# testing only to print out the headers
#printheader(myset, myset2)

database = createMap(myset2)
overall_database = createMap(myset)

#test_database()
#print_database(myset2, database)

# this is for printing out ALL the sections 
print_database(myset, overall_database)

