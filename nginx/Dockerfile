FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]

RUN cd tmp && mkdir -p cores

EXPOSE 8888