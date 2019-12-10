const mongoose = require('mongoose')

const nodeSchema = new mongoose.Schema({
    node_id:{
        type: String,
        required: true
    },node_type: {
        type: String
    },
    name_attachment:{
        type: String,
        required: true
    },
    duration: {
        type: String,
        required: true
    },
    interval:{
        type: String,
        required: true
    },
    results: {
        type: [String],
        required: true
    },
    owner: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    }
},{
    timestamps: true
})


experiment = mongoose.model('Experiment',nodeSchema)

module.exports = experiment
