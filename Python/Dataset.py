import numpy as np;
import pandas as pd;
import sys;
from bs4 import BeautifulSoup
import urllib.request
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from odo import odo

# Imports for Mongo Database
from pymongo import MongoClient
def T20_dataset(collectionName):

    print("Downloading dataset...")
    batting_records = []
    link = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=3;template=results;type=batting"
    i = 2

    list_of_title = getting_Title(link)

    while i < 23:
        print(link)
        page = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(page,'html.parser')
        table = soup.find_all('table')[2]
        for row in table.find_all('tr',class_="data1"):
            cells = []
            for cell in row.find_all('td'):
                cells.append(cell.get_text())

            batting_records.append(cells)

        link = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=3;page=" + str(i) + ";template=results;type=batting"
        i += 1
    t20_batting_dataset = cleaning_data(batting_records,list_of_title)
    print("Batting Data downloaded.")


    bowling_records = []
    link = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=3;template=results;type=bowling"
    i=2
    list_of_title = getting_Title(link)
    while i < 23:
        print(link)
        page = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(page,'html.parser')
        table = soup.find_all('table')[2]
        for row in table.find_all('tr', class_="data1"):
            cells = []
            for cell in row.find_all('td'):
                cells.append(cell.get_text())
            bowling_records.append(cells)

        link = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=3;page=" + str(i) + ";template=results;type=bowling"
        i += 1

    t20_bowling_dataset = cleaning_data(bowling_records,list_of_title)
    print("Bownling Data downloaded.")


    fielding_records = []
    link = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=3;template=results;type=fielding"
    i=2
    list_of_title = getting_Title(link)
    while i < 23:
        print(link)
        page = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(page,'html.parser')
        table = soup.find_all('table')[2]
        for row in table.find_all('tr',class_="data1"):
            cells = []
            for cell in row.find_all('td'):
                cells.append(cell.get_text())

            fielding_records.append(cells)
        link = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=3;page=" + str(i) + ";template=results;type=fielding"
        i += 1

    t20_fielding_dataset = cleaning_data(fielding_records,list_of_title)
    print("Fielding Data downloaded.")

    # Merging Bowling and Batting dataset
    for batsman in range(len(t20_batting_dataset)):
        for bowler in range(len(t20_bowling_dataset)):
            if t20_batting_dataset['Player'][batsman] == t20_bowling_dataset['Player'][bowler]:
                t20_batting_dataset.loc[batsman,'Bowling_Inns'] = t20_bowling_dataset['Inns'][bowler]
                t20_batting_dataset.loc[batsman,'Overs'] = t20_bowling_dataset['Overs'][bowler]
                t20_batting_dataset.loc[batsman,'Middens'] = t20_bowling_dataset['Mdns'][bowler]
                t20_batting_dataset.loc[batsman,'Runs_Given'] = t20_bowling_dataset['Runs'][bowler]
                t20_batting_dataset.loc[batsman,'Wickets'] = t20_bowling_dataset['Wkts'][bowler]
                t20_batting_dataset.loc[batsman,'BBI'] = t20_bowling_dataset['BBI'][bowler]
                t20_batting_dataset.loc[batsman,'Bowling_Avg'] = t20_bowling_dataset['Ave'][bowler]
                t20_batting_dataset.loc[batsman,'Econ'] = t20_bowling_dataset['Econ'][bowler]
                t20_batting_dataset.loc[batsman,'SR_Bowl'] = t20_bowling_dataset['SR'][bowler]
                t20_batting_dataset.loc[batsman,'4'] = t20_bowling_dataset['4'][bowler]
                t20_batting_dataset.loc[batsman,'5'] = t20_bowling_dataset['5'][bowler]

    t20_batting_dataset = cleaning_data(t20_batting_dataset, None)

    # Merging Fielding dataset
    for batsman in range(len(t20_batting_dataset)):
        for fielding in range(len(t20_fielding_dataset)):
            if t20_batting_dataset['Player'][batsman] == t20_fielding_dataset['Player'][fielding]:
                t20_batting_dataset.loc[batsman,'Dismis'] = t20_fielding_dataset['Dis'][fielding]
                t20_batting_dataset.loc[batsman,'Ct'] = t20_fielding_dataset['Ct'][fielding]
                t20_batting_dataset.loc[batsman,'St'] = t20_fielding_dataset['St'][fielding]
                t20_batting_dataset.loc[batsman,'D/I'] = t20_fielding_dataset['D/I'][fielding]

    t20_batting_dataset = cleaning_data(t20_batting_dataset, None)
    print("\n\nClassifying dataset")
    t20_dataset = classify_players(t20_batting_dataset)

    # Inserting Country name into the dataset
    for index,player in t20_dataset.iterrows():
        fullname = player['Player']
        countryName = fullname.split(" ")[-1]
        name_withoutCountry = ' '.join(fullname.split(' ')[:-1])
        t20_dataset.loc[index,'Country'] = countryName
        t20_dataset.loc[index,'Player'] = name_withoutCountry


    """ ADDING PSL_RATING IN T20_DATASET """

    print('Add PSL Rating in T20 dataset')
    """ first check if collection exist (psl_dataset) then download from database"""
    if is_Collection_Exits('psl_dataset'):
        print('Load PSL_Dataset from Database & then add psl_rating in t20_dataset')
        psl_dataset = loadingData('psl_t20','psl_dataset')
        t20_dataset_with_pslRating = add_psl_Dataset_in_t20_dataset(t20_dataset, psl_dataset)
    else:
        if is_Collection_Exits('psl_dataset') == False:
            print('First Scrap the PSL Dataset then add PSL Rating in t20 Dataset')
            PSL_dataset()

            print('PSL Collection exist in DB')
            psl_dataset = loadingData('psl_t20','psl_dataset')
            t20_dataset_with_pslRating = add_psl_Dataset_in_t20_dataset(t20_dataset, psl_dataset)

    """ END """


    delete_collection_from_db(collectionName)
    insertData('psl_t20',collectionName,t20_dataset_with_pslRating)
    print("Successfully inserted in DB.")
def PSL_dataset():

    batting_list = []
    bowling_list = []

    """ CALLING METHODS SECTION """
    # METHODS CALL
    # PSL BATTING DATASET 2015-16
    print('Downloading PSL Dataset...')
    url = 'http://stats.espncricinfo.com/pakistan-super-league-2015-16/engine/records/averages/batting.html?id=10555;type=tournament'
    # """ Saving temporarily in dataframe """
    psl_batting_2015_16 = grab_PSL_data(url)
    psl_batting_2015_16 = check_column_type_psl(psl_batting_2015_16)
    batting_list.append(psl_batting_2015_16)

    # PSL BOWLING DATASET 2015-16
    url = 'http://stats.espncricinfo.com/pakistan-super-league-2015-16/engine/records/averages/bowling.html?id=10555;type=tournament'
    # """ Saving temporarily in dataframe """
    psl_bowling_2015_16 = grab_PSL_data(url)
    psl_bowling_2015_16 = check_column_type_psl(psl_bowling_2015_16)
    bowling_list.append(psl_bowling_2015_16)

    # PSL BATTING DATASET 2016-17
    url = 'http://stats.espncricinfo.com/pakistan-super-league-2016-17/engine/records/averages/batting.html?id=11673;type=tournament'
    # """ Saving temporarily in dataframe """
    psl_batting_2016_17 = grab_PSL_data(url)
    psl_batting_2016_17 = check_column_type_psl(psl_batting_2016_17)
    batting_list.append(psl_batting_2016_17)


    # PSL BOWLING DATASET 2016-17
    url = 'http://stats.espncricinfo.com/pakistan-super-league-2016-17/engine/records/averages/bowling.html?id=11673;type=tournament'
    # """ Saving temporarily in dataframe """
    psl_bowling_2016_17 = grab_PSL_data(url)
    psl_bowling_2016_17 = check_column_type_psl(psl_bowling_2016_17)
    bowling_list.append(psl_bowling_2016_17)
    print('Data Downloaded.')

    # Call method to add Batting data of all season
    print('Merging the dataset in ome file...')
    psl_player_batting_records = recursive_merge_psl_batting(batting_list)

    # Call method to add Bowling data of all season
    psl_player_bowling_records = recursive_merge_psl_bowling(bowling_list)

    # Call Method for merging batting & bowling dataset

    psl_dataset = merge_PSL_batting_bowling_data(psl_player_batting_records, psl_player_bowling_records)
    print(psl_dataset)

    print('Classifying the Dataset....')
    psl_classified_data = classification_of_players(psl_dataset)
    print('Inserting data in database....')
    delete_collection_from_db('psl_dataset')
    insertData('psl_t20', 'psl_dataset', psl_classified_data)
    print('Data successfully inserted...')
    
