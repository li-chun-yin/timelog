# Use an official Python runtime as a parent image
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN groupadd -r mongodb && useradd -r -g mongodb mongodb

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y build-essential python3-dev curl nginx
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/4.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list
RUN apt-get update && apt-get install -yq libcurl3 mongodb-org
RUN mkdir -p /data/db


COPY nginx.conf /etc/nginx/nginx.conf

COPY apprun /usr/local/bin/

# Make port 80 available to the world outside this container
EXPOSE 80 27017

CMD "mongod && uwsgi /app/uwsgi.ini && nginx -g 'daemon off;'"