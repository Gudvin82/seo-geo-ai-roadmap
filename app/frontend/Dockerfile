FROM nginx:1.28-alpine

COPY app/frontend/index.html /usr/share/nginx/html/index.html
COPY app/frontend/styles.css /usr/share/nginx/html/styles.css
COPY app/frontend/app.js /usr/share/nginx/html/app.js
COPY app/frontend/scanner.html /usr/share/nginx/html/scanner.html
COPY app/frontend/scanner.js /usr/share/nginx/html/scanner.js
COPY app/frontend/graph.html /usr/share/nginx/html/graph.html
COPY app/frontend/graph.js /usr/share/nginx/html/graph.js
COPY app/frontend/integration-health.html /usr/share/nginx/html/integration-health.html
COPY app/frontend/repo-understanding.html /usr/share/nginx/html/repo-understanding.html
COPY app/frontend/llms-validator.html /usr/share/nginx/html/llms-validator.html
COPY app/frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
