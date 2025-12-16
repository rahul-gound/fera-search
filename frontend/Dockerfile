FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

COPY . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
