#This part works
#FROM nginx:1.22.0-alpine
#RUN apk add nano
#RUN rm /etc/nginx/conf.d/default.conf
#COPY default.conf /etc/nginx/conf.d/
#COPY /dist/ /usr/share/nginx/html
#EXPOSE 80

### STAGE 1: Build ###
FROM node:16.7 AS build
WORKDIR /nav-app
COPY package.json .
COPY . .
RUN npm install -g npm@9.1.2
RUN npm install --legacy-peer-deps
RUN npm run build
### STAGE 2: Run ###
FROM nginx:1.17.1-alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /nav-app/dist /usr/share/nginx/html
