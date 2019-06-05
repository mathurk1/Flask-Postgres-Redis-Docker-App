FROM python:alpine 

WORKDIR /docker-flask-app

RUN apk update && apk add --no-cache\
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    build-base \
    linux-headers \ 
    pcre-dev

COPY ./requirements.txt ./
COPY ./uwsgi-app.ini ./
RUN pip install -r requirements.txt

COPY ./.env ./
COPY ./src ./src

CMD ["uwsgi", "./uwsgi-app.ini"]