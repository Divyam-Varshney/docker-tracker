# NGINX lightweight image use kar rahe hain
FROM nginx:alpine

# Custom nginx config copy karte hain
COPY nginx.conf /etc/nginx/nginx.conf

# HTML files copy karte hain
COPY html/ /usr/share/nginx/html/

# Port 80 expose karte hain
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
