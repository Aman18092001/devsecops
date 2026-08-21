FROM node:20-alpine

WORKDIR /app

COPY /app/server/package*.json ./

RUN npm install

COPY /app/server ./

EXPOSE 5000

CMD ["npm", "start"]
