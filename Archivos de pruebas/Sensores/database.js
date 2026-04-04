const config = require('./keys.js');
const mysql = require('mysql2');
const Sequelize = require('sequelize');

module.exports = db = {};
    // create db if it doesn't already exist
    const { host, port, user, password, database } = config.database;
    const pool =  mysql.createPool({ host, port, user, password });
    // connect to db
    const sequelize = new Sequelize(database, user, password, { dialect: 'mysql',
    pool: {
        max: config.pool.max,
        min: config.pool.min,
        acquire: config.pool.acquire,
        idle: config.pool.idle
      
    } }
    
);

db.sequelize = sequelize ;
// init the Employee and Company models and add them to the exported db object
const data_ray_gpt = require('./src/models/ray_gpt.js');
const data_radob = require('./src/models/radob.js');
db.data_ray_gpt = data_ray_gpt;
db.data_radob = data_radob;
sequelize.sync();

/*
async function testDatabaseConnection() {
  try {
    await sequelize.authenticate();
    console.log('Connection has been established successfully.');
  } catch (error) {
    console.error('Unable to connect to the database:', error);
  } finally {
    // Optionally close the connection if not needed for further operations
    // sequelize.close(); 
  }
  
  //db.data_rayEmployee = Employee;
  //db.Company = Company;
  
}

testDatabaseConnection();
*/
