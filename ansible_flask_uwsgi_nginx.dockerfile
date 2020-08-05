FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV DEBIAN_FRONTEND=noninteractive

# Install ansible with kerberos
RUN apt-get update && apt -y -qq install gcc python-dev libkrb5-dev\
 python-pip krb5-user\
&& rm -rf /var/lib/apt/lists/*

# Install pythons modules needed for ansible
#RUN pip install –upgrade pip
#RUN pip install pywinrm pywinrm[kerberos] ansible

# Copy kerberos conf file
#COPY ./extra_files/krb5.conf /etc/krb5.conf

# create chaos dir
#RUN mkdir -p /etc/chaos_files/tmp