def Domestic_dataset():
    print("Domestic Dataset")
    domestic_batting_list = []
    domestic_bowling_list = []

    """ Cool&Cool Haier T20 Cup 2105 """
    """ Batting """
    print('Downloading Cool&Cool Haier T20 Cup 2105 BAtting & Bowling Datset ')
    cool_t20_batting_data_2015 = grab_Domestic_data("Cool_and_Cool_Presents_Haier_Super_Eight_T-20_Cup_2015/Batting_by_Average.html")
    """ String(remove) the new line from ave column"""
    cool_t20_batting_data_2015 = cool_t20_batting_data_2015.apply(lambda x: x.str.strip()).replace('', 0)
    cool_t20_batting_data_2015 = check_column_type_domestic(cool_t20_batting_data_2015)
    cool_t20_batting_data_2015 = removeTeam_Name(cool_t20_batting_data_2015)
    domestic_batting_list.append(cool_t20_batting_data_2015)

    """ Bowling """
    cool_t20_bowling_data_2015 = grab_Domestic_data("Cool_and_Cool_Presents_Haier_Super_Eight_T-20_Cup_2015/Bowling_by_Average.html")
    """ String(remove) the new line from ave column"""
    cool_t20_bowling_data_2015 = cool_t20_bowling_data_2015.apply(lambda x: x.str.strip()).replace('', 0)
    cool_t20_bowling_data_2015 = check_column_type_domestic(cool_t20_bowling_data_2015)
    cool_t20_bowling_data_2015 = removeTeam_Name(cool_t20_bowling_data_2015)
    domestic_bowling_list.append(cool_t20_bowling_data_2015)
    print('Successfully grab!')

    """ Cool&Cool Haier T20 Cup 2105-16 """
    """ Batting """
    print('Downloading Cool&Cool Haier T20 Cup 2105-16 Batting & Bowling Datset ')
    cool_t20_batting_data_2015_16 = grab_Domestic_data("Cool_and_Cool_Presents_Haier_Mobile_T-20_Cup_2015-16/Batting_by_Average.html")
    """ String(remove) the new line from ave column"""
    cool_t20_batting_data_2015_16 = cool_t20_batting_data_2015_16.apply(lambda x: x.str.strip()).replace('', 0)
    cool_t20_batting_data_2015_16 = check_column_type_domestic(cool_t20_batting_data_2015_16)
    cool_t20_batting_data_2015_16 = removeTeam_Name(cool_t20_batting_data_2015_16)
    domestic_batting_list.append(cool_t20_batting_data_2015_16)

    """ Bowling """
    cool_t20_bowling_data_2015_16 = grab_Domestic_data("Cool_and_Cool_Presents_Haier_Mobile_T-20_Cup_2015-16/Bowling_by_Average.html")
    """ String(remove) the new line from ave column"""
    cool_t20_bowling_data_2015_16 = cool_t20_bowling_data_2015_16.apply(lambda x: x.str.strip()).replace('', 0)
    cool_t20_bowling_data_2015_16 = check_column_type_domestic(cool_t20_bowling_data_2015_16)
    cool_t20_bowling_data_2015_16 = removeTeam_Name(cool_t20_bowling_data_2015_16)
    domestic_bowling_list.append(cool_t20_bowling_data_2015_16)

    """ Bank Al-Baraka T20 Cup 2104-15 """
    """ Batting """
    print('Downloading Bank Al-Baraka T20 Cup 2104-15 Batting & Bowling Datset ')
    al_baraka_t20_batting_data_2014_15 = grab_Domestic_data("Bank_Albaraka_Presents_Haier_T20_Cup_2014-15/Batting_by_Average.html")
    """ String(remove) the new line from ave column"""
    al_baraka_t20_batting_data_2014_15 = al_baraka_t20_batting_data_2014_15.apply(lambda x: x.str.strip()).replace('', 0)
    al_baraka_t20_batting_data_2014_15 = check_column_type_domestic(al_baraka_t20_batting_data_2014_15)
    al_baraka_t20_batting_data_2014_15 = removeTeam_Name(al_baraka_t20_batting_data_2014_15)
    domestic_batting_list.append(al_baraka_t20_batting_data_2014_15)

    """ Bowling """
    al_baraka_t20_bowling_data_2014_15 = grab_Domestic_data("Bank_Albaraka_Presents_Haier_T20_Cup_2014-15/Bowling_by_Average.html")
    """ String(remove) the new line from ave column"""
    al_baraka_t20_bowling_data_2014_15 = al_baraka_t20_bowling_data_2014_15.apply(lambda x: x.str.strip()).replace('', 0)
    al_baraka_t20_bowling_data_2014_15 = check_column_type_domestic(al_baraka_t20_bowling_data_2014_15)
    al_baraka_t20_bowling_data_2014_15 = removeTeam_Name(al_baraka_t20_bowling_data_2014_15 )
    domestic_bowling_list.append(al_baraka_t20_bowling_data_2014_15)
    print('Dataset Successfully Downloaded!')

    print('Adding Domestic T20 Batting Dataset ')
    domestic_player_batting_records = recursive_merge_domestic_batting(domestic_batting_list)
    print('Adding Domestic Bowling Dataset ')
    domestic_player_bowling_records = recursive_merge_domestic_bowling(domestic_bowling_list)
    print('Merging Batting and Bowling Datset')
    domestic_dataset = merge_domestic_batting_bowling_data(domestic_player_batting_records, domestic_player_bowling_records)
    print('Classifying Players')
    domestic_data_classification = classify_players_domestic(domestic_dataset)
    categories_data = assigning_categories(domestic_data_classification)
    data = merge_classified_data(domestic_data_classification, categories_data)
    print('Assinging Rating')
    rated_data = assigning_rating(data)
    
    rated_data = rated_data.rename(columns = {'NAME':'Player', 'PLAYER TYPE':'Player Type', 'RATING': 'Rating'})
    delete_collection_from_db('domestic_dataset')
    insertData('psl_t20', 'domestic_dataset', rated_data)
    print(rated_data)

""" PSL DATASET METHODS """
# Function for Downloading Dataset
def grab_PSL_data(url):
    list_of_rows = []
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, 'lxml')

    # """ For Title of Tabel """
    head = soup.find_all('tr', class_='head')
    list_of_title = []
    for title in soup.find_all('th'):
        list_of_title.append(title.get_text().upper())

    # """ Now Grap data from table body """
    table = soup.find('table', class_='engineTable')
    body = table.find('tbody')

    for row in body.find_all('tr', class_='data2'):
        list_of_cells= []
        for cell in row.find_all('td'):
            list_of_cells.append(cell.get_text())
        list_of_rows.append(list_of_cells)

    # """ Make DataFrame """
    dataset = pd.DataFrame(list_of_rows, columns=list_of_title)

    # """ Replace '-' with'0' """
    dataset = dataset.replace('-', 0)
    dataset.dropna(axis=1,how='all')

    return dataset
# Check dataframe's column datatype
def check_column_type_psl(df):
    for c in df.columns:
        if 'MATCHES' in c or 'MAT' in c or 'MATCH' in c or 'INNS' in c or 'INNINGS' in c or 'INNING' in c or 'INS' in c or 'NOT OUT' in c or 'NO' in c or 'NT' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'RUNS' in c or 'RUN' in c or 'RUNS CONCD' in c or 'RNS' in c or 'RUNS CONCEDED' in c or 'RUNS_CONCEDED' in c or 'BF' in c or 'BALL FACED' in c or 'BALLS FACED' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'AVE' in c or 'AVG' in c or 'AVERAGE' in c or 'BOWLING AVE' in c or 'OVERS' in c or 'OVRS' in c or 'ORS' in c or 'OVER' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')

        if 'SRATE' in c or 'SR' in c or 'STRIKE RATE' in c or 'S RATE' in c or 'S_RATE' in c or 'BOWLING SRATE' in c or 'ECON' in c or 'BOWLING ECON' in c or 'ECONOMY' in c or 'BOWLING ECONOMY' in c or 'ECON RATE' in c or 'ECONOMY RATE' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')

        if '100' in c or '100s' in c or 'HUNDREDS' in c or '4S' in c or 'FOURS' in c or '4' in c or '6S' in c or 'SIXES' in c or '6' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if '50' in c or '50s' in c or 'FIFTIES' in c or '0' in c or '0S' in c or 'ZERO' in c or 'ZEROS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        """ Bowling Type """
        if 'CT' in c or 'CATCHES' in c or 'CTS' in c or 'ST' in c or 'STUMPS' in c or 'STS' in c or 'MDNS' in c or 'MADIENS' in c or 'MADIEN' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'WKTS' in c or 'WICKETS' in c or 'WKTS TAKEN' in c or 'WKTS_TICKENS' in c or 'WICKETS TAKEN' in c or 'WICKETS_TAKEN' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')


        if '4' in c or '4WI' in c or '4 WKTS' in c or '4-WKTS' in c or '4-WICKETS' in c or '5' in c or '5WI' in c or '5 WKTS' in c or '5-WKTS' in c or '5-WICKETS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

    return df
    # End of function
