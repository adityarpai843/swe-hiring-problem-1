const router = require('express').Router();
const location = require('../controller/commands');

router.get('/commands', location.getAllCommands);
router.post('/commands', location.createCommand);


module.exports = router;

// sequelize model:generate --name commands --attributes command:string