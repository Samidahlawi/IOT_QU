// Express docs: http://expressjs.com/en/api.html
const express = require('express')
// Passport docs: http://www.passportjs.org/docs/
const passport = require('passport')

// pull in Mongoose model for examples
const Experiment = require('../models/experiment')
const User = require('../models/user')
// this is a collection of methods that help us detect situations when we need
// to throw a custom error
const customErrors = require('../../lib/custom_errors')

// we'll use this function to send 404 when non-existant document is requested
const handle404 = customErrors.handle404
// we'll use this function to send 401 when a user tries to modify a resource
// that's owned by someone else
const requireOwnership = customErrors.requireOwnership

// this is middleware that will remove blank fields from `req.body`, e.g.
// { example: { title: '', text: 'foo' } } -> { example: { text: 'foo' } }
const removeBlanks = require('../../lib/remove_blank_fields')
// passing this as a second argument to `router.<verb>` will make it
// so that a token MUST be passed for that route to be available
// it will also set `req.user`
const requireToken = passport.authenticate('bearer', { session: false })

// instantiate a router (mini app that only handles routes)
const router = express.Router()

 // INDEX
 // GET /experiments
 router.get('/experiments', requireToken, (req,res,next) => {
     User.findById(req.user.id)
     .populate('experiments')
     .then(user => {
         return user.experiments.map(experiment => experiment.toObject())
     })
     .then(experiments => res.status(200).json({experiments: experiments}))
     .catch(next)
 })


 // SHOW 
 // GET /experiments/:id
 // :id ~> MAC_IP
 router.get('/experiments/:id',requireToken,(req,res,next) => {
     Experiment.findById(req.param.id)
     .then(handle404)
     .then(experimen => res.status(200).json({ experimen : experimen.toObject() }))
     .catch(next)
 })


 // CREATE 
 // POST /experiments
 router.post('/experiments', requireToken, (req,res,next) => {
    // Get the id of the user 
    // then assign it to owner of the experiment in DB inside Table of experiment
    // there is column called 'owner'  
    req.body.experiment.owner = req.user.id
    // create the experiment in the table
    Experiment.create(req.body.experiment)
    .then(experiment => {
        res.status(201).json({ experiment : experiment.toObject() })
    })
    .catch(next)
 })



 module.exports = router