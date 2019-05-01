FROM zenato/puppeteer

USER root

WORKDIR /usr/src/app

COPY package*.json ./

RUN apt-get update && apt-get install -y build-essential && apt-get install -y python && npm install
RUN npm install

COPY . .

CMD [ "npm", "start" ]
