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

// import ANSAI excape to color the text in the terminal
const colors = require('../../ANSI_escape')


// ========================== START CHECK THE NODE DEAD OR ALIVE ======================
//  IMPORT device-registry.js
// for check for each moment if the node still alive or dead
// Import axios library 
const axios = require('axios')

// //AXIOS
const getNode = (ip,port) => {
    
    try{
      return axios.get(`http://${ip}:${port}/device`)
    } catch(error){
    //   console.log(error)
    console.log(colors.FAIL + 'Clould not reach the node by request it!! file of node_route' + colors.ENDC)
    }
  }
  
  const checkNode = async (ip,port) => {
    //   console.log('checkNode involved')
    // update the state of the node 
    // select the field or column of node 
    
    const node = getNode(ip,port)
    .then(response => { 
    //   console.log(response.data)
        Node.findOne({ip_address:ip})
        .then((node) => {
            if(node.state == 'off'){
                connectedNodes()
                return node.update({'state':'on'})
            }
        })
        .catch(() => console.log('should update the ip_address in the DB becaise still undefined'))
        
    })
    .catch(error => { //here will excute if not receive any response so that means the node not exist
            Node.findOne({ip_address:ip})
            .then(node => {
                // Should write inside the condition && node.ip_address != null
                if (node.state == 'on' && node.ip_address != 'undefined'){ // check if the current state is on then make it off
                    console.log(colors.WARNING + '**** WARNING *****' + colors.ENDC )
                    console.log(colors.WARNING + '>> THE NODE IP: '+ ip + ' NOT AVAILBEL!!' + colors.ENDC )
                    connectedNodes()
                    return node.update({'state':'off','ip_address':'undefined'})  
                }
            })
            .catch(() => {
                console.log('ERROR IN THE REQUEST TO THE NODE CHECK IF ALIVE OR DEAD!!')
            })
            
    })
  }

const checkAllNodes = () => {
    Node.find()
    .then(handle404)
    .then(nodes => {
         //['192.168.1.2','121.2.12.3',.....]
         // onNodes will take all the nodes from database whereas the state is on ONLY
         // then we use map for return a new array contain ONLY ip && port of each node connected
        let onNodes = nodes.filter(node => node.state == 'on' && node.ip_address != 'undefined')
            onNodes = onNodes.map((node) => {
                return {'ip':node.ip_address,'port':node.port}
            })
            // console.log(onNodes)
            // looping through the connected nodes and call function checkNode for make request
            // BUT before do request we have to make sure there are connected nodes in database because that I checked the length of array
            onNodes.forEach((node) => {
            if (onNodes.length){
                checkNode(node.ip,node.port)
            }
        })
    })
    .catch(() => {
        console.log(colors.WARNING + 'error no NODES in the system' + colors.ENDC)
    })
}

//Each 5 miunts the server will cheack
const sec = 1000 * 60
setInterval(checkAllNodes, 5000) /// (callback,sec)

  // ========================== END  CHECK THE NODE DEAD OR ALIVE ======================

  // =========== START CONNECTED_NODES HERE =============
/// this function will tell you which nodes is conneted rihgt-now
const connectedNodes = (next) => {
    setTimeout(() => {
        Node.find()
        .then(nodes => {
            nodesOn = nodes.filter(node => node.state == 'on')
            nodesOn.forEach(node => {
                    console.log(colors.OKGREEN + '>> THE NODE IP: '+ node.ip_address + ' WORKING...' + colors.ENDC )
            })
            if (nodesOn.length == 0){
                console.log(colors.FAIL + '>> NO NODE CONNECTED TO THE SERVER' + colors.ENDC)
            }else {
                console.log(colors.OKBLUE + '>> NUMBERS OF THE NODE CONNECTED: ' + nodesOn.length + ' ' + colors.ENDC)
            }
        })
        .catch(next)
    }, 0);
    
}
// SHOW ALL NODES CONNTECTED WITH THE SERVER RIGHT-NOW
connectedNodes()


// =========== END CONNECTED_NODES HERE =============

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
                console.log(colors.OKGREEN + '**** SUCCESSUFLLY CONNECTING *****' + colors.ENDC)
                console.log(colors.OKGREEN + '>> THE NODE IP: '+ node.ip_address + ' WORKING...' + colors.ENDC )
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
        console.log(colors.OKBLUE + '**** SUCCESSUFLLY CONNECTING *****' + colors.ENDC)
        console.log(colors.OKBLUE + '>> THE NODE IP: '+ body.ip_address + ' WORKING...' + colors.ENDC )
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