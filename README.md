# PSL-Player-Recommender
## Abstract
This is an implemenation of Pakistan Super League which is held every year in Pakistan. In this project we automating the formation of
different categories of psl (Platinum, Diamond, Gold, Silver, Emerging). Then we recommends different players for owners in the drafting
process. At the end of drafting, each owner of 6 different teams get 20 players team. Our system then give the best playing 11 to each
owner. It can alse be used by PCB to form the above 5 different categories.
## Introduction
This is web application which is made in Angular 2 and Node.js. It uses machine learning in python to recommend player to each owner. We used two machine learning algorithms in it. 
### 1. K-means
This algorithm is a unsupervised clustering algorithm. It takes a dataset of players and then clusters them into following 6 categories.
- Batsman
- Wicket Keeper
- Bowler
- All-rounder
- Batting Allrounder
- Bowling Allrounder

### 2. Genetic Algorithm
Using genetic algorithm we recommends best playing 11 to each owner from the 20 players. It gives balanced team to each owner. The team will be in the following combination.
- 1 wicket keeper
- 4 (bowlers + bowling allrounders)
- 6 (batsman + batting allrounders + all rounders)

Our applications also provides owners to maintain their complete in form of a dashboard. It also provides survay facility to users to vote for their best players and team of PSL.

## Features
### PSL Categories Formation
Our system places players into different PSL categories based on their performance. We takes their performance from following dataset.
- T20 International Data
- Previos PSL Editions (2016,2017)
- Pakistanis Domestic Data.

We use different statistical formulas to rank player. 
### Best 20 Player
We implemented the complete drafting process of PSL. In PSL drafting process their are 5 pick. In each pick owner has to select a player. Our system gives each owner, players from different categories based on player performance. Following list show complete drafting process.
- Platinum pick (3 players)
- Diamond pick (3 players)
- Gold pick (3 players)
- Silver pick (4 players)
- Emerging pick (4 players)

At the end each owner gets a team of 20 players and it is saved into its profile.
### Best Playing 11
Once owner selects a team of 20 players, our system then provide owners the facility to get best 11.

### Sign Up and Login
In order to get to drafting process, owner must have an account. Our system gives access to drafting process to six PSL owners. Normal users can only see the players of different PSL Categories.
### Ower Dashboard (Profile)
Our system maintain a complete profile for each owners. It includes:
1. Owner personal information
2. Best 20 players
3. Best 11

Owner can edit his personal information and view best 20 and 11 players.
### Survays
Our system provides different survays to users so that they can choose players and teams of thier choise. In this way our system get popularity of different PSL players and team and then add that popularity to PSL player rating.
### Previous PSL teams.
Our system also presents squad of the six different PSL teams to user. Following are the different teams in PSL.
- Peshawar Zalmi
- Queta Gladiators
- Lahore Qalandars
- Karachi Kings
- Islamabad United
- Multan Sultan

## Tools and Technologies
### Front end Technologies
- Angular 2
- Semantic UI
- Ace Editor
### Back end Technologies
- Node.js
- Express JS (Node.js Framework)
### Machine Learning using Python
- K-means
- Genetic Algorithm
### Python
- Pandas
- Numpy
- Matplotlib
- Scikit learn
### Database
- Mongo DB (NoSQL database)
## Screenshots
### Main Page
