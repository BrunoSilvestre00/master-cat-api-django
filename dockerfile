FROM python:3.11

RUN apt-get update \
    && apt-get install -y

ARG ROOT=/var/www/app

RUN mkdir -p ${ROOT}
ADD . ${ROOT}
WORKDIR ${ROOT}

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
