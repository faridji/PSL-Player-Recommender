import requests
from bs4 import BeautifulSoup
import urllib

import pandas as pd

import sys
from odo import odo
from pymongo import MongoClient

# Database Functions
def loadingData(dbName,collectionName):
    client = MongoClient()
    db = client[dbName]
    if collectionName in db.collection_names():
        collection = db[collectionName]
        return pd.DataFrame(list(collection.find()))
    else:
        df_ = pd.DataFrame()
        df_ = df_.fillna(0) # with 0s rather than NaNs
        return df_
def delete_collection_from_db(collectionName):
    client = MongoClient()
    db = client['psl_t20']
    db.drop_collection(collectionName)
def is_Collection_Exits(collectionName):
    client = MongoClient()
    db = client['psl_t20']
    if collectionName in db.collection_names():
        return True;
    return False;
def insertData(dbName,collectionName,data):
    client = MongoClient()
    db = client[dbName]
    mycollection = db[collectionName]
    odo(data, mycollection)
def delete_DB(name):
    client = MongoClient()
    client.drop_database(name)
def insert_specific_record(collectionName, team):
    df = pd.DataFrame(team)
    client = MongoClient()
    db = client['psl_t20']
    mycollection = db[collectionName]
    odo(df, mycollection)

# PSL Squad grabbing section;
def PSL_Team_Squad(url):
    r = urllib.request.urlopen(url).read()
    soap = BeautifulSoup(r,'lxml')
    
    list_of_rows = []
    """ Crawling Team's Squad """
    table = soap.find('table')
    for row in table.find_all('tr'):
        list_of_cells = []
        for cell in row.find_all('td'):
            list_of_cells.append(cell.get_text())
            list_of_cells = [(element.strip()) for element in list_of_cells]

        list_of_rows.append(list_of_cells)

    """ DataFrame """
    dataset = pd.DataFrame(list_of_rows)
    """ Fill all None value with spaces """
    dataset = dataset.fillna(" ")
    """ Change the lables of Dataframe """
    new_header = dataset.iloc[0] #grab the first row for the header
    dataset = dataset[1:] #take the data less the header row
    dataset.columns = new_header #set the header row as the df header
    """ Droping last column from Dataframe """
#     dataset.drop(dataset.columns[len(dataset.columns)-1], axis=1, inplace=True)
#     """ Droping last row from Dataframe """
#     dataset.drop(dataset.index[len(dataset)-1], inplace=True)
#     """ Drop Country  Column """
#     dataset.drop('Country', axis=1, inplace=True)
    
    return dataset



#Function called from NODE.JS SERVER to grab Peshawar Zalmi Team
if sys.argv[1] == 'peshawar_zalmi':
    
    zalmiTeam = PSL_Team_Squad('http://pslt20.com/peshawar-zalmi-squad-for-psl-2017')

    # Insert team record into database
    insertData('psl_t20', sys.argv[1],zalmiTeam);

#Function called from NODE.JS SERVER to grab Queta Gladiator Team
if sys.argv[1] == 'quetta_gladiators':
    
    quettaTeam = PSL_Team_Squad('http://pslt20.com/quetta-gladiators-squad-2017')

    # Insert team record into database
    insertData('psl_t20', sys.argv[1],quettaTeam);

#Function called from NODE.JS SERVER to grab Lahore Qalandars Team
if sys.argv[1] == 'lahore_qalandars':
    
    lahoreTeam = PSL_Team_Squad('http://pslt20.com/lahore-qalandars-squad-2017/')

    # Insert team record into database
    insertData('psl_t20', sys.argv[1],lahoreTeam);

#Function called from NODE.JS SERVER to grab Islamabad United Team
if sys.argv[1] == 'islamabad_united':
    
    islamabadTeam = PSL_Team_Squad('http://pslt20.com/islamabad-united-2017-squad/')

    # Insert team record into database
    insertData('psl_t20', sys.argv[1],islamabadTeam);

#Function called from NODE.JS SERVER to grab Karachi Kings Team
if sys.argv[1] == 'karachi_kings':
    
    karachiTeam = PSL_Team_Squad('http://pslt20.com/karachi-kings-squad-2017/')

    # Insert team record into database
    insertData('psl_t20', sys.argv[1],karachiTeam);

#Function called from NODE.JS SERVER to grab Multan Sultan Team
if sys.argv[1] == 'multan_sultan':
    # Insert team record into database
    insertData('psl_t20', sys.argv[1],pd.DataFrame(data=None));