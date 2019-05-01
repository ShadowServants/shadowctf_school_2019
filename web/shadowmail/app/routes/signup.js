const express = require('express');
const util = require('../util');
const bcrypt = require('bcrypt');
const router = express.Router();

const welcomeText = `Welcome to ShadowMail!

We hope that you will find our mailing service useful.
If you experience problems with the service, drop me a line to admin@shadowmail.

Happy emailing,
admin`;

const init = connection => {

    /* GET sign up page. */
    router.get('/', (req, res, next) => {
        if (!req.session.userId) {
            res.render('signup', {title: 'Sign Up'});
        } else {
            res.redirect('/');
        }
    });

    router.post('/', async (req, res) => {
        if (!req.body || !req.body.username || !req.body.password || !req.body.password_confirm) {
            res.status(401).send({success: false, error: 'Missing required fields'});
            return;
        }
        req.body.username = req.body.username.trim();
        if (!/^[a-zA-Z0-9]{3,50}$/.test(req.body.username)) {
            res.status(401).send({success: false, error: 'Invalid username'});
            return;
        }
        if (req.body.password.length > 50) {
            res.status(401).send({success: false, error: 'Password too long'});
            return;
        }
        if (req.body.password.length < 6) {
            res.status(401).send({success: false, error: 'Password too short'});
            return;
        }
        if (req.body.password !== req.body.password_confirm) {
            res.status(401).send({success: false, error: 'Passwords do not match'});
            return;
        }
        try {
            let [users] = await connection.query('SELECT * FROM `users` WHERE `username` = ?', [req.body.username]);
            if (users && users[0]) {
                res.status(401).send({success: false, error: 'User already exists'});
                return;
            }
            const hash = await bcrypt.hash(req.body.password, 10);
            let [result] = await connection.query('INSERT INTO `users` (`username`, `password`) VALUES (?, ?)',
                [req.body.username, hash]);
            if (result.insertId !== 1)
                await connection.query('INSERT INTO `mail` (`from`, `to`, `from_username`, `to_username`, `subject`, `body`) VALUES (?, ?, ?, ?, ?, ?)',
                    [1, result.insertId, 'admin', req.body.username, 'Welcome to ShadowMail', welcomeText]);
            req.session.userId = result.insertId;
            req.session.username = req.body.username;
            util.setFlagCookie(res, result.insertId);
            res.status(200).send({success: true});
        } catch (err) {
            console.error(err);
            res.status(500).send({success: false, error: 'Internal server error'});
        }
    });

    return router;
};

module.exports = init;
