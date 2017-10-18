import numpy as np;
import pandas as pd;
from random import randint
import sys
from odo import odo
import json

# Imports for Mongo Database
from pymongo import MongoClient

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
    print(collectionName + " collection deleted")
def is_Collection_Exits(collectionName):
    client = MongoClient()
    db = client['psl_t20']
    if collectionName in db.collection_names():
        return True;
    return False;
def insertData(dbName,collectionName,data):
    print("Inserting data to Database")
    client = MongoClient()
    db = client[dbName]
    mycollection = db[collectionName]
#     print(mycollection)
    odo(data, mycollection)
def delete_DB(name):
    client = MongoClient()
    client.drop_database(name)
def insert_specific_record(collectionName, category):
    df = pd.DataFrame(category)
    client = MongoClient()
    db = client['psl_t20']
    mycollection = db[collectionName]
    
    odo(df, mycollection)
#     print(collectionName + " collection deleted")

def reset_Categories(categoryName,category, category_list):
    # Now add the player in relevant category
    category = loadingData('psl_t20', categoryName)
    category = category.append(category_list)
    category.reset_index(drop=True, inplace=True)
    category = category.drop('_id', 1)
    category = category.groupby('Player Type').apply(pd.DataFrame.sort_values,'Overall_rating',ascending=[False])
    delete_collection_from_db(categoryName)
    insertData('psl_t20', categoryName, category)
    print('Successfully merged Data in ',categoryName, ' category')


def deleteOwnerTeam(ownerteam):
    platinum_list = []
    diamond_list = []
    gold_list = []
    silver_list = []
    emerging_list = []
    supplementory_list = []
    
    # """ Get Team based on owner name"""
    team = loadingData('psl_t20', ownerteam)
    
    # Load Dataset
    platinum = loadingData('psl_t20', 'Platinum')
    diamond = loadingData('psl_t20', 'Diamond')
    gold = loadingData('psl_t20', 'Gold')
    silver = loadingData('psl_t20', 'Silver')
    emerging = loadingData('psl_t20', 'Emerging')
    
    for index, player in team.iterrows():
        if player['Category'] == 'Platinum':
            platinum_list.append(team.loc[index])
        elif player['Category'] == 'Diamond':
            diamond_list.append(team.loc[index])
        elif player['Category'] == 'Gold':
            gold_list.append(team.loc[index])
        elif player['Category'] == 'Silver':
            silver_list.append(team.loc[index])
        elif player['Category'] == 'Emerging':
            emerging_list.append(team.loc[index])
        elif player['Category'] == 'Supplementory':
            supplementory_list.append(team.loc[index])
    
    # Now add the player in relevant category
    if len(platinum_list) > 0:
        platinum = reset_Categories('Platinum', platinum, platinum_list)
    if len(diamond_list) > 0:
        diamond = reset_Categories('Diamond', diamond, diamond_list)
    if len(gold_list) > 0:
        gold = reset_Categories('Gold', gold, gold_list)
    if len(silver_list) > 0:
        silver = reset_Categories('Silver', silver, silver_list)
    if len(emerging_list) > 0:
        emerging = reset_Categories('Emerging', emerging, emerging_list)
    if len(supplementory_list) > 0:
        supplementory = reset_Categories('Diamond', diamond, supplementory_list)
        
    # Delete best 20 and best 11
    delete_collection_from_db(ownerteam)
    delete_collection_from_db(ownerteam+'_best_11')
    print('Successfully Deleted')
    
    return team

team = deleteOwnerTeam(sys.argv[1])