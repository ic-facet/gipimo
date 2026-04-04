const { Sequelize, DataTypes } = require("sequelize");
const db = require('../../database.js');
  
const  sequelize = db.sequelize;
 
const data_ray_gpt = sequelize.define("data_ray_gpt", {
 
 datetime_utc: {
    type: DataTypes.DATE,
    autoIncrement: false,
    allowNull: false,
    primaryKey: true,
 },
 intensidad: {
    type: DataTypes.DECIMAL(6,2),
    allowNull: false,
 },
 campo_kVm: {
    type: DataTypes.DECIMAL(6,2),
    allowNull: false,
 },
 temp_C: {
    type: DataTypes.DECIMAL(6,2),
    allowNull: false,
 },
 humedad_rh: {
    type: DataTypes.DECIMAL(6,2),
    allowNull: false,
 },
 presion_hPa: {
    type: DataTypes.DECIMAL(6,2),
    allowNull: false,
 },
 cpm_escalado: {
    type: DataTypes.DECIMAL(6,2),
    allowNull: false,
 },
 avg_cpm_reciente: {
    type: DataTypes.DECIMAL(6,2),
    allowNull: false,
 }
},{timestamps: false});
module.exports = data_ray_gpt;
