const express = require('express');
const router = express.Router();

const init = connection => {

    /* GET home page. */
    router.get('/', function (req, res, next) {
        if (!req.session.userId) {
            res.redirect('/login')
        } else {
            req.session.destroy();
            res.redirect('/login')
        }
    });

    return router;
};

module.exports = init;