# Add Batting Dataset of All PSL season to make one file
def recursive_merge_psl_batting(file):
    matched_player = []
    Batting_dataset_1 = file[0]
    Batting_dataset_2 = file[1]
    file.remove(file[0])
    file.remove(file[0])

    for index_1, batsman_1 in Batting_dataset_1.iterrows():
        for index_2, batsman_2 in Batting_dataset_2.iterrows():
            if (batsman_1[0] == batsman_2[0]):
                mat = batsman_1[1] + batsman_2[1]
                inns = batsman_1[2] + batsman_2[2]
                no = batsman_1[3] + batsman_2[3]
                runs = batsman_1[4] + batsman_2[4]
                bf = batsman_1[7] + batsman_2[7]
                hundreds = batsman_1[9] + batsman_2[9]
                fifties = batsman_1[10] + batsman_2[10]
                zeros = batsman_1[11] + batsman_2[11]
                fours = batsman_1[12] + batsman_2[12]
                sixes = batsman_1[13] + batsman_2[13]

                times_out = (inns-no)
                if times_out > 0:
                    ave = round((runs)/times_out, 2)
                else:
                    if times_out <= 0:
                        ave = 0.0

                if bf > 0.0 or bf > 0:
                    sr = round((runs/bf)*100, 2)
                else:
                    if bf <= 0.0 or bf <= 0:
                        sr = 0.0

                Batting_dataset_1.loc[index_1, 'MAT'] = mat
                Batting_dataset_1.loc[index_1, 'INNS'] = inns
                Batting_dataset_1.loc[index_1, 'NO'] = no
                Batting_dataset_1.loc[index_1, 'RUNS'] = runs
                Batting_dataset_1.loc[index_1, 'AVE'] = ave
                Batting_dataset_1.loc[index_1, 'BF'] = bf
                Batting_dataset_1.loc[index_1, 'SR'] = sr
                Batting_dataset_1.loc[index_1, '100'] = hundreds
                Batting_dataset_1.loc[index_1, '50'] = fifties
                Batting_dataset_1.loc[index_1, '0'] = zeros
                Batting_dataset_1.loc[index_1, '4S'] = fours
                Batting_dataset_1.loc[index_1, '6S'] = sixes
                matched_player.append(Batting_dataset_2.loc[index_2])

    """ Now drop the player that are matched """
    for match_player in matched_player:
        for index, batsman_ in Batting_dataset_2.iterrows():
            if match_player[0] == batsman_[0]:
                Batting_dataset_2.drop(index, inplace=True)

    """ This is the end of drop matched player code """

    """ This code is for appending un-matched player to end of csv file """
    """ Because boht files are same thats why append the whole dataframe to first dataframe """
    Batting_dataset_1 = Batting_dataset_1.append(Batting_dataset_2, ignore_index=True)

    """  This is end of that code """

    if len(file) <= 0:
        return Batting_dataset_1
    elif len(file) >= 1:
        Batting_dataset_2 = file[0]
        file.remove(file[0])
        file.append(Batting_dataset_1)
        file.append(Batting_dataset_2)
        return recursive_merge_psl_batting(file)

    return Batting_dataset_1
    # End of method
# Add Bowling Dataset of All PSL season to make one file
def recursive_merge_psl_bowling(file):
    matched_player = []
    Bowling_dataset_1 = file[0]
    Bowling_dataset_2 = file[1]
    file.remove(file[0])
    file.remove(file[0])

    for index_1, bowler_1 in Bowling_dataset_1.iterrows():
        for index_2, bowler_2 in Bowling_dataset_2.iterrows():
            if (bowler_1[0] == bowler_2[0]):
                mat = bowler_1[1] + bowler_2[1]
                inns = bowler_1[2] + bowler_2[2]
                overs = bowler_1[3] + bowler_2[3]
                madiens = bowler_1[4]  + bowler_2[4]
                runs = bowler_1[5] + bowler_2[5]
                wkts = bowler_1[6] + bowler_2[6]
                fours_wkts = bowler_1[11] + bowler_2[11]
                fives_wkts = bowler_1[12] + bowler_2[12]
                ct = bowler_1[13] + bowler_2[13]
                st = bowler_1[14] + bowler_2[14]

                if wkts > 0 or wkts > 0.0:
                    avg = round((runs/wkts), 2)
                    srate = round(((overs*6)/wkts), 2)
                else:
                    if wkts <= 0 or wkts <= 0.0:
                        avg = 0.0
                        srate = 0.0

                if overs > 0 or overs > 0.0:
                    econ = round((runs/overs), 2)
                else:
                    if overs <= 0 or overs <= 0.0:
                        econ = 0.0

                Bowling_dataset_1.loc[index_1, 'MAT'] = mat
                Bowling_dataset_1.loc[index_1, 'INNS'] = inns
                Bowling_dataset_1.loc[index_1, 'OVERS'] = overs
                Bowling_dataset_1.loc[index_1, 'MDNS'] = madiens
                Bowling_dataset_1.loc[index_1, 'RUNS'] = runs
                Bowling_dataset_1.loc[index_1, 'WKTS'] = wkts
                Bowling_dataset_1.loc[index_1, 'AVE'] = avg
                Bowling_dataset_1.loc[index_1, 'ECON'] = econ
                Bowling_dataset_1.loc[index_1, 'SR'] = srate
                Bowling_dataset_1.loc[index_1, '4'] = fours_wkts
                Bowling_dataset_1.loc[index_1, '5'] = fives_wkts
                Bowling_dataset_1.loc[index_1, 'CT'] = ct
                Bowling_dataset_1.loc[index_1, 'ST'] = st
                matched_player.append(Bowling_dataset_2.loc[index_2])

    """ Now drop the player that are matched """
    for match_player in matched_player:
        for index, bowler_ in Bowling_dataset_2.iterrows():
            if match_player[0] == bowler_[0]:
                Bowling_dataset_2.drop(index, inplace=True)
    """ This is the end of drop matched player code """


    """ This code is for appending un-matched player to end of csv file """
    """ Because boht files are same thats why append the whole dataframe to first dataframe """
    Bowling_dataset_1 = Bowling_dataset_1.append(Bowling_dataset_2, ignore_index=True)

    """  This is end of that code """

    if len(file) <= 0:
        return Bowling_dataset_1

    elif len(file) >= 1:
        Bowling_dataset_2 = file[0]
        file.remove(file[0])
        file.append(Bowling_dataset_1)
        file.append(Bowling_dataset_2)
        return recursive_merge_psl_bowling(file)

    return Bowling_dataset_1
    # End of Method
    # END OF SECTION 2
# SECTION 3
# Merging Batting & Bowling Files to make one file
def merge_PSL_batting_bowling_data(psl_batting_data, psl_bowling_data):
    Batting_dataset = psl_batting_data
    Bowling_dataset = psl_bowling_data

    for index_1, batsmen in Batting_dataset.iterrows():
        for index_2, bowler in Bowling_dataset.iterrows():
            if (batsmen[0] == bowler[0]):
                Batting_dataset.loc[index_1, 'BOWLING INNS'] = bowler[2]
                Batting_dataset.loc[index_1, 'OVERS'] = bowler[3]
                Batting_dataset.loc[index_1, 'MDNS'] = bowler[4]
                Batting_dataset.loc[index_1, 'RUNS CONCEDED'] = bowler[5]
                Batting_dataset.loc[index_1, 'WKTS'] = bowler[6]
                Batting_dataset.loc[index_1, 'BBI'] = bowler[7]
                Batting_dataset.loc[index_1, 'BOWLING AVE'] = bowler[8]
                Batting_dataset.loc[index_1, 'ECON'] = bowler[9]
                Batting_dataset.loc[index_1, 'BOWLING SR'] = bowler[10]
                Batting_dataset.loc[index_1, '4WI'] = bowler[11]
                Batting_dataset.loc[index_1, '5WI'] = bowler[12]
                Batting_dataset.loc[index_1, 'CT'] = bowler[13]
                Batting_dataset.loc[index_1, 'ST'] = bowler[14]


    """ Now replace NaN with 0 """
    Batting_dataset = Batting_dataset.fillna(0)

    return Batting_dataset
    # END of method
    # END OF SECTION 3
    
