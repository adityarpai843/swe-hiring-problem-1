const express = require('express');
const app = express();
const cors = require('cors');
const commandRoutes = require('./routes/command');
require('dotenv').config();

app.use(express.json());
app.disable('x-powered-by');
app.use(cors());

app.use('/api/v1', commandRoutes);

app.listen(3000, () => {
    console.log('Server running on port 3000');
});