FROM tiangolo/uwsgi-nginx-flask:python3.7

#Install ansible with kerberos
RUN apt-get update && apt-get install -y python-devel\
 krb5-devel krb5-libs krb5-workstation kinit\
&& rm -rf /var/lib/apt/lists/*
COPY ./extra_files/krb5.conf /etc/krb5.conf

# create chaos dir
RUN mkdir -p /etc/chaos_files/tmp