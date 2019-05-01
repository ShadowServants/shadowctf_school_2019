const express = require('express');
const router = express.Router();

const init = connection => {

    /* GET home page. */
    router.get('/', (req, res, next) => {
        if (!req.session.userId) {
            res.redirect('/login')
        } else {
            res.render('inbox', {title: 'Inbox', username: req.session.username});
        }
    });

    return router;
};

module.exports = init;
