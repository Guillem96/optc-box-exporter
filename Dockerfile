FROM python:3.7.7

WORKDIR /optc-box-exporter

RUN apt-get update
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY data data
COPY ai ai
COPY optcbx optcbx
COPY wsgi.py wsgi.py

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
