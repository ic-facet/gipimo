const router = require("express").Router();
const sazController = require("../controllers/sazController")

router.get('/', function (req, res, next) {
  res.status(200).send("API Sociedad Astronómica de Zacatecas");
});

router.get('/getAllRayGPT', sazController.getAllRayGPT, function (req, res) {
  res.status(200).send(res);
});

router.post('/getRayGPTDate', sazController.getRayGPTByDate, function (req, res) {
  res.status(200).send(res);
});

router.post('/getRadobDate', sazController.getRadobByDate, function (req, res) {
  res.status(200).send(res);
});

//verifyAuthentication(req.headers.authorization),

router.post('/insertRayGPT', sazController.insertRay_GPT, function (req, res) {
  res.status(200).send(res);
});

router.post('/insertRadob', sazController.insertRadob, function (req, res) {
  res.status(200).send(res);
});

//function verifyAuthentication(){
//}

module.exports = router;


/*

router.get('/session-check', function (req, res, next){
  if (req.isAuthenticated() || req.user) {
    console.log("Autenticado:",req.user);
    return next();
  }
  console.log("No Autenticado:",req.user);
  res.redirect('/');
});

router.route('/session-check')
  .get( (req, res) => {
    console.log("User check:"+req.user);
    res.status(200).send(req.user);
});



router.get('/mascota/:id', mascotasController.getMascotaById, function (req, res, next) {
  res.status(200).send(res);
});

router.get('/mascota/:nombre/:propietario',helpers.isLoggedIn, mascotasController.getMascotaByNP, function (req, res, next) {
  res.status(200).send(res);
});

router.get('/borramascota/:id', helpers.isLoggedIn, mascotasController.delMascota, function (req, res, next) {  
  res.status(200).send(res);
});

router.post('/actualizaMascota', helpers.isLoggedIn, mascotasController.updateMascota, function (req, res, next) {
  res.status(200).send(res);
});
router.post('/signup', function (req, res, next) {
  passport.authenticate('local-signup', function (err, user, info) {
    if (err) {
      return res.status(500).send();
    }
    if(!user) {
      return res.status(404).send();
    }
    console.log("Usuario creado ",user)
    return res.status(200).send(user);
  })(req, res, next)
});

router.get('/signin', (req, res, next) => {
  res.redirect('/');
});

router.post('/signin', (req, res, next) => {
  passport.authenticate('local-signin', function (err, user, info) {
    if (err) {
      return res.status(500).send();
    }
    if(!user) {
      return res.redirect('/');
    }
    req.logIn(user, function(err) {
      console.log("Usuario firmado", user)
      return res.status(200).send(user);
    })
  })(req,res,next) 
});
 


*/
