// Requires all the dependancies
var MongoClient = require('mongodb').MongoClient;
var ObjectId = require('mongodb').ObjectID;
var express = require('express');
var config = require('./config')
var bodyParser  = require('body-parser');
var jwt = require('jsonwebtoken'); // used to create, sign, and verify tokens
var PythonShell = require('python-shell');

var url = "mongodb://localhost:27017/psl_t20";

var allowCrossDomain = function(req, res, next) {
    res.header('Access-Control-Allow-Origin', "*");
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
}
var app = express();  

// use body parser so we can get info from POST and/or URL parameters
app.use(allowCrossDomain);
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Some global variables
var data;
var error;
app.set('superSecret', config.secret); // secret variable

// ===================================================
// This is REST API section that deals client request//
// ==================================================

// Loading T20 Dataset from Mongo db;
app.get('/PSL/Dataset', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        db.collection("t20_dataset").find({}).toArray(function(err, result) {
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

// ==============================
// Loading the 6 PSL Categories//
// =============================

//Loading Platinum Category from Mongo db
app.get('/PSL/Categories/Platinum', function (req, res) {
    console.log("Platinum Category.")
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        db.collection("Platinum").find({}).toArray(function(err, result) {
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

//Loading Diamond Category from Mongo db
app.get('/PSL/Categories/Diamond', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        db.collection("Diamond").find({}).toArray(function(err, result) {
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

//Loading Gold Category from Mongo db
app.get('/PSL/Categories/Gold', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        db.collection("Gold").find({}).toArray(function(err, result) {
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

//Loading Silver Category from Mongo db
app.get('/PSL/Categories/Silver', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Successfully Established.")
        db.collection("Silver").find({}).toArray(function(err, result) {
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

//Loading Supplementory Category from Mongo db
app.get('/PSL/Categories/Supplementory', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        db.collection("Supplementory").find({}).toArray(function(err, result) {
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

//Loading Emerging Category from Mongo db
app.get('/PSL/Categories/Emerging', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        db.collection("Emerging").find({}).toArray(function(err, result) {
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result));
            db.close();
        });
    });
})


// =====================================
// Add different datasets into database//
// =====================================

// Adding and Loading T20 International Players List from Mongo db
app.post('/PSL/addT20Dataset', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        console.log("Download T20 Dataset.")
        db.collection("t20_dataset").find({}).toArray(function(err, data) {
            if (err) throw err;
            if (data.length > 0){
                console.log(JSON.stringify(data))
                res.end( JSON.stringify(data) );
                db.close();
            }
            else{
                this.data = req.body;     // your JSON
                console.log(this.data)
                var options = { args: [this.data] };
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\Dataset.py",options, function (err,data) {
                    if (err){
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else{
                        console.log(JSON.stringify(data))
                        res.end( data.toString() );
                    }
                });
            }
        });
    });

})
// Adding and Loading PSL Players List from Mongo db
app.post('/PSL/addPSL_Player_list', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("I am here.")
        db.collection("psl_player_list").find({}).toArray(function(err, data) {
            if (err) throw err;
            if (data.length > 0){
                console.log(JSON.stringify(data))
                res.end( JSON.stringify(data) );
                db.close();
            }
            else{
                this.data = req.body.data;     // your JSON
                console.log(this.data)
                var options = { args: [this.data] };
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\Categories.py", function (err,data) {
                    if (err){
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else{
                        console.log(JSON.stringify(data))
                        res.end( JSON.stringify(data) );
                    }
                });
            }
        });
    });
})

//Adding and Loading Domestic Dataset from Mongo db
app.post('/PSL/addDomesticDataset', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        console.log("Download domestic Dataset.")
        db.collection("domestic_dataset").find({}).toArray(function(err, data) {
            if (err) throw err;
            if (data.length > 0){
                console.log(JSON.stringify(data))
                res.end( JSON.stringify(data) );
                db.close();
            }
            else{
                console.log("I am here.")

                this.data = req.body;     // your JSON
                console.log(this.data)
                var options = { args: [this.data] };
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\Dataset.py",options, function (err,data) {
                    if (err){
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else{
                        console.log(JSON.stringify(data))
                        res.end( data.toString() );
                    }
                });
            }
        });
    });

})

//Adding and Loading PSL dataset from Mongo db
app.post('/PSL/addPSLDataset', function (req, res) {

    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        console.log('Downloading PSL Dataset')
        db.collection("psl_dataset").find({}).toArray(function(err, data) {
            if (err) throw err;
            if (data.length > 0){
                console.log(JSON.stringify(data))
                res.end( JSON.stringify(data) );
                db.close();
            }
            else{
                this.data = req.body;     // your JSON

                var options = { args: [this.data] };
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\Dataset.py",options, function (err,data) {
                    if (err){
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else{
                        console.log(JSON.stringify(data))
                        res.end( data.toString() );
                    }
                });
            }
        });
    });

})


