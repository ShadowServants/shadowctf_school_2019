const express = require('express');
const router = express.Router();

const init = connection => {

    /* GET inbox page. */
    router.get('/:id', async (req, res, next) => {
        if (!req.session.userId) {
            res.redirect('/');
        } else {
            let id = req.params.id;
            if (id === undefined || id === null) {
                res.redirect('/');
                return;
            }
            try {
                id = parseInt(id);
            } catch (e) {
                res.redirect('/');
                return;
            }
            if (id < 0) {
                res.redirect('/');
                return;
            }
            try {
                let [mail] = await connection.query('SELECT * FROM `mail` WHERE `id` = ? AND (`to` = ? OR `from` = ?)',
                    [id, req.session.userId, req.session.userId]);
                if (!mail || mail.length !== 1) {
                    res.redirect('/');
                    return;
                }
                if (mail[0].to === req.session.userId)
                    await connection.query('UPDATE `mail` SET `read` = 1 WHERE `id` = ?', [id]);
                res.render('mail', {username: req.session.username, mail: mail[0]});
            } catch (err) {
                console.error(err);
                res.redirect('/');
            }
        }
    });
    return router;
};

module.exports = init;
