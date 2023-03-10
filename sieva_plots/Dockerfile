#This part works
#FROM nginx:1.22.0-alpine
#COPY /dist/angular-zingcharts /usr/share/nginx/html
#EXPOSE 80


### STAGE 1: Build ###
FROM node:16.17 AS build
WORKDIR /usr/src/app
COPY package.json .
RUN npm install -g npm@9.1.2
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build
### STAGE 2: Run ###
FROM nginx:1.17.1-alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /usr/src/app/dist/angular-zingcharts /usr/share/nginx/html
