FROM node:20-alpine
WORKDIR /app
COPY /app/server/package*.json ./
RUN npm install
COPY /app/server ./
USER node
ENV NODE_ENV=production
EXPOSE 5000
CMD ["node" , "index.js"]