// ======================================================
// Queries Section (It includes various queries from db)//
// ======================================================

//Top 20 PSL Batsman
app.get('/PSL/PSL_Dataset/top_20_batsman',function (req,res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var mysort = { RUNS: -1 };
        db.collection("psl_dataset").find().sort(mysort).limit(20).toArray(function(err, result) {
            console.log("Top 20 Batsmna")
            if (err) throw err;
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

//Top 20 PSL WicketTakers
app.get('/PSL/PSL_Dataset/top_20_WicketTakers',function (req,res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var mysort = {WKTS: -1};
        db.collection("psl_dataset").find().sort(mysort).limit(20).toArray(function (err, result) {
            console.log("Top 20 Wicket Takers")
            if (err) throw err;
            res.end(JSON.stringify(result));
            db.close();
        });
    });
})

//Top 20 PSL Economical players
app.get('/PSL/PSL_Dataset/top_20_EconomicalPlayers',function (req,res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var mysort = { ECON: 1 };

        db.collection("psl_dataset").find({ ECON: { $gt: 0 } }).sort(mysort).limit(20).toArray(function (err, result) {
            console.log("Top 20 Economical Players")
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

//Top 20 PSL batting strikerakers
app.get('/PSL/PSL_Dataset/top_20_StrikeRaters',function (req,res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var mysort = { SR: -1 };

        db.collection("psl_dataset").find({ SR: { $gt: 0 } }).sort(mysort).limit(20).toArray(function (err, result) {
            console.log("Top 20 StrikeRaters")
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

//Batsman with most fifties
app.get('/PSL/PSL_Dataset/top_20_MostFifties',function (req,res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var mysort = { 50: 1 };

        db.collection("psl_dataset").find({ 50: { $gt: 0 } }).sort(mysort).limit(20).toArray(function (err, result) {
            console.log("Players with Most Fifties")
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

//Batsman with most sixes
app.get('/PSL/PSL_Dataset/top_20_MostSixes',function (req,res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var mysort = { '6S': -1 };

        db.collection("psl_dataset").find({ '6S': { $gt: 0 } }).sort(mysort).limit(20).toArray(function (err, result) {
            console.log("Players with Most sixes")
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        })
    });
})

//Getting Specific Player data 
app.post('/PSL/T20Dataset/player',function (req,res) {
    MongoClient.connect(url, function(err, db) {
        var data = req.body.playerName;
        if (err) throw err;
        db.collection("t20_dataset").find({ 'Player': data}).toArray(function (err, result) {
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result));
            db.close();
        })
    });
})

// ==============================
// Different Surveys about PSL//
// ==============================


//Survey No.1
app.post('/PSL/survey/favouritePSLPlayer',function (req,myResults) {
    MongoClient.connect(url, function(err, db) {
        db.createCollection("favouritePSLPlayer", function(err, res) {
            if (err) throw err;

            //Check if the specified player survey data is already inserted
            db.collection("favouritePSLPlayer").find({name:req.body.name}).toArray(function(err, result){
                if (err) throw err;
                console.log(JSON.stringify(result))
                //if yes then just increment its vote by one
                if(result.length == 1) {
                    db.collection("favouritePSLPlayer").update(
                        { name: req.body.name },
                        {  $inc: { vote: 1 } }
                     )
                     console.log("Record is updated")
                     //At the end, send the results back to CLIENT
                     db.collection("favouritePSLPlayer").find({}).toArray(function(err, result){
                        if (err) throw err;
                        console.log(JSON.stringify(result))
                        myResults.end(JSON.stringify(result));
                        db.close();
                    })
                }
                //else create the player survey record that is his name and vote = 1
                else{
                    var data = {
                        name: req.body.name,
                        vote: 1
                    };
                    db.collection("favouritePSLPlayer").insertOne(data, function (err, res) {
                        if (err) throw err;
                        console.log("1 document inserted.");

                         //At the end, send the results back to CLIENT
                        db.collection("favouritePSLPlayer").find({}).toArray(function(err, result){
                            if (err) throw err;
                            console.log(JSON.stringify(result))
                            myResults.end(JSON.stringify(result));
                            db.close();
                        })
                    });
                }
            });
        });
    });
})

//Survey No.2
app.post('/PSL/survey/favouritePSLTeam',function (req,myResults) {
    MongoClient.connect(url, function(err, db) {
        db.createCollection("favouritePSLTeam", function(err, res) {
            if (err) throw err;

            //Check if the specified player survey data is already inserted
            db.collection("favouritePSLTeam").find({name:req.body.name}).toArray(function(err, result){
                if (err) throw err;
                console.log(JSON.stringify(result))
                //if yes then just increment its vote by one
                if(result.length == 1) {
                    db.collection("favouritePSLTeam").update(
                        { name: req.body.name },
                        {  $inc: { vote: 1 } }
                     )
                     console.log("Record is updated")
                     //At the end, send the results back to CLIENT
                     db.collection("favouritePSLTeam").find({}).toArray(function(err, result){
                        if (err) throw err;
                        console.log(JSON.stringify(result))
                        myResults.end(JSON.stringify(result));
                        db.close();
                    })
                }
                //else create the player survey record that is his name and vote = 1
                else{
                    var data = {
                        name: req.body.name,
                        vote: 1
                    };
                    db.collection("favouritePSLTeam").insertOne(data, function (err, res) {
                        if (err) throw err;
                        console.log("1 document inserted.");

                         //At the end, send the results back to CLIENT
                        db.collection("favouritePSLTeam").find({}).toArray(function(err, result){
                            if (err) throw err;
                            console.log(JSON.stringify(result))
                            myResults.end(JSON.stringify(result));
                            db.close();
                        })
                    });
                }
            });
        });
    });
})

// =====================================
// Owner's teams of 2017 PSL edition//
// =====================================

// 1) Peshawar Zalmi
app.post('/PSL/Teams/PeshawarZalmi', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        db.collection(req.body.teamName).find().toArray(function (err, data) {
            if (err) throw err;
            if (data.length > 0) {
                console.log(JSON.stringify(data))
                res.end(JSON.stringify(data));
                db.close();
            }
            else {
              
                var options = {args: [req.body.teamName]};
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\pslTeams.py", options, function (err, data) {
                    if (err) {
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else {

                        // After inserting Platinum pick into db, load it to send back to client side;
                        db.collection(req.body.teamName).find().toArray(function (err, data) {
                            if (err) throw err;
                            if (data.length > 0) {
                                console.log(JSON.stringify(data))
                                res.end(JSON.stringify(data));
                                db.close();
                            }
                        });
                    }
                });
            }
        });
    });
});

// 2) Queta Gladiators
app.post('/PSL/Teams/QuetaGladiators', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        db.collection(req.body.teamName).find().toArray(function (err, data) {
            if (err) throw err;
            if (data.length > 0) {
                console.log(JSON.stringify(data))
                res.end(JSON.stringify(data));
                db.close();
            }
            else {
              
                var options = {args: [req.body.teamName]};
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\pslTeams.py", options, function (err, data) {
                    if (err) {
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else {

                        // After inserting Platinum pick into db, load it to send back to client side;
                        db.collection(req.body.teamName).find().toArray(function (err, data) {
                            if (err) throw err;
                            if (data.length > 0) {
                                console.log(JSON.stringify(data))
                                res.end(JSON.stringify(data));
                                db.close();
                            }
                        });
                    }
                });
            }
        });
    });
});

// 3) Lahore Qalandars
app.post('/PSL/Teams/LahoreQalandars', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        db.collection(req.body.teamName).find().toArray(function (err, data) {
            if (err) throw err;
            if (data.length > 0) {
                console.log(JSON.stringify(data))
                res.end(JSON.stringify(data));
                db.close();
            }
            else {
              
                var options = {args: [req.body.teamName]};
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\pslTeams.py", options, function (err, data) {
                    if (err) {
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else {

                        // After inserting Platinum pick into db, load it to send back to client side;
                        db.collection(req.body.teamName).find().toArray(function (err, data) {
                            if (err) throw err;
                            if (data.length > 0) {
                                console.log(JSON.stringify(data))
                                res.end(JSON.stringify(data));
                                db.close();
                            }
                        });
                    }
                });
            }
        });
    });
});