""" Feature Engineering """
def classification_of_players(dataset):
    feature1 = dataset['RUNS'].values
    feature2 = dataset['SR'].values
    feature3 = dataset['50'].values

    feature4 = dataset['WKTS'].values
    feature5 = dataset['ST'].values
    feature6 = dataset['BOWLING SR'].values
    feature7 = dataset['ECON'].values
    feature8 = dataset['OVERS'].values
    feature9 = dataset['BOWLING AVE'].values
    feature10 = dataset['AVE'].values + dataset['SR'].values
    feature11 = dataset['BOWLING AVE'].values + dataset['BOWLING SR'].values + dataset['ECON'].values
    feature12 = dataset['CT'].values

    """ Standardization """
    X = np.column_stack((feature1,feature2,feature3,feature4,feature5,feature6,feature7,feature8,feature9,feature10,
                         feature11,feature12))
    X_std = StandardScaler().fit_transform(X)

    """ Applying K-MEANS on dataset """
    model = KMeans(n_clusters=5, random_state=0).fit(X_std)

    cluster1_playerList = dataset[model.labels_==0][['PLAYER','RUNS','WKTS','ST','CT','100','ECON']]
    cluster2_playerList = dataset[model.labels_==1][['PLAYER','RUNS','WKTS','ST','CT','100', 'ECON']]
    cluster3_playerList = dataset[model.labels_==2][['PLAYER','RUNS','WKTS','ST','CT','100', 'ECON']]
    cluster4_playerList = dataset[model.labels_==3][['PLAYER','RUNS','WKTS','ST','CT','100', 'ECON']]
    cluster5_playerList = dataset[model.labels_==4][['PLAYER','RUNS','WKTS','ST','CT','100', 'ECON']]
    """ Now Assigning Categories to Players """
    for index, player in dataset.iterrows():
        for indexx, row in cluster1_playerList.iterrows():
            if player['PLAYER'] == row[0]:
                dataset.loc[index,'PLAYER TYPE'] = 'Bowler'

    for index, player in dataset.iterrows():
        for indexx, row in cluster2_playerList.iterrows():
            if player['PLAYER'] == row[0]:
                dataset.loc[index,'PLAYER TYPE'] = 'Batsman'

    for index, player in dataset.iterrows():
        for indexx, row in cluster3_playerList.iterrows():
            if player['PLAYER'] == row[0]:
                dataset.loc[index,'PLAYER TYPE'] = 'Allrounder'

    for index, player in dataset.iterrows():
        for indexx, row in cluster4_playerList.iterrows():
            if player['PLAYER'] == row[0]:
                dataset.loc[index,'PLAYER TYPE'] = 'Wicket keeper Batsman'

    for index, player in dataset.iterrows():
        for indexx, row in cluster5_playerList.iterrows():
            if player['PLAYER'] == row[0]:
                dataset.loc[index,'PLAYER TYPE'] = 'Batting Allrounder'


    """ PALYER'S CLASSIFICATION CRITERIA """
    """ ALL-ROUNDERS 66% BAT & BOWL """
    for index,player in dataset.iterrows():
        dataset.loc[index,'BATTING PERC']=round((player['INNS']*100)/player['MAT'],1)
        dataset.loc[index,'BOWLING PERC']=round((player['BOWLING INNS']*100)/player['MAT'],1)

    print('Assigning Categories to players')
    for index,player in dataset.iterrows():
        if player['ST'] >= 1 or player['ST'] >= 1.0:
            dataset.loc[index,'PLAYER TYPE'] = 'Wicket keeper Batsman'
            print(player[['PLAYER', 'ST']])
        
        if player['BATTING PERC'] >= 66.0 and player['BOWLING PERC'] >= 66.0:
            dataset.loc[index,'PLAYER TYPE'] = 'Allrounder'


        if player['BOWLING INNS'] == 0.0 and player['ST'] == 0:
            dataset.loc[index,'PLAYER TYPE'] = 'Batsman'

        if player['BOWLING PERC'] >= 85.0:
            if player['BATTING PERC'] < 20.0:
                dataset.loc[index,'PLAYER TYPE'] = 'Bowler'


        if player['INNS'] == 0.0 or player['INNS'] == 0:
            dataset.loc[index,'PLAYER TYPE'] = 'Bowler'

        if player['PLAYER TYPE'] == 'Batting Allrounder' or player['PLAYER TYPE'] == 'Allrounder':
            if player['BATTING PERC'] >= 85.0 and player['BOWLING PERC'] <=20.0:
                dataset.loc[index,'PLAYER TYPE'] = 'Batsman'

        if player['PLAYER TYPE'] == 'Bowler' or player['PLAYER TYPE'] == 'Bowling Allrounder' or player['PLAYER TYPE'] == 'Allrounder':
            if player['BATTING PERC'] >= 66.0 and player['BOWLING PERC'] < 66.0 and player['BOWLING PERC'] > 20.0:
                dataset.loc[index,'PLAYER TYPE'] = 'Batting Allrounder'

        if player['BATTING PERC'] > 30.0 and player['BATTING PERC'] < 66.0 and player['BOWLING PERC'] > 66.0:
            dataset.loc[index,'PLAYER TYPE'] = 'Bowling Allrounder'

    print('Set of Rules for assigning categories to players.')
    """ NOW ASSIGNING RATING TO BATSMAN, BOWLER, ALL ROUNDER """
    print("Assigning Batting, Bowling and Experience Point")
    for index,player in dataset.iterrows():
        if player['PLAYER TYPE'] == 'Batsman' or player['PLAYER TYPE'] == 'Wicket keeper Batsman':
            dataset.loc[index,'PBT'] = (player['SR'] * 0.4) + (player['AVE'] * 0.3) + (player['50'] * 0.2) + (player['100'] * 0.1)
            dataset.loc[index,'PBW'] = 0.0
            dataset.loc[index, 'PEX'] = player['INNS']

        elif player['PLAYER TYPE'] == 'Bowler':
            dataset.loc[index,'PBT'] = 0.0
            dataset.loc[index,'PBW'] = (player['ECON'] * 0.4) + (player['BOWLING SR'] * 0.3) + (player['4WI'] * 0.2) + (player['5WI'] * 0.1)
            dataset.loc[index, 'PEX'] = player['BOWLING INNS']

        elif player['PLAYER TYPE'] == 'Allrounder':
            dataset.loc[index,'PBT'] = ((player['SR'] * 0.4) + (player['AVE'] * 0.3) + (player['50'] * 0.2) + (player['100'] * 0.1))*0.5
            dataset.loc[index,'PBW'] = ((player['ECON'] * 0.4) + (player['BOWLING SR'] * 0.3) + (player['4WI'] * 0.2) + (player['5WI'] * 0.1))*0.5
            dataset.loc[index, 'PEX'] = player['INNS'] + player['BOWLING INNS']

        elif player['PLAYER TYPE'] == 'Batting allrounder' or player['PLAYER TYPE'] == 'Batting Allrounder':
            dataset.loc[index,'PBT'] = ((player['SR'] * 0.4) + (player['AVE'] * 0.3) + (player['50'] * 0.2) + (player['100'] * 0.1))*0.8
            dataset.loc[index,'PBW'] = ((player['ECON'] * 0.4) + (player['BOWLING SR'] * 0.3) + (player['4WI'] * 0.2) + (player['5WI'] * 0.1))*0.2
            dataset.loc[index, 'PEX'] = player['INNS'] + player['BOWLING INNS']

        elif player['PLAYER TYPE'] == 'Bowling allrounder' or player['PLAYER TYPE'] == 'Bowling Allrounder':
            dataset.loc[index,'PBT'] = ((player['SR'] * 0.4) + (player['AVE'] * 0.3) + (player['50'] * 0.2) + (player['100'] * 0.1))*0.2
            dataset.loc[index,'PBW'] = ((player['ECON'] * 0.4) + (player['BOWLING SR'] * 0.3) + (player['4WI'] * 0.2) + (player['5WI'] * 0.1))*0.8
            dataset.loc[index, 'PEX'] = player['INNS'] + player['BOWLING INNS']

    print('Now Assigning Rating on basis of PBT, PBW and PEX')        
    for index,player in dataset.iterrows():
        if player['PLAYER TYPE'] == 'Batsman' or player['PLAYER TYPE'] == 'Wicket keeper Batsman':
            dataset.loc[index, 'RATING'] = (player['PBT']*0.8) + (player['PEX']*0.2)
        elif player['PLAYER TYPE'] == 'Bowler':
            dataset.loc[index, 'RATING'] = (player['PBW']*0.8) + (player['PEX']*0.2)
        elif player['PLAYER TYPE'] == 'Allrounder':
            dataset.loc[index, 'RATING'] = (player['PBT']*0.4) + (player['PBW']*0.4) + (player['PEX']*0.2)
        elif player['PLAYER TYPE'] == 'Batting allrounder' or player['PLAYER TYPE'] == 'Batting Allrounder':
            dataset.loc[index, 'RATING'] = (player['PBT']*0.6) + (player['PBW']*0.2) + (player['PEX']*0.2)
        elif player['PLAYER TYPE'] == 'Bowling allrounder' or player['PLAYER TYPE'] == 'Bowling Allrounder':
            dataset.loc[index, 'RATING'] = (player['PBT']*0.2) + (player['PBW']*0.6) + (player['PEX']*0.2)
            
    
    return dataset

    """ END OF SECTION 4 """

