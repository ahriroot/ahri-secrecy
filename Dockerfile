FROM python:3.8
MAINTAINER "ahri"<ahriknow@ahriknow.cn>
ADD app.py /project/app.py
ADD requirements.txt /project/requirements.txt
ADD pip.conf /etc/pip.conf
WORKDIR /project
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 9000
ENTRYPOINT ["gunicorn", "-w", "2", "-b", "0.0.0.0:9000", "app:app"]