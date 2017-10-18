import numpy as np;
import pandas as pd;
import sys
from odo import odo
import json

# Genetic Algorithm imports
from random import randint,random,sample
from functools import reduce
from operator import imul,add
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
def insert_specific_record(collectionName, category):
    df = pd.DataFrame(category)
    client = MongoClient()
    db = client['psl_t20']
    mycollection = db[collectionName]
    odo(df, mycollection)
    #print(collectionName + " collection deleted")

def reducing_pickedPlayer_from_list(category_to_eliminate,category):
    #     list_of_players = pd.DataFrame(category)
    #     category_to_eliminate = pd.DataFrame(category_to_eliminate)
    for index_1, category_player in category_to_eliminate.iterrows():
        for index_2, dataset_player in category.iterrows():
            if category_player['Player'] == dataset_player['Player'] :
                category.drop(index_2,inplace=True)
                category.reset_index(drop=True,inplace=True)
    return category


def check_Foreign_local_Count():
    player_count = 1
    player_list = []
    best_20 = loadingData('psl_t20', 'best_20')
    """ Count the Local & Foreign Player """
    df = best_20['Overseas_Local'].value_counts().to_dict()
    
    """ Check Local & Foreign Player Count in First 3 Categories """
    if df['Local'] > 5 or df['Local'] > 5.0:
        list_local = []
        """ Loop for generating Local Player Dataframe"""
        for index, player in best_20.iterrows():
            if player['Overseas_Local'] == 'Local':
                list_local.append(best_20.loc[index])
                local_df = pd.DataFrame(list_local)

        """ Reset index of local player """
        local_df.reset_index(drop=True, inplace=True)
        local_count = len(local_df) 
        """ Generate random number """
        remove_player_list1 = []
        random_number = randint(0, local_count-1)
        remove_player_list1.append(local_df.loc[random_number])
        remove_specific_player_df = pd.DataFrame(remove_player_list1)
        print('Player to removeqqqq ->>>>> ', remove_specific_player_df['Player'])

        """ Delete/Remove this sepecific player from best_20 collection """
        best_20 =  reducing_pickedPlayer_from_list(remove_specific_player_df, best_20)

        """ Now check the category of Droped player """
        if remove_specific_player_df['Category'].any() == 'Platinum':
            print('Platinum category')
            platinum_category = loadingData('psl_t20', 'Platinum')
            platinum_category = platinum_category.sort_values(['Overall_rating'], ascending=[False])

            """ List for recomended top player """
            recommended_player_list = []

            recommended_player_list = recommended_Player_For_Selection(platinum_category)
            recommended_player_list_df = pd.DataFrame(recommended_player_list)
            recommended_player_list_df.reset_index(drop=True, inplace=True)
            print(recommended_player_list_df[['Player', 'Player Type']])
            recommended_player_count = len(recommended_player_list_df)
            print('count- oo --->  ',recommended_player_count)
            for index_1_r, player_1_r in  recommended_player_list_df.iterrows():
                """ Generate random number """
                specific_player_for_selection_list = []
                random_number = randint(0, recommended_player_count-1)
                print('count on----> ',recommended_player_count)
                print('rand ----  ',random_number)
                specific_player_for_selection_list.append(recommended_player_list_df.loc[random_number])
                specific_player_for_selection_df = pd.DataFrame(specific_player_for_selection_list)
                print('specific_player_for_selection_df outside if ---->>>>>  ', specific_player_for_selection_df['Player'])

                """ check the selected player that is Overseas or Local """
                if specific_player_for_selection_df['Overseas_Local'].any() == 'Foreign':
                    if player_count == 1 or player_count == 1.0:
                        selected_player = specific_player_for_selection_df
                        print('selected_player  inside if -<<<<<    ', selected_player['Player'])
                        specific_player_for_selection_df['Category'] = 'Platinum'
                        specific_player_for_selection_list = []
                        specific_player_for_selection_list.append(specific_player_for_selection_df)
                        best_20 = best_20.append(specific_player_for_selection_list, ignore_index=True)
                        """ Reset index of best 20 """
                        best_20.reset_index(drop=True, inplace=True)
                        """ Now add the removed player in platinum category """
                        platinum_category = platinum_category.append(remove_player_list1, ignore_index=True)
                        """ drop the player from platinum which is added to best 20 """
                        platinum_category = reducing_pickedPlayer_from_list(specific_player_for_selection_df, platinum_category)
                        """ Reset index of platinum category """
                        platinum_category.reset_index(drop=True, inplace=True)
                        """ Adding data to Database """
                        print(best_20[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local', 'Category']])
                        print(platinum_category[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local']])
                        delete_collection_from_db('Platinum')
                        insertData('psl_t20', 'Platinum', platinum_category)
                        
                        delete_collection_from_db('best_20')
                        insertData('psl_t20', 'best_20', best_20)
                        print('Successfully inserted')
                        player_count +=1

        if remove_specific_player_df['Category'].any() == 'Gold':
            print('Gold category')
            gold_category = loadingData('psl_t20', 'Gold')
            gold_category = gold_category.sort(['Overall_rating'], ascending=[False])

            """ List for recomended top player """
            recommended_player_list = []

            recommended_player_list = recommended_Player_For_Selection(gold_category)
            recommended_player_list_df = pd.DataFrame(recommended_player_list)
            recommended_player_list_df.reset_index(drop=True, inplace=True)
            print(recommended_player_list_df[['Player', 'Player Type']])
            recommended_player_count = len(recommended_player_list_df)
            print('count- oo --->  ',recommended_player_count)
            for index_1_r, player_1_r in  recommended_player_list_df.iterrows():
                """ Generate random number """
                specific_player_for_selection_list = []
                random_number = randint(0, recommended_player_count-1)
                print('count on----> ',recommended_player_count)
                print('rand ----  ',random_number)
                specific_player_for_selection_list.append(recommended_player_list_df.loc[random_number])
                specific_player_for_selection_df = pd.DataFrame(specific_player_for_selection_list)
                print('specific_player_for_selection_df outside if ---->>>>>  ', specific_player_for_selection_df['Player'])

                """ check the selected player that is Overseas or Local """
                if specific_player_for_selection_df['Overseas_Local'].any() == 'Foreign':
                    if player_count == 1 or player_count == 1.0:
                        selected_player = specific_player_for_selection_df
                        print('selected_player  inside if -<<<<<    ', selected_player['Player'])
                        specific_player_for_selection_df['Category'] = 'Gold'
                        specific_player_for_selection_list = []
                        specific_player_for_selection_list.append(specific_player_for_selection_df)
                        best_20 = best_20.append(specific_player_for_selection_list, ignore_index=True)
                        """ Reset index of best 20 """
                        best_20.reset_index(drop=True, inplace=True)
                        """ Now add the removed player in gold category """
                        gold_category = gold_category.append(remove_player_list1, ignore_index=True)
                        """ drop the player from gold which is added to best 20 """
                        gold_category = reducing_pickedPlayer_from_list(specific_player_for_selection_df, gold_category)
                        """ Reset index of gold category """
                        gold_category.reset_index(drop=True, inplace=True)
                        """ Adding data to Database """
                        print(best_20[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local', 'Category']])
                        print(gold_category[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local']])
                        delete_collection_from_db('Diamond')
                        insertData('psl_t20', 'Diamond', gold_category)
                        delete_collection_from_db('best_20')
                        insertData('psl_t20', 'best_20', best_20)
                        print('Successfully inserted')
                        player_count +=1

        if remove_specific_player_df['Category'].any() == 'Diamond':
            print('Diamond category')
            diamond_category = loadingData('psl_t20', 'Diamond')
            diamond_category = diamond_category.sort_values(['Overall_rating'], ascending=[False])

            """ List for recomended top player """
            recommended_player_list = []

            recommended_player_list = recommended_Player_For_Selection(diamond_category)
            recommended_player_list_df = pd.DataFrame(recommended_player_list)
            recommended_player_list_df.reset_index(drop=True, inplace=True)
            print(recommended_player_list_df[['Player', 'Player Type']])
            recommended_player_count = len(recommended_player_list_df)
            print('count- oo --->  ',recommended_player_count)
            for index_1_r, player_1_r in  recommended_player_list_df.iterrows():
                """ Generate random number """
                specific_player_for_selection_list = []
                random_number = randint(0, recommended_player_count-1)
                print('count on----> ',recommended_player_count)
                print('rand ----  ',random_number)
                specific_player_for_selection_list.append(recommended_player_list_df.loc[random_number])
                specific_player_for_selection_df = pd.DataFrame(specific_player_for_selection_list)
                print('specific_player_for_selection_df outside if ---->>>>>  ', specific_player_for_selection_df['Player'])

                """ check the selected player that is Overseas or Local """
                if specific_player_for_selection_df['Overseas_Local'].any() == 'Foreign':
                    if player_count == 1 or player_count == 1.0:
                        selected_player = specific_player_for_selection_df
                        print('selected_player  inside if -<<<<<    ', selected_player['Player'])
                        specific_player_for_selection_df['Category'] = 'Diamond'
                        specific_player_for_selection_list = []
                        specific_player_for_selection_list.append(specific_player_for_selection_df)
                        best_20 = best_20.append(specific_player_for_selection_list, ignore_index=True)
                        """ Reset index of best 20 """
                        best_20.reset_index(drop=True, inplace=True)
                        """ Now add the removed player in diamond category """
                        diamond_category = diamond_category.append(remove_player_list1, ignore_index=True)
                        """ drop the player from diamond which is added to best 20 """
                        diamond_category = reducing_pickedPlayer_from_list(specific_player_for_selection_df, diamond_category)
                        """ Reset index of diamond category """
                        diamond_category.reset_index(drop=True, inplace=True)
                        """ Adding data to Database """
                        print(best_20[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local', 'Category']])
                        print(diamond_category[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local']])
                        delete_collection_from_db('Diamond')
                        insertData('psl_t20', 'Diamond', diamond_category)
                        print('jjjjj')
                        delete_collection_from_db('best_20')
                        insertData('psl_t20', 'best_20', best_20)
                        print('Successfully inserted')
                        player_count +=1
        
    """ Check Foreign Player Count """
    if df['Foreign'] > 5 or df['Foreign'] > 5.0:
        list_foreign = []
        """ Loop for generating Foreign Player Dataframe"""
        for index, player in best_20.iterrows():
            if player['Overseas_Local'] == 'Foreign':
                list_foreign.append(best_20.loc[index])
                foreign_df = pd.DataFrame(list_foreign)

        """ Reset index of foreign player """
        foreign_df.reset_index(drop=True, inplace=True)
        foreign_count = len(foreign_df) 
        """ Generate random number """
        remove_player_list1 = []
        random_number = randint(0, foreign_count-1)
        remove_player_list1.append(foreign_df.loc[random_number])
        remove_specific_player_df = pd.DataFrame(remove_player_list1)
        print('Player to removeqqqq ->>>>> ', remove_specific_player_df['Player'])

        """ Delete/Remove this sepecific player from best_20 collection """
        best_20 =  reducing_pickedPlayer_from_list(remove_specific_player_df, best_20)

        """ Now check the category of Droped player """
        if remove_specific_player_df['Category'].any() == 'Platinum':
            print('Platinum category')
            platinum_category = loadingData('psl_t20', 'Platinum')
            platinum_category = platinum_category.sort_values(['Overall_rating'], ascending=[False])

            """ List for recomended top player """
            recommended_player_list = []

            recommended_player_list = recommended_Player_For_Selection(platinum_category)
            recommended_player_list_df = pd.DataFrame(recommended_player_list)
            recommended_player_list_df.reset_index(drop=True, inplace=True)
            print(recommended_player_list_df[['Player', 'Player Type']])
            recommended_player_count = len(recommended_player_list_df)
            print('count- oo --->  ',recommended_player_count)
            for index_1_r, player_1_r in  recommended_player_list_df.iterrows():
                """ Generate random number """
                specific_player_for_selection_list = []
                random_number = randint(0, recommended_player_count-1)
                print('count on----> ',recommended_player_count)
                print('rand ----  ',random_number)
                specific_player_for_selection_list.append(recommended_player_list_df.loc[random_number])
                specific_player_for_selection_df = pd.DataFrame(specific_player_for_selection_list)
                print('specific_player_for_selection_df outside if ---->>>>>  ', specific_player_for_selection_df['Player'])

                """ check the selected player that is Overseas or Local """
                if specific_player_for_selection_df['Overseas_Local'].any() == 'Local':
                    if player_count == 1 or player_count == 1.0:
                        selected_player = specific_player_for_selection_df
                        print('selected_player  inside if -<<<<<    ', selected_player['Player'])
                        specific_player_for_selection_df['Category'] = 'Platinum'
                        specific_player_for_selection_list = []
                        specific_player_for_selection_list.append(specific_player_for_selection_df)
                        best_20 = best_20.append(specific_player_for_selection_list, ignore_index=True)
                        """ Reset index of best 20 """
                        best_20.reset_index(drop=True, inplace=True)
                        """ Now add the removed player in platinum category """
                        platinum_category = platinum_category.append(remove_player_list1, ignore_index=True)
                        """ drop the player from platinum which is added to best 20 """
                        platinum_category = reducing_pickedPlayer_from_list(specific_player_for_selection_df, platinum_category)
                        """ Reset index of diamond category """
                        platinum_category.reset_index(drop=True, inplace=True)
                        """ Adding data to Database """
                        print(best_20[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local', 'Category']])
                        print(platinum_category[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local']])
                        delete_collection_from_db('Platinum')
                        insertData('psl_t20', 'Platinum', platinum_category)
                        print('jjjjj')
                        delete_collection_from_db('best_20')
                        insertData('psl_t20', 'best_20', best_20)
                        print('Successfully inserted')
                        player_count +=1

        if remove_specific_player_df['Category'].any() == 'Gold':
            print('Gold category')
            gold_category = loadingData('psl_t20', 'Gold')
            gold_category = gold_category.sort_values(['Overall_rating'], ascending=[False])

            """ List for recomended top player """
            recommended_player_list = []

            recommended_player_list = recommended_Player_For_Selection(gold_category)
            recommended_player_list_df = pd.DataFrame(recommended_player_list)
            recommended_player_list_df.reset_index(drop=True, inplace=True)
            print(recommended_player_list_df[['Player', 'Player Type']])
            recommended_player_count = len(recommended_player_list_df)
            print('count- oo --->  ',recommended_player_count)
            for index_1_r, player_1_r in  recommended_player_list_df.iterrows():
                """ Generate random number """
                specific_player_for_selection_list = []
                random_number = randint(0, recommended_player_count-1)
                print('count on----> ',recommended_player_count)
                print('rand ----  ',random_number)
                specific_player_for_selection_list.append(recommended_player_list_df.loc[random_number])
                specific_player_for_selection_df = pd.DataFrame(specific_player_for_selection_list)
                print('specific_player_for_selection_df outside if ---->>>>>  ', specific_player_for_selection_df['Player'])

                """ check the selected player that is Overseas or Local """
                if specific_player_for_selection_df['Overseas_Local'].any() == 'Local':
                    if player_count == 1 or player_count == 1.0:
                        selected_player = specific_player_for_selection_df
                        print('selected_player  inside if -<<<<<    ', selected_player['Player'])
                        specific_player_for_selection_df['Category'] = 'Gold'
                        specific_player_for_selection_list = []
                        specific_player_for_selection_list.append(specific_player_for_selection_df)
                        best_20 = best_20.append(specific_player_for_selection_list, ignore_index=True)
                        """ Reset index of best 20 """
                        best_20.reset_index(drop=True, inplace=True)
                        """ Now add the removed player in gold category """
                        gold_category = gold_category.append(remove_player_list1, ignore_index=True)
                        """ drop the player from gold which is added to best 20 """
                        gold_category = reducing_pickedPlayer_from_list(specific_player_for_selection_df, gold_category)
                        """ Reset index of gold category """
                        gold_category.reset_index(drop=True, inplace=True)
                        """ Adding data to Database """
                        print(best_20[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local', 'Category']])
                        print(gold_category[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local']])
                        delete_collection_from_db('Diamond')
                        insertData('psl_t20', 'Diamond', gold_category)
                        print('jjjjj')
                        delete_collection_from_db('best_20')
                        insertData('psl_t20', 'best_20', best_20)
                        print('Successfully inserted')
                        player_count +=1

        if remove_specific_player_df['Category'].any() == 'Diamond':
            print('Diamond category')
            diamond_category = loadingData('psl_t20', 'Diamond')
            diamond_category = diamond_category.sort_values(['Overall_rating'], ascending=[False])

            """ List for recomended top player """
            recommended_player_list = []

            recommended_player_list = recommended_Player_For_Selection(diamond_category)
            recommended_player_list_df = pd.DataFrame(recommended_player_list)
            recommended_player_list_df.reset_index(drop=True, inplace=True)
            print(recommended_player_list_df[['Player', 'Player Type']])
            recommended_player_count = len(recommended_player_list_df)
            print('count- oo --->  ',recommended_player_count)
            for index_1_r, player_1_r in  recommended_player_list_df.iterrows():
                """ Generate random number """
                specific_player_for_selection_list = []
                random_number = randint(0, recommended_player_count-1)
                print('count on----> ',recommended_player_count)
                print('rand ----  ',random_number)
                specific_player_for_selection_list.append(recommended_player_list_df.loc[random_number])
                specific_player_for_selection_df = pd.DataFrame(specific_player_for_selection_list)
                print('specific_player_for_selection_df outside if ---->>>>>  ', specific_player_for_selection_df['Player'])

                """ check the selected player that is Overseas or Local """
                if specific_player_for_selection_df['Overseas_Local'].any() == 'Local':
                    if player_count == 1 or player_count == 1.0:
                        selected_player = specific_player_for_selection_df
                        print('selected_player  inside if -<<<<<    ', selected_player['Player'])
                        specific_player_for_selection_df['Category'] = 'Diamond'
                        specific_player_for_selection_list = []
                        specific_player_for_selection_list.append(specific_player_for_selection_df)
                        best_20 = best_20.append(specific_player_for_selection_list, ignore_index=True)
                        """ Reset index of best 20 """
                        best_20.reset_index(drop=True, inplace=True)
                        """ Now add the removed player in diamond category """
                        diamond_category = diamond_category.append(remove_player_list1, ignore_index=True)
                        """ drop the player from diamond which is added to best 20 """
                        diamond_category = reducing_pickedPlayer_from_list(specific_player_for_selection_df, diamond_category)
                        """ Reset index of diamond category """
                        diamond_category.reset_index(drop=True, inplace=True)
                        """ Adding data to Database """
                        print(best_20[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local', 'Category']])
                        print(diamond_category[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local']])
                        delete_collection_from_db('Diamond')
                        insertData('psl_t20', 'Diamond', diamond_category)
                        print('jjjjj')
                        delete_collection_from_db('best_20')
                        insertData('psl_t20', 'best_20', best_20)
                        print('Successfully inserted')
                        player_count +=1
        

def recommended_Player_For_Selection(category):
    recommended_batsman = 1
    recommended_batting_allrounder = 1
    recommended_wicketkeeper_batsman = 1
    recommended_allrounder = 1
    recommended_bowler = 1
    recommended_bowling_allrounder = 1
    """ List for recomended top player """
    recommended_player_list = []
    for index_1, player_1 in category.iterrows():
        if player_1['Player Type'] == 'Batsman':
            if recommended_batsman <= 2 or recommended_batsman <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_batsman+=1
        if player_1['Player Type'] == 'Batting Allrounder':
            if recommended_batting_allrounder <= 2 or recommended_batting_allrounder <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_batting_allrounder+=1
        if player_1['Player Type'] == 'Wicket keeper Batsman':
            if recommended_wicketkeeper_batsman <= 2 or recommended_wicketkeeper_batsman <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_wicketkeeper_batsman+=1
        if player_1['Player Type'] == 'Allrounder':
            if recommended_allrounder <= 2 or recommended_allrounder <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_allrounder+=1
        if player_1['Player Type'] == 'Bowler':
            if recommended_bowler <= 2 or recommended_bowler <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_bowler+=1
        if player_1['Player Type'] == 'Bowling Allrounder':
            if recommended_bowling_allrounder <= 2 or recommended_bowling_allrounder <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_bowling_allrounder+=1
    
    return recommended_player_list


""" List for one Batsman, one Wicket keeper batsman and on Batting All-rounder """
def recommended_Player_Batting_Category(category):
    recommended_batsman = 1
    recommended_batting_allrounder = 1
    recommended_wicketkeeper_batsman = 1
    """ List for recomended top player """
    recommended_player_list = []
    for index_1, player_1 in category.iterrows():
        if player_1['Player Type'] == 'Batsman':
            if recommended_batsman <= 2 or recommended_batsman <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_batsman+=1
        if player_1['Player Type'] == 'Batting Allrounder':
            if recommended_batting_allrounder <= 2 or recommended_batting_allrounder <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_batting_allrounder+=1
        if player_1['Player Type'] == 'Wicket keeper Batsman':
            if recommended_wicketkeeper_batsman <= 2 or recommended_wicketkeeper_batsman <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_wicketkeeper_batsman+=1
    
    recommended_player_df = pd.DataFrame(recommended_player_list)
    """ Reset index """
    recommended_player_df.reset_index(drop=True, inplace=True)
    return recommended_player_df


""" List for Allrounder for selection """
def recommended_Player_Allrounder_Category(category):
    recommended_allrounder = 1
    """ List for recomended top player """
    recommended_player_list = []
    for index_1, player_1 in category.iterrows():
        if player_1['Player Type'] == 'Allrounder':
            if recommended_allrounder <= 3 or recommended_allrounder <= 3.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_allrounder+=1
    
    recommended_player_df = pd.DataFrame(recommended_player_list)
    """ Reset index """
    recommended_player_df.reset_index(drop=True, inplace=True)
    return recommended_player_df


def recommended_Player_Bowling_category(category):
    recommended_bowler = 1
    recommended_bowling_allrounder = 1
    """ List for recomended top player """
    recommended_player_list = []
    for index_1, player_1 in category.iterrows():
        if player_1['Player Type'] == 'Bowler':
            if recommended_bowler <= 2 or recommended_bowler <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_bowler+=1
        if player_1['Player Type'] == 'Bowling Allrounder':
            if recommended_bowling_allrounder <= 2 or recommended_bowling_allrounder <= 2.0:
                recommended_player_list.append(category.loc[index_1])
                recommended_bowling_allrounder+=1
                
    recommended_player_df = pd.DataFrame(recommended_player_list)
    """ Reset index """
    recommended_player_df.reset_index(drop=True, inplace=True)
    return recommended_player_df


def platinum_pick(category, batsman, bowler, allrounder):
    batsman_count = 1
    bowler_count = 1
    allrounder_count = 1
    platinum_pick = []

    for index, player in category.iterrows():
        if batsman_count <= batsman:
            if player['Player Type'] == 'Batsman':
                platinum_pick.append(category.loc[index])
                batsman_count += 1

        if bowler_count <= bowler:
            if player['Player Type'] == 'Bowler':
                platinum_pick.append(category.loc[index])
                bowler_count += 1

        if allrounder_count <= allrounder:
            if player['Player Type'] == 'Allrounder':
                platinum_pick.append(category.loc[index])
                allrounder_count += 1

    platinum_pick = pd.DataFrame(platinum_pick)
    for index_1, player in platinum_pick.iterrows():
        platinum_pick.loc[index_1, 'Category'] = 'Platinum'

    """ Reset index of platinum pick """
    platinum_pick.reset_index(drop=True, inplace=True)
    """ Reducing picked player from category list """
    category = reducing_pickedPlayer_from_list(platinum_pick, category)
    """ Now updating Platinum category in DB """
    delete_collection_from_db('Platinum')

    # Insert the newly created Platinum category after removing the Platinum Pick Players;
    insertData('psl_t20', 'Platinum', category)

    return platinum_pick;


def diamond_pick(category, ownerTeam):
    diamond_pick = []
    
    category = category.sort_values(['Overall_rating'], ascending=[False])
    batting_df = recommended_Player_Batting_Category(category)
    allrounder_df = recommended_Player_Allrounder_Category(category)
    bowling_df = recommended_Player_Bowling_category(category)
    
    """ Selection of Batsman or Wicket keeper or Batting allrounder """
    batting_count = len(batting_df)
    """ Generate random number """
    random_number_batting = randint(0, batting_count-1)
    print('batting random number----> ',random_number_batting)
    print('batting player ----  ',batting_df[['Player', 'Player Type']])
    diamond_pick.append(batting_df.loc[random_number_batting])
    
    """ Selection of Allrounder """
    allrounder_count = len(allrounder_df)
    """ Generate random number """
    random_number_allround = randint(0, allrounder_count-1)
    print('Allrounder random number----> ',random_number_allround)
    print('Allrounder player ----  ',allrounder_df[['Player', 'Player Type']])
    diamond_pick.append(allrounder_df.loc[random_number_allround])
    
    """ Selection of Bowler or Bowling Allrounder """
    bowling_count = len(bowling_df)
    """ Generate random number """
    random_number_bowling = randint(0, bowling_count-1)
    print('bowling_df random number----> ',random_number_bowling)
    print('bowling_df player ----  ',bowling_df[['Player', 'Player Type']])
    diamond_pick.append(bowling_df.loc[random_number_bowling])

    """ Dataframe """
    diamond_pick = pd.DataFrame(diamond_pick)
    for index_1, player in diamond_pick.iterrows():
        diamond_pick.loc[index_1, 'Category'] = 'Diamond'
        
    """ Reset index of diamond pick """
    diamond_pick.reset_index(drop=True, inplace=True)
    """ Reducing picked player from category list """
    diamond_category = loadingData('psl_t20', 'Diamond')
    category = reducing_pickedPlayer_from_list(diamond_pick, diamond_category)
    """ Now updating best20 """
    best_20 = loadingData('psl_t20', ownerTeam)
    best_20 = best_20.append(diamond_pick)
    best_20.reset_index(drop=True, inplace=True)
    delete_collection_from_db(ownerTeam)
    insertData('psl_t20', ownerTeam, best_20)
    """ Now updating Diamond category in DB """
    delete_collection_from_db('Diamond')
    insertData('psl_t20', 'Diamond', category)
    
    return diamond_pick

def gold_pick(category,ownerTeam):
    gold_pick = []
    category = category.sort_values(['Overall_rating'], ascending=[False])
    batting_df = recommended_Player_Batting_Category(category)
    allrounder_df = recommended_Player_Allrounder_Category(category)
    bowling_df = recommended_Player_Bowling_category(category)
    
    """ Selection of Batsman or Wicket keeper or Batting allrounder """
    batting_count = len(batting_df)
    """ Generate random number """
    random_number_batting = randint(0, batting_count-1)
    print('batting random number----> ',random_number_batting)
    print('batting player ----  ',batting_df[['Player', 'Player Type']])
    gold_pick.append(batting_df.loc[random_number_batting])
    
    """ Selection of Allrounder """
    allrounder_count = len(allrounder_df)
    """ Generate random number """
    random_number_allround = randint(0, allrounder_count-1)
    print('Allrounder random number----> ',random_number_allround)
    print('Allrounder player ----  ',allrounder_df[['Player', 'Player Type']])
    gold_pick.append(allrounder_df.loc[random_number_allround])
    
    """ Selection of Bowler or Bowling Allrounder """
    bowling_count = len(bowling_df)
    """ Generate random number """
    random_number_bowling = randint(0, bowling_count-1)
    print('bowling_df random number----> ',random_number_bowling)
    print('bowling_df player ----  ',bowling_df[['Player', 'Player Type']])
    gold_pick.append(bowling_df.loc[random_number_bowling])

    """ Dataframe """
    gold_pick = pd.DataFrame(gold_pick)
    for index_1, player in gold_pick.iterrows():
        gold_pick.loc[index_1, 'Category'] = 'Gold'
        
    """ Reset index of gold pick """
    gold_pick.reset_index(drop=True, inplace=True)
    """ Reducing picked player from category list """
    gold_category = loadingData('psl_t20', 'Gold')
    category = reducing_pickedPlayer_from_list(gold_pick, gold_category)
    """ Now updating best20 """
    best_20 = loadingData('psl_t20', ownerTeam)
    best_20 = best_20.append(gold_pick)
    best_20.reset_index(drop=True, inplace=True)
    delete_collection_from_db(ownerTeam)
    best_20=best_20.drop('_id',1)
    insertData('psl_t20', ownerTeam, best_20)
    """ Now updating Diamond category in DB """
    delete_collection_from_db('Gold')
    insertData('psl_t20', 'Gold', category)
    
    return gold_pick;
def Silver_Category_Foreign_Player_Count(category):
    player_count = 1
    player_list = []
    """ Count the Local & Foreign Player """
    df = category['Overseas_Local'].value_counts().to_dict()
    
    """ Check Local & Foreign Player Count in First 3 Categories """
    if df['Local'] > 3 or df['Local'] > 3.0:
        list_local = []
        """ Loop for generating Local Player Dataframe"""
        for index, player in category.iterrows():
            if player['Overseas_Local'] == 'Local':
                list_local.append(category.loc[index])
                local_df = pd.DataFrame(list_local)

        """ Reset index of local player """
        local_df.reset_index(drop=True, inplace=True)
        local_count = len(local_df) 
        """ Generate random number """
        remove_player_list1 = []
        random_number = randint(0, local_count-1)
        remove_player_list1.append(local_df.loc[random_number])
        remove_specific_player_df = pd.DataFrame(remove_player_list1)
        print('Player to removeqqqq ->>>>> ', remove_specific_player_df['Player'])

        """ Delete/Remove this sepecific player from silver pick collection """
        silver_pick =  reducing_pickedPlayer_from_list(remove_specific_player_df, category)

        """ Now check the category of Droped player """
        if remove_specific_player_df['Category'].any() == 'Silver':
            print('Silver category')
            silver_category = loadingData('psl_t20', 'Silver')
            silver_category = silver_category.sort_values(['Overall_rating'], ascending=[False])

            """ List for recomended top player """
            recommended_player_list = []

            recommended_player_list = recommended_Player_For_Selection(silver_category)
            recommended_player_list_df = pd.DataFrame(recommended_player_list)
            recommended_player_list_df.reset_index(drop=True, inplace=True)
            print(recommended_player_list_df[['Player', 'Player Type']])
            recommended_player_count = len(recommended_player_list_df)
            print('count- oo --->  ',recommended_player_count)
            for index_1_r, player_1_r in  recommended_player_list_df.iterrows():
                """ Generate random number """
                specific_player_for_selection_list = []
                random_number = randint(0, recommended_player_count-1)
                print('count on----> ',recommended_player_count)
                print('rand ----  ',random_number)
                specific_player_for_selection_list.append(recommended_player_list_df.loc[random_number])
                specific_player_for_selection_df = pd.DataFrame(specific_player_for_selection_list)
                print('specific_player_for_selection_df outside if ---->>>>>  ', specific_player_for_selection_df['Player'])

                """ check the selected player that is Overseas or Local """
                if specific_player_for_selection_df['Overseas_Local'].any() == 'Foreign':
                    if player_count == 1 or player_count == 1.0:
                        selected_player = specific_player_for_selection_df
                        print('selected_player  inside if -<<<<<    ', selected_player['Player'])
                        specific_player_for_selection_df['Category'] = 'Silver'
                        specific_player_for_selection_list = []
                        specific_player_for_selection_list.append(specific_player_for_selection_df)
                        silver_pick = silver_pick.append(specific_player_for_selection_list, ignore_index=True)
                        """ Reset index of best 20 """
                        silver_pick.reset_index(drop=True, inplace=True)
                        """ Now add the removed player in Silver category """
                        silver_category = silver_category.append(remove_player_list1, ignore_index=True)
                        """ drop the player from silver which is added to silver_pick """
                        silver_category = reducing_pickedPlayer_from_list(specific_player_for_selection_df, silver_category)
                        """ Reset index of silver category """
                        silver_category.reset_index(drop=True, inplace=True)
                        """ Adding data to Database """
                        print(silver_20[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local', 'Category']])
                        print(silver_category[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local']])
                        delete_collection_from_db('Silver')
                        insertData('psl_t20', 'Silver', silver_category)
                        print('Successfully inserted')
                        player_count +=1

        
    """ Check Foreign Player Count """
    if df['Foreign'] > 2 or df['Foreign'] > 2.0:
        list_foreign = []
        """ Loop for generating Foreign Player Dataframe"""
        for index, player in category.iterrows():
            if player['Overseas_Local'] == 'Foreign':
                list_foreign.append(category.loc[index])
                foreign_df = pd.DataFrame(list_foreign)

        """ Reset index of foreign player """
        foreign_df.reset_index(drop=True, inplace=True)
        foreign_count = len(foreign_df) 
        """ Generate random number """
        remove_player_list1 = []
        random_number = randint(0, foreign_count-1)
        remove_player_list1.append(foreign_df.loc[random_number])
        remove_specific_player_df = pd.DataFrame(remove_player_list1)
        print('Player to removeqqqq ->>>>> ', remove_specific_player_df['Player'])

        """ Delete/Remove this sepecific player from best_20 collection """
        silver_pick =  reducing_pickedPlayer_from_list(remove_specific_player_df, category)

        """ Now check the category of Droped player """
        if remove_specific_player_df['Category'].any() == 'Silver':
            print('Silver category')
            silver_category = loadingData('psl_t20', 'Silver')
            silver_category = silver_category.sort_values(['Overall_rating'], ascending=[False])

            """ List for recomended top player """
            recommended_player_list = []

            recommended_player_list = recommended_Player_For_Selection(silver_category)
            recommended_player_list_df = pd.DataFrame(recommended_player_list)
            recommended_player_list_df.reset_index(drop=True, inplace=True)
            print(recommended_player_list_df[['Player', 'Player Type']])
            recommended_player_count = len(recommended_player_list_df)
            print('count- oo --->  ',recommended_player_count)
            for index_1_r, player_1_r in  recommended_player_list_df.iterrows():
                """ Generate random number """
                specific_player_for_selection_list = []
                random_number = randint(0, recommended_player_count-1)
                print('count on----> ',recommended_player_count)
                print('rand ----  ',random_number)
                specific_player_for_selection_list.append(recommended_player_list_df.loc[random_number])
                specific_player_for_selection_df = pd.DataFrame(specific_player_for_selection_list)
                print('specific_player_for_selection_df outside if ---->>>>>  ', specific_player_for_selection_df['Player'])

                """ check the selected player that is Overseas or Local """
                if specific_player_for_selection_df['Overseas_Local'].any() == 'Local':
                    if player_count == 1 or player_count == 1.0:
                        selected_player = specific_player_for_selection_df
                        print('selected_player  inside if -<<<<<    ', selected_player['Player'])
                        specific_player_for_selection_df['Category'] = 'Silver'
                        specific_player_for_selection_list = []
                        specific_player_for_selection_list.append(specific_player_for_selection_df)
                        silver_pick = silver.append(specific_player_for_selection_list, ignore_index=True)
                        """ Reset index of silver_pick """
                        silver_pick.reset_index(drop=True, inplace=True)
                        """ Now add the removed player in silver category """
                        silver_category = silver_category.append(remove_player_list1, ignore_index=True)
                        """ drop the player from silver which is added to silver pick """
                        silver_category = reducing_pickedPlayer_from_list(specific_player_for_selection_df, silver_category)
                        """ Reset index of silver category """
                        silver_category.reset_index(drop=True, inplace=True)
                        """ Adding data to Database """
                        print(silver_pick[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local', 'Category']])
                        print(silver_category[['Player', 'Player Type', 'Overall_rating', 'Overseas_Local']])
                        delete_collection_from_db('Silver')
                        insertData('psl_t20', 'Silver', silver_category)
                        print('Successfully inserted')
                        player_count +=1

    return silver_pick


def silver_pick(category):
    silver_pick = []
    silver_category_list = []
    count = 1
    
    category = category.sort_values(['Overall_rating'], ascending=[False])
    silver_category_list = recommended_Player_For_Selection(category)
    # silver_category_df = pd.DataFrame(silver_category_list)
    silver_category_df = loadingData('psl_t20', 'Silver')
    """ Reset index """
    silver_category_df.reset_index(drop=True, inplace=True)
    for index, player in silver_category_df.iterrows():
        """ Reset index """
        silver_category_df.reset_index(drop=True, inplace=True)
        silver_category_count = len(silver_category_df)
        """ Generate random number """
        random_number = randint(0, silver_category_count-1)
        if count <= 5 or count <= 5.0:
            silver_pick.append(silver_category_df.loc[random_number])
            silver_category_df.drop(silver_category_df.index[[random_number]], inplace=True)
            count+=1
    
    
    """ Dataframe """
    silver_pick = pd.DataFrame(silver_pick)
    for index_1, player in silver_pick.iterrows():
        silver_pick.loc[index_1, 'Category'] = 'Silver'
        
    """ Reset index of silver pick """
    silver_pick.reset_index(drop=True, inplace=True)
    """ Reducing picked player from category list """
    silver_category = loadingData('psl_t20', 'Silver')
    category = reducing_pickedPlayer_from_list(silver_pick, silver_category)
    
    """ Now updating Diamond category in DB """
    delete_collection_from_db('Silver')
    insertData('psl_t20', 'Silver', category)
    
    return silver_pick

def suplementary_pick(ownerTeam):
    suplementary_pick = []
    suplementary_category_list = []
    foreign = 1
    local = 1

    suplementary_category_list = recommended_Player_For_Selection_Suplementary()
    suplementary_category_df = pd.DataFrame(suplementary_category_list)
    print(suplementary_category_df[['Player', 'Player Type']])
    for index, player in suplementary_category_df.iterrows():
        """ Reset index """
        suplementary_category_df.reset_index(drop=True, inplace=True)
        suplementary_category_count = len(suplementary_category_df)
        """ Generate random number """
        random_number = randint(0, suplementary_category_count-1)

        if suplementary_category_df.loc[random_number, "Overseas_Local"] == "Foreign":
            if foreign == 1:
                suplementary_pick.append(suplementary_category_df.loc[random_number])
                print('Foreign')
                foreign+=1

        if suplementary_category_df.loc[random_number, "Overseas_Local"] == "Local":
            if local < 4:
                suplementary_pick.append(suplementary_category_df.loc[random_number])
                print('Local')
                local+=1
        """ Drop the Selected Player """
        suplementary_category_df.drop(suplementary_category_df.index[[random_number]], inplace=True)

    """ Dataframe """
    suplementary_pick = pd.DataFrame(suplementary_pick)
    for index_1, player in suplementary_pick.iterrows():
        suplementary_pick.loc[index_1, 'Category'] = 'Supplementory'

    """ Reset index of Suplementary pick """
    suplementary_pick.reset_index(drop=True, inplace=True)
    print('Update best_20 Collection')
    # """ Now updating best20 """
    insert_specific_record(ownerTeam, suplementary_pick)
    print('Suplementory Picked')
    """ Reducing picked player from category list """
    reducingPlayers_FromCategories(suplementary_pick)

    return suplementary_pick

def recommended_Player_For_Selection_Suplementary():
    p_bst = 1
    p_bt_all = 1
    p_bl_all = 1
    p_wkt=1
    p_all=1
    p_bl = 1
    d_bst = 1
    d_bt_all = 1
    d_bl_all = 1
    d_wkt=1
    d_all=1
    d_bl = 1
    g_bst = 1
    g_bt_all = 1
    g_bl_all = 1
    g_wkt=1
    g_all=1
    g_bl = 1 
    s_bst = 1
    s_bt_all = 1
    s_bl_all = 1
    s_wkt=1
    s_all=1
    s_bl = 1 
    platinum = loadingData('psl_t20', 'Platinum')
    diamond = loadingData('psl_t20', 'Diamond')
    gold = loadingData('psl_t20', 'Gold')
    silver = loadingData('psl_t20', 'Silver')

    # platinum = pd.DataFrame.sort,'Overall_rating',ascending=[False])
    platinum = platinum.sort_values(['Overall_rating'], ascending=[False])
    """ List for recomended top player from Platinum """
    recommended_player_list = []
    for index_1, player_1 in platinum.iterrows():
        if player_1['Player Type'] == 'Batsman':
            if p_bst == 1:
                recommended_player_list.append(platinum.loc[index_1])
                p_bst+=1
        if player_1['Player Type'] == 'Batting Allrounder':
            if p_bt_all == 1:
                recommended_player_list.append(platinum.loc[index_1])
                p_bt_all+=1
        if player_1['Player Type'] == 'Wicket keeper Batsman':
            if p_wkt == 1:
                recommended_player_list.append(platinum.loc[index_1])
                p_wkt+=1
        if player_1['Player Type'] == 'Bowler':
            if p_bl == 1:
                recommended_player_list.append(platinum.loc[index_1])
                p_bl+=1
        if player_1['Player Type'] == 'Bowling Allrounder':
            if p_bl_all == 1:
                recommended_player_list.append(platinum.loc[index_1])
                p_bl_all+=1
        if player_1['Player Type'] == 'Allrounder':
            if p_all == 1:
                recommended_player_list.append(platinum.loc[index_1])
                p_all+=1
                
    diamond = diamond.sort_values(['Overall_rating'], ascending=[False])
    """ List for recomended top player from Diamond """
    for index_1, player_1 in diamond.iterrows():
        if player_1['Player Type'] == 'Batsman':
            if d_bst == 1:
                recommended_player_list.append(diamond.loc[index_1])
                d_bst+=1
        if player_1['Player Type'] == 'Batting Allrounder':
            if d_bt_all == 1:
                recommended_player_list.append(diamond.loc[index_1])
                d_bt_all+=1
        if player_1['Player Type'] == 'Wicket keeper Batsman':
            if d_wkt == 1:
                recommended_player_list.append(diamond.loc[index_1])
                d_wkt+=1
        if player_1['Player Type'] == 'Bowler':
            if d_bl == 1:
                recommended_player_list.append(diamond.loc[index_1])
                d_bl+=1
        if player_1['Player Type'] == 'Bowling Allrounder':
            if d_bl_all == 1:
                recommended_player_list.append(diamond.loc[index_1])
                d_bl_all+=1
        if player_1['Player Type'] == 'Allrounder':
            if d_all == 1:
                recommended_player_list.append(diamond.loc[index_1])
                d_all+=1
                
    gold = gold.sort_values(['Overall_rating'], ascending=[False])
    """ List for recomended top player from Gold """
    for index_1, player_1 in gold.iterrows():
        if player_1['Player Type'] == 'Batsman':
            if g_bst == 1:
                recommended_player_list.append(gold.loc[index_1])
                g_bst+=1
        if player_1['Player Type'] == 'Batting Allrounder':
            if g_bt_all == 1:
                recommended_player_list.append(gold.loc[index_1])
                g_bt_all+=1
        if player_1['Player Type'] == 'Wicket keeper Batsman':
            if g_wkt == 1:
                recommended_player_list.append(gold.loc[index_1])
                g_wkt+=1
        if player_1['Player Type'] == 'Bowler':
            if g_bl == 1:
                recommended_player_list.append(gold.loc[index_1])
                g_bl+=1
        if player_1['Player Type'] == 'Bowling Allrounder':
            if g_bl_all == 1:
                recommended_player_list.append(gold.loc[index_1])
                g_bl_all+=1
        if player_1['Player Type'] == 'Allrounder':
            if g_all == 1:
                recommended_player_list.append(gold.loc[index_1])
                g_all+=1
                
                
    silver = silver.sort_values(['Overall_rating'], ascending=[False])
    """ List for recomended top player from Silver """
    for index_1, player_1 in silver.iterrows():
        if player_1['Player Type'] == 'Batsman':
            if s_bst == 1:
                recommended_player_list.append(silver.loc[index_1])
                s_bst+=1
        if player_1['Player Type'] == 'Batting Allrounder':
            if s_bt_all == 1:
                recommended_player_list.append(silver.loc[index_1])
                s_bt_all+=1
        if player_1['Player Type'] == 'Wicket keeper Batsman':
            if s_wkt == 1:
                recommended_player_list.append(silver.loc[index_1])
                s_wkt+=1
        if player_1['Player Type'] == 'Bowler':
            if s_bl == 1:
                recommended_player_list.append(silver.loc[index_1])
                s_bl+=1
        if player_1['Player Type'] == 'Bowling Allrounder':
            if s_bl_all == 1:
                recommended_player_list.append(silver.loc[index_1])
                s_bl_all+=1
        if player_1['Player Type'] == 'Allrounder':
            if s_all == 1:
                recommended_player_list.append(silver.loc[index_1])
                s_all+=1
    
    recommended_player_df = pd.DataFrame(recommended_player_list)
    """ Reset index """
    recommended_player_df.reset_index(drop=True, inplace=True)
    return recommended_player_df
    
def reducingPlayers_FromCategories(suplementary_pick):
    platinum = loadingData('psl_t20', 'Platinum')
    diamond = loadingData('psl_t20', 'Diamond')
    gold = loadingData('psl_t20', 'Gold')
    silver = loadingData('psl_t20', 'Silver')
    
    for index_1, pick_player in suplementary_pick.iterrows():
        for index_2, dataset_player in platinum.iterrows():
            if pick_player['Player'] == dataset_player['Player'] :
                platinum.drop(index_2,inplace=True)
                platinum.reset_index(drop=True,inplace=True)
                
        for index_, dataset_player_ in diamond.iterrows():
            if pick_player['Player'] == dataset_player_['Player'] :
                diamond.drop(index_,inplace=True)
                diamond.reset_index(drop=True,inplace=True)
                
        for index_3, dataset_player_3 in gold.iterrows():
            if pick_player['Player'] == dataset_player_3['Player'] :
                gold.drop(index_3,inplace=True)
                gold.reset_index(drop=True,inplace=True)
                
        for index_4, dataset_player_4 in silver.iterrows():
            if pick_player['Player'] == dataset_player_4['Player'] :
                silver.drop(index_4,inplace=True)
                silver.reset_index(drop=True,inplace=True)
    
    """ Now updating Categories in DB """
    delete_collection_from_db('Platinum')
    insertData('psl_t20', 'Platinum', platinum)
    delete_collection_from_db('Diamond')
    insertData('psl_t20', 'Diamond', diamond)
    delete_collection_from_db('Gold')
    insertData('psl_t20', 'Gold', gold)
    delete_collection_from_db('Silver')
    insertData('psl_t20', 'Silver', silver)

def emergingPick(category,batsman,bowler, allrounder):
    batsman_count = 1
    bowler_count = 1
    allrounder_count = 1
    emerging_Pick = []

    for index, player in category.iterrows():
        if batsman_count <= batsman:
            if player['Player Type'] == 'Batsman':
                emerging_Pick.append(category.loc[index])
                batsman_count += 1

        if bowler_count <= bowler:
            if player['Player Type'] == 'Bowler':
                emerging_Pick.append(category.loc[index])
                bowler_count += 1

        if allrounder_count <= allrounder:
            if player['Player Type'] == 'Allrounder':
                emerging_Pick.append(category.loc[index])
                allrounder_count += 1

    emerging_Pick = pd.DataFrame(emerging_Pick)
    for index_1, player in emerging_Pick.iterrows():
        emerging_Pick.loc[index_1, 'Category'] = 'Emerging'

    """ Reset index of platinum pick """
    emerging_Pick.reset_index(drop=True, inplace=True)
    """ Reducing picked player from category list """
    category = reducing_pickedPlayer_from_list(emerging_Pick, category)
    """ Now updating Platinum category in DB """
    delete_collection_from_db('Emerging')

    # Insert the newly created Platinum category after removing the Platinum Pick Players;
    insertData('psl_t20', 'Emerging', category)

    return emerging_Pick;

# GENETIC ALGORITHM Section
def individual_team(length,min,max):
    """This function create a team of 11 players for population"""
    
    return sample(range(min, max), length)

def population_of_teams(number_of_teams,length,min,max):
    """
    Creates a number of teams (i.e population)
    count -> the number of teams in the population.
    length -> the number of players in a team e.g. 11.
    min -> the minimum possible value in the random list of indices.
    max -> the maximum possible value in the random list of indices.
    
    """
    return [individual_team(length,min,max) for x in range(number_of_teams)]

def fitness_function(individual_team,ownerName):
    """
    Define the fitness of individual player. Higher the value, better is fitness.
    individual_team : Team whose players are to evaluate.
    
    """  
    fitness_value = 0
    diverse_bowling = 0
    penality = 0

    best_20 = loadingData('psl_t20',ownerName)
    best_20.drop('_id',axis=1,inplace=True)


    try:
        # rating gives us overall batting and bowling talent of a team
        rating = reduce(add,best_20.loc[individual_team]['Overall_rating'],0)
        # This is a condition which checks whither a team have different bowling option (bowler and bowling allrounder in our case)
        diverse_bowling = 10*(best_20.loc[individual_team]['Player Type'].value_counts()['Bowling Allrounder']) + 10*(best_20.loc[individual_team]['Player Type'].value_counts()['Allrounder'])
    except Exception as e:
        if e.args == ('Bowling Allrounder',):
            diverse_bowling = -30
        if e.args ==('Allrounder',):
            diverse_bowling = -30
            
    penality = team_combination(individual_team,ownerName)
    return (rating + diverse_bowling) - penality

def team_combination(individual,ownerName):
    """ 
    This function checks weather a team is balanced or not.
    if a team is unbalanced then 100 points will be deducted as a penality fro the total points;
    an unbalanced team is a team which don't satisfy following criteria
    Specialist WicketKeeper
    four bowlers (bowler + bowling allrounder in our case)
    five batsman (batsman + batting allrounder + allrounder)
    
    """
    wicket_keeper = 0
    batting = 0
    bowling = 0
    penality = 0
    best_20 = loadingData('psl_t20',ownerName)
    
    for player in best_20.loc[individual]['Player Type']:
        if player == 'Wicket keeper Batsman':
            wicket_keeper += 1
        if player == 'Batting Allrounder' or player == 'Allrounder' or player == 'Batsman':
            batting += 1
        if player == 'Bowler' or player == 'Bowling Allrounder':
            bowling += 1;
    
    if wicket_keeper != 1:
        penality += 100
    if bowling < 3:
        penality += 100
    if batting < 6 or batting >7:
        penality += 100
    
    return penality

def average(pop,ownerName):
    """Find average fitness of population"""

    summed = reduce(add,(fitness_function(x,ownerName) for x in pop),0)
    return summed/(len(pop)*1.0)

def evolution_of_teams(pop,ownerName,retain=0.2,random_select = 0.05,mutate = 0.02):
    graded = [ (fitness_function(x,ownerName), x) for x in pop]
    graded = [ x[1] for x in sorted(graded,reverse=True)]

    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]
    # randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)
    
    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            randomlySelectedPlayer = randint(0, 24)
            while randomlySelectedPlayer in individual:
                pos_to_mutate = randint(0, len(individual)-1)
                randomlySelectedPlayer = randint(0, 24)
    
            individual[pos_to_mutate] = randomlySelectedPlayer
    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = int(len(male) / 2)
            child = male[:half] + female[half:]
            
            children.append(child)
    
    parents.extend(children)
    return parents

def best11_using_Genetic_Algorithm(ownerName):
    best20 = loadingData('psl_t20',ownerName)
    best20.drop('_id',axis=1,inplace=True)
    teams = population_of_teams((len(best20)), 11, 0, len(best20)-1)
    fitness_history = [average(teams,ownerName),]

    for i in range(40):
        teams = evolution_of_teams(teams,ownerName)
    delete_collection_from_db(ownerName+"_best_11")
    insertData('psl_t20',ownerName+"_best_11",best20.loc[teams[-1]])


#Function called from NODE.JS SERVER to pick platinum players in the Drafting Process
if sys.argv[1] == 'platinumPick':
    
    platinum = loadingData('psl_t20', 'Platinum')
    platinum_pick_players = platinum_pick(platinum,1,1,1)
    # Insert the best playing 20 into database;

    insertData('psl_t20', sys.argv[2], platinum_pick_players)
    print(platinum_pick_players)

#Function called from NODE.JS SERVER to pick diamond players in the Drafting Process
if sys.argv[1] == 'diamondPick':
    diamond = loadingData('psl_t20', 'Diamond')
    diamond_pick_players = diamond_pick(diamond,sys.argv[2])
    
#Function called from NODE.JS SERVER to pick gold players in the Drafting Process
if sys.argv[1] == 'goldPick':
    gold = loadingData('psl_t20', 'Gold')
    gold_pick_players = gold_pick(gold,sys.argv[2])
    

#Function called from NODE.JS SERVER to pick silver players in the Drafting Process
if sys.argv[1] == 'silverPick':
    silver = loadingData('psl_t20', 'Silver')
    silver_pick_players = silver_pick(silver)
    # Insert the best playing 20 into database;
    insert_specific_record(sys.argv[2], silver_pick_players)

#Function called from NODE.JS SERVER to pick supplementory players in the Drafting Process
if sys.argv[1] == 'supplementoryPick':
    suplementry = suplementary_pick(sys.argv[2])


#Function called from NODE.JS SERVER to pick emerging players in the Drafting Process
if sys.argv[1] == 'emergingPick':
    emerging = loadingData('psl_t20', 'Emerging')
    emerging_pick_players = emergingPick(emerging,1,1,1)
    # Insert the best playing 20 into database;

    insertData('psl_t20', sys.argv[2], emerging_pick_players)
    print(emerging_pick_players)

#Function called from NODE.JS SERVER to choose best Playing 11 for a team using GENETIC ALGORITHN
if sys.argv[1] == 'best_11':
    best11_using_Genetic_Algorithm(sys.argv[2])