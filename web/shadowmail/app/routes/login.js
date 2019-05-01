const express = require('express');
const util = require('../util');
const bcrypt = require('bcrypt');
const router = express.Router();

const init = connection => {

    /* GET login page. */
    router.get('/', (req, res, next) => {
        if (!req.session.userId) {
            res.render('login', {title: 'Login'});
        } else {
            res.redirect('/');
        }
    });

    router.post('/', async (req, res) => {
        if (!req.body || !req.body.username || !req.body.password) {
            res.status(401).send({success: false, error: 'Missing required fields'});
            return;
        }
        req.body.username = req.body.username.trim();
        try {
            let [users] = await connection.query('SELECT * FROM `users` WHERE `username` = ?',
                [req.body.username]);
            if (!users || !users.length) {
                res.status(401).send({success: false, error: 'Incorrect username or password'});
                return;
            }
            if (!(await bcrypt.compare(req.body.password, users[0].password))) {
                res.status(401).send({success: false, error: 'Incorrect username or password'});
                return;
            }
            req.session.userId = users[0].id;
            req.session.username = req.body.username;
            util.setFlagCookie(res, users[0].id);
            res.status(200).send({success: true});
        } catch (err) {
            console.error(err);
            res.status(500).send({success: false, error: 'Internal server error'});
        }

    });

    return router;
};

module.exports = init;