// 4) Islamabad United
app.post('/PSL/Teams/IslamabadUnited', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        db.collection(req.body.teamName).find().toArray(function (err, data) {
            if (err) throw err;
            if (data.length > 0) {
                console.log(JSON.stringify(data))
                res.end(JSON.stringify(data));
                db.close();
            }
            else {
              
                var options = {args: [req.body.teamName]};
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\pslTeams.py", options, function (err, data) {
                    if (err) {
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else {

                        // After inserting Platinum pick into db, load it to send back to client side;
                        db.collection(req.body.teamName).find().toArray(function (err, data) {
                            if (err) throw err;
                            if (data.length > 0) {
                                console.log(JSON.stringify(data))
                                res.end(JSON.stringify(data));
                                db.close();
                            }
                        });
                    }
                });
            }
        });
    });
});

// 5) Karachi Kings
app.post('/PSL/Teams/KarachiKings', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        db.collection(req.body.teamName).find().toArray(function (err, data) {
            if (err) throw err;
            if (data.length > 0) {
                console.log(JSON.stringify(data))
                res.end(JSON.stringify(data));
                db.close();
            }
            else {
              
                var options = {args: [req.body.teamName]};
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\pslTeams.py", options, function (err, data) {
                    if (err) {
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else {

                        // After inserting Platinum pick into db, load it to send back to client side;
                        db.collection(req.body.teamName).find().toArray(function (err, data) {
                            if (err) throw err;
                            if (data.length > 0) {
                                console.log(JSON.stringify(data))
                                res.end(JSON.stringify(data));
                                db.close();
                            }
                        });
                    }
                });
            }
        });
    });
});


