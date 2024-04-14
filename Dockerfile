FROM python:3.11-alpine

WORKDIR ./app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./prod.requirements.txt ./
RUN pip install -r prod.requirements.txt

COPY . .

CMD ["python", "./app/main.py"]