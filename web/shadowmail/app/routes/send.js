const express = require('express');
const router = express.Router();

const init = connection => {

    router.post('/', async (req, res) => {
        if (!req.session.userId) {
            res.status(403).send({success: false, error: 'You must be logged in to perform this action'});
        } else {
            if (req.session.userId === 1) {
                res.status(403).send({success: false, error: 'This user is read-only'});
                return;
            }
            if (!req.body || !req.body.email || !req.body.subject || !req.body.body) {
                res.status(400).send({success: false, error: 'Missing required fields'});
                return;
            }
            req.body.email = req.body.email.trim();
            req.body.subject = req.body.subject.trim();
            req.body.body = req.body.body.trim();
            if (!req.body.email.endsWith('@shadowmail')) {
                res.status(400).send({success: false, error: 'Invalid e-mail'});
                return;
            }
            let email = req.body.email.substring(0, req.body.email.length - '@shadowmail'.length);

            if (req.body.subject.length > 50) {
                res.status(400).send({success: false, error: 'Subject too long'});
                return;
            }
            if (req.body.body.length > 500) {
                res.status(400).send({success: false, error: 'Body too long'});
                return;
            }
            try {
                let [users] = await connection.query('SELECT * FROM `users` WHERE `username` = ?', [email]);
                if (!users || users.length < 1) {
                    res.status(400).send({success: false, error: 'Recipient not found'});
                    return;
                }
                if (users[0].id === req.session.userId) {
                    res.status(400).send({success: false, error: 'Cannot email yourself'});
                    return;
                }
                await connection.query('INSERT INTO `mail` (`from`, `to`, `from_username`, `to_username`, `subject`, `body`) VALUES (?, ?, ?, ?, ?, ?)',
                    [req.session.userId, users[0].id, req.session.username, users[0].username, req.body.subject, req.body.body]);
                res.status(200).send({success: true});
            } catch (err) {
                console.error(err);
                res.status(500).send({success: false, error: 'Internal server error'});
            }
        }
    });

    return router;
};

module.exports = init;
