const puppeteer = require('puppeteer');

class Bot {

    constructor(logger, maxXhrRequests = -1) {
        this.browser = null;
        this.page = null;
        this.logger = logger;
        this.maxXhrRequests = maxXhrRequests;
        this.numPageXhr = 0;
        this.targetUrl = null;
        this.targetHit = false;
        this.strictNavigation = false;
        this.postData = null;
        this.postHeaders = null;
        this.gotoOptions = {waitUntil: 'load', timeout: 3000};
    }

    async initBrowser() {
        this.logger.info('Initializing browser');
        this.browser = await puppeteer.launch({headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox']});
        this.page = await this.browser.newPage();
        await this.page.setRequestInterception(true);
        this.page.on('request', this.requestInterceptor.bind(this));
    }

    requestInterceptor(request) {
        let data = {};
        this.logger.info(`Requesting: ${request.url()}, navigation = ${request.isNavigationRequest()}, resource = ${request.resourceType()}`);
        if (this.postData) {
            this.logger.info('Adding POST payload');
            const headers = Object.assign({}, request.headers(), this.postHeaders || {});
            data = {
                method: 'POST',
                postData: this.postData,
                headers: headers
            };
            this.postData = null;
            this.postHeaders = null;
        }


        if (request.isNavigationRequest() && request.redirectChain().length !== 0) {
            this.logger.warn('Found redirect chain, aborting');
            request.abort();
            return;
        }

        if (request.isNavigationRequest() && this.strictNavigation) {
            if (request.url() === this.targetUrl) {
                if (!this.targetHit) {
                    this.targetHit = true;
                } else {
                    this.logger.warn('Aborting request as target url is already loaded');
                    request.abort();
                    return;
                }
            } else {
                this.logger.warn('Aborting request as url does not match target url');
                request.abort();
                return;
            }
        }

        if (request.resourceType() === 'xhr' && this.maxXhrRequests > 0) {
            if (this.numPageXhr++ === this.maxXhrRequests) {
                this.logger.warn('Aborting as maximum number of XHR requests was reached');
                request.abort();
                return;
            }
        }
        request.continue(data);
    }

    async post(url, data = '', headers = null, options = this.gotoOptions) {
        this.postData = data;
        this.postHeaders = headers;
        return this.get(url, options);
    }

    async get(url, options = this.gotoOptions) {
        this.targetUrl = url;
        this.numPageXhr = 0;
        this.targetHit = false;
        return this.page.goto(url, options);
    }

    setStrictNavigation(strictNavigation) {
        this.strictNavigation = strictNavigation;
        this.logger.info(`Strict navigation is now ${strictNavigation ? 'enabled' : 'disabled'}`);
    }

    async shutdown() {
        this.logger.info('Shutting down');
        await this.browser.close();
    }

}

module.exports = Bot;
