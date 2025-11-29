FROM node:20-alpine

RUN mkdir /app
WORKDIR /app

COPY . /app

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]