// 6) Multan Sultan
app.post('/PSL/Teams/MultanSultan', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        db.collection(req.body.teamName).find().toArray(function (err, data) {
            if (err) throw err;
            if (data.length > 0) {
                console.log(JSON.stringify(data))
                res.end(JSON.stringify(data));
                db.close();
            }
            else {
              
                var options = {args: [req.body.teamName]};
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\pslTeams.py", options, function (err, data) {
                    if (err) {
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else {

                        // After inserting Platinum pick into db, load it to send back to client side;
                        db.collection(req.body.teamName).find().toArray(function (err, data) {
                            if (err) throw err;
                            if (data.length > 0) {
                                console.log(JSON.stringify(data))
                                res.end(JSON.stringify(data));
                                db.close();
                            }
                        });
                    }
                });
            }
        });
    });
});


// =====================================
// Pakistan Super League Drafting Process//
// =====================================

// 1) Platinum Pick
app.post('/PSL/platinumPick', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        db.collection(req.body.owner).find( { 'Category': { $eq: 'Platinum' } } ).toArray(function (err, data) {
            if (err) throw err;
            if (data.length > 0) {
                console.log(JSON.stringify(data))
                res.end(JSON.stringify(data));
                db.close();
            }
            else {
              
                var options = {args: [req.body.pick,req.body.owner]};
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\DraftingProcess.py", options, function (err, data) {
                    if (err) {
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else {

                        // After inserting Platinum pick into db, load it to send back to client side;
                        db.collection(req.body.owner).find( { 'Category': { $eq: 'Platinum' } } ).toArray(function (err, data) {
                            if (err) throw err;
                            if (data.length > 0) {
                                console.log(JSON.stringify(data))
                                res.end(JSON.stringify(data));
                                db.close();
                            }
                        });
                    }
                });
            }
        });
    });
});

