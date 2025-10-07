# Nginx to serve frontend and reverse-proxy /api to backend
FROM nginx:stable-alpine

# Nginx config
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Static site
COPY frontend /usr/share/nginx/html

# Use production API config
COPY frontend/static/js/config.production.js /usr/share/nginx/html/static/js/config.js

EXPOSE 80
