const model = require('../database/models');
const Command = model.commands;

const getAllCommands = async (req, res) => {
    try {
        const locations = await Command.findAll(include = {all: true});
        res.status(200).json(locations);
        
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}

const createCommand = async (req, res) => {
    try{
        const command = await Command.create({
            command: req.body.command,
            shell:req.body.shell
        });
        return res.status(201).json({
            command,
        });
    }
    catch (error) {
        return res.status(500).json({ error: error.message });
    
    }
}

    module.exports = {
        getAllCommands,
        createCommand
    }