""" Domestic Dataset Method """
def add_psl_Dataset_in_t20_dataset(t20_dataset, psl_dataset):
    for t20player_index, t20_player in t20_dataset.iterrows():
        for pslplayer_index, psl_player in psl_dataset.iterrows():
            if t20_player['Player'] == psl_player['PLAYER']:
                pslrating = psl_player['RATING']
                t20_dataset.loc[t20player_index,'psl_rating'] = pslrating
                t20_dataset.loc[t20player_index,'Overall_rating'] = (t20_player['Rating']*0.6) + (psl_player['RATING']*0.4)
                break;
            else:
                t20_dataset.loc[t20player_index,'Overall_rating'] = t20_player['Rating']*0.6

    t20_dataset.replace('NaN',0,inplace=True)
    return t20_dataset
def grab_Domestic_data(link):

    records = []

    """ Make a complete link by combining event information provided in link argument of the function"""
    full_link = "http://www.pcboard.com.pk/Events/" + link

    page = urllib.request.urlopen(full_link).read()
    soup = BeautifulSoup(page,'html.parser')
    table = soup.find_all('table')[2]
    table = table.find_all('table')[5]

    """ For Title of Table """
    head = table.find('tr')
    list_of_title = []
    for title in head.find_all('td'):
        for title_name in title.find_all('b'):
            list_of_title.append(title_name.get_text().upper())

    """ For Body of Table """
    for row in table.find_all('tr'):
        cells = []
        for cell in row.find_all('td'):
            cells.append(cell.get_text())
        records.append(cells)

    """ Make a pandas's Dataframe """
    records = pd.DataFrame(records, columns=list_of_title)

    """ Replace '*' with "" """
    records.dropna(axis=1,how='all')
    """ Remove the first row from dataframe """
    records.drop(records.index[:1], inplace=True)

    return records
def check_column_type_domestic(df):
    for c in df.columns:
        if 'MATCHES' in c or 'MAT' in c or 'MATCH' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'INNS' in c or 'INNINGS' in c or 'INNING' in c or 'INS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'NOT OUT' in c or 'NO' in c or 'NT' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'RUNS' in c or 'RUN' in c or 'RNS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'AVE' in c or 'AVG' in c or 'AVERAGE' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')

        if 'SRATE' in c or 'SR' in c or 'STRIKE RATE' in c or 'S RATE' in c or 'S_RATE' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')

        if '100' in c or '100s' in c or 'HUNDREDS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if '50' in c or '50s' in c or 'FIFTIES' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'CT' in c or 'CATCHES' in c or 'CTS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'ST' in c or 'STUMPS' in c or 'STS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')


        """ Bowling Type """
        if 'BALLS' in c or 'BALL' in c or 'STS' in c or 'MDNS' in c or 'MADIENS' in c or 'MADIEN' in c or 'RUNS' in c or 'RUNS CONCD' in c or 'RNS' in c or 'RUNS CONCEDED' in c or 'RUNS_CONCEDED' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'WKTS' in c or 'WICKETS' in c or 'WKTS TAKEN' in c or 'WKTS_TICKENS' in c or 'WICKETS TAKEN' in c or 'WICKETS_TAKEN' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'AVE' in c or 'AVG' in c or 'AVERAGE' in c or 'BOWLING AVE' in c or 'SRATE' in c or 'SR' in c or 'STRIKE RATE' in c or 'S RATE' in c or 'S_RATE' in c or 'BOWLING SRATE' in c or 'ECON' in c or 'BOWLING ECON' in c or 'ECONOMY' in c or 'BOWLING ECONOMY' in c or 'ECON RATE' in c or 'ECONOMY RATE' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')

        if '4WI' in c or '4 WKTS' in c or '4-WKTS' in c or '4-WICKETS' in c or '5WI' in c or '5 WKTS' in c or '5-WKTS' in c or '5-WICKETS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

    return df
def recursive_merge_domestic_batting(file):
    matched_player = []
    Batting_dataset_1 = file[0]
    Batting_dataset_2 = file[1]
    file.remove(file[0])
    file.remove(file[0])

    for index_1, batsman_1 in Batting_dataset_1.iterrows():
        for index_2, batsman_2 in Batting_dataset_2.iterrows():
            if (batsman_1[0] == batsman_2[0]):
                mat = batsman_1[1] + batsman_2[1]
                inns = batsman_1[2]  + batsman_2[2]
                no = batsman_1[3] + batsman_2[3]
                runs = batsman_1[4] + batsman_2[4]
                sr = round(((batsman_1[7] + batsman_2[7])/2),2)
                hundreds = batsman_1[8] + batsman_2[8]
                fifties = batsman_1[9] + batsman_2[9]
                ct = batsman_1[10] + batsman_2[10]
                st = batsman_1[11] + batsman_2[11]

                times_out = (inns-no)
                if times_out > 0:
                    ave = round((runs)/times_out, 2)
                else:
                    if times_out <= 0:
                        ave = 0.0

                Batting_dataset_1.loc[index_1, 'MATCHES'] = mat
                Batting_dataset_1.loc[index_1, 'INNS'] = inns
                Batting_dataset_1.loc[index_1, 'NOT OUT'] = no
                Batting_dataset_1.loc[index_1, 'RUNS'] = runs
                Batting_dataset_1.loc[index_1, 'AVE'] = ave
                Batting_dataset_1.loc[index_1, 'SRATE'] = sr
                Batting_dataset_1.loc[index_1, '100'] = hundreds
                Batting_dataset_1.loc[index_1, '50'] = fifties
                Batting_dataset_1.loc[index_1, 'CT'] = ct
                Batting_dataset_1.loc[index_1, 'ST'] = st
                matched_player.append(Batting_dataset_2.loc[index_2])

    """ Now drop the player that are matched """
    for match_player in matched_player:
        for index, batsman_ in Batting_dataset_2.iterrows():
            if match_player[0] == batsman_[0]:
                Batting_dataset_2.drop(index, inplace=True)

    """ This is the end of drop matched player code """

    """ This code is for appending un-matched player to end of csv file """
    """ Because boht files are same thats why append the whole dataframe to first dataframe """
    Batting_dataset_1 = Batting_dataset_1.append(Batting_dataset_2, ignore_index=True)

    """  This is end of that code """

    if len(file) <= 0:
        return Batting_dataset_1
    elif len(file) >= 1:
        Batting_dataset_2 = file[0]
        file.remove(file[0])
        file.append(Batting_dataset_1)
        file.append(Batting_dataset_2)
        return recursive_merge_domestic_batting(file)

    return Batting_dataset_1
