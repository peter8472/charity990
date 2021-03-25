import argparse
import pdb
import sys
import csv
import sqlite3
import os
import glob
import re
import urllib.request
import datetime
import time
import csvsqlite3

from xml.dom import minidom

home = os.getenv("USERPROFILE")
dldir = os.path.join(home,"Downloads")
s3url = "https://s3.amazonaws.com/irs-form-990/"
file2019 = glob.glob(os.path.join(dldir,"irs charity 990", "index_2019.csv"))[0]
file2018 = glob.glob(os.path.join(dldir,"irs charity 990", "index_2018.csv"))[0]
file2020 = glob.glob(os.path.join(dldir,"irs charity 990", "index_2020.csv"))[0]
file2020 = glob.glob(os.path.join(dldir,"irs charity 990", "index_2021.csv"))[0]
SHOW = "show"
REBUILD  = "rebuild"


def first_tagval_ifany(dom,tagname):
    'TODO: get rid of dom, make this a class or something'
    'throw exception if length not in 0..1'
    desc = dom.getElementsByTagName(tagname)
    
    if len(desc) > 0:
        for line in desc:
            print(line.firstChild.nodeValue)
        
def save_file(object_id):
    # fname = s3url 
    base= object_id+  "_public.xml"
    fname = s3url + base
    print(fname)
    u = urllib.request.urlopen(fname)
    v = u.read()
    with open(base,'wb') as outfile:
        outfile.write(v)
def get_matching_orgs(orgname,saveorg=None,filename=None,ein=None):
    'gets matching charities, writes their xml files to disk'
    search = re.compile(orgname,re.IGNORECASE)
    
    f = open(filename,"r",encoding="utf-8-sig")
    reader = csv.DictReader(f)
    print("names: {}".format(reader.fieldnames))
    totalfound = 0
    
    for x in reader:
        if x['EIN'] == ein or (ein ==None and search.search(x["TAXPAYER_NAME"])):

            if saveorg != None:
                saveorg(x['OBJECT_ID'])
            print(x["TAXPAYER_NAME"],x['EIN'])
            totalfound +=1
    return totalfound
            
            
def show_data():
    """prints the name, description, and website of all the files
    in the directory that end with a digit, or end in _public.xml
    """

    files = glob.glob("*[0-9]") + glob.glob("*_public.xml")
    for x in files:
        print("=========================")
        infile = open(x, encoding="utf-8-sig")
        dom = minidom.parse(infile)
        name = first_tagval_ifany(dom,"BusinessNameLine1Txt")
        desc = first_tagval_ifany(dom,"ActivityOrMissionDesc")
        website = first_tagval_ifany(dom,"WebsiteAddressTxt")




def rebuild_database(sourcefile, sqliteFilename):
    ''
    start = time.time()
    tbl = csvsqlite3.tablemaker(sqliteFilename)
    tbl.save_to_database(sourcefile)
    print("elapsed: {}".format(time.time() - start))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='enter a search string')
    parser.add_argument('-s', '--save', action="store_const", const=save_file, default=print)
    parser.add_argument('name',  type=str, help='regex of charity  name')
    201812759349300326
    parser.add_argument('-e',  type=str, help='EIN of charity  name')
    parser.add_argument('-d', '--dump', action="store_const", const=SHOW, help="dump all the data in the database")
    parser.add_argument('-r', '--rebuild', action="store_const", const=REBUILD)
    
    args = parser.parse_args()
    print(args)
    if args.dump == SHOW:
        show_data()
        exit()
    elif args.rebuild == REBUILD:
        
        rebuild_database(file2018, "irs.sqlite")
        rebuild_database(file2019, "irs.sqlite")
        rebuild_database(file2020, "irs.sqlite")
        rebuild_database(file2021, "irs.sqlite")

    if 'e' in args:
        ein = args.e
    else:
        ein = None

    get_matching_orgs(args.name,args.save,file2020, ein=ein)
    get_matching_orgs(args.name,args.save,file2021, ein=ein)

    x = input("continue with 2019 records? ")

    if x == 'y':
        get_matching_orgs(args.name,args.save,file2019, ein=ein)
    else:
        exit(0)
    x = input("continue with 2018 records? ")
    if x == 'y':
        get_matching_orgs(args.name,args.save,file2018, ein=ein)