FROM chaos-platform/chaos-injector:base

ENV LISTEN_PORT 5002
ENV DB_API="http://52.255.160.180:5001"

EXPOSE 5002
RUN mkdir -p /etc/chaos_files/tmp
COPY ./extra_files/fault_runner.py /etc/chaos_files/fault_runner.pyc

RUN pip install -r requirements.txt
