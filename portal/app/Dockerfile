
FROM python:3-jessie
LABEL app=portal_web

COPY requirements.txt /var
RUN pip3 install -r /var/requirements.txt

VOLUME /data

CMD [ "python3", "/data/app/app.py", "-c", "dev" ]