// 2) Diamond Pick
app.post('/PSL/diamondPick', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        db.collection(req.body.owner).find( { 'Category': 'Diamond' } ).toArray(function (err, data) {
            if (err) throw err;

            if (data.length > 0) {
                console.log(JSON.stringify(data))
                res.end(JSON.stringify(data));
                db.close();
            }
            else {
                var options = {args: [req.body.pick,req.body.owner]};
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\DraftingProcess.py", options, function (err, data) {
                    if (err) {
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else {

                        // After inserting Platinum pick into db, load it to send back to client side;
                        db.collection(req.body.owner).find( { 'Category': 'Diamond' } ).toArray(function (err, data) {
                            if (err) throw err;
                            if (data.length > 0) {
                                console.log(JSON.stringify(data))
                                res.end(JSON.stringify(data));
                                db.close();
                            }
                        });
                    }
                });
            }
        });
    });
});

// 3) Gold Pick
app.post('/PSL/goldPick', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        db.collection(req.body.owner).find( { 'Category': 'Gold' } ).toArray(function (err, data) {
            if (err) throw err;

            if (data.length > 0) {
                console.log(JSON.stringify(data))
                res.end(JSON.stringify(data));
                db.close();
            }
            else {
                var options = {args: [req.body.pick,req.body.owner]};
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\DraftingProcess.py", options, function (err, data) {
                    if (err) {
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else {
                        // After inserting Platinum pick into db, load it to send back to client side;
                        db.collection(req.body.owner).find( { 'Category': 'Gold' } ).toArray(function (err, data) {
                            if (err) throw err;
                            if (data.length > 0) {
                                console.log(JSON.stringify(data))
                                res.end(JSON.stringify(data));
                                db.close();
                            }
                        });
                    }
                });
            }
        });
    });
});

// 4) Silver Pick
// 3) Gold Pick
app.post('/PSL/silverPick', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        db.collection(req.body.owner).find( { 'Category': 'Silver' } ).toArray(function (err, data) {
            if (err) throw err;

            if (data.length > 0) {
                console.log(JSON.stringify(data))
                res.end(JSON.stringify(data));
                db.close();
            }
            else {
                var options = {args: [req.body.pick,req.body.owner]};
                PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\DraftingProcess.py", options, function (err, data) {
                    if (err) {
                        throw err
                        res.end(JSON.stringify(err))
                    }
                    else {
                        // After inserting Platinum pick into db, load it to send back to client side;
                        db.collection(req.body.owner).find( { 'Category': 'Silver' } ).toArray(function (err, data) {
                            if (err) throw err;
                            if (data.length > 0) {
                                console.log(JSON.stringify(data))
                                res.end(JSON.stringify(data));
                                db.close();
                            }
                        });
                    }
                });
            }
        });
    });
});



// 5) Supplementory Pick
app.post('/PSL/supplementoryPick', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        var options = {args: [req.body.pick,req.body.owner]};
        PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\DraftingProcess.py", options, function (err, data) {
            if (err) {
                throw err
                res.end(JSON.stringify(err))
            }
            else {
                // After inserting Platinum pick into db, load it to send back to client side;
                db.collection(req.body.owner).find().toArray(function (err, data) {
                    if (err) throw err;
                    if (data.length > 0) {
                        console.log(JSON.stringify(data))
                        res.end(JSON.stringify(data));
                        db.close();
                    }
                });
            }
        });
    });
});


// 6) Emerging Pick
app.post('/PSL/emergingPick', function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        console.log("Connection Established.")

        var options = {args: [req.body.pick,req.body.owner]};
        PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\DraftingProcess.py", options, function (err, data) {
            if (err) {
                throw err
                res.end(JSON.stringify(err))
            }
            else {
                // After inserting Platinum pick into db, load it to send back to client side;
                db.collection(req.body.owner).find().toArray(function (err, data) {
                    if (err) throw err;
                    if (data.length > 0) {
                        console.log(JSON.stringify(data))
                        res.end(JSON.stringify(data));
                        db.close();
                    }
                });
            }
        });
    });
});



