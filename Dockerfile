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
COPY optcbx optcbx

ENTRYPOINT ["python", "-u", "-m", "optcbx", "flask", "--prod"]
