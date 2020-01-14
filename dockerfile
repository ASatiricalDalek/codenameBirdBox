FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.7
RUN apk --update add bash nano
ENV STATIC URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
