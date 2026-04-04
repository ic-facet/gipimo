// server.js (Anexa los frameworks instalados)
const express = require('express');
const path = require('path');
const session = require('express-session');


// initializations
const app = express();
app.use(express.json());
app.use(express.urlencoded({limit: "5mb", extended: true}));

//require('./database');
//require('./src/passport/local-auth');

// routes
app.use('/', require('./src/routes/index'));


// settings
app.set('port', process.env.PORT || 3000);



// middlewares
app.use(express.urlencoded({extended: true}));


// Starting the server
app.listen(app.get('port'), () => {
  console.log('server on port', app.get('port'));
});
