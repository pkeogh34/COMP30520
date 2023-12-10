FROM python:3.9-slim

WORKDIR /usr/src/app


COPY ../requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ../rabbitmq_setup.py /usr/src/app/
COPY ./demonstrator_cc/demonstrator_cc.py .

CMD ["python", "./demonstrator_cc.py"]
