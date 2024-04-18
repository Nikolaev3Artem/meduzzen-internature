FROM python:3.11-alpine

WORKDIR ./app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./pyproject.toml ./
RUN pip install .

COPY . .


CMD ["python", "./app/main.py"]