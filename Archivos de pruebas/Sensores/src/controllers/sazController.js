/// Controller
const sazService = require("../services/sazService");

module.exports ={
    getAllRayGPT,
    getRayGPTByDate,
    getRadobByDate,
    insertRay_GPT,
    insertRadob
};

function insertRay_GPT(req, res) {
    const registros_ray_gpt = req.body
    console.log('RayGPT Insert: ',registros_ray_gpt.length);
    sazService
        .insertRay_GPT(registros_ray_gpt)
        .then(response => {
            res.status(200).send(response);
        })
        .catch(err => { 
            console.log(err);
        });
}
function insertRadob(req, res) {
    const registros_radob = req.body
    console.log('Radob Insert: ',registros_radob.length);
    sazService
        .insertRadob(registros_radob)
        .then(response => {
            res.status(200).send(response);
        })
        .catch(err => { 
            console.log(err);
        });
}

function getAllRayGPT(req, res) {
    //console.log('getAllRayGPT Controller');
    sazService
        .getAllRayGPT()
        .then(response => {
            //console.log('Controlador response:',response);
            res.status(200).send(response);
        })
        .catch(err => { });
}

function getRayGPTByDate(req, res) {
    const fechaInicial = req.body.fechainicial;
    const fechaFinal = req.body.fechafinal;
    console.log("Consulta RayGPT Date:",fechaInicial,fechaFinal);
    sazService
        .getRayGPTByDate(fechaInicial,fechaFinal)
        .then(response => {
            res.status(200).send(response);
        })
        .catch(err => { });
}

function getRadobByDate(req, res) {
    const fechaInicial = req.body.fechainicial;
    const fechaFinal = req.body.fechafinal;
    console.log("Consulta Radob Date:",fechaInicial,fechaFinal);
    sazService
        .getRadobByDate(fechaInicial,fechaFinal)
        .then(response => {
            res.status(200).send(response);
        })
        .catch(err => { });
}
/*
function getMascotaById(req, res) {
    const { id } = req.params

    mascotasService
        .getMascotaById(id)
        .then(response => {
            res.status(200).send(response);
        })
        .catch(err => { });
}

function getMascotaByNP(req, res) {
    const { nombre } = req.params
    const { propietario } = req.params


    mascotasService
        .getMascotaByNP(nombre,propietario)
        .then(response => {
            res.status(200).send(response);
        })
        .catch(err => { });
}

function updateMascota(req, res) {
  const {_id} = req.body
  const {especie} = req.body
  const {sexo} = req.body
  const {nacimiento} = req.body
  const {servicios} = req.body
  const {accesorios} = req.body
  const {cuidado} = req.body
  const {fallecimiento} = req.body
  mascotasService
        .updateMascota(_id,especie,sexo,nacimiento,servicios,accesorios,cuidado,fallecimiento)
        .then(response => {
            res.status(200).send(response);
        })
        .catch(err => { });
}

function insertMascota(req, res) {

    const mascota = req.body
 
    const {nombre} = req.body
    const {propietario} = req.body
    const {especie} = req.body
    const {sexo} = req.body
    const {nacimiento} = req.body
    const {servicios} = req.body
    const {accesorios} = req.body
    const {cuidado} = req.body
    const {fallecimiento} = req.body

    mascotasService
        //.insertMascota(nombre,propietario,especie,sexo,nacimiento,servicios,accesorios,cuidado,fallecimiento)
        .insertMascota(mascota)
        .then(response => {
            res.status(200).send(response);
        })
        .catch(err => { 
            console.log(err);
        });
}

function delMascota(req, res) {

  const {_id} = req.body
  mascotasService
      .delMascota(_id)
      .then(response => {
          res.status(200).send(response);
      })
      .catch(err => { 
          console.log(err);
      });
}
*/
