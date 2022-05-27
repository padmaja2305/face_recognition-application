FROM python:3.8-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake 
RUN apt-get install -y gfortran 
RUN apt-get install -y git 
RUN apt-get install -y wget 
RUN apt-get install -y curl 
RUN apt-get install -y libgraphicsmagick1-dev 
RUN apt-get install -y libatlas-base-dev 
RUN apt-get install -y libavcodec-dev 
RUN apt-get install -y libavformat-dev 
RUN apt-get install -y libgtk2.0-dev 
RUN apt-get install -y libjpeg-dev 
RUN apt-get install -y liblapack-dev 
RUN apt-get install -y libswscale-dev 
RUN apt-get install -y pkg-config 
RUN apt-get install -y python3-dev 
RUN apt-get install -y python3-numpy 
RUN apt-get install -y software-properties-common 
RUN apt-get install -y zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && mkdir build && cd build && cmake .. &&  cmake --build . &&\
    cd .. && python3 setup.py install
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/
RUN cd /app 
RUN ls | cat
RUN pip install -r requirment.txt

EXPOSE 8000
RUN python3 /app/attendenceAPI/manage.py migrate
CMD ["python3", "/app/attendenceAPI/manage.py", "runserver"]
