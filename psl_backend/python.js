// =======================
// get the packages we need ============
// =======================
var express     = require('express');
var app         = express();

var MongoClient = require('mongodb').MongoClient;
var config = require('./config.js')
var jwt    = require('jsonwebtoken'); // used to create, sign, and verify tokens
var url = "mongodb://localhost:27017/psl_t20";

const bodyParser = require('body-parser')
app.use(bodyParser.text());

// =======================
// configuration =========
// =======================
var port = process.env.PORT || 8080; // used to create, sign, and verify tokens

app.set('superSecret', config.secret); // secret variable


// =======================
// routes ================
// =======================
// basic route
app.get('/', function(req, res) {
    res.send('Hello! The API is at http://localhost:' + port + '/api');
});

// Inserting owner into database;
app.get('/setup', function(req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        db.createCollection('Owners', function(res,err){
            if (err) throw err;
            console.log("Collection created!");
            // create a sample user
            var farid = new User({
                name: 'Farid ullah',
                password: 'pakistan',
                cnic:'21705-2309678-1',
                email:'faridullah@gmail.com',
                teamName: 'Peshawar Zalmi',
            });
            db.collection("Owners").insertOne(farid, function(err, res) {
                if (err) throw err;
                console.log("1 document inserted");
            });
            db.close();
        })
    });
})

// get an instance of the router for api routes
var apiRoutes = express.Router();

apiRoutes.get('/users', function(req, res) {
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        console.log("Connection Established.")
        db.collection('Owners').find({}).toArray(function(data,err){
            if (err) throw err;
            console.log(result);
            res.end(JSON.stringify(data))
            db.close();
        })
    });
});

// =======================
// start the server ======
// =======================
app.listen(port);
console.log('Magic happens at http://localhost:' + port);