app.post('/PSL/createOwner', function(req, result) {
    
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        db.createCollection("PSL_Owners", function(err, res) {
            if (err) throw err;

            console.log("Collection created!");
            var owner = {
                name: req.body.owner_name,
                password: req.body.password,
                cnic: req.body.cnic,
                email: req.body.email,
                teamName: req.body.team_name
            };
            db.collection("PSL_Owners").find({}).toArray(function(err, number_of_owners){
                if(number_of_owners.length < 6) {
                    db.collection("PSL_Owners").find({},{'email' : true, 'cnic' : true, 'name':true, 'teamName':true}).toArray(function(err, data){

                        if (data.length > 0 ){
                            for(var val of data) {
                                if (val.email == req.body.email || val.cnic == req.body.cnic || val.name == req.body.owner_name || val.teamName == req.body.team_name){
                                    console.log('Validation.')
                                    if (val.email == req.body.email){
                                         return result.send({success: false, message: 'Email Already Exits.'});
                                         db.close();
                                     } 
                                     else if (val.cnic == req.body.cnic){
                                         return result.send({success: false, message: 'CNIC Already Exits.'});
                                         db.close();
                                     } 
                                     else if (val.name == req.body.owner_name){
                                        return result.send({success: false, message: 'Owner Name Already Exits.'});
                                        db.close();
                                    } 
                                    else if (val.teamName == req.body.team_name){
                                        return result.send({success: false, message: 'Team Name Already Exits.'});
                                        db.close();
                                    } 
                                }else{ 
                                    console.log("Creating Owner Account.")
                                    db.collection("PSL_Owners").insertOne(owner, function (err, res) {
                                        if (err) throw err;
                
                                        console.log("1 document inserted.");
                                        return result.send({success: true, message: 'Registration successful.'});
                                        db.close();
                                    });
                                    
                                }
                            }
                            
                        }else{
                            db.collection("PSL_Owners").insertOne(owner, function (err, res) {
                                if (err) throw err;
        
                                console.log("1 document inserted.");
                                return result.send({success: true, message: 'Registration successful.'});
                                db.close();
                            });
                        }
                    });
                
                }else {
                    console.log("Owner can't created")
                    return result.send({success: false, message: 'Six PSL Owners already registered.'});
                    db.close();
                    
                }
            });
        });
    });
})

//View All PSL Owners
app.get('/PSL/Owners', function(req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log('Connection Established.')
        var query = {}
        db.collection("PSL_Owners").find({}).toArray(function(err, result) {
            if (err) throw err;

            res.end(JSON.stringify(result))
            db.close();
        });
    });
});


// ==============================
// Owners Authentication Section//
// ==============================

// get an instance of the router for api routes
var apiRoutes = express.Router();

// route to authenticate a user (POST http://localhost:8081)
app.post('/authenticate', function(req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err
        console.log('Connection Established.')
        var query = {email: req.body.email};
        console.log(query)
        db.collection("PSL_Owners").findOne(query, function (err, user) {
            if (err) throw err;
            if (!user) {
                console.log("Invalid User email")
                res.json({success: false, message: 'Authentication failed. email not found.'});
            } else if (user) {
                // check if password matches
                if (user.password != req.body.password) {
                    console.log("Invalid password.")
                    res.json({success: false, message: 'Authentication failed. Wrong password.'});
                } else {

                    console.log("Creating Token")
                    // if user is found and password is right
                    // create a token
                    var token = jwt.sign(user, app.get('superSecret'), {
                        expiresIn: 60*60*24 // expires in 24 hours
                    });
                    console.log(user.name)

                    // return the information including token as JSON
                    res.json({
                        success: true,
                        message: 'Authentication Successful',
                        token: token,
                        name: user.name,
                        id: user._id
                    });
                }
            }
        });
    });
});

// route middleware to verify a token
apiRoutes.use(function (req,res,next) {
    // check header or url parameters or post parameters for token
    var token = req.body.token || req.query.token || req.headers['x-access-token'];

    // decode token
    if (token) {

        // verifies secret and checks exp
        jwt.verify(token, app.get('superSecret'), function(err, decoded) {
            if (err) {
                return res.json({ success: false, message: 'Failed to authenticate token.' });
            } else {
                // if everything is good, save to request for use in other routes
                req.decoded = decoded;
                next();
            }
        });

    } else {

        // if there is no token
        // return an error
        return res.status(403).send({
            success: false,
            message: 'No token provided.'
        });
    }
});

