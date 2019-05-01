const express = require('express');
const router = express.Router();

const init = connection => {

    /* GET inbox page. */
    router.get('/', async (req, res, next) => {
        if (!req.session.userId) {
            res.status(403).send({success: false, error: 'You must be logged in to perform this action'});
        } else {
            try {
                let [mail] = await connection.query('SELECT * FROM `mail` WHERE `to` = ?',
                    [req.session.userId]);
                res.status(200).send({success: true, data: mail});
            } catch (err) {
                console.error(err);
                res.status(500).send({success: false, error: 'Internal server error'});
            }
        }
    });
    return router;
};

module.exports = init;
