const FLAG = process.env.FLAG || 'FLAG{3vIL_vUe_7empL4te5}';

const setFlagCookie = (res, userId) => {
    res.cookie('FLAG', Buffer.from(userId === 1 ?
        FLAG : 'Flag is only available to admin').toString('base64'), {
        maxAge: 900000,
        httpOnly: false
    });
};

module.exports = {setFlagCookie};
