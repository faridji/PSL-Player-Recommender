from pymongo import MongoClient;
import pandas as pd;
import sys;
from odo import odo

# Database Releted Functions
def insertData(dbName,collectionName,data):
    client = MongoClient()
    db = client[dbName]
    myCollection = db[collectionName]
    odo(data,myCollection)
def loadingData(dbName,collectionName):
    client = MongoClient()
    db = client[dbName]
    collection = db[collectionName]
    return pd.DataFrame(list(collection.find()))
def delete_DB(name):
    client = MongoClient()
    client.drop_database(name)
    print(name + " database deleted")
def delete_collection_from_db(collectionName):
    client = MongoClient()
    db = client['psl_t20']
    db.drop_collection(collectionName)
    print(collectionName + " collection deleted")
def is_Collection_Exits(collectionName):
    client = MongoClient()
    db = client['psl_t20']
    if "silver" in db.collection_names():
        return True;
    return False;

def getting_data_of_psl_Players(dataset,matched_international_players):
    records = []

    for index,t20_player in dataset.iterrows():
        for index2,psl_listplayer in matched_international_players.iterrows():
            if t20_player['Player'] + " " + t20_player['Country'] == psl_listplayer[0]:
                records.append(dataset.loc[index])
    df = pd.DataFrame(records)
    return df

def Make_A_Category(category_name,dataset,batsman,allrounder,bowler,batting_allrounder,wicket_keeper,bowling_allrounder):

    category = category_name
    player_sorted = dataset
    count_batsman = 1
    count_bowler = 1
    count_wicket_keeper_batsman = 1
    count_allrounder = 1
    count_batting_allrounder = 1
    count_bowling_allrounder = 1
    for player in range(len(player_sorted)):
        if count_batsman <= batsman:
            if player_sorted['Player Type'][player] == 'Batsman':
                category.append(player_sorted.loc[player])
                count_batsman += 1;

        if count_allrounder <= allrounder:

            if player_sorted['Player Type'][player] == 'Allrounder' or player_sorted['Player Type'][player] == 'All_rounder':
                category.append(player_sorted.loc[player])
                count_allrounder += 1;

        if count_bowler <= bowler:
            if player_sorted['Player Type'][player] == 'Bowler':
                category.append(player_sorted.loc[player])
                count_bowler += 1;

        if count_batting_allrounder <= batting_allrounder:
            if player_sorted['Player Type'][player] == 'Batting Allrounder':
                category.append(player_sorted.loc[player])
                count_batting_allrounder += 1;

        if count_wicket_keeper_batsman <= wicket_keeper:
            if player_sorted['Player Type'][player] == 'Wicket keeper Batsman':
                category.append(player_sorted.loc[player])
                count_wicket_keeper_batsman += 1;

        if count_bowling_allrounder <= bowling_allrounder:
            if player_sorted['Player Type'][player] == 'Bowling Allrounder':
                category.append(player_sorted.loc[player])
                count_bowling_allrounder += 1;
    return category;

def reducing_pslPlayers_list(category_to_eliminate,list_of_players):
    list_of_players = pd.DataFrame(list_of_players)
    category_to_eliminate = pd.DataFrame(category_to_eliminate)
    for index_1, category_player in category_to_eliminate.iterrows():
        for index_2, dataset_player in list_of_players.iterrows():
            if category_player['Player'] == dataset_player['Player'] :
                list_of_players.drop(index_2,inplace=True)
                list_of_players.reset_index(drop=True,inplace=True)
    return list_of_players


# Different PSL Categories Creation functions
def makePlatinumCategory(sorted_data):
    platinum_category_players = []
    platinum_category_players = Make_A_Category(platinum_category_players,sorted_data,5,10,5,3,2,5)
    platinum_category_players = pd.DataFrame(platinum_category_players)

    delete_collection_from_db('Platinum')
    insertData('psl_t20','Platinum',platinum_category_players)
    print("Successfully Inserted Platinum Category into Database.")
    return platinum_category_players;
