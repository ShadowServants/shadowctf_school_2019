const createError = require('http-errors');
const express = require('express');
const session = require('express-session');
const path = require('path');
const fs = require('fs');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const mysql = require('mysql2/promise');
const MySQLStore = require('express-mysql-session')(session);

const options = {
    host: process.env.HOST || 'localhost',
    port: process.env.SQL_PORT || 3306,
    user: 'app',
    password: 'password',
    database: 'shadowmail'
};

const sessionStore = new MySQLStore(options);

const indexRouter = require('./routes/index');
const loginRouter = require('./routes/login');
const signUpRouter = require('./routes/signup');
const logoutRouter = require('./routes/logout');
const inboxRouter = require('./routes/inbox');
const sentRouter = require('./routes/sent');
const sendRouter = require('./routes/send');
const mailRouter = require('./routes/mail');

module.exports = async () => {
    const app = express();

// view engine setup
    app.set('views', path.join(__dirname, 'views'));
    app.set('view engine', 'hbs');

    app.use(logger('dev'));
    app.use(express.json());
    app.use(cookieParser());
    app.use(express.static(path.join(__dirname, 'public')));
    app.use(session({
        secret: String(fs.readFileSync(path.resolve(__dirname, 'secret'))),
        resave: false,
        store: sessionStore,
        name: 'SESSION',
        saveUninitialized: false
    }));
    let connection = null;
    try {
        connection = await mysql.createConnection(options);
    } catch (err) {
        console.error('Unable to connect to MySQL');
        console.error(err);
        process.exit(1);
    }
    app.use('/', indexRouter(connection));
    app.use('/login', loginRouter(connection));
    app.use('/signup', signUpRouter(connection));
    app.use('/logout', logoutRouter(connection));
    app.use('/inbox', inboxRouter(connection));
    app.use('/sent', sentRouter(connection));
    app.use('/send', sendRouter(connection));
    app.use('/mail', mailRouter(connection));

// catch 404 and forward to error handler
    app.use((req, res, next) => {
        next(createError(404));
    });

// error handler
    app.use((err, req, res, next) => {
        // set locals, only providing error in development
        res.locals.message = err.message;
        res.locals.error = req.app.get('env') === 'development' ? err : {};

        // render the error page
        res.status(err.status || 500);
        res.render('error');
    });
    return app;
};
