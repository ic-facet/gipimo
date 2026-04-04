const { Sequelize, DataTypes } = require("sequelize");
const db = require('../../database.js');
  
const  sequelize = db.sequelize;
 
const data_radob = sequelize.define("data_radob", {
 
 datetime_utc: {
    type: DataTypes.DATE,
    autoIncrement: false,
    allowNull: false,
    primaryKey: true,
 },
 ua: {
    type: DataTypes.DECIMAL(22,10),
    allowNull: false,
 }
},{timestamps: false});
module.exports = data_radob;