def recursive_merge_domestic_bowling(file):
    matched_player = []
    Bowling_dataset_1 = file[0]
    Bowling_dataset_2 = file[1]
    file.remove(file[0])
    file.remove(file[0])

    for index_1, bowler_1 in Bowling_dataset_1.iterrows():
        for index_2, bowler_2 in Bowling_dataset_2.iterrows():
            if (bowler_1[0] == bowler_2[0]):
                balls = bowler_1[1] + bowler_2[1]
                madiens = bowler_1[2]  + bowler_2[2]
                runs = bowler_1[3] + bowler_2[3]
                wkts = bowler_1[4] + bowler_2[4]
                fours_wkts = bowler_1[7] + bowler_2[7]
                fives_wkts = bowler_1[8] + bowler_2[8]

                if wkts > 0 or 0.0:
                    ave = round((runs/wkts), 2)
                    sr = round((balls/wkts), 2)
                else:
                    if wkts <= 0 or wkts <= 0.0:
                        ave = 0.0
                        sr = 0.0

                if balls > 0.0 or balls > 0:
                    """ Find number of overs from balls and then calculate economy rate """
                    no_of_balls_in_over = 6.0
                    quoient = int(balls/no_of_balls_in_over)
                    reminder = int(balls%no_of_balls_in_over)
                    overs = float(str(quoient)+"."+str(reminder))
                    econ = round((runs/overs), 2)
                else:
                    if balls <= 0 or balls <= 0.0:
                        econ = 0.0

                        #             print('SR of %s%d',bowler_1[0], sr)

                Bowling_dataset_1.loc[index_1, 'BALLS'] = balls
                Bowling_dataset_1.loc[index_1, 'MDNS'] = madiens
                Bowling_dataset_1.loc[index_1, 'RUNS'] = runs
                Bowling_dataset_1.loc[index_1, 'WKTS'] = wkts
                #                 Bowling_dataset_1.loc[index_1, 'BB'] = hs
                Bowling_dataset_1.loc[index_1, 'AVE'] = ave
                Bowling_dataset_1.loc[index_1, '4WI'] = fours_wkts
                Bowling_dataset_1.loc[index_1, '5WI'] = fives_wkts
                Bowling_dataset_1.loc[index_1, 'SRATE'] = sr
                Bowling_dataset_1.loc[index_1, 'ECON'] = econ
                matched_player.append(Bowling_dataset_2.loc[index_2])

    """ Now drop the player that are matched """
    for match_player in matched_player:
        for index, bowler_ in Bowling_dataset_2.iterrows():
            if match_player[0] == bowler_[0]:
                Bowling_dataset_2.drop(index, inplace=True)

    """ This is the end of drop matched player code """


    """ This code is for appending un-matched player to end of csv file """
    """ Because boht files are same thats why append the whole dataframe to first dataframe """
    Bowling_dataset_1 = Bowling_dataset_1.append(Bowling_dataset_2, ignore_index=True)

    """  This is end of that code """

    if len(file) <= 0:
        return Bowling_dataset_1

    elif len(file) >= 1:
        Bowling_dataset_2 = file[0]
        file.remove(file[0])
        file.append(Bowling_dataset_1)
        file.append(Bowling_dataset_2)
        return recursive_merge_domestic_bowling(file)

    return Bowling_dataset_1
def merge_domestic_batting_bowling_data(domestic_batting_data, domestic_bowling_data):

    Batting_dataset = domestic_batting_data
    Bowling_dataset = domestic_bowling_data

    for index_1, batsmen in Batting_dataset.iterrows():
        for index_2, bowler in Bowling_dataset.iterrows():
            if (batsmen[0] == bowler[0]):
                Batting_dataset.loc[index_1, 'BALLS'] = bowler[1]
                Batting_dataset.loc[index_1, 'MDNS'] = bowler[2]
                Batting_dataset.loc[index_1, 'RUNS CONCEDED'] = bowler[3]
                Batting_dataset.loc[index_1, 'WKTS'] = bowler[4]
                Batting_dataset.loc[index_1, 'BB'] = bowler[5]
                Batting_dataset.loc[index_1, 'BOWLING AVE'] = bowler[6]
                Batting_dataset.loc[index_1, '4WI'] = bowler[7]
                Batting_dataset.loc[index_1, '5WI'] = bowler[8]
                Batting_dataset.loc[index_1, 'BOWLING SR'] = bowler[9]
                Batting_dataset.loc[index_1, 'ECON'] = bowler[10]

    """ Now replace NaN with 0 """
    Batting_dataset = Batting_dataset.fillna(0)

    return Batting_dataset
def classify_players_domestic(dataset):
    #feature selection;
    #     feature1 = dataset['RUNS'].values
    feature2 = dataset['AVE'].values
    #     feature3 = dataset['100'].values
    feature4 = dataset['SRATE'].values
    feature5 = dataset['50'].values
    feature6 = dataset['WKTS'].values
    feature7 = dataset['CT'].values
    feature8 = dataset['ST'].values
    feature9 = dataset['BOWLING SR'].values
    feature10 = dataset['ECON'].values
    #     feature11 = dataset['BALLS'].values
    feature12 = dataset['BOWLING AVE'].values

    #preprocessing
    X = np.column_stack((feature2,feature4,feature5,feature6,feature7,feature8
                         ,feature9,feature10,feature12))
    X_std = StandardScaler().fit_transform(X)
    print("Applying k-means on Downloaded Dataset")
    model = KMeans(n_clusters=5, random_state=0).fit(X_std)
    cluster1_playerList = dataset[model.labels_==0][['NAME','RUNS','WKTS','ST','CT','100']]
    cluster2_playerList = dataset[model.labels_==1][['NAME','RUNS','WKTS','ST','CT','100']]
    cluster3_playerList = dataset[model.labels_==2][['NAME','RUNS','WKTS','ST','CT','100']]
    cluster4_playerList = dataset[model.labels_==3][['NAME','RUNS','WKTS','ST','CT','100']]
    cluster5_playerList = dataset[model.labels_==4][['NAME','RUNS','WKTS','ST','CT','100']]
    print("Assigning Categories i.e Bowler,Batsman,allrounder etc")
    # Assigning Categories
    for index, player in dataset.iterrows():
        for indexx, row in cluster1_playerList.iterrows():
            if player[0] == row[0]:
                dataset.loc[index,'PLAYER TYPE'] = 'Allrounder'

    for index, player in dataset.iterrows():
        for indexx, row in cluster2_playerList.iterrows():
            if player[0] == row[0]:
                dataset.loc[index,'PLAYER TYPE'] = 'Bowling Allrounder'

    for index, player in dataset.iterrows():
        for indexx, row in cluster3_playerList.iterrows():
            if player[0] == row[0]:
                dataset.loc[index,'PLAYER TYPE'] = 'Batsman'

    for index, player in dataset.iterrows():
        for indexx, row in cluster4_playerList.iterrows():
            if player[0] == row[0]:
                dataset.loc[index,'PLAYER TYPE'] = 'Batting Allrounder'

    for index, player in dataset.iterrows():
        for indexx, row in cluster5_playerList.iterrows():
            if player[0] == row[0]:
                dataset.loc[index,'PLAYER TYPE'] = 'Wicket keeper Batsman'

    for index, player in dataset.iterrows():
        if player[21] <= 0.0 or player[21] <= 0:
            if player[22] == 'Wicket keeper Batsman':
                dataset.loc[index, 'PLAYER TYPE'] = 'Wicket keeper Batsman'
            elif player[22] != 'Wicket keeper Batsman':
                dataset.loc[index, 'PLAYER TYPE'] = 'Batsman'

    for index, player in dataset.iterrows():
        if player[6] <= 0.0 or player[6] <= 0:
            dataset.loc[index, 'PLAYER TYPE'] = 'Bowler'
        else:
            if player['PLAYER TYPE'] != 'Bowler':
                if player[6] <= 0.0 or player[6] <= 0:
                    dataset.loc[index, 'PLAYER TYPE'] = 'Bowler'

    return dataset;
