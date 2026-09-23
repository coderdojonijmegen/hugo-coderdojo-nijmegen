FROM node:26-alpine

WORKDIR /usr/src/app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

RUN npm run build
RUN npm prune --omit=dev

CMD ["npm", "start"]

EXPOSE 3000
