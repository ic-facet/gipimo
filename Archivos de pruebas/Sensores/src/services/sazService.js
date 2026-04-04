//"use strict";
const db = require('../../database');
const data_Ray_GPT = db.data_ray_gpt;
const data_Radob = db.data_radob;
const { Op } = require('sequelize');

const insertRay_GPT = async (registros_ray_gpt) => {
    const newRegistros = await data_Ray_GPT.bulkCreate(registros_ray_gpt,{logging: false});
    //console.log(newRegistros);
    return newRegistros;
};
const insertRadob = async (registros_radob) => {
    const newRegistros = await data_Radob.bulkCreate(registros_radob,{logging: false});
    //console.log(newRegistros);
    return newRegistros;
};
const getAllRayGPT = async () => {
    const AllRegistros = await data_Ray_GPT.findAll();
    const AllResults = JSON.stringify(AllRegistros, null, 2);
    //console.log('Registros JSON: ',AllResults);
    
    return AllResults;
};

const getRayGPTByDate = async (fechaInicial,fechaFinal) => {
    const startDate = new Date(fechaInicial);
    const endDate = new Date(fechaFinal);
    console.log(startDate);
    const ResultRayGPTByDate = await data_Ray_GPT.findAll({
      where: {datetime_utc: { [Op.between]: [startDate, endDate] }
      }
    });
    const ResultJSON = JSON.stringify(ResultRayGPTByDate, null, 2);
    //console.log('Registros Por fecha: ',ResultJSON);
    
    return ResultJSON;
};
const getRadobByDate = async (fechaInicial,fechaFinal) => {
    const startDate = new Date(fechaInicial);
    const endDate = new Date(fechaFinal);
    console.log(startDate);
    const ResultRadobByDate = await data_Radob.findAll({
      where: {datetime_utc: {
          [Op.between]: [startDate, endDate]
        }
      }
    });
    const ResultJSON = JSON.stringify(ResultRadobByDate, null, 2);
    
    return ResultJSON;
};
module.exports = {
    getRayGPTByDate,
    getRadobByDate,
    getAllRayGPT,
    insertRay_GPT,
    insertRadob,
};
/*
const getMascotaById = async (id) => {
    const mascota = await Mascotas.find({"_id":id});
    return mascota
};

const getMascotaByNP = async (nombre,propietario) => {
    const mascota = await Mascotas.findOne({"nombre":nombre,"propietario":propietario});
    return mascota
};

const insertMascota = async (mascota) => {
    const newMascota = await Mascotas.create(mascota);
    return newMascota;
}

const insertMascota = async (nombre,propietario,especie,sexo,nacimiento,servicios,accesorios,cuidado,fallecimiento) => {
    
    const newMascota = new Mascotas();
    
    newMascota.nombre = nombre;
    newMascota.propietario = propietario;
    newMascota.especie = especie;
    newMascota.sexo = sexo;
    newMascota.nacimiento = nacimiento;
    newMascota.servicios = servicios;
    newMascota.accesorios = accesorios;
    newMascota.cuidado = cuidado;
    newMascota.fallecimiento = fallecimiento;

    const nuevaMascota = await newMascota.create();
    return nuevaMascota;
}


const updateMascota =  async (id,especie,sexo,nacimiento,servicios,accesorios,cuidado,fallecimiento) => {
    const filter = { "_id": id };
    const update = { "especie":especie,"sexo":sexo,"nacimiento":nacimiento,"servicios":servicios,"accesorios":accesorios,"cuidado":cuidado,"fallecimiento":fallecimiento};
    const mascotaActualizada = await Mascotas.findOneAndUpdate(filter,update);
    return mascotaActualizada


}
const delMascota = async (id) => {
    const mascota = await Mascotas.deleteOne({"_id":id});
    return mascota
};

*/
