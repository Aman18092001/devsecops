require('dotenv').config();

const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const csurf = require('csurf');

const getConnection = require('./utils/getConnection');
const userRoutes = require('./routes/user');
const homeRoutes = require('./routes/home');

const app = express();

// Middleware
app.use(cors());

app.use(express.json());

app.use(
    express.urlencoded({
        extended: true,
    })
);

app.use(cookieParser());

// CSRF Protection
app.use(
    csurf({
        cookie: true,
    })
);

// Routes
app.use('/', homeRoutes);
app.use('/user/auth', userRoutes);

// Error Handler
app.use((error, req, res) => {
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