def makeDiamondCategory(platinum_Category_Players, sorted_data):
    diamond_category_players = []
    diamond_category_players = Make_A_Category(diamond_category_players,sorted_data,10,10,10,5,2,5)
    diamond_category_players = pd.DataFrame(diamond_category_players)

    delete_collection_from_db('Diamond')
    insertData('psl_t20','Diamond',diamond_category_players)
    print("Successfully Inserted diamond Category into Database.")
    return diamond_category_players;
def makeGoldCategory(diamond_Category_Players, sorted_data):
    gold_category_players = []
    gold_category_players = Make_A_Category(gold_category_players,sorted_data,15,15,15,7,2,7)
    gold_category_players = pd.DataFrame(gold_category_players)

    delete_collection_from_db('Gold')
    insertData('psl_t20','Gold',gold_category_players)
    print("Successfully Inserted gold Category into Database.")
    return gold_category_players;
def makeSilverCategory(gold_Category_Players, sorted_data):
    silver_category_players = []

    silver_category_players = Make_A_Category(silver_category_players,sorted_data,30,30,30,10,2,10)
    silver_category_players = pd.DataFrame(silver_category_players)

    delete_collection_from_db('Silver')
    insertData('psl_t20','Silver',silver_category_players)
    print("Successfully Inserted silver Category into Database.")
    return silver_category_players;
# def makeSupplementoryCategory(silver_Category_Players, sorted_data):
#     supplementory_category_players = []

#     supplementory_category_players = Make_A_Category(supplementory_category_players,sorted_data,30,30,30,10,2,10)
#     supplementory_category_players = pd.DataFrame(supplementory_category_players)

#     delete_collection_from_db('Supplementory')
#     insertData('psl_t20','Supplementory',supplementory_category_players)
#     print("Successfully Inserted supplementory Category into Database.")
#     return supplementory_category_players;

