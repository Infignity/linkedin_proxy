FROM python:3.11

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install ca-certificates curl

RUN pip install curl_cffi --upgrade

EXPOSE 80

WORKDIR /src

COPY requirements.txt /src

RUN mkdir ./files

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]