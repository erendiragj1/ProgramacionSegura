FROM tsl0922/ttyd:latest

RUN apt-get update -y && apt-get upgrade -y && apt-get -y clean
RUN apt-get install net-tools -y
RUN apt-get install ssh -y
RUN apt-get install iputils-ping -y


CMD ttyd -c usrttyd:pwdttyd --p 8888 bash

EXPOSE 8888

#docker run --name mitty -d -p 8888:8888 terminal