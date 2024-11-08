FROM python:3.12.7-bullseye

WORKDIR /app

COPY . .

RUN pip install -r /requirements.txt

CMD ["unicorn", "main:app", "--host 0.0.0.0", "--port 8007"]