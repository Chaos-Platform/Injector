FROM chaos-platform/chaos-injector:base

ENV SERVER_PORT 5002
ENV DB_API="http://52.255.160.180:5001"

COPY ./app /app

EXPOSE 5002
COPY ./extra_files/fault_runner.py /etc/chaos_files/fault_runner.pyc
WORKDIR /app

RUN pip install -r requirements.txt