//Random message;
apiRoutes.get('/', function(req, res) {
    res.json({ message: 'Welcome to the coolest API on earth!' });
});

//Get details of specific Owner;
app.post('/PSL/specificOwner', function(req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log('Connection Established.')
       
        db.collection("PSL_Owners").findOne({"_id": new ObjectId(req.body._id)}, function(err, data) {
            if (err) throw err;

            console.log(JSON.stringify(data))
            res.end(JSON.stringify(data));
            db.close();
        });
    });
});


// =====================
// Choose Best Players //
// =====================

//Best 20 Players
app.post('/PSL/best_20', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        console.log("Best 20 Owner : ", req.body.name)
        db.collection(req.body.name).find({}).toArray(function(err, result) {
            if (err) throw err;
            console.log(JSON.stringify(result))
            res.end( JSON.stringify(result) );
            db.close();
        });
    });
})

//Best Playing 11
app.post('/PSL/best_11', function (req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        
        db.collection(req.body.name).find({}).toArray(function(err, best_20_players) {
            if(best_20_players.length > 11){
                
                db.collection(req.body.name + '_best_11').find({}).toArray(function(err, result) {
                    if (err) throw err;
                    
                    if (result.length > 0){
                       
                        console.log(JSON.stringify(result))
                        res.send({success:true, data: JSON.stringify(result) || []} )

                    }else{
                        console.log("Applying Genetic Algorithm")
                        var options = {args: [req.body.pick,req.body.name]};
                        PythonShell.run("G:\\COURSE WORK\\psl_1.1\\Python\\DraftingProcess.py", options, function (err, data) {
                            if (err) {
                                throw err
                                res.end(JSON.stringify(err))
                            }else{
                                db.collection(req.body.name + '_best_11').find({}).toArray(function(err, result) {
                                    res.send({success:true, data: JSON.stringify(result)} )
                                });
                            }
                        });
                    }
                }); 
            }
            else{
                console.log("I am in else condition")
                res.json({success:false});
            }
        });
    });
})

app.put('/PSL/updateOwner', function(req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log('Connection Established.')

        db.collection("PSL_Owners").update({"_id": new ObjectId(req.body._id)},{ $set: { image: req.body.image} },function(err, result) {
            if (err) throw err;

            res.end(JSON.stringify(result))
            db.close();
        });
    });
});




// apply the routes to our application with the prefix /api
app.use('/api', apiRoutes);

app.delete('/deleteCollection',function (err,res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        db.collection("favouritePSLPlayer").drop(function(err, delOK) {
            if (err) throw err;
            if (delOK) res.end("Collection deleted");
            db.close();
        });
    });
});

// ===============
// Delete Section //
// ================

// Delete a document inside a collection
app.delete('/PSL/deleteDocument',function(req,res){
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
    console.log(req.body.id);
    db.collection("Owners").deleteOne({"_id": new ObjectId(req.body.id)}, function(err, obj) {
      if (err) throw err;
      console.log("1 document deleted");
      db.close();
    });
});
})

//Delete a collection;
app.delete('/deleteCollection',function (req,res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var collection = req.body;
        console.log("Deleting Collection : ",collection)
    
        db.collection(req.body).drop(function(err, delOK) {
            if (err) throw err;
            if (delOK) res.end("Collection deleted");
            db.close();
        });
    });
});

app.get('/deleteOwners',function (err,res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        db.collection("PSL_Owners").drop(function(err, delOK) {
            if (err) throw err;
            if (delOK) res.end("Collection deleted");
            db.close();
        });
    });
});

app.get('/deteteSurvey',function (err,res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        db.collection("favouritePSLPlayer").drop(function(err, delOK) {
            if (err) throw err;
            if (delOK) res.end("Collection deleted");
            db.close();
        });
    });
});

//Running the server on local host and port = 8081
var server = app.listen(8081, function () {
    var host = server.address().address
    var port = server.address().port

    console.log("Server is listening at http://%s:%s", host, port)
})