def assigning_categories(classified_data):
    matched_player_list = []
    for index, bowler in classified_data.iterrows():
        if bowler[7] > 0.0 or bowler[7] > 0:
            if bowler[21] > 0.0 or bowler[21] > 0:
                if bowler[6] > 0.0 or bowler[6] > 0:
                    if bowler[11] <= 0 or bowler[11] <= 0.0:
                        matched_player_list.append(classified_data.loc[index])

    domestic_player_data = pd.DataFrame(matched_player_list)
    """ For droping the index of old dataframe """
    domestic_player_data = domestic_player_data.reset_index(drop=True)

    player_sorted_SR = domestic_player_data.sort(['SRATE'], ascending=[1])
    player_sorted_ECON = domestic_player_data.sort(['ECON'], ascending=[1])
    """ Reset the index and then start from 1 """
    player_sorted_SR = player_sorted_SR.reset_index(drop=True)
    player_sorted_ECON = player_sorted_ECON.reset_index(drop=True)
    player_sorted_SR.index +=1
    player_sorted_ECON.index +=1
    sr_len = len(player_sorted_SR)
    econ_len = len(player_sorted_ECON)

    """ Find median of SRATE """
    sr_position = (sr_len+1)/2
    if sr_position%2 != 0 or sr_position%2 != 0.0:
        mdn = sr_position
        n1 = int(mdn)
        n2 = int(mdn) + 1
        sr_1 = player_sorted_SR.get_value(n1, 'SRATE', takeable=False)
        sr_2 = player_sorted_SR.get_value(n2, 'SRATE', takeable=False)
        sr_median = (sr_1 + sr_2)/2
    elif sr_position%2 == 0 or sr_position%2 == 0:
        sr_median_pos = int(sr_position)
        sr_median = player_sorted_SR.get_value(sr_median_pos, 'SRATE', takeable=False)

    """ Find median of ECON """
    econ_position = (econ_len+1)/2
    if econ_position%2 != 0 or econ_position%2 != 0.0:
        mdn = econ_position
        n1 = int(mdn)
        n2 = int(mdn) + 1
        econ_1 = player_sorted_ECON.get_value(n1, 'ECON', takeable=False)
        econ_2 = player_sorted_ECON.get_value(n2, 'ECON', takeable=False)
        econ_median = (econ_1 + econ_2)/2
    elif econ_position%2 == 0 or econ_position%2 == 0.0:
        econ_median_pos = int(econ_position)
        econ_median = player_sorted_ECON.get_value(econ_median_pos, 'ECON', takeable=False)

    """ Assigning the categories to player on the basis of rules """
    for player in range(len(domestic_player_data)):
        if domestic_player_data['SRATE'][player] > sr_median and domestic_player_data['ECON'][player] < econ_median:
            domestic_player_data.loc[player, 'PLAYER TYPE'] = 'Allrounder'

        elif domestic_player_data['SRATE'][player] > sr_median and domestic_player_data['ECON'][player] > econ_median:
            domestic_player_data.loc[player, 'PLAYER TYPE'] = 'Batting Allrounder'

        elif domestic_player_data['SRATE'][player] < sr_median and domestic_player_data['ECON'][player] < econ_median:
            domestic_player_data.loc[player, 'PLAYER TYPE'] = 'Bowling Allrounder'

        elif domestic_player_data['SRATE'][player] < sr_median and domestic_player_data['ECON'][player] > econ_median:
            domestic_player_data.loc[player, 'PLAYER TYPE'] = 'Bowler'

        elif domestic_player_data['AVE'][player] <= 2.0 or domestic_player_data['AVE'][player] <= 2:
            domestic_player_data.loc[player, 'PLAYER TYPE'] = 'Bowler'

    return domestic_player_data
def merge_classified_data(classified_data, domestic_player_data):
    """ Now  assign this classification to original domestic dataset """
    for player_1 in range(len(classified_data)):
        for player_2 in range(len(domestic_player_data)):
            if (classified_data['NAME'][player_1] == domestic_player_data['NAME'][player_2]):
                classified_data.loc[player_1, 'PLAYER TYPE'] = domestic_player_data['PLAYER TYPE'][player_2]
    return classified_data
def assigning_rating(dataset):
    print("Assigning Rating Points.")
    for index,player in dataset.iterrows():
        if player['PLAYER TYPE'] == 'Batsman' or player['PLAYER TYPE'] == 'Wicket keeper Batsman':
            dataset.loc[index,'RATING'] = (player['SRATE'] * 0.4) + (player['AVE'] * 0.3) + (player['50'] * 0.2) + (player['100'] * 0.1)
        elif player['PLAYER TYPE'] == 'Bowler':
            dataset.loc[index,'RATING'] = (player['ECON'] * 0.4) + (player['BOWLING SR'] * 0.3) + (player['4WI'] * 0.2) + (player['5WI'] * 0.1)
        elif player['PLAYER TYPE'] == 'Allrounder':
            dataset.loc[index,'RATING'] = ((player['SRATE'] * 0.4) + (player['AVE'] * 0.3) + (player['50'] * 0.2) + (player['100'] * 0.1))*0.5 + ((player['ECON'] * 0.4) + (player['BOWLING SR'] * 0.3) + (player['4WI'] * 0.2) + (player['5WI'] * 0.1))*0.5
        elif player['PLAYER TYPE'] == 'Batting allrounder' or player['PLAYER TYPE'] == 'Batting Allrounder':
            dataset.loc[index,'RATING'] = (((player['SRATE'] * 0.4) + (player['AVE'] * 0.3) + (player['50'] * 0.2) + (player['100'] * 0.1))*0.8) + (((player['ECON'] * 0.4) + (player['BOWLING SR'] * 0.3) + (player['4WI'] * 0.2) + (player['5WI'] * 0.1))*0.2)
        elif player['PLAYER TYPE'] == 'Bowling allrounder' or player['PLAYER TYPE'] == 'Bowling Allrounder':
            dataset.loc[index,'RATING'] = (((player['SRATE'] * 0.4) + (player['AVE'] * 0.3) + (player['50'] * 0.2) + (player['100'] * 0.1))*0.2) + (((player['ECON'] * 0.4) + (player['BOWLING SR'] * 0.3) + (player['4WI'] * 0.2) + (player['5WI'] * 0.1))*0.8)
    return dataset


def getting_Title(url):
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page,'html.parser')

    """ For Title of Tabel """
    head = soup.find_all('tr', class_='head')
    list_of_title = []
    for title in soup.find_all('th'):
        list_of_title.append(title.get_text())
    return list_of_title;
def cleaning_data(data,titles):
    dataframe = pd.DataFrame(data,columns=titles)
    dataset = dataframe.replace('-', 0)
    if '' in dataset.columns:
        dataset[''].replace('', np.nan, inplace=True)
    dataset.dropna(axis=1,how='all',inplace=True)
    dataset.fillna(0,inplace=True)
    return dataset
def download_webPage(url):
    list_of_rows = []
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, 'lxml')

    """ For Title of Tabel """
    head = soup.find_all('tr', class_='head')
    list_of_title = []
    for title in soup.find_all('th'):
        list_of_title.append(title.get_text())
    list_of_rows.append(list_of_title)

    """ Now Grap data from table body """
    for row in soup.find_all('tr', class_='data2'):
        list_of_cells= []
        for cell in row.find_all('td'):
            list_of_cells.append(cell.get_text())
        list_of_rows.append(list_of_cells)

    """ Make DataFrame """
    dataset = pd.DataFrame(list_of_rows)

    """ Replace '-' with'0' """
    dataset = dataset.replace('-', 0)
    return dataset
def insertData(dbName,collectionName,data):
    print("Inserting data to Database")
    client = MongoClient()
    db = client[dbName]
    mycollection = db[collectionName]
    odo(data, mycollection)
def delete_DB(name):
    client = MongoClient()
    client.drop_database(name)

def classify_players(dataset):
    #feature selection;
    feature1 = dataset['Runs'].values
    feature2 = dataset['Ave'].values
    feature3 = dataset['100'].values
    feature4 = dataset['SR'].values
    feature5 = dataset['50'].values
    feature6 = dataset['Wickets'].values
    feature7 = dataset['Ct'].values
    feature8 = dataset['St']
    feature9 = dataset['Dismis']
    feature10 = dataset['SR_Bowl']
    feature11 = dataset['Econ']
    feature12 = dataset['Overs']
    feature13 = dataset['Bowling_Avg']

    #preprocessing
    X = np.column_stack((feature1,feature2,feature3,feature4,feature5,feature6,feature7,feature8
                         ,feature9,feature10,feature11,feature12,feature13))
    X_std = StandardScaler().fit_transform(X)
    print("Applying k-means on Downloaded Dataset")
    model = KMeans(n_clusters=5, random_state=0).fit(X_std)
    cluster1_playerList = dataset[model.labels_==0][['Player','Runs','Wickets','St','Ct','100']]
    cluster2_playerList = dataset[model.labels_==1][['Player','Runs','Wickets','St','Ct','100']]
    cluster3_playerList = dataset[model.labels_==2][['Player','Runs','Wickets','St','Ct','100']]
    cluster4_playerList = dataset[model.labels_==3][['Player','Runs','Wickets','St','Ct','100']]
    cluster5_playerList = dataset[model.labels_==4][['Player','Runs','Wickets','St','Ct','100']]
    print("Assigning Categories i.e Bowler,Batsman,allrounder etc")
    # Assigning Categories
    for index, player in dataset.iterrows():
        for indexx, row in cluster1_playerList.iterrows():
            if player[0] == row[0]:
                dataset.loc[index,'Player Type'] = 'Allrounder'

    for index, player in dataset.iterrows():
        for indexx, row in cluster2_playerList.iterrows():
            if player[0] == row[0]:
                dataset.loc[index,'Player Type'] = 'Bowling Allrounder'

    for index, player in dataset.iterrows():
        for indexx, row in cluster3_playerList.iterrows():
            if player[0] == row[0]:
                dataset.loc[index,'Player Type'] = 'Batsman'

    for index, player in dataset.iterrows():
        for indexx, row in cluster4_playerList.iterrows():
            if player[0] == row[0]:
                dataset.loc[index,'Player Type'] = 'Batting Allrounder'

