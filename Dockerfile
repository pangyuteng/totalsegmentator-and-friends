FROM python:3.8.16-bullseye

RUN apt-get update -y; apt-get install -y libgl1-mesa-dev xvfb

# Copy the package requirements
COPY requirements.txt /opt

WORKDIR /opt
# Install the package requirements
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /opt

# prevent container from exiting - useful for development.
CMD tail -f /dev/null