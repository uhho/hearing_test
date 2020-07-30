FROM ubuntu:20.04

RUN \
  apt -y update --fix-missing && \
  apt -y install software-properties-common && \
  apt -y update && \
  apt -y upgrade

RUN apt -y install python3-pip portaudio19-dev
#rm -rf /var/lib/apt/lists/*

#RUN apt -y install portaudio19-dev python-pyaudio python3-pyaudio
#RUN apt -y install portaudio19-dev python3-pyaudio
#RUN apt -y install python3-alsaaudio

WORKDIR /workspace
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . /workspace
