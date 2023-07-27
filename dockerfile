# Pull base image
FROM python:3.11

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Install dependencies

COPY . /code/

RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 8000