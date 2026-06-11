FROM nginx:1.28-alpine

COPY app/frontend/index.html /usr/share/nginx/html/index.html
COPY app/frontend/styles.css /usr/share/nginx/html/styles.css
COPY app/frontend/app.js /usr/share/nginx/html/app.js
COPY app/frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