def process_psl_PlayerList():
    psl_list = pd.read_csv("G:\\COURSE WORK\\psl\\Python\\psl_player_list.csv",index_col=False)
    replace_list = []
    for index, player in psl_list.iterrows():
        """ first short the countries names and save in original list and then add that players in international player list
        (replace_list) """
        if 'West Indies' in player['Player'] or 'WI' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('West Indies', 'WI')
            replace_list.append(psl_list.loc[index, 'Player'])

        elif 'Pakistan' in player['Player'] or 'PAK' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('Pakistan', 'PAK')
            replace_list.append(psl_list.loc[index, 'Player'])

        elif 'Sri Lanka' in player['Player'] or 'Sri lanka' in player['Player'] or 'SL' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('Sri Lanka', 'SL')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'Australia' in player['Player'] or 'AUS' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('Australia', 'AUS')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'England' in player['Player'] or 'ENG' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('England', 'ENG')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'South Africa' in player['Player'] or 'SA' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('South Africa', 'SA')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'New Zealand' in player['Player'] or 'NZ' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('New Zealand', 'NZ')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'Scotland' in player['Player'] or 'SCOT' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('Scotland', 'SCOT')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'Canada' in player['Player'] or 'CAN' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('Canada', 'CAN')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'Ireland' in player['Player'] or 'IRE' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('Ireland', 'IRE')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'Bangladesh' in player['Player'] or 'BDESH' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('Bangladesh', 'BDESH')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'USA' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('USA', 'USA')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'Zimbabwe' in player['Player'] or 'ZIM' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('Zimbabwe', 'ZIM')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'UAE' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('UAE', 'UAE')
            replace_list.append(psl_list.loc[index, 'Player'])
        elif 'Afghanistan' in player['Player'] or 'AFG' in player['Player']:
            psl_list['Player'] = psl_list['Player'].str.replace('Afghanistan', 'AFG')
            replace_list.append(psl_list.loc[index, 'Player'])


    matched_international_player = pd.DataFrame(replace_list, columns=['Player'])

    # Extract the matched international Players and put the remaining players into domestic list
    domestic_list = psl_list[~psl_list.Player.isin(matched_international_player.Player)]

    # Getting t20 dataset from database
    print("Loading T20 International Dataset")
    t20_dataset = loadingData('psl_t20','t20_dataset')
    psl_dataset = loadingData('psl_t20','psl_dataset')
    if 'psl_rating' in t20_dataset.columns and 'Overall_rating' in t20_dataset.columns:
        data = getting_data_of_psl_Players(t20_dataset,matched_international_player)
        data.drop("_id",axis=1,inplace=True)
        delete_collection_from_db('psl_player_list')
        insertData('psl_t20','psl_player_list',data)


        sorted_data = data.groupby('Player Type').apply(pd.DataFrame.sort,'Overall_rating',ascending=[False])
        # This will drop the column created after grouping the data
        sorted_data = sorted_data.reset_index(drop=True)

        print("Creating Platinum Category.")
        platinum_Category_Players = makePlatinumCategory(sorted_data)
        sorted_data = reducing_pslPlayers_list(platinum_Category_Players,sorted_data)
        print("Creating Diamond Category.")
        diamond_Category_Players = makeDiamondCategory(platinum_Category_Players,sorted_data)
        sorted_data = reducing_pslPlayers_list(diamond_Category_Players,sorted_data)
        print("Creating Gold Category.")
        gold_Category_Players = makeGoldCategory(diamond_Category_Players,sorted_data)
        sorted_data = reducing_pslPlayers_list(gold_Category_Players,sorted_data)
        # print("Creating Silver Category.")
        # silver_Category_Players = makeSilverCategory(gold_Category_Players,sorted_data)
        # sorted_data = reducing_pslPlayers_list(silver_Category_Players,sorted_data)
        # print("Creating Supplementory Category.")
        # supplementory_Category_Players = makeSupplementoryCategory(silver_Category_Players,sorted_data)
    else:
        print("Calculating overall Rating")
        for index_of_t20player, t20_player in t20_dataset.iterrows():
            for index_of_pslplayer, psl_player in psl_dataset.iterrows():
                if t20_player['Player'] == psl_player['PLAYER']:
                    t20_dataset.loc[index_of_t20player,'psl_rating'] = psl_player['RATING']
                    t20_dataset.loc[index_of_t20player,'Overall_rating'] = (t20_player['Rating']*0.7) + (psl_player['RATING']*0.3)

                else:
                    t20_dataset.loc[index_of_t20player,'Overall_rating'] = t20_player['Rating']*0.7
        t20_dataset.replace('NaN',0,inplace=True)

        data = getting_data_of_psl_Players(t20_dataset,matched_international_player)
        data.drop("_id",axis=1,inplace=True)
        delete_collection_from_db('psl_player_list')
        insertData('psl_t20','psl_player_list',data)
        print("Successfully inserted psl_player_list in Database.")
        sorted_data = data.groupby('Player_Type').apply(pd.DataFrame.sort,'Overall_rating',ascending=[False])
        # This will drop the column created after grouping the data
        sorted_data = sorted_data.reset_index(drop=True)

        print("Creating Platinum Category.")
        platinum_Category_Players = makePlatinumCategory(sorted_data)
        sorted_data = reducing_pslPlayers_list(platinum_Category_Players,sorted_data)
        print("Creating Diamond Category.")
        diamond_Category_Players = makeDiamondCategory(platinum_Category_Players,sorted_data)
        sorted_data = reducing_pslPlayers_list(diamond_Category_Players,sorted_data)
        print("Creating Gold Category.")
        gold_Category_Players = makeGoldCategory(diamond_Category_Players,sorted_data)
        sorted_data = reducing_pslPlayers_list(gold_Category_Players,sorted_data)
        # print("Creating Silver Category.")
        # silver_Category_Players = makeSilverCategory(gold_Category_Players,sorted_data)
        # sorted_data = reducing_pslPlayers_list(silver_Category_Players,sorted_data)
        # print("Creating Supplementory Category.")
        # supplementory_Category_Players = makeSupplementoryCategory(silver_Category_Players,sorted_data)

print("Python Code.")
process_psl_PlayerList()
