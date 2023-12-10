FROM python:3.9-slim

WORKDIR /usr/src/app

COPY ../requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ../rabbitmq_setup.py /usr/src/app/
COPY ./teaching_assistant/teaching_assistant.py .

CMD ["python", "./teaching_assistant.py"]
