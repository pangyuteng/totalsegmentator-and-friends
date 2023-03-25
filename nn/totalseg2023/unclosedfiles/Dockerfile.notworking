#FROM tensorflow/tensorflow:2.8.0-gpu-jupyter
#FROM tensorflow/tensorflow:nightly-gpu-jupyter
FROM tensorflow/tensorflow:2.10.0-gpu-jupyter

WORKDIR /opt
RUN /usr/bin/python3 -m pip install --upgrade pip
COPY requirements.txt /opt
RUN pip install -r requirements.txt
#RUN pip install git+https://www.github.com/keras-team/keras-contrib.git
#RUN apt-get update;apt-get upgrade -yq;apt-get install ffmpeg vim wget -yq

