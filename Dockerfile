FROM python:3.10-slim

WORKDIR /usr/src/ldap-webserver
COPY . /usr/src/ldap-webserver

RUN apt clean
RUN apt update
RUN apt install -y gcc libc-dev 
RUN apt install -y  g++
RUN apt install -y libsasl2-dev libldap2-dev libssl-dev
#RUN apk update && apk add gcc libc-dev openldap-dev
#RUN apk add make automake gcc g++ subversion python3-dev
# some developer is stupid and puts the file in the wrong place
#RUN ln -s /usr/lib/libldap.so /usr/lib/libldap_r.so
RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt
RUN python setup.py

#CMD ["waitress-serve", "--port", "80", "--call", "app:create_app"]
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:create_app()"]
