require('dotenv').config();

const express = require('express');

const getConnection = require('./utils/getConnection');
const userRoutes = require('./routes/user');
const homeRoutes = require('./routes/home');

const app = express();

// Middleware


app.use(express.json());

app.use(
    express.urlencoded({
        extended: true,
    })
);

// Routes
app.use('/', homeRoutes);
app.use('/user/auth', userRoutes);

#app.get('/',(req,res)=>{
#   res.send('API is running smoothly')
#})
// Error Handler
app.use((error, req, res, next) => {
    const message = error.message || 'Internal Server Error';
    const statusCode = error.statusCode || 500;

    res.status(statusCode).json({
        message,
    });
});

// Database Connection
getConnection();

// Start Server
app.listen(process.env.PORT, () => {
    console.log(
        'Server is running on port: ' + process.env.PORT
    );
});
