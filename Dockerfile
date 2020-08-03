FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./extra_files/nginx.conf /etc/nginx/conf.d/nginx.conf

COPY ./extra_files/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./app /app

ENV LISTEN_PORT 5002
ENV DB_API="http://52.255.160.180:5001"

EXPOSE 5002
RUN mkdir -p /etc/chaos_files/tmp
COPY ./extra_files/fault_runner.py /etc/chaos_files/fault_runner.pyc

# Install ansible with kerberos
#RUN yum -y install python-devel krb5-devel krb5-libs krb5-workstation
#RUN yum install kinit

RUN pip install -r requirements.txt
