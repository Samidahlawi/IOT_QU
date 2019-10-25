const mongoose = require('mongoose')

const nodeSchema = new mongoose.Schema({
    id:{
        type: String,
        required: true
    },attachments:[String],
    device_type:{
        type:String,
    },
    ip_address:{
        type:String,
        required: true
    },
    start:{
        type:String
    },
    power_supply:{
        type:String,
    },
    state:{
        type:String,
        required:true
    },
    port:{
        type:String,
        required:true
    }
},
{
    timestamps: true
})

node = mongoose.model('Node',nodeSchema)

module.exports = node