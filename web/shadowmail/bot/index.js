const winston = require('winston');
const dns = require('dns');
const Bot = require('./bot');

const SCHEME = 'http';
const HOST = process.env.HOST || 'localhost';
const PORT = process.env.PORT || 3000;
const SLEEP_INTERVAL = process.env.SLEEP_INTERVAL || 30000;
let ip = null;

const logger = new winston.Logger({
    transports: [
        new (winston.transports.Console)({
            level: 'debug',
            name: 'console',
            handleExceptions: true,
            json: false,
            timestamp: true
        }),
        new (winston.transports.File)({
            filename: `./all.log`,
            level: 'debug',
            name: 'all',
            handleExceptions: true,
            json: false,
            timestamp: true
        })
    ]
});

const MAX_XHR_REQUESTS = 1;

const JSON_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
};

const credentials = {
    username: 'admin',
    password: '079A9A9FF6AF845FC8EE36A3F8C38557'
};

const buildUrl = (path = '') => {
    return `${SCHEME}://${ip}:${PORT}/${path}`;
};

const sleep = time => new Promise(resolve => setTimeout(resolve, time));

const checkSignUp = async bot => {
    logger.info('Checking if the bot is signed up');
    try {
        let data = {...credentials, password_confirm: credentials.password};
        let result = await bot.post(buildUrl('signup'), JSON.stringify(data), JSON_HEADERS);
        let resJson = await result.json();
        if (!resJson.success && resJson.error.indexOf('exists') > 0) {
            logger.info('Bot is already signed up');
        } else if (resJson.success) {
            logger.info('Bot was successfully registered');
        } else {
            throw new Error('Malformed response');
        }
    } catch (e) {
        logger.error('Error while signing up');
        logger.error(e);
        await bot.shutdown();
        process.exit(0);
    }
};

const logIn = async bot => {
    logger.info('Logging the bot in');
    try {
        let result = await bot.post(buildUrl('login'), JSON.stringify(credentials), JSON_HEADERS);
        let resJson = await result.json();
        if (resJson.success) {
            logger.info('Logged in successfully');
        } else {
            throw new Error(resJson.error);
        }
    } catch (e) {
        logger.info('Unable to login');
        logger.error(JSON.stringify(e));
        await bot.shutdown();
        process.exit(0);
    }
};

const tick = async bot => {
    // Re-login bot every time
    await logIn(bot);
    let inboxResponse = await bot.get(buildUrl('inbox'));
    let inbox = await inboxResponse.json();
    if (!inbox.success) {
        logger.error('Unable to fetch inbox');
        logger.error(inbox.error);
        return;
    }
    bot.setStrictNavigation(true);
    let unreadLetters = inbox.data.filter(letter => letter.read === 0);
    logger.info(`Found ${unreadLetters.length} unread letters`);
    for (let letter of unreadLetters) {
        try {
            await bot.get(buildUrl('mail/' + letter.id), {waitUntil: 'load', timeout: 1500});
        } catch (e) {
            logger.error(`Unable to load page for letter with id ${letter.id}`);
            logger.error(JSON.stringify(e));
        }
    }
    bot.setStrictNavigation(false);
};

start = async () => {
    dns.lookup(HOST, async (err, result) => {
        ip = result;
        let bot = new Bot(logger, MAX_XHR_REQUESTS);
        await bot.initBrowser();
        await checkSignUp(bot);
        while (true) {
            try {
                logger.info('Starting tick');
                await tick(bot);
            } catch (e) {

            }
            logger.info(`Sleeping for ${SLEEP_INTERVAL}ms`);
            await sleep(SLEEP_INTERVAL);
        }
    });
};

start();


