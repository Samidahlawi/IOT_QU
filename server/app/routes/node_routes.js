//import express
const express = require('express')
//import passport 
const passport = require('passport')

// pull in mongoose model of nodes
const Node = require('../models/node')



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


// ========================== START CHECK THE NODE DEAD OR ALIVE ======================
//  IMPORT device-registry.js
// for check for each moment if the node still live or dead
// Import axios library 
const axios = require('axios')

// //AXIOS
const getNode = (ip) => {
    try{
      return axios.get(`http://${ip}:9090/device-info`) //return object of node
    } catch(error){
    //   console.log(error)
    console.log('check node can not make request to node!! file of node_route')
    }
  }
  
  const checkNode = async (ip) => {
    //   console.log('checkNode involved')
    // update the state of the node 
    // select the field or column of node 
    
    const node = getNode(ip)
    .then(response => { 
    //   console.log(response.data)
    })
    .catch(error => { //here will excute if not receive any response so that means the node not exist
            Node.findOne({ip_address:ip})
            .then(node => {
                if (node.state == 'on'){ // check if the current state is on then make it off
                    console.log('**** WARNING *****')
                    console.log('>> THE NODE IP: '+ ip + ' NOT AVAILBEL!!')
                    return node.update({'state':'off'})  
                }
                 
            })
            
    })
  }

const checkAllNodes = () => {
    Node.find()
    .then(handle404)
    .then(nodes => {
         //['192.168.1.2','121.2.12.3',.....]
        let ips = nodes.filter(node => node.state == 'on')
            ips = ips.map((node) => node.ip_address)
        ips.forEach((node) => {
            if (ips.length){
                checkNode(node)
            }
        })
    })
    .catch(() => {
        console.log('error not any nodes in the system')
    })
}

//Each 5 miunts the server will cheack
const sec = 1000 * 60
setInterval(checkAllNodes, 5000) /// (callback,sec)

  // ========================== END  CHECK THE NODE DEAD OR ALIVE ======================




// Index
// get /nodes
router.get('/nodes',(req,res,next) => {
    Node.find()
    .then(nodes => {
        res.status(200).json({'nodes':nodes})
    })
    .catch(next)
})



// create
// post /nodes/device-registry
router.post('/nodes/device-registry',(req,res,next) => {
    body = req.body
    nodeID = body.id
    Node.count({id:nodeID},function(err,count){
        if(count > 0){
            //When the id exist in the DB will return stats:exist
            //Should the node do anthor request to update the data 
            res.status(201).json({'state':'exist'})
        }else{
            // the First time of request for the node
            //When the id not ex res.status(201).json({"stats":ist in the DBand will create new node 
            body['state'] = 'on'
            Node.create(body)
            // respond to succesful `create` with status 201 and JSON of new "example"
            .then(node => {
                console.log('**** SUCCESSUFLLY CONNECTING *****')
                console.log('>> THE NODE IP: '+ node.ip_address + ' WORKING...')
                res.status(201).json({'state':'created'})
            })  
            .catch(next)
            
        }
    })
}) 




// update
// patch /nodes/:id
router.patch('/nodes/:id',(req,res,next) => {
    nodeID = req.params.id
    body = req.body
    body['state'] = 'on'
    Node.findOne({id:nodeID})
    .then(handle404)
    .then(node => {
        console.log('**** SUCCESSUFLLY CONNECTING *****')
        console.log('>> THE NODE IP: '+ node.ip_address + ' WORKING...')
        return node.update(body)   
    })
    //if that succeeded, return 204 and no JSON
    .then(() => res.sendStatus(204))
    //if an error occurs, pass it to the handler
    .catch(next)
})



//Destroy
// DELETE /nodes/:id
router.delete('/nodes/:id', (req,res,next) => {
    nodeID = req.params.id // get the id from url by params
    Node.remove({id:nodeID})
    .then(handle404)
    .then(() => res.sendStatus(204)) //204 the back 204 and no content if the deletion succeeded
    //if an error occurs, pass it to the handler
    .catch(next)
})



module.exports = router