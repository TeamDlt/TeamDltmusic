FROM python:3.9.7-slim-buster
RUN apt-get update && apt-get upgrade -y
RUN apt-get install git curl python3-pip ffmpeg -y
RUN python3 -m pip install --upgrade pip
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN pip3 uninstall pyrogram -y
RUN pip3 install git+https://github.com/pyrogram/pyrogram@master
RUN npm i -g npm
COPY . /app
WORKDIR /app
RUN python3 -m pip install -U -r requirements.txt
CMD python3 main.py
