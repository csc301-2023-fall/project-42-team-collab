FROM python:alpine3.18

WORKDIR /app
COPY . .

RUN pip install -r ./main/requirements.txt
