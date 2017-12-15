FROM python:3

COPY libgit2-0.26.0.tar.gz /tmp/

# Setup for ssh onto github
RUN mkdir -p /root/.ssh

RUN touch /root/.ssh/known_hosts

RUN ssh-keygen -R github.com

WORKDIR /repo
RUN git clone https://github.com/SaberFans/test.git

WORKDIR /tmp

RUN tar xvf libgit2-0.26.0.tar.gz
WORKDIR libgit2-0.26.0

RUN apt-get update; apt-get -y install build-essential; apt-get -y install cmake

RUN cmake .; make; make install

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

RUN ldconfig
RUN python -c 'import pygit2'

CMD ["python", "app.py"]