#     for index, player in dataset.iterrows():
#         for indexx, row in cluster5_playerList.iterrows():
#             if player[0] == row[0]:
#                 dataset.loc[index,'Player Type'] = 'Wicket keeper Batsman'
#                 print('/////////////////////////////////////')
#                 print('Cluster keeper   ',row[0])

    print("Changing dtypes of the columns to appropriete ones")
    dataset = check_column_type(dataset)

    print("Specifying more rules....")
    # Correcting the player list obtained from the k-means algorithm;
    for index,player in dataset.iterrows():
        dataset.loc[index,'Batting_perc'] = round((player[3]*100)/player[2],1)
        dataset.loc[index,'Bowling_perc'] = round((player[15]*100)/player[2],1)


    for index,player in dataset.iterrows():
        if player['St'] >= 1:
            dataset.loc[index,'Player Type'] = 'Wicket keeper Batsman'
        elif player[31] > 66.0 and player[32] >66.0:
            dataset.loc[index,'Player Type'] = 'Allrounder'
        elif player[15] == 0.0 and player[30] != 'Wicket keeper Batsman':
            dataset.loc[index,'Player Type'] = 'Batsman'
        elif player[32] >= 90.0:
            dataset.loc[index,'Player Type'] = 'Bowler'
        elif player[30] == 'Batting Allrounder':
            if player[31] >= 90.0 and player[32] <=15.0:
                dataset.loc[index,'Player Type'] = 'Batsman'
        elif player[30] == 'Bowling Allrounder':
            if player[31] >= 66.0 and player[32] < 66.0:
                dataset.loc[index,'Player Type'] = 'Batting Allrounder'
        elif player['St'] > 0 or player['St'] > 0.0:
            dataset.loc[index,'Player Type'] = 'Wicket keeper Batsman'
            

    print("Assigning Rating Points.")
    for index,player in dataset.iterrows():
        if player[30] == 'Batsman' or player[30] == 'Wicket keeper Batsman':
            dataset.loc[index,'PBT'] = (player[9] * 0.4) + (player[7] * 0.3) + (player[11] * 0.2) + (player[10] * 0.1)
            dataset.loc[index,'PBW'] = 0.0
            dataset.loc[index,'PEX'] = player['Inns']
            
        elif player[30] == 'Bowler':
            dataset.loc[index,'PBT'] = 0.0
            dataset.loc[index,'PBW'] = (player[22] * 0.4) + (player[23] * 0.3) + (player[24] * 0.2) + (player[25] * 0.1)
            dataset.loc[index,'PEX'] = player['Bowling_Inns']
            
        elif player[30] == 'Allrounder':
            dataset.loc[index,'PBT'] = ((player[9] * 0.4) + (player[7] * 0.3) + (player[11] * 0.2) + (player[10] * 0.1))*0.5
            dataset.loc[index,'PBW'] = ((player[22] * 0.4) + (player[23] * 0.3) + (player[24] * 0.2) + (player[25] * 0.1))*0.5
            dataset.loc[index,'PEX'] = player['Inns'] + player['Bowling_Inns']
            
        elif player[30] == 'Batting Allrounder':
            dataset.loc[index,'PBT'] = ((player[9] * 0.4) + (player[7] * 0.3) + (player[11] * 0.2) + (player[10] * 0.1))*0.8
            dataset.loc[index,'PBW'] = ((player[22] * 0.4) + (player[23] * 0.3) + (player[24] * 0.2) + (player[25] * 0.1))*0.2
            dataset.loc[index,'PEX'] = player['Inns'] + player['Bowling_Inns']
            
        elif player[30] == 'Bowling Allrounder':
            dataset.loc[index,'PBT'] = ((player[9] * 0.4) + (player[7] * 0.3) + (player[11] * 0.2) + (player[10] * 0.1))*0.2
            dataset.loc[index,'PBW'] = ((player[22] * 0.4) + (player[23] * 0.3) + (player[24] * 0.2) + (player[25] * 0.1))*0.8
            dataset.loc[index,'PEX'] = player['Inns'] + player['Bowling_Inns']
            
            
    for index,player in dataset.iterrows():
        if player[30] == 'Batsman' or player[30] == 'Wicket keeper Batsman':
            dataset.loc[index,'Rating'] = (player['PBT'] * 0.8) + (player['PEX'] * 0.2)
        elif player[30] == 'Bowler':
            dataset.loc[index,'Rating'] = (player['PBW'] * 0.8) + (player['PEX'] * 0.2)
        elif player[30] == 'Allrounder':
            dataset.loc[index,'Rating'] = (player['PBT'] * 0.4) + (player['PBW'] * 0.4) + (player['PEX'] * 0.2)
        elif player[30] == 'Batting Allrounder':
            dataset.loc[index,'Rating'] = (player['PBT'] * 0.6) + (player['PBW'] * 0.2) + (player['PEX'] * 0.2)
        elif player[30] == 'Bowling Allrounder':
            dataset.loc[index,'Rating'] = (player['PBT'] * 0.2) + (player['PBW'] * 0.6) + (player['PEX'] * 0.2)

    return dataset;
def check_column_type(df):
    for c in df.columns:
        if 'Mat' in c or 'Match' in c or 'MATCH' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'Inns' in c or 'INNINGS' in c or 'INNING' in c or 'INS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'NO' in c or 'NOT OUT' in c or 'NT' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'Runs' in c or 'RUN' in c or 'RNS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

                #         if 'HS' in c or 'HIGHEST' in c or 'HIGH' in c:
                #             for item in df['HS']:
                #                 if '*' in item:
                #                     df = item.replace('*', "")
                #                     print(df)
                #             if df[c].dtype == object:

                #                 if '*' in df['HS']:
                #                     df = df['HS'].replace('*', "")
                #                     print('YESSSSSSSSSSSSSSSSSSS')
                #                 df[c] = df[c].astype(str)

        if 'Ave'in c or 'AVE' in c or 'AVG' in c or 'AVERAGE' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')

        if 'BF' in c or 'Ball faced' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'SRATE' in c or 'SR' in c or 'STRIKE RATE' in c or 'S RATE' in c or 'S_RATE' in c:

            if df[c].dtype == object:
                print("Sr")
                df[c] = df[c].astype('float64')

        if '100' in c or '100s' in c or 'HUNDREDS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if '50' in c or '50s' in c or 'FIFTIES' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if '0' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if '4s' in c or 'fours' in c or 'four' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if '6s' in c or 'sixes' in c or 'six' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'Bowling Inns' in c or 'Inns' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'Overs' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')

        if 'Middens' in c or 'Mdns' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'Runs Given' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'Wickets' in c or 'Wicket' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'Bowling Avg' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')

        if 'SR Bowl' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')

        if '4' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if '5' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'Econ' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')

        if 'Dismis' in c or 'Dismissels' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'Ct' in c or 'CT' in c or 'CATCHES' in c or 'CTS' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'St' in c or 'STUMPS' in c or 'STS' in c or 'ST' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('int64')

        if 'D/I' in c:
            if df[c].dtype == object:
                df[c] = df[c].astype('float64')
    return df
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

def removeTeam_Name(domestic_dataset):
    for index,player in domestic_dataset.iterrows():
        fullname = player['NAME']
        teamName = fullname.split(" ")[-1]
        name_withoutTeam = ' '.join(fullname.split(' ')[:-1])
#         t20_dataset.loc[index,'TEAM'] = countryName
        domestic_dataset.loc[index,'NAME'] = name_withoutTeam
    return domestic_dataset
#Choosing the data set to download based on the instruction from node server;
print("I am here in python")
sys.stdout.flush()
if sys.argv[1] == 't20_dataset':

    print("I am here in t20_dataset Download option")

    T20_dataset(sys.argv[1])

if sys.argv[1] == 'domestic_dataset':
    print("I am here in domestic Download option")
    Domestic_dataset()

if sys.argv[1] == 'psl_dataset':
    print("I am here in PSL Dataset Download option")
    PSL_dataset()
